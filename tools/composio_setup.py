from composio_crewai import ComposioToolSet, App, Action
from config.settings import settings


class ComposioTools:
    def __init__(self):
        self.toolset = ComposioToolSet()
        self.entity_id = settings.ENTITY_ID

    def get_github_tools(self):
        """Get GitHub-specific tools."""
        return self.toolset.get_tools(apps=[App.GITHUB], entity_id=self.entity_id)

    def get_notion_tools(self):
        """Get Notion-specific tools."""
        return self.toolset.get_tools(apps=[App.NOTION], entity_id=self.entity_id)

    def get_calendar_tools(self):
        """Get Google Calendar tools."""
        return self.toolset.get_tools(
            apps=[App.GOOGLECALENDAR], entity_id=self.entity_id
        )

    def get_specific_actions(self, actions):
        """Get specific Composio actions."""
        return self.toolset.get_tools(actions=actions, entity_id=self.entity_id)


# Initialize tools
composio_tools = ComposioTools()
