from langchain_groq import ChatGroq
from langchain.agents import create_agent

from src.tools import create_tools


def create_documind_agent(retriever, documents):
    """
    Create the DocuMind AI agent with access
    to the document tools.
    """

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0
    )

    tools = create_tools(
        retriever,
        documents
    )

    system_prompt = """
You are DocuMind AI, an intelligent document
and workflow assistant.

Your job is to help users understand and work
with their uploaded documents.

You have access to these tools:

1. search_documents
   Use this when the user asks a question that
   requires information from the uploaded documents.

2. summarize_document
   Use this when the user wants document content
   summarized.

3. extract_information
   Use this when the user asks for specific
   information or fields to be extracted.

4. document_statistics
   Use this when the user asks about the number
   of documents, pages, or chunks.

Important rules:

- Use the tools when document information is required.
- Do not invent information.
- Do not use outside knowledge for document questions.
- If the requested information cannot be found,
  clearly say that it is not available in the
  uploaded documents.
- Give concise and useful answers.
"""

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt
    )

    return agent