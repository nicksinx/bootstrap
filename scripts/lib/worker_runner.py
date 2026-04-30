#!/usr/bin/env python3
"""Background agent worker runner (Codex / Claude): manifests, status, dispatch."""

from __future__ import annotations

import argparse
import json
import os
import random
import signal
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Any

import yaml

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover
    Draft202012Validator = None  # type: ignore


def project_root_from_here() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def load_project_id(root: Path) -> str:
    cfg = root / "project.config.yaml"
    if not cfg.is_file():
        sys.stderr.write(f"missing {cfg}\n")
        sys.exit(2)
    data = yaml.safe_load(cfg.read_text()) or {}
    pid = data.get("project_id")
    if not pid:
        sys.stderr.write("project.config.yaml missing project_id\n")
        sys.exit(2)
    return str(pid)


def parse_task_frontmatter(task_path: Path) -> dict[str, Any]:
    raw = task_path.read_text()
    if not raw.startswith("---\n"):
        sys.stderr.write(f"{task_path}: missing YAML frontmatter\n")
        sys.exit(2)
    parts = raw.split("---\n", 2)
    if len(parts) < 3:
        sys.stderr.write(f"{task_path}: invalid frontmatter\n")
        sys.exit(2)
    return yaml.safe_load(parts[1]) or {}


def safe_rel_project(path: str, root: Path) -> Path:
    """Reject absolute paths and traversal."""
    p = Path(path)
    if p.is_absolute():
        raise ValueError(f"absolute path not allowed: {path}")
    parts = p.parts
    if ".." in parts:
        raise ValueError(f"path traversal not allowed: {path}")
    resolved = (root / p).resolve()
    root_r = root.resolve()
    if root_r not in resolved.parents and resolved != root_r:
        if not str(resolved).startswith(str(root_r) + os.sep):
            raise ValueError(f"path escapes project root: {path}")
    return resolved


def route_agent(fm: dict[str, Any]) -> str:
    hint = (fm.get("agent_hint") or "").lower()
    skills = " ".join(fm.get("required_skills") or []).lower()
    if "claude" in hint or "claude" in skills:
        return "claude"
    if "codex" in hint or "codex" in skills or "gpt" in hint:
        return "codex"
    default = os.environ.get("WORKER_DEFAULT_AGENT", "codex").lower().strip()
    return default if default in ("codex", "claude") else "codex"


def default_binary(agent: str) -> str:
    if agent == "codex":
        return os.environ.get("WORKER_CODEX_BIN", "codex").strip() or "codex"
    return os.environ.get("WORKER_CLAUDE_BIN", "claude").strip() or "claude"


def resolve_binary(agent: str, argv_bin: str | None) -> str:
    name = argv_bin or default_binary(agent)
    path = Path(name)
    if path.is_file() and os.access(path, os.X_OK):
        exe = str(path.resolve())
    else:
        import shutil

        found = shutil.which(name)
        if not found:
            sys.stderr.write(
                f"worker binary not found: {name} "
                f"(set WORKER_{agent.upper()}_BIN or PATH)\n"
            )
            sys.exit(3)
        exe = found
    allow = os.environ.get("WORKER_COMMAND_ALLOWLIST", "").strip()
    if allow:
        allowed = {os.path.realpath(x.strip()) for x in allow.split(",") if x.strip()}
        real = os.path.realpath(exe)
        if real not in allowed:
            sys.stderr.write(
                f"binary not in WORKER_COMMAND_ALLOWLIST: {exe}\n"
            )
            sys.exit(10)
    return exe


def validate_manifest(doc: dict[str, Any], schema_path: Path) -> None:
    if Draft202012Validator is None or not schema_path.is_file():
        return
    schema = json.loads(schema_path.read_text())
    Draft202012Validator(schema).validate(doc)


def write_atomic_json(path: Path, doc: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n")
    tmp.replace(path)


def append_worker_event(
    root: Path,
    *,
    level: str,
    event: str,
    project_id: str | None = None,
    task_id: str | None = None,
    run_id: str | None = None,
    agent: str | None = None,
    phase: str | None = None,
    message: str | None = None,
) -> None:
    payload: dict[str, Any] = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "level": level,
        "event": event,
    }
    if message:
        payload["message"] = message
    if project_id:
        payload["project_id"] = project_id
    if task_id:
        payload["task_id"] = task_id
    if run_id:
        payload["run_id"] = run_id
    if agent:
        payload["agent"] = agent
    if phase:
        payload["phase"] = phase
    log_file = root / "logs" / "worker.jsonl"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload, sort_keys=True) + "\n")


def correlation_id() -> str:
    return os.environ.get("BOOTSTRAP_CORRELATION_ID") or str(uuid.uuid4())


def manifest_paths(root: Path, agent: str, run_id: str) -> tuple[Path, Path]:
    out = root / "runs" / agent / run_id
    return out, out / "manifest.json"


def status_path(root: Path, agent: str, run_id: str) -> Path:
    return root / "runs" / "status" / f"{agent}-{run_id}.json"


def build_manifest(
    *,
    schema_version: int,
    run_id: str,
    task_id: str,
    project_id: str,
    agent: str,
    phase: str,
    task_file: str,
    output_dir: str,
    command: list[str] | None,
    pid: int | None,
    started_at: str | None,
    ended_at: str | None,
    exit_code: int | None,
    timeout_seconds: int,
    allow_git: bool,
    retry_attempt: int,
    cid: str,
    error_message: str | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": schema_version,
        "run_id": run_id,
        "task_id": task_id,
        "project_id": project_id,
        "agent": agent,
        "phase": phase,
        "pid": pid,
        "started_at": started_at,
        "ended_at": ended_at,
        "task_file": task_file,
        "output_dir": output_dir,
        "command": command or [],
        "exit_code": exit_code,
        "timeout_seconds": timeout_seconds,
        "allow_git_mutation": allow_git,
        "retry_attempt": retry_attempt,
        "correlation_id": cid,
        "error_message": error_message,
        "manifest_path": str(Path(output_dir) / "manifest.json"),
        "stdout_log": str(Path(output_dir) / "stdout.log"),
        "stderr_log": str(Path(output_dir) / "stderr.log"),
    }


def iso_now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def run_agent_child() -> None:
    ap = argparse.ArgumentParser(description="internal worker child")
    ap.add_argument("--project-root", required=True)
    ap.add_argument("--agent", required=True, choices=("codex", "claude"))
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--task-file", required=True)
    ap.add_argument("--timeout", type=int, default=3600)
    ap.add_argument("--max-retries", type=int, default=2)
    ap.add_argument("--allow-git", action="store_true")
    ap.add_argument("--binary", required=True)
    args = ap.parse_args()

    root = Path(args.project_root).resolve()
    schema_manifest = root / "schemas" / "worker-manifest.schema.json"
    task_path = Path(args.task_file).resolve()
    if not task_path.is_file():
        sys.stderr.write(f"missing task file: {task_path}\n")
        sys.exit(2)
    if root not in task_path.parents and task_path != root:
        sys.stderr.write("task file outside project root\n")
        sys.exit(2)

    fm = parse_task_frontmatter(task_path)
    task_id = fm.get("task_id") or "UNKNOWN"
    project_id = load_project_id(root)
    run_id = args.run_id
    agent = args.agent
    out_dir, man_path = manifest_paths(root, agent, run_id)
    out_dir.mkdir(parents=True, exist_ok=True)
    cid = correlation_id()
    if man_path.is_file():
        try:
            cid = json.loads(man_path.read_text()).get("correlation_id", cid)
        except json.JSONDecodeError:
            pass

    stdout_path = out_dir / "stdout.log"
    stderr_path = out_dir / "stderr.log"
    rel_task = os.path.relpath(task_path, root)

    cmd = [args.binary, str(task_path)]
    allow_git = args.allow_git

    attempt = 0
    max_retries = max(0, args.max_retries)
    timeout_sec = max(1, args.timeout)
    last_exit: int | None = None
    err_msg: str | None = None

    while attempt <= max_retries:
        started = iso_now()
        phase_run = "running"
        man = build_manifest(
            schema_version=1,
            run_id=run_id,
            task_id=str(task_id),
            project_id=project_id,
            agent=agent,
            phase=phase_run,
            task_file=rel_task,
            output_dir=str(out_dir.relative_to(root)),
            command=cmd,
            pid=os.getpid(),
            started_at=started,
            ended_at=None,
            exit_code=None,
            timeout_seconds=timeout_sec,
            allow_git=allow_git,
            retry_attempt=attempt,
            cid=cid,
        )
        validate_manifest(man, schema_manifest)
        write_atomic_json(man_path, man)
        st_path = status_path(root, agent, run_id)
        write_atomic_json(
            st_path,
            {
                "run_id": run_id,
                "agent": agent,
                "state": "running",
                "pid": os.getpid(),
                "updated_at": started,
            },
        )
        append_worker_event(
            root,
            level="info",
            event="worker.run_started",
            project_id=project_id,
            task_id=str(task_id),
            run_id=run_id,
            agent=agent,
            phase="running",
            message=f"attempt={attempt}",
        )

        env = os.environ.copy()
        if not allow_git:
            env["WORKER_GIT_MUTATION_ALLOWED"] = "0"
            env["GIT_ALLOWED"] = "0"

        try:
            with open(stdout_path, "wb") as so, open(stderr_path, "wb") as se:
                proc = subprocess.run(
                    cmd,
                    cwd=str(root),
                    env=env,
                    stdout=so,
                    stderr=se,
                    timeout=timeout_sec,
                )
            last_exit = proc.returncode
        except subprocess.TimeoutExpired:
            last_exit = 124
            err_msg = f"timeout after {timeout_sec}s"
            phase_run = "timeout"
        except OSError as e:
            last_exit = 1
            err_msg = str(e)
            phase_run = "failed"

        ended = iso_now()
        ok = last_exit == 0 and phase_run != "timeout"
        if ok:
            phase_final = "completed"
        elif phase_run == "timeout":
            phase_final = "timeout"
        else:
            phase_final = "failed"

        man = build_manifest(
            schema_version=1,
            run_id=run_id,
            task_id=str(task_id),
            project_id=project_id,
            agent=agent,
            phase=phase_final,
            task_file=rel_task,
            output_dir=str(out_dir.relative_to(root)),
            command=cmd,
            pid=None,
            started_at=started,
            ended_at=ended,
            exit_code=last_exit,
            timeout_seconds=timeout_sec,
            allow_git=allow_git,
            retry_attempt=attempt,
            cid=cid,
            error_message=err_msg,
        )
        validate_manifest(man, schema_manifest)
        write_atomic_json(man_path, man)
        write_atomic_json(
            st_path,
            {
                "run_id": run_id,
                "agent": agent,
                "state": phase_final,
                "pid": None,
                "updated_at": ended,
            },
        )
        append_worker_event(
            root,
            level="info" if ok else "error",
            event="worker.run_finished",
            project_id=project_id,
            task_id=str(task_id),
            run_id=run_id,
            agent=agent,
            phase=phase_final,
            message=f"exit_code={last_exit}",
        )

        if ok:
            return
        if attempt >= max_retries:
            sys.exit(5 if last_exit == 5 else 1)
        backoff = min(60, (2**attempt) + random.random())
        time.sleep(backoff)
        attempt += 1
        err_msg = None


def cmd_start(args: argparse.Namespace) -> None:
    root = project_root_from_here()
    task_rel = args.task_file
    try:
        task_path = safe_rel_project(task_rel, root)
    except ValueError as e:
        sys.stderr.write(f"{e}\n")
        sys.exit(2)
    if not task_path.is_file():
        sys.stderr.write(f"missing task: {task_path}\n")
        sys.exit(2)

    fm = parse_task_frontmatter(task_path)
    task_id = fm.get("task_id")
    if not task_id:
        sys.stderr.write("task frontmatter missing task_id\n")
        sys.exit(2)

    agent = args.agent or route_agent(fm)
    run_id = args.run_id or uuid.uuid4().hex[:12]
    timeout_sec = max(1, args.timeout)
    binary = resolve_binary(agent, args.binary)

    out_dir, man_path = manifest_paths(root, agent, run_id)
    out_dir.mkdir(parents=True, exist_ok=True)
    (root / "runs" / "status").mkdir(parents=True, exist_ok=True)
    (root / "logs").mkdir(parents=True, exist_ok=True)

    project_id = load_project_id(root)
    cid = correlation_id()
    rel_task = os.path.relpath(task_path, root)
    started = iso_now()

    man = build_manifest(
        schema_version=1,
        run_id=run_id,
        task_id=str(task_id),
        project_id=project_id,
        agent=agent,
        phase="starting",
        task_file=rel_task,
        output_dir=str(out_dir.relative_to(root)),
        command=[binary, str(task_path)],
        pid=None,
        started_at=started,
        ended_at=None,
        exit_code=None,
        timeout_seconds=timeout_sec,
        allow_git=args.allow_git,
        retry_attempt=0,
        cid=cid,
    )
    schema_manifest = root / "schemas" / "worker-manifest.schema.json"
    validate_manifest(man, schema_manifest)
    write_atomic_json(man_path, man)

    worker_py = Path(__file__).resolve()
    child_argv = [
        sys.executable,
        str(worker_py),
        "agent-run-child",
        "--project-root",
        str(root),
        "--agent",
        agent,
        "--run-id",
        run_id,
        "--task-file",
        str(task_path),
        "--timeout",
        str(timeout_sec),
        "--max-retries",
        str(args.max_retries),
        "--binary",
        binary,
    ]
    if args.allow_git:
        child_argv.append("--allow-git")

    if args.foreground:
        os.execv(sys.executable, child_argv)
        return

    log_out = open(root / "logs" / "worker-spawn.log", "a", encoding="utf-8")
    proc = subprocess.Popen(
        child_argv,
        cwd=str(root),
        stdin=subprocess.DEVNULL,
        stdout=log_out,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    spawn_pid = proc.pid
    man["phase"] = "running"
    man["pid"] = spawn_pid
    man["started_at"] = started
    validate_manifest(man, schema_manifest)
    write_atomic_json(man_path, man)
    st_path = status_path(root, agent, run_id)
    write_atomic_json(
        st_path,
        {
            "run_id": run_id,
            "agent": agent,
            "state": "running",
            "pid": spawn_pid,
            "updated_at": started,
        },
    )
    append_worker_event(
        root,
        level="info",
        event="worker.spawned",
        project_id=project_id,
        task_id=str(task_id),
        run_id=run_id,
        agent=agent,
        phase="running",
        message=f"pid={spawn_pid}",
    )
    print(json.dumps({"run_id": run_id, "agent": agent, "pid": spawn_pid}, indent=2))


def cmd_status(args: argparse.Namespace) -> None:
    root = project_root_from_here()
    status_dir = root / "runs" / "status"
    if not status_dir.is_dir():
        print("[]")
        return
    rows = []
    for p in sorted(status_dir.glob("*.json")):
        try:
            rows.append(json.loads(p.read_text()))
        except json.JSONDecodeError:
            continue
    if args.run_id:
        rows = [r for r in rows if r.get("run_id") == args.run_id]
    print(json.dumps(rows, indent=2))


def cmd_stop(args: argparse.Namespace) -> None:
    root = project_root_from_here()
    agent = args.agent
    run_id = args.run_id
    st_path = status_path(root, agent, run_id)
    if not st_path.is_file():
        sys.stderr.write(f"unknown run: {agent} {run_id}\n")
        sys.exit(2)
    st = json.loads(st_path.read_text())
    pid = st.get("pid")
    if pid:
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
    _, man_path = manifest_paths(root, agent, run_id)
    if man_path.is_file():
        man = json.loads(man_path.read_text())
        task_id = str(man.get("task_id") or "")
        project_id = str(man.get("project_id") or "")
        man["phase"] = "stopped"
        man["ended_at"] = iso_now()
        man["pid"] = None
        write_atomic_json(man_path, man)
        append_worker_event(
            root,
            level="warn",
            event="worker.stopped",
            project_id=project_id or None,
            task_id=task_id or None,
            run_id=run_id,
            agent=agent,
            phase="stopped",
            message="stop requested",
        )
    st["state"] = "stopped"
    st["pid"] = None
    st["updated_at"] = iso_now()
    write_atomic_json(st_path, st)
    print(json.dumps({"stopped": run_id}))


def recover_stale(root: Path) -> None:
    status_dir = root / "runs" / "status"
    if not status_dir.is_dir():
        return
    for p in status_dir.glob("*.json"):
        try:
            st = json.loads(p.read_text())
        except json.JSONDecodeError:
            continue
        if st.get("state") != "running":
            continue
        pid = st.get("pid")
        if not pid:
            continue
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            rid = st.get("run_id")
            agent = st.get("agent")
            if not rid or not agent:
                continue
            _, man_path = manifest_paths(root, str(agent), str(rid))
            st["state"] = "stale"
            st["pid"] = None
            st["updated_at"] = iso_now()
            write_atomic_json(p, st)
            if man_path.is_file():
                man = json.loads(man_path.read_text())
                man["phase"] = "failed"
                man["error_message"] = "stale pid (process ended)"
                man["ended_at"] = iso_now()
                write_atomic_json(man_path, man)


def count_running(root: Path) -> int:
    recover_stale(root)
    status_dir = root / "runs" / "status"
    if not status_dir.is_dir():
        return 0
    n = 0
    for p in status_dir.glob("*.json"):
        try:
            st = json.loads(p.read_text())
        except json.JSONDecodeError:
            continue
        if st.get("state") == "running" and st.get("pid"):
            try:
                os.kill(int(st["pid"]), 0)
                n += 1
            except (ProcessLookupError, ValueError, TypeError):
                pass
    return n


def cmd_dispatch_start(args: argparse.Namespace) -> None:
    root = project_root_from_here()
    recover_stale(root)
    max_g = int(os.environ.get("WORKER_MAX_GLOBAL", "4"))
    max_a = int(os.environ.get("WORKER_MAX_PER_AGENT", "2"))

    if count_running(root) >= max_g:
        sys.stderr.write("WORKER_MAX_GLOBAL reached\n")
        sys.exit(5)

    qpath = root / "backlog" / "queue.yaml"
    if not qpath.is_file():
        sys.stderr.write("missing backlog/queue.yaml\n")
        sys.exit(2)
    queue_doc = yaml.safe_load(qpath.read_text()) or {}
    entries = queue_doc.get("queue") or []

    task_id = args.task_id
    chosen: dict[str, Any] | None = None
    for e in entries:
        if e.get("task_id") == task_id:
            chosen = e
            break
    if not chosen:
        sys.stderr.write(f"task_id not in queue: {task_id}\n")
        sys.exit(2)

    tfile = root / "backlog" / "tasks" / f"{task_id}.md"
    if not tfile.is_file():
        sys.stderr.write(f"missing task file: {tfile}\n")
        sys.exit(2)

    fm = parse_task_frontmatter(tfile)
    agent = route_agent(fm)

    same_agent = 0
    status_dir = root / "runs" / "status"
    if status_dir.is_dir():
        for p in status_dir.glob("*.json"):
            try:
                st = json.loads(p.read_text())
            except json.JSONDecodeError:
                continue
            if st.get("agent") == agent and st.get("state") == "running":
                try:
                    if st.get("pid"):
                        os.kill(int(st["pid"]), 0)
                        same_agent += 1
                except (ProcessLookupError, ValueError, TypeError):
                    pass
    if same_agent >= max_a:
        sys.stderr.write("WORKER_MAX_PER_AGENT reached for this agent\n")
        sys.exit(5)

    ns = argparse.Namespace(
        task_file=os.path.relpath(tfile, root),
        run_id=args.run_id,
        agent=agent,
        timeout=args.timeout,
        max_retries=args.max_retries,
        allow_git=args.allow_git,
        foreground=args.foreground,
        binary=None,
    )
    cmd_start(ns)


def cmd_dispatch_next(args: argparse.Namespace) -> None:
    root = project_root_from_here()
    recover_stale(root)
    qpath = root / "backlog" / "queue.yaml"
    if not qpath.is_file():
        sys.stderr.write("missing backlog/queue.yaml\n")
        sys.exit(2)
    queue_doc = yaml.safe_load(qpath.read_text()) or {}
    entries = queue_doc.get("queue") or []
    done = set()
    for p in (root / "runs").glob("*/*/manifest.json"):
        try:
            m = json.loads(p.read_text())
            if m.get("phase") == "completed":
                done.add(m.get("task_id"))
        except json.JSONDecodeError:
            continue

    for e in entries:
        tid = e.get("task_id")
        if e.get("status") != "ready":
            continue
        deps = e.get("depends_on") or []
        if any(d not in done for d in deps):
            continue
        if tid in done:
            continue
        ds_args = argparse.Namespace(
            task_id=tid,
            run_id=args.run_id,
            timeout=args.timeout,
            max_retries=args.max_retries,
            allow_git=args.allow_git,
            foreground=args.foreground,
        )
        cmd_dispatch_start(ds_args)
        return
    sys.stderr.write("no dispatchable ready task\n")
    sys.exit(4)


def cmd_review(args: argparse.Namespace) -> None:
    root = project_root_from_here()
    manifests: list[tuple[float, Path]] = []
    for man in root.glob("runs/*/*/manifest.json"):
        try:
            manifests.append((man.stat().st_mtime, man))
        except OSError:
            continue
    manifests.sort(key=lambda x: -x[0])
    limit = max(1, args.limit)
    out = []
    for _, path in manifests[:limit]:
        try:
            out.append(json.loads(path.read_text()))
        except json.JSONDecodeError:
            continue
    print(json.dumps(out, indent=2))


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "agent-run-child":
        sys.argv = [sys.argv[0]] + sys.argv[2:]
        run_agent_child()
        return

    ap = argparse.ArgumentParser(prog="worker_runner")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_start = sub.add_parser("start", help="start worker for a task file")
    p_start.add_argument("--task-file", required=True)
    p_start.add_argument("--run-id")
    p_start.add_argument("--agent", choices=("codex", "claude"))
    p_start.add_argument("--timeout", type=int, default=3600)
    p_start.add_argument("--max-retries", type=int, default=2)
    p_start.add_argument("--allow-git", action="store_true")
    p_start.add_argument("--foreground", action="store_true")
    p_start.add_argument("--binary")
    p_start.set_defaults(func=cmd_start)

    p_st = sub.add_parser("status", help="list run status files")
    p_st.add_argument("--run-id")
    p_st.set_defaults(func=cmd_status)

    p_stop = sub.add_parser("stop", help="stop a run")
    p_stop.add_argument("--agent", required=True, choices=("codex", "claude"))
    p_stop.add_argument("--run-id", required=True)
    p_stop.set_defaults(func=cmd_stop)

    p_dn = sub.add_parser("dispatch-next", help="run first ready queued task")
    p_dn.add_argument("--run-id")
    p_dn.add_argument("--timeout", type=int, default=3600)
    p_dn.add_argument("--max-retries", type=int, default=2)
    p_dn.add_argument("--allow-git", action="store_true")
    p_dn.add_argument("--foreground", action="store_true")
    p_dn.set_defaults(func=cmd_dispatch_next)

    p_ds = sub.add_parser("dispatch-start", help="start worker for task id from queue")
    p_ds.add_argument("--task-id", required=True)
    p_ds.add_argument("--run-id")
    p_ds.add_argument("--timeout", type=int, default=3600)
    p_ds.add_argument("--max-retries", type=int, default=2)
    p_ds.add_argument("--allow-git", action="store_true")
    p_ds.add_argument("--foreground", action="store_true")
    p_ds.set_defaults(func=cmd_dispatch_start)

    p_rv = sub.add_parser("review", help="print recent manifests")
    p_rv.add_argument("--limit", type=int, default=10)
    p_rv.set_defaults(func=cmd_review)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
