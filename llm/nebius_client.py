# llm/nebius_client.py
"""
Nebius LLM Client for CrewAI integration
Handles LLM initialization and configuration for all agents
"""

import openai
from typing import Optional, Dict, Any
import logging
from config.settings import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NebiusClient:
    """
    Wrapper class for Nebius LLM integration with CrewAI
    """

    def __init__(self):
        """Initialize Nebius client with configuration from settings"""
        self.client = None
        self.model = settings.NEBIUS_MODEL
        self.base_url = settings.NEBIUS_BASE_URL
        self.api_key = settings.NEBIUS_API_KEY

        self._initialize_client()

    def _initialize_client(self) -> None:
        """Initialize the OpenAI-compatible client for Nebius"""
        try:
            self.client = openai.OpenAI(api_key=self.api_key, base_url=self.base_url)
            logger.info(f"✅ Nebius client initialized with model: {self.model}")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Nebius client: {e}")
            raise

    def get_crewai_llm(self) -> openai.OpenAI:
        """
        Get the LLM client configured for CrewAI agents

        Returns:
            openai.OpenAI: Configured client for CrewAI
        """
        if not self.client:
            raise ValueError("Nebius client not initialized")

        return self.client

    def test_connection(self) -> bool:
        """
        Test the connection to Nebius API

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Simple test chat completion
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello, are you working?"}],
                max_tokens=10,
            )

            logger.info("✅ Nebius API connection test successful")
            return True

        except Exception as e:
            logger.error(f"❌ Nebius API connection test failed: {e}")
            return False

    def analyze_labels(self, labels: list) -> Dict[str, Any]:
        """
        Analyze GitHub issue/PR labels to determine if action is needed

        Args:
            labels (list): List of label names from GitHub

        Returns:
            Dict[str, Any]: Analysis results including bug detection and priority
        """
        try:
            labels_str = ", ".join(labels) if labels else "no labels"

            prompt = f"""
            Analyze these GitHub issue/PR labels: {labels_str}
            
            Determine:
            1. Is this a bug? (yes/no)
            2. Priority level (low/medium/high/critical)
            3. Should we schedule a meeting? (yes/no)
            4. Meeting urgency (within 24h/within week/no urgency)
            
            Respond with ONLY a JSON object like this:
            {{
                "is_bug": true/false,
                "priority": "low/medium/high/critical",
                "schedule_meeting": true/false,
                "meeting_urgency": "within 24h/within week/no urgency",
                "reasoning": "brief explanation"
            }}
            """

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a GitHub issue analyzer. Respond only with valid JSON.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=200,
                temperature=0.1,  # Low temperature for consistent analysis
            )

            # Parse the JSON response
            import json

            analysis = json.loads(response.choices[0].message.content.strip())

            logger.info(f"✅ Label analysis completed for: {labels_str}")
            return analysis

        except Exception as e:
            logger.error(f"❌ Label analysis failed: {e}")
            # Return safe defaults
            return {
                "is_bug": settings.BUG_LABEL in labels,
                "priority": "medium",
                "schedule_meeting": settings.BUG_LABEL in labels,
                "meeting_urgency": "within week",
                "reasoning": "Fallback analysis due to API error",
            }

    def generate_meeting_summary(self, issue_data: Dict[str, Any]) -> str:
        """
        Generate a meeting summary for calendar events

        Args:
            issue_data (Dict[str, Any]): GitHub issue/PR data

        Returns:
            str: Generated meeting summary
        """
        try:
            title = issue_data.get("title", "Unknown Issue")
            number = issue_data.get("number", "N/A")
            labels = issue_data.get("labels", [])
            repository = issue_data.get("repository", settings.TARGET_REPOSITORY)

            labels_str = ", ".join([label.get("name", "") for label in labels])

            prompt = f"""
            Create a concise meeting summary for this GitHub issue:
            
            Title: {title}
            Number: #{number}
            Repository: {repository}
            Labels: {labels_str}
            
            Generate a professional meeting summary that includes:
            - Brief description of the issue
            - Why this meeting is needed
            - Expected outcome
            
            Keep it under 100 words and professional.
            """

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You create professional meeting summaries for development teams.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=150,
                temperature=0.3,
            )

            summary = response.choices[0].message.content.strip()
            logger.info(f"✅ Meeting summary generated for issue #{number}")
            return summary

        except Exception as e:
            logger.error(f"❌ Meeting summary generation failed: {e}")
            # Return fallback summary
            return f"Discussion needed for GitHub issue #{issue_data.get('number', 'N/A')}: {issue_data.get('title', 'Unknown Issue')}"


# Global instance for easy import
nebius_client = NebiusClient()
