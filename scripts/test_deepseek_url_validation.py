#!/usr/bin/env python3
"""Validation test for DeepSeek base URL validation.

No external network calls. Tests validation logic only.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "padiem_ai"))

import importlib.util

spec = importlib.util.spec_from_file_location(
    "config", os.path.join(os.path.dirname(__file__), "..", "padiem_ai", "padiem_ai", "ai", "config.py")
)
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)


def test_validation():
    test_cases = [
        ("https://api.deepseek.com/v1", True, "default https"),
        ("https://api.deepseek.com/v1/", True, "trailing slash"),
        ("https://api.deepseek.com", True, "no path"),
        ("http://api.deepseek.com/v1", False, "http not allowed"),
        ("https://localhost/v1", False, "localhost blocked"),
        ("https://LOCALHOST/v1", False, "LOCALHOST blocked"),
        ("https://localhost./v1", False, "localhost. blocked"),
        ("https://127.0.0.1/v1", False, "127.0.0.1 blocked"),
        ("https://[::1]/v1", False, "::1 blocked"),
        ("https://169.254.169.254/v1", False, "metadata IP blocked"),
        ("", False, "empty URL"),
        ("file:///tmp/test", False, "file scheme blocked"),
        ("ftp://api.deepseek.com/v1", False, "ftp scheme blocked"),
        ("https://user:pass@api.deepseek.com/v1", False, "userinfo blocked"),
        ("https://api.deepseek.com/v1?x=1", False, "query string blocked"),
        ("https://api.deepseek.com/v1#fragment", False, "fragment blocked"),
        ("https://api.deepseek.com:444/v1", False, "non-443 port blocked"),
        ("https://api.deepseek.com:8080/v1", False, "8080 port blocked"),
        ("https://api.deepseek.com/custom/path", False, "non-v1 path blocked"),
    ]

    passed = 0
    failed = 0

    for url, should_pass, description in test_cases:
        try:
            result = config.validate_deepseek_base_url(url)
            if should_pass:
                print(f"  PASS: {description} -> {result}")
                passed += 1
            else:
                print(f"  FAIL: {description} should have raised error")
                failed += 1
        except ValueError as e:
            if not should_pass:
                print(f"  PASS: {description} -> blocked: {e}")
                passed += 1
            else:
                print(f"  FAIL: {description} should have passed but blocked: {e}")
                failed += 1
        except Exception as e:
            print(f"  ERROR: {description} -> {type(e).__name__}: {e}")
            failed += 1

    print(f"\n  Results: {passed} passed, {failed} failed")
    return failed == 0


def _run_case(url, should_pass, description, passed, failed):
    """Run a single validation case and update counters."""
    try:
        result = config.validate_deepseek_base_url(url)
        if should_pass:
            print(f"  PASS: {description} -> {result}")
            passed += 1
        else:
            print(f"  FAIL: {description} should have raised error")
            failed += 1
    except ValueError as e:
        if not should_pass:
            print(f"  PASS: {description} -> blocked: {e}")
            passed += 1
        else:
            print(f"  FAIL: {description} should have passed but blocked: {e}")
            failed += 1
    except Exception as e:
        print(f"  ERROR: {description} -> {type(e).__name__}: {e}")
        failed += 1
    return passed, failed


def test_custom_flag_off():
    """Custom flag OFF: only default host allowed, custom hosts blocked."""
    print("\n--- Custom flag OFF ---")
    os.environ.pop("PA_DIEM_ALLOW_CUSTOM_DEEPSEEK_BASE_URL", None)

    cases = [
        ("https://api.deepseek.com/v1", True, "default host allowed"),
        ("https://example.com/v1", False, "custom host blocked (flag off)"),
    ]

    passed, failed = 0, 0
    for url, should_pass, desc in cases:
        passed, failed = _run_case(url, should_pass, desc, passed, failed)

    print(f"  Results: {passed} passed, {failed} failed")
    return failed == 0


def test_custom_flag_on():
    """Custom flag ON: custom hosts allowed, but localhost/private/metadata still blocked."""
    print("\n--- Custom flag ON ---")
    os.environ["PA_DIEM_ALLOW_CUSTOM_DEEPSEEK_BASE_URL"] = "true"

    cases = [
        ("https://example.com/v1", True, "custom host allowed"),
        ("https://localhost/v1", False, "localhost blocked"),
        ("https://LOCALHOST/v1", False, "LOCALHOST blocked"),
        ("https://localhost./v1", False, "localhost. blocked"),
        ("https://127.0.0.1/v1", False, "127.0.0.1 blocked"),
        ("https://[::1]/v1", False, "::1 blocked"),
        ("https://169.254.169.254/v1", False, "metadata IP blocked"),
        ("https://10.0.0.1/v1", False, "10.x private IP blocked"),
        ("https://192.168.0.1/v1", False, "192.168.x private IP blocked"),
        ("https://172.16.0.1/v1", False, "172.16.x private IP blocked"),
    ]

    passed, failed = 0, 0
    for url, should_pass, desc in cases:
        passed, failed = _run_case(url, should_pass, desc, passed, failed)

    # Cleanup
    os.environ.pop("PA_DIEM_ALLOW_CUSTOM_DEEPSEEK_BASE_URL", None)

    print(f"  Results: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    s1 = test_validation()
    s2 = test_custom_flag_off()
    s3 = test_custom_flag_on()

    all_passed = s1 and s2 and s3
    print(f"\n{'='*40}")
    print(f"Overall: {'ALL PASSED' if all_passed else 'SOME FAILED'}")
    sys.exit(0 if all_passed else 1)
