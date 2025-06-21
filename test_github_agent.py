# test_github_agent.py
"""
Complete test for GitHub agent, tasks, and workflow
Tests the full CrewAI sequential process with kickoff()
"""

import sys
import os
import json
from datetime import datetime

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from workflow.github_workflow import github_workflow, run_github_workflow
from agents.github_agent import github_agent
from tasks.github_tasks import github_tasks
from config.settings import settings


def test_agent_setup():
    """Test if GitHub agent is properly configured"""
    print("🤖 Testing GitHub Agent Setup...")
    print("=" * 60)

    try:
        # Check agent properties
        assert (
            github_agent.role == "GitHub Data Fetcher"
        ), f"Wrong role: {github_agent.role}"
        assert github_agent.tools is not None, "Agent has no tools"
        assert len(github_agent.tools) > 0, "Agent has empty tools list"

        print(f"✅ Agent Role: {github_agent.role}")
        print(f"✅ Agent Tools: {len(github_agent.tools)} tools loaded")
        print(f"✅ Agent LLM: Configured")
        print(f"✅ Allow Delegation: {github_agent.allow_delegation}")

        return True

    except Exception as e:
        print(f"❌ Agent setup test failed: {e}")
        return False


def test_tasks_creation():
    """Test if GitHub tasks are properly created"""
    print("\n📋 Testing GitHub Tasks Creation...")
    print("-" * 50)

    try:
        # Test individual task creation
        issues_task = github_tasks.fetch_issues_task()
        prs_task = github_tasks.fetch_pull_requests_task()
        analysis_task = github_tasks.analyze_github_data_task()

        tasks = [
            ("Fetch Issues", issues_task),
            ("Fetch PRs", prs_task),
            ("Analyze Data", analysis_task),
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
    """Test if GitHub workflow is properly configured"""
    print("\n⚙️  Testing GitHub Workflow Setup...")
    print("-" * 50)

    try:
        # Check workflow properties
        info = github_workflow.get_workflow_info()

        assert info["total_tasks"] == 3, f"Wrong task count: {info['total_tasks']}"
        assert (
            info["process_type"] == "sequential"
        ), f"Wrong process: {info['process_type']}"
        assert (
            info["target_repository"] == settings.TARGET_REPOSITORY
        ), "Wrong repository"

        print(f"✅ Agent Role: {info['agent_role']}")
        print(f"✅ Total Tasks: {info['total_tasks']}")
        print(f"✅ Task Names: {', '.join(info['task_names'])}")
        print(f"✅ Process Type: {info['process_type']}")
        print(f"✅ Target Repository: {info['target_repository']}")
        print(f"✅ Bug Label: {info['bug_label']}")

        # Check crew setup
        assert github_workflow.crew is not None, "Crew not initialized"
        assert len(github_workflow.crew.agents) == 1, "Wrong number of agents"
        assert len(github_workflow.crew.tasks) == 3, "Wrong number of tasks"

        print("✅ Crew configuration: VALID")

        return True

    except Exception as e:
        print(f"❌ Workflow setup test failed: {e}")
        return False


def test_workflow_execution():
    """Test the actual workflow execution with kickoff()"""
    print("\n🚀 Testing GitHub Workflow Execution...")
    print("=" * 60)
    print("⚠️  This will make actual API calls to GitHub and Nebius")
    print(f"📂 Repository: {settings.TARGET_REPOSITORY}")

    try:
        # Execute the workflow
        print("\n🔄 Starting workflow execution...")
        result = run_github_workflow()

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
        print(f"✅ Bug Label: {settings.BUG_LABEL}")
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
    print("🧪 GitHub Agent Complete Test Suite")
    print("=" * 60)
    print("🎯 This tests the full GitHub agent workflow with CrewAI")

    # Track test results
    test_results = []

    # Run setup tests first
    print("\n📋 SETUP TESTS:")
    test_results.append(("Configuration", test_configuration_validation()))
    test_results.append(("Agent Setup", test_agent_setup()))
    test_results.append(("Tasks Creation", test_tasks_creation()))
    test_results.append(("Workflow Setup", test_workflow_setup()))

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
        print("✅ GitHub agent is working perfectly!")
        print("🚀 Ready to add Notion and Calendar agents!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
        if passed >= 4:  # Setup tests passed
            print("💡 Setup is good, check execution issues.")
        else:
            print("💡 Fix setup issues before proceeding.")

    print("\n🎯 GitHub Agent Test Complete!")
    print("=" * 60)
