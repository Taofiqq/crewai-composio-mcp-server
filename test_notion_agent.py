# test_notion_agent.py
"""
Complete test for Notion agent, tasks, and workflow
Tests the full CrewAI sequential process with kickoff()
"""

import sys
import os
import json
from datetime import datetime

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from workflow.notion_workflow import notion_workflow, run_notion_workflow_standalone
from agents.notion_agent import notion_agent
from tasks.notion_tasks import notion_tasks
from config.settings import settings


def test_agent_setup():
    """Test if Notion agent is properly configured"""
    print("🤖 Testing Notion Agent Setup...")
    print("=" * 60)

    try:
        # Check agent properties
        assert (
            notion_agent.role == "Notion Database Manager"
        ), f"Wrong role: {notion_agent.role}"
        assert notion_agent.tools is not None, "Agent has no tools"
        assert len(notion_agent.tools) > 0, "Agent has empty tools list"

        print(f"✅ Agent Role: {notion_agent.role}")
        print(f"✅ Agent Tools: {len(notion_agent.tools)} tools loaded")
        print(f"✅ Agent LLM: Configured")
        print(f"✅ Allow Delegation: {notion_agent.allow_delegation}")

        return True

    except Exception as e:
        print(f"❌ Agent setup test failed: {e}")
        return False


def test_tasks_creation():
    """Test if Notion tasks are properly created"""
    print("\n📋 Testing Notion Tasks Creation...")
    print("-" * 50)

    try:
        # Test individual task creation
        search_task = notion_tasks.search_parent_pages_task()
        database_task = notion_tasks.create_github_database_task()
        insert_task = notion_tasks.insert_github_data_task()

        tasks = [
            ("Search Parent Pages", search_task),
            ("Create GitHub Database", database_task),
            ("Insert GitHub Data", insert_task),
        ]

        for task_name, task in tasks:
            assert task.description is not None, f"{task_name} has no description"
            assert (
                task.expected_output is not None
            ), f"{task_name} has no expected output"
            assert task.agent is not None, f"{task_name} has no agent assigned"

            print(f"   ✅ {task_name}: CONFIGURED")

        print(f"✅ All {len(tasks)} tasks created successfully")
        return True

    except Exception as e:
        print(f"❌ Tasks creation test failed: {e}")
        return False


def test_workflow_setup():
    """Test if Notion workflow is properly configured"""
    print("\n⚙️  Testing Notion Workflow Setup...")
    print("-" * 50)

    try:
        # Check workflow properties
        info = notion_workflow.get_workflow_info()

        assert info["total_tasks"] == 3, f"Wrong task count: {info['total_tasks']}"
        assert (
            info["process_type"] == "sequential"
        ), f"Wrong process: {info['process_type']}"
        assert (
            info["target_repository"] == settings.TARGET_REPOSITORY
        ), "Wrong repository"
        assert info["database_name"] == "GitHub Issues & PRs", "Wrong database name"

        print(f"✅ Agent Role: {info['agent_role']}")
        print(f"✅ Total Tasks: {info['total_tasks']}")
        print(f"✅ Task Names: {', '.join(info['task_names'])}")
        print(f"✅ Process Type: {info['process_type']}")
        print(f"✅ Target Repository: {info['target_repository']}")
        print(f"✅ Database Name: {info['database_name']}")

        # Check crew setup
        assert notion_workflow.crew is not None, "Crew not initialized"
        assert len(notion_workflow.crew.agents) == 1, "Wrong number of agents"
        assert len(notion_workflow.crew.tasks) == 3, "Wrong number of tasks"

        print("✅ Crew configuration: VALID")

        return True

    except Exception as e:
        print(f"❌ Workflow setup test failed: {e}")
        return False


def test_notion_tools():
    """Test if Notion tools are properly loaded"""
    print("\n🛠️  Testing Notion Tools...")
    print("-" * 50)

    try:
        # Check if agent has notion tools
        tools = notion_agent.tools

        assert tools is not None, "No tools loaded"
        assert len(tools) > 0, "Empty tools list"

        print(f"✅ Notion tools loaded: {len(tools)} tools")

        # Try to import the actions to verify they exist
        from composio_crewai import Action

        notion_actions = [
            Action.NOTION_SEARCH_NOTION_PAGE,
            Action.NOTION_CREATE_DATABASE,
            Action.NOTION_INSERT_ROW_DATABASE,
        ]

        for action in notion_actions:
            print(f"✅ Notion action available: {action}")

        return True

    except Exception as e:
        print(f"❌ Notion tools test failed: {e}")
        return False


def test_workflow_execution():
    """Test the actual workflow execution with kickoff()"""
    print("\n🚀 Testing Notion Workflow Execution...")
    print("=" * 60)
    print("⚠️  This will make actual API calls to Notion and Nebius")
    print("📝 Will create 'GitHub Issues & PRs' database in Notion")

    try:
        # Execute the workflow with sample data
        print("\n🔄 Starting workflow execution...")
        result = run_notion_workflow_standalone()

        print(f"\n📊 Execution Results:")
        print(f"   Success: {result['success']}")
        print(f"   Execution Time: {result['execution_time']:.2f} seconds")
        print(f"   Repository: {result['repository']}")
        print(f"   Timestamp: {result['timestamp']}")

        if result["success"]:
            print("\n✅ WORKFLOW EXECUTION: SUCCESS!")
            print("🎯 Workflow Result Preview:")

            # Try to show a preview of the result
            if isinstance(result["result"], str):
                # Show first 500 characters
                preview = result["result"][:500]
                print(f"   {preview}...")
                if len(result["result"]) > 500:
                    print(f"   ... ({len(result['result'])} total characters)")
            else:
                print(f"   Result Type: {type(result['result'])}")

            print("\n📝 Expected Notion Database:")
            print("   - Database Name: 'GitHub Issues & PRs'")
            print("   - Sample Issues: Chapter 15 error, Security vulnerability")
            print("   - Sample PR: Fix highlight bug")

            return True
        else:
            print(f"\n❌ WORKFLOW EXECUTION: FAILED!")
            print(f"   Error: {result['error']}")
            return False

    except Exception as e:
        print(f"❌ Workflow execution test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_configuration_validation():
    """Validate configuration before running workflow"""
    print("\n🔧 Testing Configuration Validation...")
    print("-" * 50)

    try:
        # Check settings
        print(f"✅ Target Repository: {settings.TARGET_REPOSITORY}")
        print(f"✅ Entity ID: {settings.ENTITY_ID}")

        # Check API keys (without exposing them)
        composio_key = "✓" if settings.COMPOSIO_API_KEY else "❌"
        nebius_key = "✓" if settings.NEBIUS_API_KEY else "❌"

        print(f"✅ Composio API Key: {composio_key}")
        print(f"✅ Nebius API Key: {nebius_key}")

        if not settings.COMPOSIO_API_KEY or not settings.NEBIUS_API_KEY:
            print("⚠️  Missing API keys - workflow may fail")
            return False

        return True

    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        return False


if __name__ == "__main__":
    print("🧪 Notion Agent Complete Test Suite")
    print("=" * 60)
    print("🎯 This tests the full Notion agent workflow with CrewAI")

    # Track test results
    test_results = []

    # Run setup tests first
    print("\n📋 SETUP TESTS:")
    test_results.append(("Configuration", test_configuration_validation()))
    test_results.append(("Agent Setup", test_agent_setup()))
    test_results.append(("Tasks Creation", test_tasks_creation()))
    test_results.append(("Workflow Setup", test_workflow_setup()))
    test_results.append(("Notion Tools", test_notion_tools()))

    # Check if setup tests passed
    setup_passed = all(result for _, result in test_results)

    if setup_passed:
        print("\n🚀 EXECUTION TEST:")
        test_results.append(("Workflow Execution", test_workflow_execution()))
    else:
        print("\n⚠️  Skipping execution test due to setup failures")
        test_results.append(("Workflow Execution", False))

    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print("-" * 30)

    passed = 0
    total = len(test_results)

    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1

    print("-" * 30)
    print(f"Total: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Notion agent is working perfectly!")
        print("📝 Check your Notion workspace for the 'GitHub Issues & PRs' database!")
        print("🚀 Ready to integrate with GitHub agent!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
        if passed >= 5:  # Setup tests passed
            print("💡 Setup is good, check execution issues.")
        else:
            print("💡 Fix setup issues before proceeding.")

    print("\n🎯 Notion Agent Test Complete!")
    print("\n📋 Prerequisites for success:")
    print("1. Run: composio add notion")
    print("2. Authenticate with your Notion account")
    print("3. Grant database creation permissions")
    print("=" * 60)
