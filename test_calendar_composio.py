from composio_openai import ComposioToolSet, Action
from openai import OpenAI
import json
from datetime import datetime, timedelta

# Initialize
openai_client = OpenAI(api_key="")
composio_toolset = ComposioToolSet(entity_id="default")

print("🔍 Testing Google Calendar Event Creation...")
print("=" * 60)

# First, make sure Google Calendar is connected
print("📅 Step 1: Check Google Calendar Connection")
try:
    # You should have already connected: composio add googlecalendar
    print("✅ Make sure you've run: composio add googlecalendar")
except Exception as e:
    print(f"❌ Connection issue: {e}")

print("\n📅 Step 2: Create Test Calendar Event")
print("-" * 50)

try:
    # Get the calendar creation action
    tools_create_event = composio_toolset.get_tools(
        actions=[Action.GOOGLECALENDAR_CREATE_EVENT]
    )

    print(f"✅ Calendar tools retrieved: {len(tools_create_event)} tools")

    # Calculate start time (1 hour from now)
    start_time = datetime.now() + timedelta(hours=1)
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")

    # Create a test event simulating a bug meeting
    task_create_event = f"""
    Create a Google Calendar event with these details:
    - summary: "Bug Review: Chapter 15 Highlight Error (#1070)"
    - description: "Discuss bug found in vercel/next-learn repository. GitHub issue: https://github.com/vercel/next-learn/issues/1070"
    - start_datetime: "{start_time_str}"
    - event_duration_minutes: 30
    - attendees: ["abumahfuz21@gmail.com"]
    - location: "Virtual Meeting"
    
    Use the GOOGLECALENDAR_CREATE_EVENT action.
    """

    print(f"📝 Creating event starting at: {start_time_str}")

    response_create_event = openai_client.chat.completions.create(
        model="gpt-4o",
        tools=tools_create_event,
        messages=[
            {
                "role": "system",
                "content": "You create Google Calendar events using the provided tools. Always use the available calendar tools.",
            },
            {"role": "user", "content": task_create_event},
        ],
    )

    # Execute event creation
    result_create_event = composio_toolset.handle_tool_calls(response_create_event)

    print(f"📊 Event creation results: {len(result_create_event)} results")

    for item in result_create_event:
        if item.get("successful"):
            print("✅ Calendar Event Created Successfully!")
            print(f"Event Data: {json.dumps(item['data'], indent=2)}")

            # Extract event details
            event_data = item["data"]
            if "id" in event_data:
                print(f"\n🆔 Event ID: {event_data['id']}")
            if "htmlLink" in event_data:
                print(f"🔗 Event Link: {event_data['htmlLink']}")
            if "start" in event_data:
                print(f"⏰ Start Time: {event_data['start']}")

        else:
            print("❌ Event Creation Failed!")
            print(f"Error: {item.get('error', 'Unknown error')}")

except Exception as e:
    print(f"❌ Exception occurred: {e}")
    import traceback

    traceback.print_exc()

print("\n" + "=" * 60)
print("🎯 This calendar integration will be used for:")
print("- Creating bug review meetings automatically")
print("- Scheduling with GitHub issue/PR participants")
print("- Adding GitHub context to meeting descriptions")

print("\n📋 Prerequisites:")
print("1. Run: composio add googlecalendar")
print("2. Authenticate with your Google account")
print("3. Grant calendar write permissions")
