from src.agents.github_analyzer import GitHubAnalyzer


def test_github_agent():
    try:
        print("🔍 Creating GitHub Analyzer Agent...")
        analyzer = GitHubAnalyzer()
        agent = analyzer.get_agent()

        print("✅ GitHub Agent created successfully!")
        print(f"   Role: {agent.role}")
        print(f"   Tools available: {len(agent.tools)}")
        print(f"   LLM: {agent.llm}")
        print(f"   Max retry limit: {agent.max_retry_limit}")

        return True
    except Exception as e:
        print(f"❌ Failed to create GitHub agent: {e}")
        return False


if __name__ == "__main__":
    test_github_agent()
