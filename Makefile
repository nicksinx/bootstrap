.PHONY: test-contracts test-launch-smoke test-intake test-okf-conformance test-okf-migration test-scaffold-consolidation test-skill-contracts test-okf-tooling test-openwiki-sidecar test-okf-mcp test-attested-computation okf-validate-strict okf-migrate-check okf-index-check okf-freshness-check okf-adapter-check check

test-contracts:
	python3 tests/test_contracts.py

test-launch-smoke:
	python3 tests/test_launch_smoke.py

test-intake:
	python3 tests/test_project_intake.py

test-okf-conformance:
	python3 tests/test_okf_conformance.py

test-okf-migration:
	python3 tests/test_okf_migration.py

test-scaffold-consolidation:
	python3 tests/test_scaffold_consolidation.py

test-skill-contracts:
	python3 tests/test_skill_contracts.py

test-okf-tooling:
	python3 tests/test_okf_tooling.py

test-openwiki-sidecar:
	python3 tests/test_openwiki_sidecar.py

test-okf-mcp:
	python3 tests/test_okf_mcp.py

test-attested-computation:
	python3 tests/test_attested_computation.py

okf-validate-strict:
	scripts/okf-validate --strict

okf-migrate-check:
	scripts/okf-migrate --check

okf-index-check:
	scripts/okf-index --check

okf-freshness-check:
	scripts/okf-freshness --check

okf-adapter-check:
	scripts/okf-check-adapters

check: test-contracts test-launch-smoke test-intake test-okf-conformance test-okf-migration test-scaffold-consolidation test-skill-contracts test-okf-tooling test-openwiki-sidecar test-okf-mcp test-attested-computation okf-validate-strict okf-migrate-check okf-index-check okf-freshness-check okf-adapter-check
