.PHONY: test-contracts test-launch-smoke check

test-contracts:
	python3 tests/test_contracts.py

test-launch-smoke:
	python3 tests/test_launch_smoke.py

check: test-contracts test-launch-smoke
