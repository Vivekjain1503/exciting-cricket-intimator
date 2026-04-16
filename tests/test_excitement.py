"""
Test script to verify excitement detection algorithm
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from excitement_detector import ExcitementDetector

def test_excitement_detection():
    """Test excitement detection with various scenarios"""
    detector = ExcitementDetector()
    
    test_scenarios = [
        {
            "name": "Close Match",
            "match": {
                "team1": "MI",
                "team2": "CSK",
                "live": True,
                "score": ["145-3 18.2", "142-4 19.5"],
                "status": "LIVE",
            }
        },
        {
            "name": "Batting Team in Trouble",
            "match": {
                "team1": "RCB",
                "team2": "DC",
                "live": True,
                "score": ["180-2 20.0", "165-6 18.0"],
                "status": "LIVE",
            }
        },
        {
            "name": "Regular Match",
            "match": {
                "team1": "KKR",
                "team2": "SRH",
                "live": True,
                "score": ["150-2 15.0", "60-1 6.0"],
                "status": "LIVE",
            }
        },
    ]
    
    print("=" * 70)
    print("TESTING EXCITEMENT DETECTION ALGORITHM")
    print("=" * 70)
    
    all_passed = True
    
    for scenario in test_scenarios:
        print(f"\nTest: {scenario['name']}")
        print("-" * 70)
        
        match = scenario['match']
        is_exciting, reason, score = detector.is_match_exciting(match)
        level = detector.get_excitement_level(score)
        
        print(f"Excitement Score: {score:.2f}")
        print(f"Level: {level}")
        print(f"Reason: {reason}")
        print(f"Is Exciting: {is_exciting}")
        
        # Basic validation
        if score < 0 or score > 1:
            print("❌ FAILED: Score out of range (0-1)")
            all_passed = False
        else:
            print("✅ PASSED")
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✅ All excitement detection tests passed!")
    else:
        print("❌ Some tests failed")
    print("=" * 70)
    
    return all_passed

if __name__ == "__main__":
    result = test_excitement_detection()
    sys.exit(0 if result else 1)
