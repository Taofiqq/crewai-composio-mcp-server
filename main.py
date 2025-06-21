# # main.py
# """
# Main entry point for GitHub repository analysis
# Analyzes GitHub repos and creates Notion databases with the data
# """

# import argparse
# import sys
# import os
# from datetime import datetime

# # Add the backend directory to Python path
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# from workflow.orchestrator import run_github_notion_workflow
# from config.settings import settings
# import logging

# # Set up logging
# logging.basicConfig(
#     level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# )
# logger = logging.getLogger(__name__)


# def validate_repository(repo: str) -> bool:
#     """Validate repository format (owner/repo)"""
#     if not repo or "/" not in repo:
#         return False

#     parts = repo.split("/")
#     if len(parts) != 2:
#         return False

#     owner, name = parts
#     if not owner or not name:
#         return False

#     return True


# def main():
#     """Main function to run GitHub repository analysis"""

#     parser = argparse.ArgumentParser(
#         description="Analyze GitHub repository and create Notion database",
#         formatter_class=argparse.RawDescriptionHelpFormatter,
#         epilog="""
# Examples:
#   python main.py --repo vercel/next-learn
#   python main.py --repo facebook/react
#   python main.py --repo microsoft/vscode
#   python main.py  # Uses default repo from settings
#         """,
#     )

#     parser.add_argument(
#         "--repo",
#         "--repository",
#         type=str,
#         help='GitHub repository in format "owner/repo" (e.g., vercel/next-learn)',
#         default=None,
#     )

#     parser.add_argument(
#         "--verbose", "-v", action="store_true", help="Enable verbose output"
#     )

#     args = parser.parse_args()

#     # Set up logging level
#     if args.verbose:
#         logging.getLogger().setLevel(logging.DEBUG)

#     # Determine target repository
#     target_repo = args.repo or settings.TARGET_REPOSITORY

#     # Validate repository format
#     if not validate_repository(target_repo):
#         logger.error(f"❌ Invalid repository format: {target_repo}")
#         logger.error(
#             "Repository must be in format 'owner/repo' (e.g., 'vercel/next-learn')"
#         )
#         sys.exit(1)

#     # Print startup information
#     print("🚀 GitHub Repository Analysis & Notion Integration")
#     print("=" * 60)
#     print(f"📂 Target Repository: {target_repo}")
#     print(f"📝 Notion Database: GitHub Issues & PRs")
#     print(f"🔍 Bug Label: {settings.BUG_LABEL}")
#     print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
#     print("=" * 60)

#     try:
#         # Validate configuration
#         if not settings.COMPOSIO_API_KEY:
#             logger.error("❌ COMPOSIO_API_KEY not found in environment")
#             sys.exit(1)

#         if not settings.NEBIUS_API_KEY:
#             logger.error("❌ NEBIUS_API_KEY not found in environment")
#             sys.exit(1)

#         logger.info("✅ Configuration validated")

#         # Execute the combined workflow
#         logger.info(f"🔄 Starting analysis of repository: {target_repo}")

#         result = run_github_notion_workflow(target_repo)

#         # Process results
#         if result["success"]:
#             print("\n" + "=" * 60)
#             print("🎉 ANALYSIS COMPLETED SUCCESSFULLY!")
#             print("=" * 60)
#             print(f"✅ Repository: {result['repository']}")
#             print(f"✅ Execution Time: {result['execution_time']:.2f} seconds")
#             print(f"✅ GitHub Agent: {result['github_agent']}")
#             print(f"✅ Notion Agent: {result['notion_agent']}")
#             print(f"✅ Database Created: {result['database_created']}")
#             print(f"✅ Timestamp: {result['timestamp']}")

#             print("\n📊 What was accomplished:")
#             print("• Fetched GitHub issues from the repository")
#             print("• Fetched GitHub pull requests from the repository")
#             print("• Analyzed GitHub data for bugs and priorities")
#             print("• Created 'GitHub Issues & PRs' database in Notion")
#             print("• Inserted all GitHub data into the Notion database")

#             print("\n🎯 Next Steps:")
#             print(
#                 "• Check your Notion workspace for the 'GitHub Issues & PRs' database"
#             )
#             print("• Review the inserted GitHub issues and pull requests")
#             print("• Use the data for project management and bug tracking")

#             sys.exit(0)

#         else:
#             print("\n" + "=" * 60)
#             print("❌ ANALYSIS FAILED!")
#             print("=" * 60)
#             print(f"❌ Repository: {result['repository']}")
#             print(f"❌ Error: {result['error']}")
#             print(f"❌ Execution Time: {result['execution_time']:.2f} seconds")
#             print(f"❌ Timestamp: {result['timestamp']}")

#             print("\n💡 Troubleshooting:")
#             print("• Check that the repository exists and is accessible")
#             print("• Verify your Composio and Nebius API keys")
#             print("• Ensure GitHub and Notion are connected to Composio")
#             print("• Check your internet connection")

#             sys.exit(1)

#     except KeyboardInterrupt:
#         print("\n\n⚠️ Analysis interrupted by user")
#         logger.info("Analysis interrupted by user (Ctrl+C)")
#         sys.exit(1)

#     except Exception as e:
#         print(f"\n❌ Unexpected error: {e}")
#         logger.error(f"Unexpected error: {e}", exc_info=True)
#         sys.exit(1)


# if __name__ == "__main__":
#     main()


# main.py
"""
Main entry point for GitHub repository analysis
Analyzes GitHub repos and creates Notion databases with the data
"""

import argparse
import sys
import os
from datetime import datetime

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from workflow.full_orchestrator import run_complete_workflow
from config.settings import settings
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def validate_repository(repo: str) -> bool:
    """Validate repository format (owner/repo)"""
    if not repo or "/" not in repo:
        return False

    parts = repo.split("/")
    if len(parts) != 2:
        return False

    owner, name = parts
    if not owner or not name:
        return False

    return True


def main():
    """Main function to run GitHub repository analysis"""

    parser = argparse.ArgumentParser(
        description="Analyze GitHub repository and create Notion database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --repo vercel/next-learn
  python main.py --repo facebook/react
  python main.py --repo microsoft/vscode
  python main.py  # Uses default repo from settings
        """,
    )

    parser.add_argument(
        "--repo",
        "--repository",
        type=str,
        help='GitHub repository in format "owner/repo" (e.g., vercel/next-learn)',
        default=None,
    )

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )

    args = parser.parse_args()

    # Set up logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Determine target repository
    target_repo = args.repo or settings.TARGET_REPOSITORY

    # Validate repository format
    if not validate_repository(target_repo):
        logger.error(f"❌ Invalid repository format: {target_repo}")
        logger.error(
            "Repository must be in format 'owner/repo' (e.g., 'vercel/next-learn')"
        )
        sys.exit(1)

    # Print startup information
    print("🚀 Complete GitHub Repository Analysis & Integration")
    print("=" * 60)
    print(f"📂 Target Repository: {target_repo}")
    print(f"📝 Notion Database: GitHub Issues & PRs")
    print(f"📅 Calendar Meetings: Bug review meetings")
    print(f"📧 Meeting Invitations: {settings.DEFAULT_ATTENDEE_EMAIL}")
    print(f"🔍 Bug Label: {settings.BUG_LABEL}")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    try:
        # Validate configuration
        if not settings.COMPOSIO_API_KEY:
            logger.error("❌ COMPOSIO_API_KEY not found in environment")
            sys.exit(1)

        if not settings.NEBIUS_API_KEY:
            logger.error("❌ NEBIUS_API_KEY not found in environment")
            sys.exit(1)

        logger.info("✅ Configuration validated")

        # Execute the combined workflow
        logger.info(f"🔄 Starting analysis of repository: {target_repo}")

        result = run_complete_workflow(target_repo)

        # Process results
        if result["success"]:
            print("\n" + "=" * 60)
            print("🎉 ANALYSIS COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            print(f"✅ Repository: {result['repository']}")
            print(f"✅ Execution Time: {result['execution_time']:.2f} seconds")
            print(f"✅ GitHub Agent: {result['github_agent']}")
            print(f"✅ Notion Agent: {result['notion_agent']}")
            print(f"✅ Calendar Agent: {result['calendar_agent']}")
            print(f"✅ Database Created: {result['database_created']}")
            print(f"✅ Meetings Scheduled: {result['meetings_scheduled']}")
            print(f"✅ Meeting Recipient: {result['meeting_recipient']}")
            print(f"✅ Timestamp: {result['timestamp']}")

            print("\n📊 What was accomplished:")
            print("• Fetched GitHub issues from the repository")
            print("• Fetched GitHub pull requests from the repository")
            print("• Analyzed GitHub data for bugs and priorities")
            print("• Created 'GitHub Issues & PRs' database in Notion")
            print("• Inserted all GitHub data into the Notion database")
            print("• Detected bug-labeled items requiring meetings")
            print("• Scheduled bug review meetings in Google Calendar")
            print(f"• Sent meeting invitations to {result['meeting_recipient']}")

            print("\n🎯 Next Steps:")
            print(
                "• Check your Notion workspace for the 'GitHub Issues & PRs' database"
            )
            print("• Review the inserted GitHub issues and pull requests")
            print(
                f"• Check {result['meeting_recipient']}'s calendar for bug meeting invitations"
            )
            print("• Attend scheduled bug review meetings")
            print("• Use the data for project management and bug tracking")

            sys.exit(0)

        else:
            print("\n" + "=" * 60)
            print("❌ ANALYSIS FAILED!")
            print("=" * 60)
            print(f"❌ Repository: {result['repository']}")
            print(f"❌ Error: {result['error']}")
            print(f"❌ Execution Time: {result['execution_time']:.2f} seconds")
            print(f"❌ Timestamp: {result['timestamp']}")

            print("\n💡 Troubleshooting:")
            print("• Check that the repository exists and is accessible")
            print("• Verify your Composio and Nebius API keys")
            print("• Ensure GitHub and Notion are connected to Composio")
            print("• Check your internet connection")

            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n⚠️ Analysis interrupted by user")
        logger.info("Analysis interrupted by user (Ctrl+C)")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
