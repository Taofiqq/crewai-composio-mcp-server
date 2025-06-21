# tasks/github_tasks.py
"""
GitHub-specific tasks for CrewAI workflow
Defines tasks for fetching issues and pull requests
"""

from crewai import Task
from agents.github_agent import github_agent
from config.settings import settings
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GitHubTasks:
    """Container class for GitHub-related tasks"""

    @staticmethod
    def fetch_issues_task() -> Task:
        """Task to fetch GitHub issues from target repository"""

        task = Task(
            description=f"""
            Fetch the most recent GitHub issues from the {settings.TARGET_REPOSITORY} repository.
            
            Requirements:
            1. Get at least 1 recent issues (open or closed)
            2. Extract the following information for each issue:
               - Title
               - Issue number
               - State (open/closed)
               - Labels (especially look for '{settings.BUG_LABEL}' labels)
               - Assignees
               - Created date
               - Author
            3. Focus on issues that might need attention (bugs, critical issues)
            4. Return the data in a structured format
            
            Repository: {settings.TARGET_REPOSITORY}
            """,
            expected_output="""
            A structured report containing:
            - Total number of issues fetched
            - List of issues with their details (title, number, labels, assignees, dates)
            - Summary of any bug-labeled issues found
            - Issues that might need immediate attention
            
            Format the output as a clear, organized report.
            """,
            agent=github_agent,
            tools=github_agent.tools,
        )

        logger.info("✅ GitHub issues task created")
        return task

    @staticmethod
    def fetch_pull_requests_task() -> Task:
        """Task to fetch GitHub pull requests from target repository"""

        task = Task(
            description=f"""
            Fetch the most recent GitHub pull requests from the {settings.TARGET_REPOSITORY} repository.
            
            Requirements:
            1. Get at least 3 recent pull requests (open or closed)
            2. Extract the following information for each PR:
               - Title
               - PR number
               - State (open/closed/merged)
               - Labels (especially look for '{settings.BUG_LABEL}' labels)
               - Author
               - Assignees
               - Requested reviewers
               - Created date
               - Draft status
            3. Focus on PRs that might contain bug fixes or critical changes
            4. Return the data in a structured format
            
            Repository: {settings.TARGET_REPOSITORY}
            """,
            expected_output="""
            A structured report containing:
            - Total number of pull requests fetched
            - List of PRs with their details (title, number, labels, assignees, reviewers, dates)
            - Summary of any bug-related PRs found
            - PRs that might need review attention
            
            Format the output as a clear, organized report.
            """,
            agent=github_agent,
            tools=github_agent.tools,
        )

        logger.info("✅ GitHub pull requests task created")
        return task

    @staticmethod
    def analyze_github_data_task() -> Task:
        """Task to analyze the fetched GitHub data"""

        task = Task(
            description=f"""
            Analyze the GitHub issues and pull requests data that was fetched in the previous tasks.
            
            Requirements:
            1. Review all the issues and PRs data
            2. Identify items labeled with '{settings.BUG_LABEL}' or similar critical labels
            3. List all unique assignees and reviewers found
            4. Categorize issues/PRs by priority (based on labels and content)
            5. Provide actionable insights
            
            Focus on finding items that might need immediate attention or meeting scheduling.
            """,
            expected_output="""
            An analysis report containing:
            - Summary statistics (total issues, PRs, bugs found)
            - List of bug-labeled items with their assignees
            - List of all people involved (assignees, reviewers, authors)
            - Priority categorization of found items
            - Recommendations for follow-up actions
            
            This analysis will be used to determine what meetings need to be scheduled.
            """,
            agent=github_agent,
            context=[],  # Will be populated with previous task outputs
        )

        logger.info("✅ GitHub analysis task created")
        return task


# Create task instances for easy import
github_tasks = GitHubTasks()

# Individual task instances
fetch_issues_task = github_tasks.fetch_issues_task()
fetch_pull_requests_task = github_tasks.fetch_pull_requests_task()
analyze_github_data_task = github_tasks.analyze_github_data_task()
