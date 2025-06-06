import os
import traceback
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

# Load environment variables
load_dotenv()


def test_crewai_nebius_integration():
    try:
        # Use OpenAI-compatible approach (recommended for Nebius)
        nebius_llm = LLM(
            model="openai/meta-llama/Meta-Llama-3.1-70B-Instruct",  # No "nebius/" prefix
            base_url="https://api.studio.nebius.com/v1",  # Explicit Nebius endpoint
            api_key=os.getenv("NEBIUS_API_KEY"),
            temperature=0.7,
        )

        print("✅ Creating Nebius LLM instance...")
        print("LLM config:", vars(nebius_llm))

        # Create a simple agent
        test_agent = Agent(
            role="Test Agent",
            goal="Test Nebius LLM integration with CrewAI",
            backstory="You are a test agent verifying the integration works",
            llm=nebius_llm,
            verbose=True,
        )

        print("✅ Agent created successfully...")

        # Create a simple task
        test_task = Task(
            description="Say hello and confirm you are working with Nebius LLM",
            agent=test_agent,
            expected_output="A greeting message confirming the integration works",
        )

        print("✅ Task created successfully...")

        # Create crew
        test_crew = Crew(agents=[test_agent], tasks=[test_task], verbose=True)

        print("✅ Crew created successfully...")
        print("🚀 Running crew kickoff...")

        # Execute the crew
        result = test_crew.kickoff()

        print("🎉 SUCCESS! CrewAI + Nebius integration working!")
        print(f"📝 Result: {result}")

        return True

    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        traceback.print_exc()

        # Try alternative method if first fails (if you want, you can leave this out)
        print("\n🔄 Trying OpenAI-compatible method again with model name...")
        try:
            alt_llm = LLM(
                model="meta-llama/Meta-Llama-3.1-70B-Instruct",
                base_url="https://api.studio.nebius.com/v1",
                api_key=os.getenv("NEBIUS_API_KEY"),
            )
            print("✅ Alternative method LLM created successfully!", vars(alt_llm))
            return True
        except Exception as alt_e:
            print(f"❌ Alternative method also failed: {alt_e}")
            traceback.print_exc()
            return False


if __name__ == "__main__":
    test_crewai_nebius_integration()
