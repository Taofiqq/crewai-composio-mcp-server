from crewai import Task


def create_notion_documentation_task(notion_agent):
    """Create task for generating Notion documentation"""
    return Task(
        description="""
        Create comprehensive Notion documentation based on the GitHub analysis:
        1. Generate a well-structured page with clear sections
        2. Include executive summary for stakeholders
        3. Add technical details for developers
        4. Create actionable next steps and recommendations
        5. Format content with proper headings, callouts, and tables
        6. Link to the original GitHub issue/PR
        
        Use the analysis data to create professional documentation that both
        technical and non-technical team members can understand and act upon.
        """,
        agent=notion_agent,
        expected_output="""
        A complete Notion page with:
        - Executive summary callout
        - Technical analysis details
        - Stakeholder information
        - Recommended actions table
        - Links to GitHub and related resources
        - Page ID and URL for reference
        """,
        # output_json=True,
    )
