from crewai import Agent, LLM
from composio_crewai import ComposioToolSet, App
from config.settings import *


class NotionWriter:
    def __init__(self):
        self.toolset = ComposioToolSet(api_key=COMPOSIO_API_KEY)
        self.notion_tools = self._get_notion_tools()
        self.agent = self._create_agent()

    def _get_notion_tools(self):
        """Get Notion tools for our workflow"""
        return self.toolset.get_tools(apps=[App.NOTION])

    def _create_agent(self):
        """Create the Notion documentation agent"""
        return Agent(
            role="Technical Documentation Specialist",
            goal="Create comprehensive technical documentation in Notion with proper formatting and structure",
            backstory="""You are a professional technical writer with expertise in software documentation. 
            You specialize in:
            - Transforming complex technical analysis into clear, actionable documentation
            - Creating structured Notion pages with proper formatting and organization
            - Building documentation databases and tracking systems
            - Writing executive summaries and technical deep-dives
            - Organizing information for easy consumption by technical and non-technical stakeholders""",
            tools=self.notion_tools,
            llm=LLM(
                model=NEBIUS_MODEL,
                api_base=NEBIUS_BASE_URL,
                api_key=NEBIUS_API_KEY,
                temperature=0.7,
            ),
            memory=True,
            max_retry_limit=MAX_RETRY_LIMIT,
            verbose=VERBOSE_MODE,
        )

    def get_agent(self):
        """Return the configured agent"""
        return self.agent
