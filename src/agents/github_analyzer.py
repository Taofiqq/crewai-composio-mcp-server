# from crewai import Agent, LLM
# from composio_crewai import ComposioToolSet, Action, App
# from config.settings import *


# class GitHubAnalyzer:
#     def __init__(self):
#         self.toolset = ComposioToolSet(api_key=COMPOSIO_API_KEY)
#         self.github_tools = self._get_github_tools()
#         self.agent = self._create_agent()

#     def _get_github_tools(self):
#         """Get GitHub tools for our workflow"""
#         return self.toolset.get_tools(apps=[App.GITHUB])

#     def _create_agent(self):
#         """Create the GitHub analysis agent"""
#         return Agent(
#             role="Senior GitHub Repository Analyst",
#             goal="Analyze GitHub issues and PRs for bug detection, priority assessment, and maintainer identification",
#             backstory="""You are an expert software engineer with 10+ years of experience
#             analyzing GitHub repositories. You specialize in:
#             - Identifying bug patterns and severity levels
#             - Extracting maintainer and contributor information
#             - Analyzing issue labels and content for priority classification
#             - Understanding repository structure and project health metrics""",
#             tools=self.github_tools,
#             # llm=LLM(model="gpt-4o", temperature=0.3),
#             memory=True,
#             max_retry_limit=MAX_RETRY_LIMIT,
#             verbose=VERBOSE_MODE,
#         )

#     def get_agent(self):
#         """Return the configured agent"""
#         return self.agent


from crewai import Agent, LLM
from composio_crewai import ComposioToolSet, App
from config.settings import *


class GitHubAnalyzer:
    def __init__(self):
        self.toolset = ComposioToolSet(api_key=COMPOSIO_API_KEY)
        self.github_tools = self._get_github_tools()
        self.agent = self._create_agent()

    def _get_github_tools(self):
        """Get GitHub tools for our workflow"""
        return self.toolset.get_tools(apps=[App.GITHUB])

    def _create_agent(self):
        """Create the GitHub analysis agent"""
        return Agent(
            role="Senior GitHub Repository Analyst",
            goal="Analyze GitHub issues and PRs for bug detection, priority assessment, and maintainer identification",
            backstory="""You are an expert software engineer with 10+ years of experience 
            analyzing GitHub repositories.""",
            tools=self.github_tools,
            llm=LLM(
                model=NEBIUS_MODEL,
                api_base=NEBIUS_BASE_URL,
                api_key=NEBIUS_API_KEY,
                temperature=0.3,
            ),
            memory=True,
            max_retry_limit=MAX_RETRY_LIMIT,
            verbose=VERBOSE_MODE,
        )

    def get_agent(self):
        return self.agent
