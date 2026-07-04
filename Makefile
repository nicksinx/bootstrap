.PHONY: test-contracts test-launch-smoke test-intake check

test-contracts:
	python3 tests/test_contracts.py

test-launch-smoke:
	python3 tests/test_launch_smoke.py

test-intake:
	python3 tests/test_project_intake.py

check: test-contracts test-launch-smoke test-intake
