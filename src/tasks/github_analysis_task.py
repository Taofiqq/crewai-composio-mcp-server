from crewai import Task


def create_github_analysis_task(github_agent):
    """Create task for analyzing GitHub issues and PRs"""
    return Task(
        description="""
        Analyze the provided GitHub repository issue or PR for:
        1. Bug severity classification (critical, high, medium, low)
        2. Extract maintainer and contributor information
        3. Identify technical components affected
        4. Analyze labels and content for priority indicators
        5. Determine if this requires team discussion or documentation
        
        Repository URL: {repo_url}
        Issue/PR Number: {issue_number}
        
        Focus on identifying:
        - Whether this is actually a bug or feature request
        - Severity level based on impact and urgency
        - Key stakeholders who should be involved
        - Technical complexity and review requirements
        """,
        agent=github_agent,
        expected_output="""
        A structured analysis report containing:
        - Issue/PR classification (bug/feature/other)
        - Severity level (critical/high/medium/low)
        - Affected components and systems
        - Key stakeholders and maintainers
        - Recommended next actions
        - Priority score (1-10)
        """,
        # output_json=True,
    )
