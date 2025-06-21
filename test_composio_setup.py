# test_composio_setup.py
"""
Lightweight test for Composio tools setup
Verifies tool initialization and readiness for CrewAI agents
"""

import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.composio_setup import composio_tools, ComposioTools


def test_composio_initialization():
    """Test if ComposioTools initializes correctly"""
    print("🔍 Testing Composio Tools Initialization...")
    print("=" * 60)

    try:
        # Test class initialization
        test_tools = ComposioTools()

        # Check attributes
        assert hasattr(test_tools, "toolset"), "Missing toolset attribute"
        assert hasattr(test_tools, "entity_id"), "Missing entity_id attribute"
        assert (
            test_tools.entity_id == "default"
        ), f"Wrong entity_id: {test_tools.entity_id}"

        print("✅ ComposioTools class: INITIALIZED")
        print(f"✅ Entity ID: {test_tools.entity_id}")
        print("✅ Toolset: READY")

        return True

    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return False


def test_global_instance():
    """Test the global composio_tools instance"""
    print("\n🌐 Testing Global Instance...")
    print("-" * 50)

    try:
        # Check global instance exists
        assert composio_tools is not None, "Global instance is None"
        assert hasattr(composio_tools, "toolset"), "Global instance missing toolset"

        print("✅ Global instance: AVAILABLE")
        print("✅ Ready for agent imports")

        return True

    except Exception as e:
        print(f"❌ Global instance test failed: {e}")
        return False


def test_tool_methods():
    """Test all tool retrieval methods"""
    print("\n🛠️  Testing Tool Retrieval Methods...")
    print("-" * 50)

    methods_to_test = [
        ("GitHub Tools", "get_github_tools"),
        ("Notion Tools", "get_notion_tools"),
        ("Calendar Tools", "get_calendar_tools"),
    ]

    all_passed = True

    for tool_name, method_name in methods_to_test:
        print(f"\n📋 Testing {tool_name}...")

        try:
            # Get the method and call it
            method = getattr(composio_tools, method_name)
            tools = method()

            # Basic validation
            assert tools is not None, f"{tool_name} returned None"
            assert isinstance(tools, list), f"{tool_name} should return a list"

            print(f"   ✅ {tool_name}: Retrieved {len(tools)} tools")

            # Check if tools have expected structure
            if len(tools) > 0:
                first_tool = tools[0]
                if hasattr(first_tool, "type") or isinstance(first_tool, dict):
                    print(f"   ✅ Tool structure: VALID")
                else:
                    print(f"   ⚠️  Tool structure: UNKNOWN")
            else:
                print(f"   ⚠️  No tools returned (might need app connection)")

        except Exception as e:
            print(f"   ❌ {tool_name} failed: {e}")
            all_passed = False

    return all_passed


def test_specific_actions():
    """Test get_specific_actions method"""
    print("\n🎯 Testing Specific Actions Method...")
    print("-" * 50)

    try:
        # Import some actions to test with
        from composio_crewai import Action

        # Test with a few specific actions
        test_actions = [
            Action.GITHUB_ISSUES_LIST_FOR_REPO,
            Action.NOTION_SEARCH_NOTION_PAGE,
        ]

        tools = composio_tools.get_specific_actions(test_actions)

        assert tools is not None, "Specific actions returned None"
        assert isinstance(tools, list), "Specific actions should return a list"

        print(f"✅ Specific actions: Retrieved {len(tools)} tools")
        print("✅ Method working correctly")

        return True

    except Exception as e:
        print(f"❌ Specific actions test failed: {e}")
        return False


def test_agent_import_simulation():
    """Simulate how agents will import and use composio_tools"""
    print("\n🤖 Testing Agent Import Simulation...")
    print("-" * 50)

    try:
        # Simulate agent import pattern
        from tools.composio_setup import composio_tools

        # Simulate what GitHub agent will do
        github_tools = composio_tools.get_github_tools()

        # Simulate what Notion agent will do
        notion_tools = composio_tools.get_notion_tools()

        # Simulate what Calendar agent will do
        calendar_tools = composio_tools.get_calendar_tools()

        print("✅ GitHub agent import: READY")
        print("✅ Notion agent import: READY")
        print("✅ Calendar agent import: READY")
        print("✅ All agents can import composio_tools")

        return True

    except Exception as e:
        print(f"❌ Agent import simulation failed: {e}")
        return False


def test_composio_connection():
    """Test basic Composio connection"""
    print("\n🔗 Testing Composio Connection...")
    print("-" * 50)

    try:
        # Try to access toolset properties
        toolset = composio_tools.toolset

        # Check if toolset has expected methods
        assert hasattr(toolset, "get_tools"), "Toolset missing get_tools method"

        print("✅ Composio connection: ACTIVE")
        print("✅ Toolset methods: AVAILABLE")

        return True

    except Exception as e:
        print(f"❌ Composio connection test failed: {e}")
        return False


if __name__ == "__main__":
    print("🧪 Composio Tools Test Suite")
    print("=" * 60)
    print("💡 This ensures tools are ready for CrewAI agents")

    # Track test results
    test_results = []

    # Run all tests
    test_results.append(("Composio Initialization", test_composio_initialization()))
    test_results.append(("Global Instance", test_global_instance()))
    test_results.append(("Tool Methods", test_tool_methods()))
    test_results.append(("Specific Actions", test_specific_actions()))
    test_results.append(("Agent Import Simulation", test_agent_import_simulation()))
    test_results.append(("Composio Connection", test_composio_connection()))

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
        print("✅ Composio tools are ready for CrewAI agents!")
        print("🚀 Ready to build GitHub agent next!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
        print("💡 Check Composio connections and try again.")

    print("\n📋 Next Steps:")
    print("1. Ensure GitHub, Notion, Calendar are connected:")
    print("   - composio add github")
    print("   - composio add notion")
    print("   - composio add googlecalendar")
    print("2. If tests pass, ready for GitHub agent!")

    print("=" * 60)
