import sys

sys.path.append(".")
from src.agents.calendar_scheduler import CalendarScheduler


def test_calendar_agent():
    try:
        print("📅 Creating Calendar Scheduler Agent...")
        scheduler = CalendarScheduler()
        agent = scheduler.get_agent()

        print("✅ Calendar Agent created successfully!")
        print(f"   Role: {agent.role}")
        print(f"   Tools available: {len(agent.tools)}")
        print(f"   LLM: {agent.llm}")
        print(f"   Temperature: {agent.llm.temperature}")

        return True
    except Exception as e:
        print(f"❌ Failed to create Calendar agent: {e}")
        return False


if __name__ == "__main__":
    test_calendar_agent()
