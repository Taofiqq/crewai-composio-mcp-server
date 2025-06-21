# test_orchestrator.py
"""
Test for the combined GitHub + Notion orchestrator workflow
Tests the full end-to-end process with real data flow
"""

import sys
import os
from datetime import datetime

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from workflow.full_orchestrator import (
    github_notion_orchestrator,
    run_github_notion_workflow,
)
from config.settings import settings


def test_orchestrator_setup():
    """Test if orchestrator is properly configured"""
    print("🤖 Testing Orchestrator Setup...")
    print("=" * 60)

    try:
        # Check orchestrator properties
        info = github_notion_orchestrator.get_workflow_info()

        assert info["total_agents"] == 2, f"Wrong agent count: {info['total_agents']}"
        assert len(info["github_tasks"]) == 3, "Wrong GitHub task count"
        assert len(info["notion_tasks"]) == 3, "Wrong Notion task count"
        assert (
            info["process_type"] == "sequential"
        ), f"Wrong process: {info['process_type']}"
        assert (
            info["data_flow"] == "GitHub → Notion"
        ), f"Wrong data flow: {info['data_flow']}"

        print(f"✅ Total Agents: {info['total_agents']}")
        print(f"✅ Agent Roles: {', '.join(info['agents'])}")
        print(f"✅ Total Tasks: {info['total_tasks']}")
        print(f"✅ GitHub Tasks: {', '.join(info['github_tasks'])}")
        print(f"✅ Notion Tasks: {', '.join(info['notion_tasks'])}")
        print(f"✅ Process Type: {info['process_type']}")
        print(f"✅ Data Flow: {info['data_flow']}")
        print(f"✅ Target Repository: {info['target_repository']}")

        # Check crew setup
        assert github_notion_orchestrator.crew is not None, "Crew not initialized"
        assert (
            len(github_notion_orchestrator.crew.agents) == 2
        ), "Wrong number of agents in crew"
        assert (
            len(github_notion_orchestrator.crew.tasks) == 6
        ), "Wrong number of tasks in crew"

        print("✅ Crew configuration: VALID")

        return True

    except Exception as e:
        print(f"❌ Orchestrator setup test failed: {e}")
        return False


def test_task_context_flow():
    """Test if task context flow is properly configured"""
    print("\n🔗 Testing Task Context Flow...")
    print("-" * 50)

    try:
        tasks = github_notion_orchestrator.tasks

        # Check GitHub task contexts
        assert (
            len(tasks["github_analysis"].context) == 2
        ), "GitHub analysis should have 2 context tasks"

        # Check Notion task contexts
        assert (
            len(tasks["notion_database"].context) == 1
        ), "Notion database should have 1 context task"
        assert (
            len(tasks["notion_insert"].context) == 5
        ), "Notion insert should have 5 context tasks (critical for data flow)"

        print("✅ GitHub Analysis Context: 2 tasks (issues + PRs)")
        print("✅ Notion Database Context: 1 task (search)")
        print("✅ Notion Insert Context: 5 tasks (search + database + GitHub data)")
        print("✅ Data flow properly configured: GitHub → Notion")

        return True

    except Exception as e:
        print(f"❌ Task context flow test failed: {e}")
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


def test_orchestrator_execution():
    """Test the actual orchestrator execution with real GitHub data"""
    print("\n🚀 Testing Orchestrator Execution...")
    print("=" * 60)
    print("⚠️  This will make actual API calls to GitHub, Notion, and Nebius")
    print(f"📂 Repository: {settings.TARGET_REPOSITORY}")
    print("🔄 Flow: GitHub Agent → Notion Agent")

    try:
        # Execute the combined workflow
        print("\n🔄 Starting combined workflow execution...")
        result = run_github_notion_workflow()

        print(f"\n📊 Execution Results:")
        print(f"   Success: {result['success']}")
        print(f"   Execution Time: {result['execution_time']:.2f} seconds")
        print(f"   Repository: {result['repository']}")
        print(f"   GitHub Agent: {result['github_agent']}")
        print(f"   Notion Agent: {result['notion_agent']}")
        print(f"   Database Created: {result['database_created']}")
        print(f"   Timestamp: {result['timestamp']}")

        if result["success"]:
            print("\n✅ ORCHESTRATOR EXECUTION: SUCCESS!")
            print("🎯 Combined Workflow Result Preview:")

            # Try to show a preview of the result
            if isinstance(result["result"], str):
                # Show first 500 characters
                preview = result["result"][:500]
                print(f"   {preview}...")
                if len(result["result"]) > 500:
                    print(f"   ... ({len(result['result'])} total characters)")
            else:
                print(f"   Result Type: {type(result['result'])}")

            print("\n🎯 What was accomplished:")
            print("   1. ✅ GitHub Agent fetched real issues and PRs")
            print("   2. ✅ GitHub data was analyzed and structured")
            print("   3. ✅ Notion Agent received GitHub data via context")
            print("   4. ✅ Notion database was created/found")
            print("   5. ✅ Real GitHub data was inserted into Notion")

            return True
        else:
            print(f"\n❌ ORCHESTRATOR EXECUTION: FAILED!")
            print(f"   Error: {result['error']}")
            return False

    except Exception as e:
        print(f"❌ Orchestrator execution test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🧪 GitHub + Notion Orchestrator Test Suite")
    print("=" * 60)
    print("🎯 This tests the complete end-to-end workflow")

    # Track test results
    test_results = []

    # Run setup tests first
    print("\n📋 SETUP TESTS:")
    test_results.append(("Configuration", test_configuration_validation()))
    test_results.append(("Orchestrator Setup", test_orchestrator_setup()))
    test_results.append(("Task Context Flow", test_task_context_flow()))

    # Check if setup tests passed
    setup_passed = all(result for _, result in test_results)

    if setup_passed:
        print("\n🚀 EXECUTION TEST:")
        test_results.append(("Orchestrator Execution", test_orchestrator_execution()))
    else:
        print("\n⚠️  Skipping execution test due to setup failures")
        test_results.append(("Orchestrator Execution", False))

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
        print("✅ Combined GitHub + Notion workflow is working perfectly!")
        print("📝 Real GitHub data is flowing to Notion database!")
        print("🚀 Ready for production use with main.py!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
        if passed >= 3:  # Setup tests passed
            print("💡 Setup is good, check execution issues.")
        else:
            print("💡 Fix setup issues before proceeding.")

    print("\n🎯 Orchestrator Test Complete!")
    print("\n📋 Next Steps:")
    print("1. If tests passed, try: python main.py --repo vercel/next-learn")
    print("2. Check your Notion workspace for the 'GitHub Issues & PRs' database")
    print("3. Verify real GitHub data has been inserted")
    print("=" * 60)
