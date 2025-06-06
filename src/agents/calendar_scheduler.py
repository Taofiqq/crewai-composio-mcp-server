from crewai import Agent, LLM
from composio_crewai import ComposioToolSet, App
from config.settings import *


class CalendarScheduler:
    def __init__(self):
        self.toolset = ComposioToolSet(api_key=COMPOSIO_API_KEY)
        self.calendar_tools = self._get_calendar_tools()
        self.agent = self._create_agent()

    def _get_calendar_tools(self):
        """Get Google Calendar tools for our workflow"""
        return self.toolset.get_tools(apps=[App.GOOGLECALENDAR])

    def _create_agent(self):
        """Create the calendar scheduling agent"""
        return Agent(
            role="Meeting Coordination Specialist",
            goal="Schedule meetings by analyzing participant availability and optimizing time slots based on priority",
            backstory="""You are an efficient scheduling coordinator with expertise in time management 
            and calendar optimization for technical teams. You specialize in:
            - Analyzing bug severity and priority to determine meeting urgency
            - Scheduling appropriate meeting durations based on complexity
            - Managing attendee lists and ensuring proper stakeholder involvement
            - Optimizing meeting timing across timezones
            - Creating meeting agendas and linking relevant documentation
            - Coordinating follow-up meetings and recurring check-ins
            
            IMPORTANT SCHEDULING RULES:
            1. Current date is {datetime.now().strftime('%Y-%m-%d')}
            2. Always schedule meetings in the FUTURE, never in the past
            3. For critical issues: Schedule within 1-2 days from today
            4. For high priority: Schedule within 2-3 days from today  
            5. For medium priority: Schedule within 3-5 days from today
            6. Meeting times should be in business hours (9 AM - 5 PM)
            7. Always include the user's email as an attendee
            8. Use proper timezone formatting (e.g., 2025-06-07T14:00:00)
            """,
            tools=self.calendar_tools,
            llm=LLM(
                model=NEBIUS_MODEL,
                api_base=NEBIUS_BASE_URL,
                api_key=NEBIUS_API_KEY,
                temperature=0.7,
            ),
            # Lower temperature for precise scheduling
            memory=True,
            max_retry_limit=MAX_RETRY_LIMIT,
            verbose=VERBOSE_MODE,
        )

    def get_agent(self):
        """Return the configured agent"""
        return self.agent
