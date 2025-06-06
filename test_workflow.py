import sys

sys.path.append(".")
from src.workflows.github_workflow import GitHubWorkflow


def test_workflow_setup():
    """Test that the workflow can be initialized"""
    try:
        print("🔧 Testing workflow initialization...")
        workflow = GitHubWorkflow()

        print("✅ Workflow initialized successfully!")

        info = workflow.get_crew_info()
        print("📊 Crew Info:")
        for key, value in info.items():
            print(f"   {key}: {value}")

        return True

    except Exception as e:
        print(f"❌ Workflow initialization failed: {e}")
        return False


if __name__ == "__main__":
    test_workflow_setup()
