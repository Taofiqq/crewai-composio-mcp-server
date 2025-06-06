import sys

sys.path.append(".")
from src.workflows.github_workflow import GitHubWorkflow


def main():
    """Main entry point for the GitHub analysis workflow"""

    # Example usage
    repo_url = "https://github.com/facebook/react"
    issue_number = "31902"  # A real React issue for testing

    try:
        print("🔧 Initializing GitHub Analysis Workflow...")
        workflow = GitHubWorkflow()

        print("📊 Crew Information:")
        info = workflow.get_crew_info()
        for key, value in info.items():
            print(f"   {key}: {value}")

        print(f"\n🎯 Executing workflow for: {repo_url}/issues/{issue_number}")
        result = workflow.execute(repo_url, issue_number)

        print(f"\n📋 Workflow Result:")
        print(result)

    except Exception as e:
        print(f"💥 Error: {e}")


if __name__ == "__main__":
    main()
