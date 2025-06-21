# test_calendar_bug_agent.py
"""
Test for Calendar bug meeting agent, tasks, and workflow
Tests bug detection and meeting scheduling to abumahfuz21@gmail.com only
"""

import sys
import os
import json
from datetime import datetime

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from workflow.calendar_workflow import (
    calendar_bug_workflow,
    run_calendar_bug_workflow_standalone,
)
from agents.calendar_agent import calendar_agent
from tasks.calendar_tasks import calendar_tasks
from config.settings import settings


def test_agent_setup():
    """Test if Calendar bug agent is properly configured"""
    print("🤖 Testing Calendar Bug Agent Setup...")
    print("=" * 60)

    try:
        # Check agent properties
        assert (
            calendar_agent.role == "Bug Meeting Scheduler"
        ), f"Wrong role: {calendar_agent.role}"
        assert calendar_agent.tools is not None, "Agent has no tools"
        assert len(calendar_agent.tools) > 0, "Agent has empty tools list"

        print(f"✅ Agent Role: {calendar_agent.role}")
        print(f"✅ Agent Tools: {len(calendar_agent.tools)} tools loaded")
        print(f"✅ Agent LLM: Configured")
        print(f"✅ Allow Delegation: {calendar_agent.allow_delegation}")
        print("✅ Single Email Focus: abumahfuz21@gmail.com")

        # Check agent backstory mentions single email
        assert (
            "abumahfuz21@gmail.com" in calendar_agent.backstory
        ), "Agent doesn't mention target email"
        print("✅ Agent configured for single email recipient")

        return True

    except Exception as e:
        print(f"❌ Agent setup test failed: {e}")
        return False


def test_tasks_creation():
    """Test if Calendar bug tasks are properly created"""
    print("\n📋 Testing Calendar Bug Tasks Creation...")
    print("-" * 50)

    try:
        # Test individual task creation
        detection_task = calendar_tasks.detect_bugs_task()
        scheduling_task = calendar_tasks.schedule_bug_meetings_task()
        confirmation_task = calendar_tasks.meeting_confirmation_task()

        tasks = [
            ("Detect Bugs", detection_task),
            ("Schedule Bug Meetings", scheduling_task),
            ("Meeting Confirmation", confirmation_task),
        ]

        for task_name, task in tasks:
            assert task.description is not None, f"{task_name} has no description"
            assert (
                task.expected_output is not None
            ), f"{task_name} has no expected output"
            assert task.agent is not None, f"{task_name} has no agent assigned"

            print(f"   ✅ {task_name}: CONFIGURED")

        # Check that scheduling task mentions single email
        assert (
            "abumahfuz21@gmail.com" in scheduling_task.description
        ), "Scheduling task doesn't specify target email"
        print("✅ Scheduling task configured for single email recipient")

        print(f"✅ All {len(tasks)} tasks created successfully")
        return True

    except Exception as e:
        print(f"❌ Tasks creation test failed: {e}")
        return False


def test_workflow_setup():
    """Test if Calendar bug workflow is properly configured"""
    print("\n⚙️  Testing Calendar Bug Workflow Setup...")
    print("-" * 50)

    try:
        # Check workflow properties
        info = calendar_bug_workflow.get_workflow_info()

        assert info["total_tasks"] == 3, f"Wrong task count: {info['total_tasks']}"
        assert (
            info["process_type"] == "sequential"
        ), f"Wrong process: {info['process_type']}"
        assert (
            info["meeting_duration"] == settings.MEETING_DURATION_MINUTES
        ), "Wrong meeting duration"
        assert (
            info["recipient_email"] == "abumahfuz21@gmail.com"
        ), "Wrong recipient email"
        assert (
            info["meeting_schedule"] == "24 hours from execution time"
        ), "Wrong meeting schedule"

        print(f"✅ Agent Role: {info['agent_role']}")
        print(f"✅ Total Tasks: {info['total_tasks']}")
        print(f"✅ Task Names: {', '.join(info['task_names'])}")
        print(f"✅ Process Type: {info['process_type']}")
        print(f"✅ Meeting Duration: {info['meeting_duration']} minutes")
        print(f"✅ Bug Label: {info['bug_label']}")
        print(f"✅ Recipient Email: {info['recipient_email']}")
        print(f"✅ Meeting Schedule: {info['meeting_schedule']}")

        # Check crew setup
        assert calendar_bug_workflow.crew is not None, "Crew not initialized"
        assert len(calendar_bug_workflow.crew.agents) == 1, "Wrong number of agents"
        assert len(calendar_bug_workflow.crew.tasks) == 3, "Wrong number of tasks"

        print("✅ Crew configuration: VALID")
        print("✅ Single email workflow: CONFIGURED")

        return True

    except Exception as e:
        print(f"❌ Workflow setup test failed: {e}")
        return False


def test_calendar_tools():
    """Test if Calendar tools are properly loaded"""
    print("\n🛠️  Testing Calendar Tools...")
    print("-" * 50)

    try:
        # Check if agent has calendar tools
        tools = calendar_agent.tools

        assert tools is not None, "No tools loaded"
        assert len(tools) > 0, "Empty tools list"

        print(f"✅ Calendar tools loaded: {len(tools)} tools")

        # Try to import the action to verify it exists
        from composio_crewai import Action

        calendar_action = Action.GOOGLECALENDAR_CREATE_EVENT

        print("✅ Calendar action available: GOOGLECALENDAR_CREATE_EVENT")
        print("✅ Ready for bug meeting scheduling")

        return True

    except Exception as e:
        print(f"❌ Calendar tools test failed: {e}")
        return False


def test_bug_workflow_execution():
    """Test the actual bug meeting workflow execution"""
    print("\n🚀 Testing Calendar Bug Workflow Execution...")
    print("=" * 60)
    print("⚠️  This will make actual API calls to Google Calendar and Nebius")
    print("🐛 Will create bug meetings for sample GitHub data")
    print("📧 Meetings will be sent ONLY to: abumahfuz21@gmail.com")
    print(f"📅 Meeting Duration: {settings.MEETING_DURATION_MINUTES} minutes")
    print("⏰ Meetings scheduled 24 hours from now")

    try:
        # Execute the workflow with sample bug data
        print("\n🔄 Starting bug meeting workflow execution...")
        result = run_calendar_bug_workflow_standalone()

        print(f"\n📊 Execution Results:")
        print(f"   Success: {result['success']}")
        print(f"   Execution Time: {result['execution_time']:.2f} seconds")
        print(f"   Bug Label: {result['bug_label']}")
        print(f"   Meeting Duration: {result['meeting_duration']} minutes")
        print(f"   Recipient Email: {result['recipient_email']}")
        print(f"   Timestamp: {result['timestamp']}")

        if result["success"]:
            print("\n✅ BUG WORKFLOW EXECUTION: SUCCESS!")
            print("🎯 Bug Meeting Workflow Result Preview:")

            # Try to show a preview of the result
            if isinstance(result["result"], str):
                # Show first 500 characters
                preview = result["result"][:500]
                print(f"   {preview}...")
                if len(result["result"]) > 500:
                    print(f"   ... ({len(result['result'])} total characters)")
            else:
                print(f"   Result Type: {type(result['result'])}")

            print("\n📧 Expected Meeting Invitations:")
            print("   - Recipient: abumahfuz21@gmail.com ONLY")
            print("   - Subject: Bug Review: Making Composio work (#1)")
            print("   - Subject: Bug Review: Security vulnerability in auth (#1055)")
            print("   - Subject: Bug Review: Fix highlight bug in chapter 15 (#105)")
            print("   - Time: 24 hours from execution time")
            print("   - Duration: 30 minutes each")

            return True
        else:
            print(f"\n❌ BUG WORKFLOW EXECUTION: FAILED!")
            print(f"   Error: {result['error']}")
            return False

    except Exception as e:
        print(f"❌ Bug workflow execution test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_configuration_validation():
    """Validate configuration before running workflow"""
    print("\n🔧 Testing Configuration Validation...")
    print("-" * 50)

    try:
        # Check settings
        print(f"✅ Meeting Duration: {settings.MEETING_DURATION_MINUTES} minutes")
        print(f"✅ Bug Label: {settings.BUG_LABEL}")
        print(f"✅ Entity ID: {settings.ENTITY_ID}")

        # Check API keys (without exposing them)
        composio_key = "✓" if settings.COMPOSIO_API_KEY else "❌"
        nebius_key = "✓" if settings.NEBIUS_API_KEY else "❌"

        print(f"✅ Composio API Key: {composio_key}")
        print(f"✅ Nebius API Key: {nebius_key}")
        print("✅ Target Email: abumahfuz21@gmail.com")
        print("✅ Meeting Schedule: 24 hours from execution")

        if not settings.COMPOSIO_API_KEY or not settings.NEBIUS_API_KEY:
            print("⚠️  Missing API keys - workflow may fail")
            return False

        return True

    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        return False


if __name__ == "__main__":
    print("🧪 Calendar Bug Meeting Test Suite")
    print("=" * 60)
    print("🎯 This tests bug detection and meeting scheduling")
    print("📧 All meetings sent ONLY to: abumahfuz21@gmail.com")

    # Track test results
    test_results = []

    # Run setup tests first
    print("\n📋 SETUP TESTS:")
    test_results.append(("Configuration", test_configuration_validation()))
    test_results.append(("Agent Setup", test_agent_setup()))
    test_results.append(("Tasks Creation", test_tasks_creation()))
    test_results.append(("Workflow Setup", test_workflow_setup()))
    test_results.append(("Calendar Tools", test_calendar_tools()))

    # Check if setup tests passed
    setup_passed = all(result for _, result in test_results)

    if setup_passed:
        print("\n🚀 EXECUTION TEST:")
        test_results.append(("Bug Workflow Execution", test_bug_workflow_execution()))
    else:
        print("\n⚠️  Skipping execution test due to setup failures")
        test_results.append(("Bug Workflow Execution", False))

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
        print("✅ Calendar bug meeting system is working perfectly!")
        print("🐛 Bug detection and meeting scheduling ready!")
        print("📧 Meetings will be sent ONLY to: abumahfuz21@gmail.com")
        print("⏰ Meetings scheduled 24 hours from execution time")
        print("🚀 Ready to integrate with GitHub + Notion workflow!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
        if passed >= 5:  # Setup tests passed
            print("💡 Setup is good, check execution issues.")
        else:
            print("💡 Fix setup issues before proceeding.")

    print("\n🎯 Calendar Bug Meeting Test Complete!")
    print("\n📋 Prerequisites for success:")
    print("1. Run: composio add googlecalendar")
    print("2. Authenticate with your Google account")
    print("3. Grant calendar write permissions")
    print("4. Ensure abumahfuz21@gmail.com is a valid email")
    print("=" * 60)
