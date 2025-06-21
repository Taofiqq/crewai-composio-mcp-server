# agents/calendar_agent.py
"""
Google Calendar Agent for scheduling bug meetings
Sends meeting invitations ONLY to abumahfuz21@gmail.com when bugs are detected
"""

from crewai import Agent, LLM
from composio_crewai import Action
from tools.composio_setup import composio_tools
from config.settings import settings
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CalendarAgentBuilder:
    """Builder class for creating Calendar-focused CrewAI agent"""

    def __init__(self):
        self.tools = self._get_calendar_tools()

    def _get_calendar_tools(self):
        """Get specific Google Calendar tools needed for our workflow"""
        try:
            # Get the specific calendar action we tested and know works
            calendar_actions = [Action.GOOGLECALENDAR_CREATE_EVENT]

            tools = composio_tools.get_specific_actions(calendar_actions)
            logger.info(f"✅ Calendar tools loaded: {len(tools)} tools available")
            return tools

        except Exception as e:
            logger.error(f"❌ Failed to load Calendar tools: {e}")
            raise

    def create_agent(self) -> Agent:
        """Create and configure the Calendar agent"""

        agent = Agent(
            role="Bug Meeting Scheduler",
            goal=f"""Schedule Google Calendar meetings for bug-labeled GitHub issues and pull requests. 
            When bugs are detected, create meetings with a fixed attendee ({settings.DEFAULT_ATTENDEE_EMAIL}) and include 
            GitHub context in meeting descriptions. Focus on scheduling meetings within 
            {settings.MEETING_DURATION_MINUTES} minutes for items labeled with '{settings.BUG_LABEL}' or similar critical labels.
            
            CRITICAL: Always send meeting invitations ONLY to "{settings.DEFAULT_ATTENDEE_EMAIL}" - ignore all other emails.
            IMPORTANT: Always use the GOOGLECALENDAR_CREATE_EVENT tool to create calendar events.""",
            backstory="""You are a specialized bug meeting coordination agent. Your expertise lies in analyzing 
            GitHub issue and PR data to identify bugs that need immediate attention. When you find bugs, you 
            create well-structured calendar events with clear context and meaningful descriptions. You always 
            schedule meetings exactly 24 hours from the current time and include all relevant GitHub information 
            in the meeting details.
            
            Your key responsibility: When bugs are detected, schedule meetings with ONLY "{settings.DEFAULT_ATTENDEE_EMAIL}" 
            as the attendee. You ignore all GitHub assignees, reviewers, and authors - the meeting invitation 
            goes to one person only for centralized bug management.
            
            When creating calendar events, you always use the GOOGLECALENDAR_CREATE_EVENT tool with proper parameters.""",
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

        logger.info("✅ Calendar agent created successfully")
        return agent


def create_calendar_agent() -> Agent:
    """Factory function to create Calendar agent"""
    builder = CalendarAgentBuilder()
    return builder.create_agent()


# Create the agent instance for easy import
calendar_agent = create_calendar_agent()
