# agents/notion_agent.py
"""
Notion Agent for managing GitHub data in Notion databases
Handles database creation and data insertion from GitHub analysis
"""

from crewai import Agent, LLM
from composio_crewai import Action
from tools.composio_setup import composio_tools
from config.settings import settings
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NotionAgentBuilder:
    """Builder class for creating Notion-focused CrewAI agent"""

    def __init__(self):
        self.tools = self._get_notion_tools()

    def _get_notion_tools(self):
        """Get specific Notion tools needed for our workflow"""
        try:
            # Get the specific Notion actions we tested and know work
            notion_actions = [
                Action.NOTION_SEARCH_NOTION_PAGE,
                Action.NOTION_CREATE_DATABASE,
                Action.NOTION_INSERT_ROW_DATABASE,
            ]

            tools = composio_tools.get_specific_actions(notion_actions)
            logger.info(f"✅ Notion tools loaded: {len(tools)} tools available")
            return tools

        except Exception as e:
            logger.error(f"❌ Failed to load Notion tools: {e}")
            raise

    def create_agent(self) -> Agent:
        """Create and configure the Notion agent"""

        agent = Agent(
            role="Notion Database Manager",
            goal=f"""Manage GitHub data in Notion databases. Create a 'GitHub Issues & PRs' database 
            and populate it with GitHub issues and pull requests data from the analysis. 
            Follow the 3-step process: 1) Search for parent pages, 2) Create database, 3) Insert GitHub data.
            
            IMPORTANT: Always use the exact Notion action names:
            - NOTION_SEARCH_NOTION_PAGE
            - NOTION_CREATE_DATABASE  
            - NOTION_INSERT_ROW_DATABASE""",
            backstory="""You are a specialized Notion database management agent. Your expertise lies in 
            organizing GitHub repository data into structured Notion databases. You understand the Notion API 
            workflow: first finding parent pages, then creating databases with proper schemas, and finally 
            inserting data in the correct format. You always format GitHub data properly for Notion, 
            converting arrays to comma-separated strings and ensuring all values are in the right format.
            
            You follow this workflow:
            1. Search for available parent pages in the workspace
            2. Create a 'GitHub Issues & PRs' database with proper schema
            3. Insert GitHub issues and PRs data using the correct property format""",
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

        logger.info("✅ Notion agent created successfully")
        return agent


def create_notion_agent() -> Agent:
    """Factory function to create Notion agent"""
    builder = NotionAgentBuilder()
    return builder.create_agent()


# Create the agent instance for easy import
notion_agent = create_notion_agent()
