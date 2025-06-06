#!/usr/bin/env python3
"""
Test Composio Quickstart - GitHub Username Fetch
Based on official Composio documentation quickstart
"""

import os
from dotenv import load_dotenv
from composio_openai import ComposioToolSet, Action
from openai import OpenAI

load_dotenv()


def test_composio_quickstart():
    """Test the exact quickstart flow from Composio docs"""
    try:
        print("🚀 Testing Composio Quickstart...")

        # Initialize Composio ToolSet
        toolset = ComposioToolSet()
        print("✅ ComposioToolSet initialized")

        # Get tools for specific GitHub action
        tools = toolset.get_tools(actions=[Action.GITHUB_GET_THE_AUTHENTICATED_USER])
        print(f"✅ Tools retrieved: {len(tools)} tool(s)")

        # Initialize OpenAI client
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        print("✅ OpenAI client initialized")

        # Task for the LLM
        task = "Get my GitHub username."

        # Prepare messages
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that can use tools.",
            },
            {"role": "user", "content": task},
        ]

        print(f"📝 Task: {task}")
        print("🤖 Asking LLM to decide which tool to use...")

        # LLM reasoning - let it decide what tool to use
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # As per docs
            tools=tools,  # Available tools from Composio
            messages=messages,
        )

        print("✅ LLM response received")

        # Execute the tool call via Composio
        print("🔧 Executing tool call via Composio...")
        result = toolset.handle_tool_calls(response)

        print("✅ Tool execution completed!")
        print(f"📊 Result: {result}")

        return True

    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


def test_environment():
    """Verify environment setup"""
    print("🔍 Checking environment...")

    required_vars = ["COMPOSIO_API_KEY", "OPENAI_API_KEY"]

    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)

    if missing:
        print(f"❌ Missing environment variables: {missing}")
        return False

    print("✅ Environment variables set")
    return True


def debug_tools():
    """Debug what tools look like"""
    try:
        print("🔍 Debugging tool structure...")

        toolset = ComposioToolSet()
        tools = toolset.get_tools(actions=[Action.GITHUB_GET_THE_AUTHENTICATED_USER])

        print(f"Number of tools: {len(tools)}")

        if tools:
            tool = tools[0]
            print(f"Tool type: {type(tool)}")
            print(f"Tool attributes: {dir(tool)}")

            # Try to access common attributes
            for attr in ["name", "description", "function", "type"]:
                if hasattr(tool, attr):
                    print(f"Tool.{attr}: {getattr(tool, attr)}")

            # If it's a dict
            if isinstance(tool, dict):
                print(f"Tool dict keys: {tool.keys()}")
                print(f"Tool content: {tool}")

        return True

    except Exception as e:
        print(f"❌ Debug failed: {str(e)}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 COMPOSIO QUICKSTART TEST")
    print("=" * 60)

    # Step 1: Check environment
    if not test_environment():
        print("Fix environment variables and try again.")
        exit(1)

    # Step 2: Debug tools (to understand structure)
    print("\n" + "-" * 40)
    debug_tools()

    # Step 3: Run the quickstart test
    print("\n" + "-" * 40)
    success = test_composio_quickstart()

    print("\n" + "=" * 60)
    if success:
        print("🎉 COMPOSIO QUICKSTART TEST PASSED!")
        print("✅ Ready to integrate with CrewAI")
    else:
        print("❌ COMPOSIO QUICKSTART TEST FAILED!")
        print("🔧 Check your setup and try again")
    print("=" * 60)
