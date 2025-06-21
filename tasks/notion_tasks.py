# tasks/notion_tasks.py
"""
Notion-specific tasks for CrewAI workflow
Defines tasks for creating databases and inserting GitHub data
"""

from crewai import Task
from agents.notion_agent import notion_agent
from config.settings import settings
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NotionTasks:
    """Container class for Notion-related tasks"""

    @staticmethod
    def search_parent_pages_task() -> Task:
        """Task to search for available parent pages in Notion workspace"""

        task = Task(
            description=f"""
            Search for available pages in the Notion workspace to find a parent page for database creation.
            
            Requirements:
            1. Use NOTION_SEARCH_NOTION_PAGE to search for pages in the workspace
            2. Find any available page that can serve as a parent for database creation
            3. Extract the page ID from the search results
            4. Choose the first available page from the results
            
            IMPORTANT: Use the exact action name NOTION_SEARCH_NOTION_PAGE
            
            Focus on finding any page that can be used as a parent for the GitHub database.
            """,
            expected_output="""
            A report containing:
            - List of available pages found in the workspace
            - Selected parent page ID for database creation
            - Page title and details of the chosen parent page
            - Confirmation that a suitable parent page was found
            
            Format the parent page ID clearly for use in database creation.
            """,
            agent=notion_agent,
            tools=notion_agent.tools,
        )

        logger.info("✅ Notion search parent pages task created")
        return task

    @staticmethod
    def create_github_database_task() -> Task:
        """Task to create the GitHub Issues & PRs database"""

        task = Task(
            description=f"""
            Create a 'GitHub Issues & PRs' database in Notion using the parent page found in the previous task.
            
            Requirements:
            1. Use NOTION_CREATE_DATABASE to create the database
            2. Set title as "GitHub Issues & PRs"
            3. Use the parent page ID from the previous task
            4. Create the database with these properties (as a LIST):
               - Title (type: title)
               - Number (type: number)
               - Type (type: select with options: Issue/red, PR/blue)
               - Labels (type: multi_select)
               - Assignees (type: multi_select)
               - State (type: select with options: open/green, closed/gray)
               - Repository (type: rich_text)
               - Created Date (type: date)
            
            IMPORTANT: 
            - Use exact action name NOTION_CREATE_DATABASE
            - Format properties as a LIST, not dictionary
            - Include select options with colors as shown in the example
            """,
            expected_output="""
            A report containing:
            - Confirmation of database creation success
            - Database ID for future data insertion
            - Database title and parent page information
            - Database schema with all configured properties
            - Direct link to the created Notion database
            
            Include the database ID prominently for use in data insertion.
            """,
            agent=notion_agent,
            tools=notion_agent.tools,
            context=[],  # Will be populated with parent page results
        )

        logger.info("✅ Notion create database task created")
        return task

    @staticmethod
    def insert_github_data_task() -> Task:
        """Task to insert GitHub data into the created database"""

        task = Task(
            description=f"""
            Insert GitHub issues and pull requests data into the Notion database created in the previous task.
            
            Requirements:
            1. Use NOTION_INSERT_ROW_DATABASE to insert data
            2. Use the database ID from the previous task
            3. For each GitHub issue/PR from the context, create a row with properties:
               - Title: Issue/PR title (type: title, value: string)
               - Number: Issue/PR number (type: number, value: string - NOT integer)
               - Type: "Issue" or "PR" (type: select, value: string)
               - Labels: Comma-separated labels (type: multi_select, value: "bug,frontend")
               - Assignees: Comma-separated assignees (type: multi_select, value: "user1,user2")
               - State: "open" or "closed" (type: select, value: string)
               - Repository: Repository name (type: rich_text, value: string)
               - Created Date: Date in YYYY-MM-DD format (type: date, value: string)
            
            IMPORTANT:
            - Use exact action name NOTION_INSERT_ROW_DATABASE
            - Format properties as a LIST
            - Convert number to string, not integer
            - Convert arrays to comma-separated strings
            - Use proper date format YYYY-MM-DD
            
            Process all GitHub issues and PRs from the GitHub analysis context.
            """,
            expected_output="""
            A summary report containing:
            - Number of GitHub items processed (issues and PRs)
            - Details of each inserted row with confirmation
            - Any insertion errors or issues encountered
            - Final confirmation of data insertion success
            - Links to the populated Notion database
            
            Include verification that all GitHub data has been properly formatted and inserted.
            """,
            agent=notion_agent,
            tools=notion_agent.tools,
            context=[],  # Will be populated with database ID and GitHub data
        )

        logger.info("✅ Notion insert data task created")
        return task


# Create task instances for easy import
notion_tasks = NotionTasks()

# Individual task instances
search_parent_pages_task = notion_tasks.search_parent_pages_task()
create_github_database_task = notion_tasks.create_github_database_task()
insert_github_data_task = notion_tasks.insert_github_data_task()
