# agents/github_agent.py
"""
GitHub Agent for fetching issues and pull requests
Handles GitHub data retrieval and processing for the MCP client
"""

from crewai import Agent, LLM
from composio_crewai import Action
from tools.composio_setup import composio_tools
from llm.nebius_client import nebius_client
from config.settings import settings
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GitHubAgentBuilder:
    """Builder class for creating GitHub-focused CrewAI agent"""

    def __init__(self):
        self.llm = nebius_client.get_crewai_llm()
        self.tools = self._get_github_tools()

    def _get_github_tools(self):
        """Get specific GitHub tools needed for our workflow"""
        try:
            # Get the specific actions we tested and know work
            github_actions = [
                Action.GITHUB_ISSUES_LIST_FOR_REPO,
                Action.GITHUB_LIST_PULL_REQUESTS,
            ]

            tools = composio_tools.get_specific_actions(github_actions)
            logger.info(f"✅ GitHub tools loaded: {len(tools)} tools available")
            return tools

        except Exception as e:
            logger.error(f"❌ Failed to load GitHub tools: {e}")
            raise

    def create_agent(self) -> Agent:
        """Create and configure the GitHub agent"""

        agent = Agent(
            role="GitHub Data Fetcher",
            goal=f"""Fetch and analyze GitHub issues and pull requests from the {settings.TARGET_REPOSITORY} repository. 
            Focus on retrieving comprehensive data including titles, numbers, labels, assignees, and creation dates.""",
            backstory="""You are a specialized GitHub data analyst agent. Your expertise lies in efficiently 
            retrieving GitHub repository data, particularly issues and pull requests. You understand GitHub's 
            data structure and can extract meaningful information that will be used for project management 
            and bug tracking workflows. You always fetch recent data and pay special attention to labels 
            that might indicate bugs or urgent issues.""",
            verbose=True,
            allow_delegation=False,  # This agent works independently
            tools=self.tools,
            llm=LLM(
                model=settings.NEBIUS_MODEL,
                api_base=settings.NEBIUS_BASE_URL,
                api_key=settings.NEBIUS_API_KEY,
                temperature=0.3,
            ),
            max_execution_time=300,  # 5 minutes timeout
        )

        logger.info("✅ GitHub agent created successfully")
        return agent


def create_github_agent() -> Agent:
    """Factory function to create GitHub agent"""
    builder = GitHubAgentBuilder()
    return builder.create_agent()


# Create the agent instance for easy import
github_agent = create_github_agent()
