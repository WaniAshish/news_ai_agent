# import re
# import streamlit as st
# from dotenv import load_dotenv
# from agno.agent import Agent, RunResponse
# from agno.tools.googlesearch import GoogleSearchTools

# # Load environment variables (e.g., API keys)
# load_dotenv()

# # Initialize the agent
# title = "🗞️ Humanoid Robot News Agent"
# ag_description = "You are a news agent that helps users find the latest news."
# ag_instructions = [
#     "Given a topic by the user, respond with 10 latest news items about that topic.",
#     "Return them as plain markdown with section headers for English and German.",
# ]
# agent = Agent(
#     tools=[GoogleSearchTools()],
#     description=ag_description,
#     instructions=ag_instructions,
#     show_tool_calls=False,
#     debug_mode=False,
# )

# # Page title and user input
# st.title(title)
# topic = st.text_input("Enter a topic:", "Humanoid Robot")

# # Helper: render a table of items
# def render_table(items, header):
#     if items:
#         st.subheader(header)
#         st.table(items)
#     else:
#         st.warning(f"No items found for {header}.")

# # Fetch and display on button click
# if st.button("Fetch News"):
#     with st.spinner("Retrieving news…"):
#         raw = agent.run(topic)
#         md = raw.content if isinstance(raw, RunResponse) else str(raw)

#         # Split English/German blocks
#         eng_block, ger_block = md, ""
#         parts = re.split(r"## English", md, maxsplit=1)
#         if len(parts) > 1:
#             rest = parts[1]
#             sub = re.split(r"## German", rest, maxsplit=1)
#             eng_block = sub[0]
#             ger_block = sub[1] if len(sub) > 1 else ""

#         # Regex matching both **Title** and [Title] patterns
#         ITEM_RE = re.compile(
#             r"""
#             ^\d+\.\s*                              # list number
#             (?:                                       
#               \*\*(?P<title_bold>.+?)\*\*         # bold title
#               |                                        # or
#               \[(?P<title_link>.+?)\]               # [Title]
#             )                                         
#             [\s\S]*?                                # skip until link
#             \[.*?\]\(                              # match link text brackets
#             (?P<url>https?://[^\)]+)\)              # capture URL
#             """,
#             re.MULTILINE | re.VERBOSE,
#         )

#         # Parse each section
#         def parse_section(block: str):
#             return [
#                 {"Title": (m.group("title_bold") or m.group("title_link") or "").strip(),
#                  "URL": m.group("url")}  
#                 for m in ITEM_RE.finditer(block)
#             ]

#         eng_items = parse_section(eng_block)
#         ger_items = parse_section(ger_block)

#         # Render results
#         render_table(eng_items, "📢 News in English")
#         render_table(ger_items, "📢 Nachrichten auf Deutsch")

import re
import streamlit as st
from dotenv import load_dotenv
from agno.agent import Agent, RunResponse
from agno.tools.googlesearch import GoogleSearchTools

# Load environment variables (e.g., API keys)
load_dotenv()

# Initialize the agent
title = "🗞️ Humanoid Robot News Agent"
ag_description = "You are a news agent that helps users find the latest news."
ag_instructions = [
    "Given a topic by the user, respond with N latest news items about that topic.",
    "Return them as plain markdown with section headers for English and German.",
]
agent = Agent(
    tools=[GoogleSearchTools()],
    description=ag_description,
    instructions=ag_instructions,
    show_tool_calls=False,
    debug_mode=False,
)

# Page title and user input
st.title(title)
topic = st.text_input("Enter a topic:", "Humanoid Robot")

# Helper: render a table of items
def render_table(items, header):
    if items:
        st.subheader(header)
        st.table(items)
    else:
        st.warning(f"No items found for {header}.")

# Fetch and display on button click
if st.button("Fetch News"):
    with st.spinner("Retrieving news…"):
        # Run the agent and get markdown content
        raw = agent.run(topic)
        md = raw.content if isinstance(raw, RunResponse) else str(raw)

        # Split into English / German sections
        eng_block, ger_block = md, ""
        parts = re.split(r"## English", md, maxsplit=1)
        if len(parts) > 1:
            rest = parts[1]
            sub = re.split(r"## German", rest, maxsplit=1)
            eng_block = sub[0]
            ger_block = sub[1] if len(sub) > 1 else ""

        # Simplified regex: match numbered markdown links
        ITEM_RE = re.compile(
            r"^(?P<num>\d+)\.\s*\[(?P<title>.+?)\]\((?P<url>https?://[^\)]+)\)",
            re.MULTILINE,
        )

        def parse_section(block: str):
            return [
                {"Title": m.group("title").strip(), "URL": m.group("url")}
                for m in ITEM_RE.finditer(block)
            ]

        # Parse items
        eng_items = parse_section(eng_block)
        ger_items = parse_section(ger_block)

        # Render results
        render_table(eng_items, "📢 News in English")
        render_table(ger_items, "📢 Nachrichten auf Deutsch")
