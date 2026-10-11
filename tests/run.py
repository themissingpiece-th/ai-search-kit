#!/usr/bin/env python3
"""Run the kit tests without pytest: python3 tests/run.py"""
import os, sys, traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import test_kit  # noqa: E402

fails = 0
tests = [(n, f) for n, f in vars(test_kit).items() if n.startswith('test_') and callable(f)]
for name, fn in tests:
    try:
        fn()
        print('PASS', name)
    except Exception:
        fails += 1
        print('FAIL', name)
        traceback.print_exc()
print(f'{len(tests) - fails}/{len(tests)} passed')
sys.exit(1 if fails else 0)
