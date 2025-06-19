import os
os.environ["AUTOGEN_USE_DOCKER"] = "False"

import autogen
from autogen import UserProxyAgent, AssistantAgent, GroupChat, GroupChatManager

# Mock LLM config (no real API call)
llm_config = {
    "config_list": [
        {
            "model": "gpt-3.5-turbo",
            "api_key": "sk-fake"
        }
    ],
    "temperature": 0
}


# Define mock reply logic
mock_prs = [
    {"id": 1, "category": "Football"},
    {"id": 2, "category": "Cricket"}
]

def mock_reply(agent, messages, sender, config):
    last_msg = messages[-1]["content"].lower()
    if "fetch prs" in last_msg:
        return True, f"Fetched PRs: {mock_prs}"
    elif "recommend supplier" in last_msg:
        for pr in mock_prs:
            category = pr["category"]
            supplier = "Premier League" if category == "Football" else "ICC"
            return True, f"Recommended supplier for {category}: {supplier}"
    elif "create rfq" in last_msg:
        rfqs = []
        for pr in mock_prs:
            supplier = "Premier League" if pr["category"] == "Football" else "ICC"
            rfq = {
                "rfq_id": f"rfq-{pr['id']}",
                "category": pr["category"],
                "supplier": supplier
            }
            rfqs.append(rfq)
        return True, f"Created RFQs: {rfqs}"
    else:
        return True, "Task completed."

# Create agents
user = UserProxyAgent(name="User", human_input_mode="NEVER", max_consecutive_auto_reply=3)
pr_fetcher = AssistantAgent(name="PRFetcher", llm_config=llm_config)
supplier_recommender = AssistantAgent(name="SupplierRecommender", llm_config=llm_config)
rfq_creator = AssistantAgent(name="RFQCreator", llm_config=llm_config)

# Register mocked reply logic to all agents
pr_fetcher.register_reply(trigger=lambda *args, **kwargs: True, reply_func=mock_reply)
supplier_recommender.register_reply(trigger=lambda *args, **kwargs: True, reply_func=mock_reply)
rfq_creator.register_reply(trigger=lambda *args, **kwargs: True, reply_func=mock_reply)

# Group chat setup
group_chat = GroupChat(
    agents=[user, pr_fetcher, supplier_recommender, rfq_creator],
    messages=[],
    max_round=6
)
manager = GroupChatManager(groupchat=group_chat, llm_config=llm_config)

# Start the conversation
task_prompt = """
Simulate a 3-agent orchestration:

1. PRFetcher fetches PRs like [{'id': 1, 'category': 'Football'}, {'id': 2, 'category': 'Cricket'}]
2. SupplierRecommender picks supplier based on category.
3. RFQCreator creates an RFQ using PR and Supplier.
"""

user.initiate_chat(manager=manager, recipient=manager, message=task_prompt)