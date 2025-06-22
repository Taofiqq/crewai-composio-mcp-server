from composio_openai import ComposioToolSet, Action
from openai import OpenAI
import json
import os

# Initialize
openai_client = OpenAI()
composio_toolset = ComposioToolSet(entity_id="default")

# ========> Get PAGES LIST <==========

# print("🔍 STEP 1: Finding Notion Pages/Workspaces...")
# print("=" * 60)

# try:
#     # First, let's try to search for existing pages
#     tools_search = composio_toolset.get_tools(
#         actions=[Action.NOTION_SEARCH_NOTION_PAGE]
#     )

#     print(f"✅ Search tools retrieved: {len(tools_search)} tools")

#     task_search = "Search for pages in my Notion workspace to find a parent page where I can create a database"

#     response_search = openai_client.chat.completions.create(
#         model="gpt-4o",
#         tools=tools_search,
#         messages=[
#             {
#                 "role": "system",
#                 "content": "You help users find pages in their Notion workspace.",
#             },
#             {"role": "user", "content": task_search},
#         ],
#     )

#     result_search = composio_toolset.handle_tool_calls(response_search)

#     print(f"📊 Search results: {len(result_search)} results")

#     if len(result_search) > 0:
#         print("📋 Found pages:")
#         for i, item in enumerate(result_search):
#             if item.get("successful"):
#                 print(f"✅ Page {i+1}:")
#                 print(json.dumps(item["data"], indent=2))
#             else:
#                 print(f"❌ Search failed: {item.get('error')}")
#     else:
#         print("⚠️ No pages found or search didn't execute")

# except Exception as e:
#     print(f"❌ Search error: {e}")

# print("\n" + "=" * 60)

# # Alternative: Try direct action execution to see required parameters
# print("🔧 STEP 2: Testing Direct Database Creation...")
# print("-" * 50)

# try:
#     # Let's see what parameters are actually required
#     result_direct = composio_toolset.execute_action(
#         action=Action.NOTION_CREATE_DATABASE,
#         params={
#             "title": "GitHub Issues Test Direct"
#             # Intentionally leaving out parent_id to see the error
#         },
#         entity_id="default",
#     )
#     print(f"✅ Direct creation success: {result_direct}")

# except Exception as e:
#     print(f"❌ Direct creation error (this will show us required params): {e}")

# print("\n" + "=" * 60)
# print("🎯 Next Steps:")
# print("1. We need to find your Notion workspace/page ID")
# print("2. Or create a parent page first")
# print("3. Then create the database inside that page")
# ========> END OF PAGES LIST <==========


# ========> DB PAGE CREATION <========
# Use the "Publishing your React Native to Google Playstore" page as parent
# parent_page_id = "15f5b3db-a1d5-80bb-b591-d250d21e8200"

# print("🔍 Creating Database with Corrected Properties Format...")
# print("=" * 70)

# try:
#     # Fixed: Properties as a LIST, not dictionary
#     result_direct = composio_toolset.execute_action(
#         action=Action.NOTION_CREATE_DATABASE,
#         params={
#             "title": "GitHub Issues & PRs",
#             "parent_id": parent_page_id,
#             "properties": [  # ✅ Changed to LIST
#                 {"name": "Title", "type": "title"},
#                 {"name": "Number", "type": "number"},
#                 {
#                     "name": "Type",
#                     "type": "select",
#                     "select": {
#                         "options": [
#                             {"name": "Issue", "color": "red"},
#                             {"name": "PR", "color": "blue"},
#                         ]
#                     },
#                 },
#                 {"name": "Labels", "type": "multi_select"},
#                 {"name": "Assignees", "type": "multi_select"},
#                 {
#                     "name": "State",
#                     "type": "select",
#                     "select": {
#                         "options": [
#                             {"name": "open", "color": "green"},
#                             {"name": "closed", "color": "gray"},
#                         ]
#                     },
#                 },
#                 {"name": "Repository", "type": "rich_text"},
#                 {"name": "Created Date", "type": "date"},
#             ],
#         },
#         entity_id="default",
#     )

#     print("📊 Creation Result:")
#     print(json.dumps(result_direct, indent=2))

#     if result_direct.get("successful"):
#         print("\n✅ Database Created Successfully!")
#         database_id = result_direct["data"].get("id")
#         print(f"🆔 Database ID: {database_id}")
#         if database_id:
#             print(f"🎯 Database URL: https://notion.so/{database_id.replace('-', '')}")

#     else:
#         print("\n❌ Database Creation Failed!")
#         print(f"Error: {result_direct.get('error', 'Unknown error')}")

# except Exception as e:
#     print(f"❌ Exception occurred: {e}")
#     import traceback

#     traceback.print_exc()

# print("\n" + "=" * 70)
# print("🎯 Fixed: Properties now formatted as a list instead of dictionary!")
# ========> END OF DATABASE CREATION <==========


print("🔍 Step 1: Finding Our Database ID...")
print("=" * 60)

try:
    # Search for our database
    tools_search = composio_toolset.get_tools(
        actions=[Action.NOTION_SEARCH_NOTION_PAGE]
    )

    task_search = "Search for the 'GitHub Issues & PRs' database in my Notion workspace"

    response_search = openai_client.chat.completions.create(
        model="gpt-4o",
        tools=tools_search,
        messages=[
            {
                "role": "system",
                "content": "You search for databases and pages in Notion workspaces.",
            },
            {"role": "user", "content": task_search},
        ],
    )

    result_search = composio_toolset.handle_tool_calls(response_search)

    database_id = None

    for item in result_search:
        if item.get("successful"):
            results = item["data"]["response_data"]["results"]

            for result in results:
                if result.get("object") == "database":
                    # Check if this is our GitHub database
                    title_data = result.get("title", [])
                    if title_data and len(title_data) > 0:
                        title = title_data[0].get("plain_text", "")
                        if "GitHub Issues" in title:
                            database_id = result["id"]
                            print(f"✅ Found Database: {title}")
                            print(f"🆔 Database ID: {database_id}")
                            break

    if not database_id:
        print("❌ Database not found. Let's look at all results:")
        print(json.dumps(result_search, indent=2))

except Exception as e:
    print(f"❌ Search error: {e}")

# Step 2: Insert data using the actual database ID
if database_id:
    print(f"\n🔍 Step 2: Inserting Data into Database {database_id}")
    print("-" * 50)

    try:
        # ✅ FIXED: Direct insertion with properties as LIST
        result_insert = composio_toolset.execute_action(
            action=Action.NOTION_INSERT_ROW_DATABASE,
            params={
                "database_id": database_id,
                "properties": [
                    {
                        "name": "Title",
                        "type": "title",
                        "value": "Chapter 15: Highlight error",  # ✅ String
                    },
                    {
                        "name": "Number",
                        "type": "number",
                        "value": "1070",  # ✅ String (not integer)
                    },
                    {
                        "name": "Type",
                        "type": "select",
                        "value": "Issue",  # ✅ String (not object)
                    },
                    {
                        "name": "Labels",
                        "type": "multi_select",
                        "value": "bug,frontend",  # ✅ Comma-separated string
                    },
                    {"name": "State", "type": "select", "value": "open"},  # ✅ String
                    {
                        "name": "Repository",
                        "type": "rich_text",
                        "value": "vercel/next-learn",  # ✅ String
                    },
                    {
                        "name": "Created Date",
                        "type": "date",
                        "value": "2025-06-16",  # ✅ String date format
                    },
                ],
            },
            entity_id="default",
        )

        print("📊 Insert Result:")
        print(json.dumps(result_insert, indent=2))

        if result_insert.get("successful"):
            print("\n✅ GitHub Issue Data Inserted Successfully!")
        else:
            print(f"\n❌ Insert Failed: {result_insert.get('error')}")

    except Exception as e:
        print(f"❌ Insert error: {e}")

else:
    print("\n⚠️ Cannot insert - database ID not found")

print("\n🎯 Check your Notion database for the new row!")
