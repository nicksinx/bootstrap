.PHONY: test-contracts test-launch-smoke test-intake test-okf-conformance okf-validate-strict check

test-contracts:
	python3 tests/test_contracts.py

test-launch-smoke:
	python3 tests/test_launch_smoke.py

test-intake:
	python3 tests/test_project_intake.py

test-okf-conformance:
	python3 tests/test_okf_conformance.py

okf-validate-strict:
	scripts/okf-validate --strict

check: test-contracts test-launch-smoke test-intake test-okf-conformance okf-validate-strict
