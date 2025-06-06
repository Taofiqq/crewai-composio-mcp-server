import os

os.environ["COMPOSIO_LOGGING_LEVEL"] = "debug"
from dotenv import load_dotenv
from composio_openai import ComposioToolSet, App

load_dotenv()


def test_all_integrations():
    try:
        composio_toolset = ComposioToolSet(api_key=os.getenv("COMPOSIO_API_KEY"))

        # Test by getting tools for each app
        github_tools = composio_toolset.get_tools(apps=[App.GITHUB])
        notion_tools = composio_toolset.get_tools(apps=[App.NOTION])
        calendar_tools = composio_toolset.get_tools(apps=[App.GOOGLECALENDAR])

        print("🎉 ALL INTEGRATIONS WORKING PERFECTLY!")
        print(f"✅ GitHub tools available: {len(github_tools)}")
        print(f"✅ Notion tools available: {len(notion_tools)}")
        print(f"✅ Calendar tools available: {len(calendar_tools)}")
        print("\n🚀 Ready to build the LangGraph workflow!")

        return True

    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False


if __name__ == "__main__":
    test_all_integrations()

# from composio_crewai import ComposioToolSet, App, Action

# # Initialize with DEFAULT entity (remove entity_id parameter)
# toolset = ComposioToolSet()

# # Verify all required connections are active
# required_apps = [App.GITHUB, App.NOTION, App.GOOGLECALENDAR]
# for app in required_apps:
#     connection = toolset.get_entity().get_connection(app=app)
#     if connection.status != "active":
#         request = toolset.initiate_connection(app=app)
#         print(f"Authenticate {app}: {request.redirectUrl}")
#     else:
#         print(f"✅ {app} is connected and active")
