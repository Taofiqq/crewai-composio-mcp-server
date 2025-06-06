import sys

sys.path.append(".")
from src.agents.notion_writer import NotionWriter


def test_notion_agent():
    try:
        print("📝 Creating Notion Writer Agent...")
        writer = NotionWriter()
        agent = writer.get_agent()

        print("✅ Notion Agent created successfully!")
        print(f"   Role: {agent.role}")
        print(f"   Tools available: {len(agent.tools)}")
        print(f"   LLM: {agent.llm}")
        print(f"   Temperature: {agent.llm.temperature}")

        return True
    except Exception as e:
        print(f"❌ Failed to create Notion agent: {e}")
        return False


if __name__ == "__main__":
    test_notion_agent()
