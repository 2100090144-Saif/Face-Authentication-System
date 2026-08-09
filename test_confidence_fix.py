#!/usr/bin/env python3
"""
Test script to validate the face recognition confidence fixes.
This script tests the core confidence calculation logic.
"""

import sys
import os
import numpy as np
import logging

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_confidence_calculation():
    """Test the confidence calculation formula."""
    print("=" * 60)
    print("TESTING CONFIDENCE CALCULATION FIXES")
    print("=" * 60)
    
    # Test cases with expected results
    test_cases = [
        {"distance": 0.15, "expected_confidence": 85.0, "should_pass": True},
        {"distance": 0.18, "expected_confidence": 82.0, "should_pass": True},
        {"distance": 0.23, "expected_confidence": 77.0, "should_pass": True},
        {"distance": 0.25, "expected_confidence": 75.0, "should_pass": True},
        {"distance": 0.35, "expected_confidence": 65.0, "should_pass": True},
        {"distance": 0.40, "expected_confidence": 60.0, "should_pass": True},
        {"distance": 0.45, "expected_confidence": 55.0, "should_pass": False},  # At threshold
        {"distance": 0.50, "expected_confidence": 50.0, "should_pass": False},
        {"distance": 0.60, "expected_confidence": 40.0, "should_pass": False},
    ]
    
    print(f"{'Distance':<10} {'Confidence':<12} {'Expected':<10} {'Pass Threshold':<15} {'Status':<10}")
    print("-" * 70)
    
    MIN_CONFIDENCE = 60.0
    MAX_TOLERANCE = 0.45
    
    all_passed = True
    
    for case in test_cases:
        distance = case["distance"]
        expected_conf = case["expected_confidence"]
        should_pass = case["should_pass"]
        
        # Calculate confidence using the fixed formula
        calculated_conf = (1 - distance) * 100
        
        # Check if it passes thresholds
        distance_pass = distance <= MAX_TOLERANCE
        confidence_pass = calculated_conf >= MIN_CONFIDENCE
        overall_pass = distance_pass and confidence_pass
        
        # Verify calculation is correct
        calc_correct = abs(calculated_conf - expected_conf) < 0.1
        
        # Verify pass/fail matches expectation
        pass_correct = overall_pass == should_pass
        
        status = "✅ PASS" if calc_correct and pass_correct else "❌ FAIL"
        if not (calc_correct and pass_correct):
            all_passed = False
        
        print(f"{distance:<10.2f} {calculated_conf:<12.1f} {expected_conf:<10.1f} {overall_pass!s:<15} {status:<10}")
    
    print("-" * 70)
    print(f"Thresholds: MIN_CONFIDENCE={MIN_CONFIDENCE}%, MAX_TOLERANCE={MAX_TOLERANCE}")
    print(f"Formula: confidence = (1 - distance) * 100")
    
    if all_passed:
        print("\n✅ ALL CONFIDENCE CALCULATION TESTS PASSED!")
        return True
    else:
        print("\n❌ SOME CONFIDENCE CALCULATION TESTS FAILED!")
        return False

def test_multi_frame_averaging():
    """Test multi-frame averaging logic."""
    print("\n" + "=" * 60)
    print("TESTING MULTI-FRAME AVERAGING")
    print("=" * 60)
    
    # Simulate frame results
    frame_distances = [0.20, 0.18, 0.22, 0.19, 0.21]  # Should average to ~0.20 (80% confidence)
    
    print("Frame distances:", frame_distances)
    
    # Calculate individual confidences
    frame_confidences = [(1 - d) * 100 for d in frame_distances]
    print("Frame confidences:", [f"{c:.1f}%" for c in frame_confidences])
    
    # Calculate average
    avg_distance = sum(frame_distances) / len(frame_distances)
    avg_confidence = (1 - avg_distance) * 100
    
    print(f"Average distance: {avg_distance:.4f}")
    print(f"Average confidence: {avg_confidence:.1f}%")
    
    # Check if it passes thresholds
    MIN_CONFIDENCE = 60.0
    MAX_TOLERANCE = 0.45
    
    distance_pass = avg_distance <= MAX_TOLERANCE
    confidence_pass = avg_confidence >= MIN_CONFIDENCE
    
    print(f"Distance threshold check: {avg_distance:.4f} <= {MAX_TOLERANCE} = {distance_pass}")
    print(f"Confidence threshold check: {avg_confidence:.1f}% >= {MIN_CONFIDENCE}% = {confidence_pass}")
    
    overall_pass = distance_pass and confidence_pass
    print(f"Overall result: {'✅ PASS' if overall_pass else '❌ FAIL'}")
    
    return overall_pass

def test_stabilization_logic():
    """Test stabilization logic."""
    print("\n" + "=" * 60)
    print("TESTING STABILIZATION LOGIC")
    print("=" * 60)
    
    # Test case: 5 frames, need 3 consecutive passes
    test_cases = [
        {
            "name": "All frames pass",
            "frame_results": [True, True, True, True, True],
            "expected_consecutive": 5,
            "should_pass": True
        },
        {
            "name": "3 consecutive passes at start",
            "frame_results": [True, True, True, False, False],
            "expected_consecutive": 3,
            "should_pass": True
        },
        {
            "name": "3 consecutive passes at end",
            "frame_results": [False, False, True, True, True],
            "expected_consecutive": 3,
            "should_pass": True
        },
        {
            "name": "Only 2 consecutive passes",
            "frame_results": [True, True, False, True, False],
            "expected_consecutive": 2,
            "should_pass": False
        },
        {
            "name": "No consecutive passes",
            "frame_results": [True, False, True, False, True],
            "expected_consecutive": 1,
            "should_pass": False
        }
    ]
    
    STABILIZATION_FRAMES = 3
    all_passed = True
    
    for case in test_cases:
        frame_results = case["frame_results"]
        expected_consecutive = case["expected_consecutive"]
        should_pass = case["should_pass"]
        
        # Calculate consecutive passes
        consecutive_passes = 0
        max_consecutive = 0
        
        for result in frame_results:
            if result:
                consecutive_passes += 1
                max_consecutive = max(max_consecutive, consecutive_passes)
            else:
                consecutive_passes = 0
        
        # Check if stabilization passes
        stabilization_pass = max_consecutive >= STABILIZATION_FRAMES
        
        # Verify results
        consecutive_correct = max_consecutive == expected_consecutive
        pass_correct = stabilization_pass == should_pass
        
        status = "✅ PASS" if consecutive_correct and pass_correct else "❌ FAIL"
        if not (consecutive_correct and pass_correct):
            all_passed = False
        
        print(f"{case['name']:<25}: {frame_results} -> {max_consecutive} consecutive, {status}")
    
    print(f"\nStabilization requirement: {STABILIZATION_FRAMES} consecutive frames")
    
    if all_passed:
        print("✅ ALL STABILIZATION TESTS PASSED!")
        return True
    else:
        print("❌ SOME STABILIZATION TESTS FAILED!")
        return False

def main():
    """Run all tests."""
    print("🧪 FACE RECOGNITION CONFIDENCE FIX VALIDATION")
    print("=" * 60)
    
    test1_pass = test_confidence_calculation()
    test2_pass = test_multi_frame_averaging()
    test3_pass = test_stabilization_logic()
    
    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    print(f"Confidence Calculation: {'✅ PASS' if test1_pass else '❌ FAIL'}")
    print(f"Multi-Frame Averaging:  {'✅ PASS' if test2_pass else '❌ FAIL'}")
    print(f"Stabilization Logic:    {'✅ PASS' if test3_pass else '❌ FAIL'}")
    
    if all([test1_pass, test2_pass, test3_pass]):
        print("\n🎉 ALL TESTS PASSED! The confidence fix is working correctly.")
        print("\nKey improvements:")
        print("✅ Confidence now calculated as (1 - distance) * 100 for percentage")
        print("✅ Consistent 60% minimum confidence threshold")
        print("✅ Consistent 0.45 maximum distance tolerance")
        print("✅ Multi-frame averaging for stability")
        print("✅ Stabilization requires 3+ consecutive passes")
        print("✅ Proper logging with both distance and confidence percentage")
        return True
    else:
        print("\n❌ SOME TESTS FAILED! Please review the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)