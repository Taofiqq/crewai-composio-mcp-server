from composio_openai import ComposioToolSet, Action
from openai import OpenAI
import json
import os

# Initialize
openai_client = OpenAI(api_key="sk-proj-pLasvgbTY0bgpQEms5Cy6uUQQ_Pd")
composio_toolset = ComposioToolSet(entity_id="default")

# ======== ISSUES LIST TEST ========>
# Get the specific action we want to test
# tools = composio_toolset.get_tools(actions=[Action.GITHUB_ISSUES_LIST_FOR_REPO])

# task = "Fetch the first 3 open issues from vercel/next-learn repository on GitHub"

# print("🔍 Testing GITHUB_ISSUES_LIST_FOR_REPO...")
# print(f"Task: {task}")
# print("-" * 50)

# response = openai_client.chat.completions.create(
#     model="gpt-4o",
#     tools=tools,
#     messages=[
#         {
#             "role": "system",
#             "content": "You are a helpful assistant that can fetch GitHub issues.",
#         },
#         {"role": "user", "content": task},
#     ],
# )

# result = composio_toolset.handle_tool_calls(response)

# print("📋 Full Results (No Truncation):")
# print("-" * 50)

# for item in result:
#     if item.get("successful"):
#         print("✅ Success!")

#         # Print FULL raw data structure (no truncation)
#         print("\n🔧 Complete Raw Data Structure:")
#         print(json.dumps(item["data"], indent=2))

#         # Try to extract and display key information
#         try:
#             # Handle both possible data structures
#             if "details" in item["data"]:
#                 issues_data = item["data"]["details"]
#                 print(
#                     f"\n📊 Data structure: item['data']['details'] with {len(issues_data)} issues"
#                 )
#             else:
#                 issues_data = item["data"]
#                 print(
#                     f"\n📊 Data structure: item['data'] directly with {len(issues_data)} issues"
#                 )

#             if isinstance(issues_data, list):
#                 # Show ALL issues, not just first 3
#                 for i, issue in enumerate(issues_data):
#                     print(f"\n--- Issue {i+1} ---")
#                     print(f"Title: {issue.get('title', 'N/A')}")
#                     print(f"Number: #{issue.get('number', 'N/A')}")
#                     print(f"State: {issue.get('state', 'N/A')}")
#                     print(
#                         f"Labels: {[label.get('name') for label in issue.get('labels', [])]}"
#                     )
#                     print(
#                         f"Assignees: {[assignee.get('login') for assignee in issue.get('assignees', [])]}"
#                     )
#                     print(f"Created: {issue.get('created_at', 'N/A')}")
#             else:
#                 print(f"⚠️  Issues data is not a list, it's: {type(issues_data)}")
#                 print(f"Content: {issues_data}")

#         except Exception as e:
#             print(f"Error parsing issues: {e}")
#             print(f"Raw item data type: {type(item['data'])}")
#             print(f"Raw item data: {item['data']}")
#     else:
#         print("❌ Failed!")
#         print(f"Error: {item.get('error', 'Unknown error')}")

# <============ END OF ISSUES LIST TEST ========>

# ======== GET PRs ========>

# tools = composio_toolset.get_tools(actions=[Action.GITHUB_LIST_PULL_REQUESTS])

# # Test with explicit count to avoid per_page=1 default
# task = "Get the 2 newest open pull requests from vercel/next-learn repository, sorted by most recently created first"

# print("🔍 Testing GITHUB_LIST_PULL_REQUESTS...")
# print(f"Task: {task}")
# print("-" * 50)

# response = openai_client.chat.completions.create(
#     model="gpt-4o",
#     tools=tools,
#     messages=[
#         {
#             "role": "system",
#             "content": "You are a helpful assistant. When fetching GitHub pull requests, try to get multiple PRs, not just one.",
#         },
#         {"role": "user", "content": task},
#     ],
# )

# # Execute the action
# result = composio_toolset.handle_tool_calls(response)

# print("📋 Full Results (No Truncation):")
# print("-" * 50)

# for item in result:
#     if item.get("successful"):
#         print("✅ Success!")

#         # Print FULL raw data structure (no truncation)
#         print("\n🔧 Complete Raw Data Structure:")
#         print(json.dumps(item["data"], indent=2))

#         # Try to extract and display key information
#         try:
#             # Handle both possible data structures
#             if "details" in item["data"]:
#                 prs_data = item["data"]["details"]
#                 print(
#                     f"\n📊 Data structure: item['data']['details'] with {len(prs_data)} PRs"
#                 )
#             else:
#                 prs_data = item["data"]
#                 print(
#                     f"\n📊 Data structure: item['data'] directly with {len(prs_data)} PRs"
#                 )

#             if isinstance(prs_data, list):
#                 # Show ALL PRs
#                 for i, pr in enumerate(prs_data):
#                     print(f"\n--- PR {i+1} ---")
#                     print(f"Title: {pr.get('title', 'N/A')}")
#                     print(f"Number: #{pr.get('number', 'N/A')}")
#                     print(f"State: {pr.get('state', 'N/A')}")
#                     print(f"Author: {pr.get('user', {}).get('login', 'N/A')}")
#                     print(
#                         f"Labels: {[label.get('name') for label in pr.get('labels', [])]}"
#                     )

#                     # Check for assignees (key for your workflow)
#                     print(
#                         f"Assignees: {[assignee.get('login') for assignee in pr.get('assignees', [])]}"
#                     )

#                     # Check for reviewers (key for your workflow)
#                     requested_reviewers = pr.get("requested_reviewers", [])
#                     print(
#                         f"Requested Reviewers: {[reviewer.get('login') for reviewer in requested_reviewers]}"
#                     )

#                     print(f"Created: {pr.get('created_at', 'N/A')}")
#                     print(f"Draft: {pr.get('draft', 'N/A')}")

#             else:
#                 print(f"⚠️  PRs data is not a list, it's: {type(prs_data)}")
#                 print(f"Content: {prs_data}")

#         except Exception as e:
#             print(f"Error parsing PRs: {e}")
#             print(f"Raw item data type: {type(item['data'])}")
#             print(f"Raw item data: {item['data']}")
#     else:
#         print("❌ Failed!")
#         print(f"Error: {item.get('error', 'Unknown error')}")

# print("\n" + "=" * 50)
# print("🎯 This PR data will be used for:")
# print("- Creating Notion pages with PR info")
# print("- Detecting 'bug' labels on PRs")
# print("- Finding assignees + reviewers for meeting scheduling")
# ======== END OF GETTING PRs ========>

# ============> GETTING COLLABORATORS <===========

# Get the repository collaborators action
tools = composio_toolset.get_tools(
    actions=[Action.GITHUB_LIST_REPOSITORY_COLLABORATORS]
)

# Test with the same repo we've been using
task = "List all collaborators for the Taofiqq/crewai-composio-mcp-server repository"

print("🔍 Testing GITHUB_LIST_REPOSITORY_COLLABORATORS...")
print(f"Task: {task}")
print("-" * 50)

response = openai_client.chat.completions.create(
    model="gpt-4o",
    tools=tools,
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant that can fetch GitHub repository collaborators.",
        },
        {"role": "user", "content": task},
    ],
)

# Execute the action
result = composio_toolset.handle_tool_calls(response)

print("📋 Full Results (No Truncation):")
print("-" * 50)

for item in result:
    if item.get("successful"):
        print("✅ Success!")

        # Print FULL raw data structure (no truncation)
        print("\n🔧 Complete Raw Data Structure:")
        print(json.dumps(item["data"], indent=2))

        # Try to extract and display key information
        try:
            # Handle both possible data structures
            if "details" in item["data"]:
                collaborators_data = item["data"]["details"]
                print(
                    f"\n📊 Data structure: item['data']['details'] with {len(collaborators_data)} collaborators"
                )
            else:
                collaborators_data = item["data"]
                print(
                    f"\n📊 Data structure: item['data'] directly with {len(collaborators_data)} collaborators"
                )

            if isinstance(collaborators_data, list):
                # Show ALL collaborators
                for i, collaborator in enumerate(collaborators_data):
                    print(f"\n--- Collaborator {i+1} ---")
                    print(f"Username: {collaborator.get('login', 'N/A')}")
                    print(f"Name: {collaborator.get('name', 'N/A')}")
                    print(f"Email: {collaborator.get('email', 'N/A')}")
                    print(f"Role/Permissions: {collaborator.get('permissions', 'N/A')}")
                    print(f"Type: {collaborator.get('type', 'N/A')}")
                    print(f"Site Admin: {collaborator.get('site_admin', 'N/A')}")

            else:
                print(
                    f"⚠️  Collaborators data is not a list, it's: {type(collaborators_data)}"
                )
                print(f"Content: {collaborators_data}")

        except Exception as e:
            print(f"Error parsing collaborators: {e}")
            print(f"Raw item data type: {type(item['data'])}")
            print(f"Raw item data: {item['data']}")
    else:
        print("❌ Failed!")
        print(f"Error: {item.get('error', 'Unknown error')}")

print("\n" + "=" * 50)
print("🎯 This collaborator data will be used for:")
print("- Identifying repository maintainers")
print("- Adding maintainers to meeting invitations when bugs are found")
print("- Understanding who has write access to the repository")
