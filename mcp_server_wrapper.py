#!/usr/bin/env python3
"""
MCP Server Wrapper for CrewAI + Composio + Nebius Backend
Exposes GitHub analysis workflows as MCP tools via SSE transport
"""

import asyncio
import logging
from typing import Any, Dict, List
from datetime import datetime
import json

# MCP imports - using FastMCP for easier setup
from mcp.server.fastmcp import FastMCP
from mcp.types import Tool, TextContent

# Your existing workflow imports
from workflow.full_orchestrator import run_complete_workflow
from workflow.github_workflow import run_github_workflow
from workflow.notion_workflow import run_notion_workflow_with_data
from workflow.calendar_workflow import run_calendar_bug_workflow_with_data
from config.settings import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("github-analysis-mcp-server")

# Create FastMCP Server
mcp = FastMCP("github-analysis-backend")


@mcp.tool()
async def analyze_github_repository(
    repository: str, meeting_recipient: str = settings.DEFAULT_ATTENDEE_EMAIL
) -> str:
    """
    Complete GitHub repository analysis with Notion database creation and bug meeting scheduling.
    This is a long-running process (2-5 minutes) that will stream progress updates.

    Args:
        repository: GitHub repository in format 'owner/repo' (e.g., 'vercel/next-learn')
        meeting_recipient: Email address for meeting invitations
    """
    return await execute_complete_analysis(
        {"repository": repository, "meeting_recipient": meeting_recipient}
    )


@mcp.tool()
async def fetch_github_data(repository: str) -> str:
    """
    Fetch and analyze GitHub issues and pull requests only (no Notion/Calendar integration).
    Returns structured GitHub data.

    Args:
        repository: GitHub repository in format 'owner/repo'
    """
    result = await execute_github_fetch({"repository": repository})
    return result[0].text if result else "Error fetching GitHub data"


@mcp.tool()
async def create_notion_database(github_data: str) -> str:
    """
    Create Notion database with provided GitHub data. Takes structured GitHub analysis results.

    Args:
        github_data: JSON string or formatted text containing GitHub issues and PRs data
    """
    result = await execute_notion_creation({"github_data": github_data})
    return result[0].text if result else "Error creating Notion database"


@mcp.tool()
async def schedule_bug_meetings(
    github_data: str, meeting_recipient: str = settings.DEFAULT_ATTENDEE_EMAIL
) -> str:
    """
    Schedule bug review meetings based on GitHub data with bug labels.
    Analyzes data for bug-labeled items.

    Args:
        github_data: GitHub data containing issues/PRs with bug labels
        meeting_recipient: Email address for meeting invitations
    """
    result = await execute_calendar_scheduling(
        {"github_data": github_data, "meeting_recipient": meeting_recipient}
    )
    return result[0].text if result else "Error scheduling meetings"


@mcp.tool()
async def get_workflow_status() -> str:
    """
    Get current configuration and status of the GitHub analysis backend. Quick status check.
    """
    result = await execute_status_check()
    return result[0].text if result else "Error checking status"


async def execute_complete_analysis(arguments: Dict[str, Any]) -> str:
    """
    Execute complete GitHub analysis workflow with progress streaming
    This is the long-running process (2-5 minutes)
    """

    repository = arguments.get("repository")
    meeting_recipient = arguments.get(
        "meeting_recipient", settings.DEFAULT_ATTENDEE_EMAIL
    )

    logger.info(f"🚀 Starting complete analysis for: {repository}")

    # Validate repository format
    if not repository or "/" not in repository:
        return [
            TextContent(
                type="text",
                text="❌ Invalid repository format. Use 'owner/repo' format.",
            )
        ]

    # Update settings if meeting recipient provided
    if meeting_recipient != settings.DEFAULT_ATTENDEE_EMAIL:
        settings.DEFAULT_ATTENDEE_EMAIL = meeting_recipient

    # Create progress tracking
    progress_messages = []

    try:
        # Initial progress
        progress_messages.append("🚀 **Analysis Started**")
        progress_messages.append(f"📂 Repository: {repository}")
        progress_messages.append(f"📧 Meeting recipient: {meeting_recipient}")
        progress_messages.append("⏱️ Estimated time: 2-5 minutes")
        progress_messages.append("")

        # Execute the long-running workflow
        progress_messages.append("🔄 **Phase 1/3: GitHub Data Collection**")
        progress_messages.append("• Connecting to GitHub API...")
        progress_messages.append("• Fetching issues and pull requests...")
        progress_messages.append("• Analyzing bug labels and priorities...")

        # Note: In a real streaming implementation, you'd send these messages
        # as they happen. For now, we're collecting them and running the workflow.

        start_time = datetime.now()
        result = run_complete_workflow(repository)
        end_time = datetime.now()

        if result["success"]:
            progress_messages.append("✅ GitHub data collection completed!")
            progress_messages.append("")
            progress_messages.append("🔄 **Phase 2/3: Notion Database Creation**")
            progress_messages.append("• Searching for parent pages in Notion...")
            progress_messages.append("• Creating 'GitHub Issues & PRs' database...")
            progress_messages.append("• Inserting GitHub data into Notion...")
            progress_messages.append("✅ Notion database created successfully!")
            progress_messages.append("")
            progress_messages.append("🔄 **Phase 3/3: Bug Meeting Scheduling**")
            progress_messages.append("• Detecting bug-labeled items...")
            progress_messages.append("• Scheduling review meetings...")
            progress_messages.append("• Sending calendar invitations...")
            progress_messages.append("✅ Bug meetings scheduled successfully!")
            progress_messages.append("")

            # Final summary
            execution_time = (end_time - start_time).total_seconds()
            summary = f"""✅ **Complete Analysis Finished Successfully!**

📊 **Results Summary:**
• Repository: {result['repository']}
• Execution Time: {execution_time:.1f} seconds
• GitHub Agent: {result['github_agent']}
• Notion Agent: {result['notion_agent']}
• Calendar Agent: {result['calendar_agent']}
• Database Created: {result['database_created']}
• Meetings Scheduled: {result['meetings_scheduled']}
• Meeting Recipient: {result['meeting_recipient']}

🎯 **What was accomplished:**
• Fetched GitHub issues and pull requests
• Analyzed data for bugs and priorities  
• Created 'GitHub Issues & PRs' database in Notion
• Inserted all GitHub data into Notion
• Detected bug-labeled items requiring meetings
• Scheduled bug review meetings in Google Calendar
• Sent meeting invitations to {result['meeting_recipient']}

🔗 **Next Steps:**
• Check Notion workspace for the new database
• Review scheduled calendar meetings
• Attend bug review sessions as planned"""

            progress_messages.append(summary)

        else:
            progress_messages.append(f"❌ **Analysis Failed**")
            progress_messages.append(f"Error: {result['error']}")
            progress_messages.append(
                f"Execution time: {result['execution_time']:.1f} seconds"
            )

        # Return all progress as a single response
        # In a real streaming implementation, these would be sent as individual SSE events
        full_response = "\n".join(progress_messages)
        return full_response

    except Exception as e:
        error_message = f"❌ **Unexpected Error During Analysis**\n\nError: {str(e)}\nRepository: {repository}"
        return error_message


async def execute_github_fetch(arguments: Dict[str, Any]) -> List[TextContent]:
    """Execute GitHub data fetching only"""

    repository = arguments.get("repository")
    logger.info(f"📂 Fetching GitHub data for: {repository}")

    try:
        # Temporarily update target repository
        original_repo = settings.TARGET_REPOSITORY
        settings.TARGET_REPOSITORY = repository

        # Run GitHub workflow only
        result = run_github_workflow()

        # Restore original setting
        settings.TARGET_REPOSITORY = original_repo

        if result["success"]:
            response = f"""✅ **GitHub Data Fetched Successfully!**

📂 **Repository:** {result['repository']}
⏱️ **Execution Time:** {result['execution_time']:.1f} seconds
🕒 **Completed:** {result['timestamp']}

📊 **Data Retrieved:**
• GitHub issues with labels and assignees
• Pull requests with authors and states
• Bug analysis and priority assessment

📋 **Summary:**
{str(result['result'])[:500]}{'...' if len(str(result['result'])) > 500 else ''}

💡 **Usage:**
Use this data with 'create_notion_database' or 'schedule_bug_meetings' tools."""

            return [TextContent(type="text", text=response)]

        else:
            return [
                TextContent(
                    type="text",
                    text=f"❌ **GitHub Fetch Failed**\n\nError: {result['error']}\nRepository: {repository}",
                )
            ]

    except Exception as e:
        return [
            TextContent(
                type="text",
                text=f"❌ **Error Fetching GitHub Data**\n\nError: {str(e)}\nRepository: {repository}",
            )
        ]


async def execute_notion_creation(arguments: Dict[str, Any]) -> List[TextContent]:
    """Execute Notion database creation with GitHub data"""

    github_data = arguments.get("github_data", "")
    logger.info("📝 Creating Notion database with provided GitHub data")

    try:
        result = run_notion_workflow_with_data(github_data)

        if result["success"]:
            response = f"""✅ **Notion Database Created Successfully!**

⏱️ **Execution Time:** {result['execution_time']:.1f} seconds
🕒 **Completed:** {result['timestamp']}

📊 **Accomplished:**
• Searched for parent pages in Notion
• Created 'GitHub Issues & PRs' database
• Inserted provided GitHub data
• Structured data with proper properties and relations

🎯 **Next Steps:**
Check your Notion workspace for the new 'GitHub Issues & PRs' database!"""

            return [TextContent(type="text", text=response)]

        else:
            return [
                TextContent(
                    type="text",
                    text=f"❌ **Notion Creation Failed**\n\nError: {result['error']}",
                )
            ]

    except Exception as e:
        return [
            TextContent(
                type="text",
                text=f"❌ **Error Creating Notion Database**\n\nError: {str(e)}",
            )
        ]


async def execute_calendar_scheduling(arguments: Dict[str, Any]) -> List[TextContent]:
    """Execute calendar meeting scheduling for bugs"""

    github_data = arguments.get("github_data", "")
    meeting_recipient = arguments.get(
        "meeting_recipient", settings.DEFAULT_ATTENDEE_EMAIL
    )

    logger.info(f"📅 Scheduling bug meetings for: {meeting_recipient}")

    try:
        # Update settings if recipient provided
        if meeting_recipient != settings.DEFAULT_ATTENDEE_EMAIL:
            settings.DEFAULT_ATTENDEE_EMAIL = meeting_recipient

        result = run_calendar_bug_workflow_with_data(github_data)

        if result["success"]:
            response = f"""✅ **Bug Review Meetings Scheduled Successfully!**

⏱️ **Execution Time:** {result['execution_time']:.1f} seconds
📧 **Meeting Recipient:** {result['recipient_email']}
⏰ **Meeting Duration:** {result['meeting_duration']} minutes
🏷️ **Bug Label:** {result['bug_label']}
🕒 **Completed:** {result['timestamp']}

📊 **Accomplished:**
• Detected bug-labeled items in GitHub data
• Scheduled review meetings 24 hours from now
• Sent calendar invitations to {result['recipient_email']}
• Set up {result['meeting_duration']}-minute meeting slots

🎯 **Next Steps:**
Check {result['recipient_email']}'s calendar for meeting invitations!"""

            return [TextContent(type="text", text=response)]

        else:
            return [
                TextContent(
                    type="text",
                    text=f"❌ **Calendar Scheduling Failed**\n\nError: {result['error']}",
                )
            ]

    except Exception as e:
        return [
            TextContent(
                type="text", text=f"❌ **Error Scheduling Meetings**\n\nError: {str(e)}"
            )
        ]


async def execute_status_check() -> List[TextContent]:
    """Execute workflow status and configuration check"""

    try:
        config_status = f"""📊 **GitHub Analysis Backend Status**

🔧 **Configuration:**
• Target Repository: {settings.TARGET_REPOSITORY}
• Bug Label: {settings.BUG_LABEL}
• Meeting Duration: {settings.MEETING_DURATION_MINUTES} minutes
• Default Attendee: {settings.DEFAULT_ATTENDEE_EMAIL}

🔑 **API Keys Status:**
• Composio API Key: {'✅ Configured' if settings.COMPOSIO_API_KEY else '❌ Missing'}
• Nebius API Key: {'✅ Configured' if settings.NEBIUS_API_KEY else '❌ Missing'}

🛠️ **Available Workflows:**
• Complete Analysis (GitHub → Notion → Calendar)
• GitHub Data Fetching Only
• Notion Database Creation
• Bug Meeting Scheduling

🔌 **MCP Integration:**
• Server Status: ✅ Running
• Transport: SSE (Server-Sent Events)
• Tools Available: 5
• Protocol: JSON-RPC 2.0

⏰ **System Info:**
• Timestamp: {datetime.now().isoformat()}
• Logging Level: INFO
• Long-running Process Support: ✅ Yes (2-5 minutes)"""

        return [TextContent(type="text", text=config_status)]

    except Exception as e:
        return [
            TextContent(
                type="text", text=f"❌ **Error Checking Status**\n\nError: {str(e)}"
            )
        ]


def main():
    """Main entry point for FastMCP server with SSE transport"""

    logger.info("🚀 Starting GitHub Analysis MCP Server")
    logger.info(f"📂 Default repository: {settings.TARGET_REPOSITORY}")
    logger.info(f"🔧 Available tools: 5")
    logger.info("🌐 SSE transport enabled for long-running processes")
    logger.info("⏱️ Ready to handle 2-5 minute CrewAI workflows")
    logger.info("🌐 Server will be available at http://localhost:8080/sse")

    # Run the FastMCP server with SSE transport
    # FastMCP automatically sets up SSE at /sse endpoint
    mcp.run(transport="sse")


if __name__ == "__main__":
    # Run the FastMCP server (non-async for FastMCP)
    main()
