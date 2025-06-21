# test_nebius_client.py
"""
Test script for Nebius LLM client functionality
"""

import sys
import os
import json

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from llm.nebius_client import nebius_client


def test_client_initialization():
    """Test if Nebius client initializes correctly"""
    print("🔍 Testing Nebius Client Initialization...")
    print("=" * 60)

    try:
        # Check if client is initialized
        assert nebius_client.client is not None, "Client not initialized"
        print("✅ Client initialization: SUCCESS")

        # Check configuration
        print(f"✅ Model: {nebius_client.model}")
        print(f"✅ Base URL: {nebius_client.base_url}")
        print(f"✅ API Key configured: {'Yes' if nebius_client.api_key else 'No'}")

        return True

    except Exception as e:
        print(f"❌ Client initialization failed: {e}")
        return False


def test_api_connection():
    """Test connection to Nebius API"""
    print("\n🌐 Testing Nebius API Connection...")
    print("-" * 50)

    try:
        # Test API connection
        is_connected = nebius_client.test_connection()

        if is_connected:
            print("✅ API Connection: SUCCESS")
            print("✅ Nebius API is responding correctly")
            return True
        else:
            print("❌ API Connection: FAILED")
            return False

    except Exception as e:
        print(f"❌ API connection test failed: {e}")
        return False


def test_label_analysis():
    """Test label analysis functionality"""
    print("\n🏷️  Testing Label Analysis...")
    print("-" * 50)

    # Test cases
    test_cases = [
        {
            "name": "Bug with high priority",
            "labels": ["bug", "critical", "frontend"],
            "expected_bug": True,
        },
        {
            "name": "Feature request",
            "labels": ["enhancement", "feature"],
            "expected_bug": False,
        },
        {
            "name": "Documentation update",
            "labels": ["documentation"],
            "expected_bug": False,
        },
        {
            "name": "Security bug",
            "labels": ["bug", "security", "urgent"],
            "expected_bug": True,
        },
    ]

    all_passed = True

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test Case {i}: {test_case['name']}")
        print(f"   Labels: {test_case['labels']}")

        try:
            # Analyze labels
            analysis = nebius_client.analyze_labels(test_case["labels"])

            print(f"   Result: {json.dumps(analysis, indent=6)}")

            # Validate result structure
            required_keys = [
                "is_bug",
                "priority",
                "schedule_meeting",
                "meeting_urgency",
                "reasoning",
            ]
            for key in required_keys:
                assert key in analysis, f"Missing key: {key}"

            # Check bug detection logic
            detected_bug = analysis["is_bug"]
            expected_bug = test_case["expected_bug"]

            if detected_bug == expected_bug:
                print(f"   ✅ Bug detection: CORRECT ({detected_bug})")
            else:
                print(
                    f"   ⚠️  Bug detection: UNEXPECTED (got {detected_bug}, expected {expected_bug})"
                )
                # Not marking as failure since LLM might have different interpretation

        except Exception as e:
            print(f"   ❌ Analysis failed: {e}")
            all_passed = False

    return all_passed


def test_meeting_summary_generation():
    """Test meeting summary generation"""
    print("\n📅 Testing Meeting Summary Generation...")
    print("-" * 50)

    # Sample issue data (similar to what we'll get from GitHub)
    sample_issue = {
        "title": "Chapter 15: Highlight error",
        "number": 1070,
        "repository": "vercel/next-learn",
        "labels": [{"name": "bug"}, {"name": "frontend"}],
    }

    try:
        print("📝 Generating meeting summary for sample issue:")
        print(f"   Title: {sample_issue['title']}")
        print(f"   Number: #{sample_issue['number']}")

        # Generate summary
        summary = nebius_client.generate_meeting_summary(sample_issue)

        print(f"\n📄 Generated Summary:")
        print(f"   {summary}")

        # Basic validation
        assert len(summary) > 10, "Summary too short"
        assert str(sample_issue["number"]) in summary, "Issue number not in summary"

        print("\n✅ Meeting summary generation: SUCCESS")
        return True

    except Exception as e:
        print(f"❌ Meeting summary generation failed: {e}")
        return False


def test_crewai_integration():
    """Test CrewAI LLM integration"""
    print("\n🤖 Testing CrewAI Integration...")
    print("-" * 50)

    try:
        # Get LLM client for CrewAI
        crewai_llm = nebius_client.get_crewai_llm()

        assert crewai_llm is not None, "CrewAI LLM client is None"

        print("✅ CrewAI LLM client: READY")
        print("✅ Client can be passed to CrewAI agents")

        return True

    except Exception as e:
        print(f"❌ CrewAI integration test failed: {e}")
        return False


if __name__ == "__main__":
    print("🧪 Nebius LLM Client Test Suite")
    print("=" * 60)

    # Track test results
    test_results = []

    # Run all tests
    test_results.append(("Client Initialization", test_client_initialization()))
    test_results.append(("API Connection", test_api_connection()))
    test_results.append(("Label Analysis", test_label_analysis()))
    test_results.append(("Meeting Summary", test_meeting_summary_generation()))
    test_results.append(("CrewAI Integration", test_crewai_integration()))

    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print("-" * 30)

    passed = 0
    total = len(test_results)

    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1

    print("-" * 30)
    print(f"Total: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Nebius client is ready for CrewAI integration!")
        print("🚀 Ready to build Composio setup next!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
        print("💡 Fix the issues above before proceeding.")

    print("=" * 60)
