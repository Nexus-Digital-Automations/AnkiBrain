#!/usr/bin/env python3
"""
Test script to verify GPT-5 model compatibility mapping works correctly
"""

import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(__file__))

from model_compatibility import (
    get_compatible_model_name,
    is_model_supported,
    get_model_info,
    log_model_usage,
)


def test_model_compatibility():
    """Test the model compatibility mapping functionality"""
    print("Testing GPT-5 Model Compatibility Mapping...")
    print("=" * 50)

    # Test cases: (requested_model, expected_compatible_model)
    test_cases = [
        ("gpt-3.5-turbo", "gpt-3.5-turbo"),  # Already supported
        ("gpt-4", "gpt-4"),  # Already supported
        ("gpt-5", "gpt-4"),  # Should map to gpt-4
        ("gpt-5-mini", "gpt-4"),  # Should map to gpt-4
        ("gpt-5-turbo", "gpt-4-turbo"),  # Should map to gpt-4-turbo
        ("unknown-model", "gpt-4"),  # Unknown should fallback to gpt-4
    ]

    print("Testing get_compatible_model_name():")
    all_passed = True

    for requested, expected in test_cases:
        result = get_compatible_model_name(requested)
        status = "✅ PASS" if result == expected else "❌ FAIL"
        print(f"  {requested} -> {result} ({status})")
        if result != expected:
            print(f"    Expected: {expected}, Got: {result}")
            all_passed = False

    print()
    print("Testing is_model_supported():")
    support_tests = [
        ("gpt-3.5-turbo", True),
        ("gpt-4", True),
        ("gpt-5", False),
        ("gpt-5-mini", False),
    ]

    for model, expected in support_tests:
        result = is_model_supported(model)
        status = "✅ PASS" if result == expected else "❌ FAIL"
        print(f"  {model} supported: {result} ({status})")
        if result != expected:
            all_passed = False

    print()
    print("Testing get_model_info():")
    info = get_model_info("gpt-5")
    print(f"  GPT-5 Info: {info}")
    expected_info = {
        "original_model": "gpt-5",
        "compatible_model": "gpt-4",
        "is_mapped": True,
        "is_supported": False,
    }
    info_passed = info == expected_info
    status = "✅ PASS" if info_passed else "❌ FAIL"
    print(f"  Info structure correct: {status}")
    if not info_passed:
        print(f"    Expected: {expected_info}")
        print(f"    Got: {info}")
        all_passed = False

    print()
    print("Testing log_model_usage() (should not crash):")
    try:
        log_model_usage("gpt-5", "gpt-4")
        log_model_usage("gpt-4", "gpt-4")
        print("  ✅ PASS - Logging functions executed without errors")
    except Exception as e:
        print(f"  ❌ FAIL - Logging failed: {e}")
        all_passed = False

    print()
    print("=" * 50)
    if all_passed:
        print("🎉 ALL TESTS PASSED - GPT-5 compatibility mapping working correctly!")
        return True
    else:
        print("❌ SOME TESTS FAILED - Check model compatibility implementation")
        return False


if __name__ == "__main__":
    success = test_model_compatibility()
    sys.exit(0 if success else 1)
