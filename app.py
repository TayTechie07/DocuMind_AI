import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from src.document_processor import process_documents
from src.vector_store import (
    create_vector_store,
    create_retriever
)
from src.agent import create_documind_agent


# =========================================================
# CONFIGURATION
# =========================================================

load_dotenv()

st.set_page_config(
    page_title="DocuMind AI",
    page_icon="🧠",
    layout="wide"
)


# =========================================================
# SESSION STATE
# =========================================================

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "agent" not in st.session_state:
    st.session_state.agent = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "documents_loaded" not in st.session_state:
    st.session_state.documents_loaded = False


# =========================================================
# LOAD LLM
# =========================================================

@st.cache_resource
def load_llm():

    return ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0
    )


llm = load_llm()


# =========================================================
# HEADER
# =========================================================

st.title("🧠 DocuMind AI")

st.markdown(
    """
    ### Intelligent Document & Workflow Agent

    **Upload. Understand. Ask. Automate.**
    """
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("📚 Knowledge Base")

    uploaded_files = st.file_uploader(
        "Upload PDF documents",
        type=["pdf"],
        accept_multiple_files=True
    )

    process_button = st.button(
        "🚀 Process Documents",
        use_container_width=True
    )


# =========================================================
# PROCESS DOCUMENTS
# =========================================================

if process_button:

    if not uploaded_files:

        st.warning(
            "Please upload at least one PDF."
        )

    else:

        with st.spinner(
            "📚 Processing your documents..."
        ):

            # Load and split documents
            chunks = process_documents(
                uploaded_files
            )

            # Create vector store
            vectorstore = create_vector_store(
                chunks
            )

            # Create retriever
            retriever = create_retriever(
                vectorstore
            )

            # Save retriever
            st.session_state.retriever = retriever

            # Create AI agent
            st.session_state.agent = create_documind_agent(
                retriever,
                chunks
            )

            # Update status
            st.session_state.documents_loaded = True

            # Clear previous chat
            st.session_state.messages = []

        st.success(
            f"✅ {len(uploaded_files)} "
            "document(s) processed successfully!"
        )


# =========================================================
# STATUS
# =========================================================

if st.session_state.documents_loaded:

    st.sidebar.success(
        "🟢 Knowledge base ready"
    )

else:

    st.info(
        "👈 Upload your PDF documents "
        "from the sidebar to get started."
    )


# =========================================================
# CHAT
# =========================================================

if (
    st.session_state.documents_loaded
    and st.session_state.agent is not None
):

    # -----------------------------------------------------
    # Display previous messages
    # -----------------------------------------------------

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


    # -----------------------------------------------------
    # Chat input
    # -----------------------------------------------------

    question = st.chat_input(
        "Ask something about your documents..."
    )


    if question:

        # -------------------------------------------------
        # User message
        # -------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):

            st.markdown(question)


        # -------------------------------------------------
        # AI Agent response
        # -------------------------------------------------

        with st.chat_message("assistant"):

            with st.spinner(
                "🤖 DocuMind is thinking..."
            ):

                result = st.session_state.agent.invoke(
                    {
                        "messages": [
                            {
                                "role": "user",
                                "content": question
                            }
                        ]
                    }
                )


            # ---------------------------------------------
            # Final answer
            # ---------------------------------------------

            answer = result["messages"][-1].content

            st.markdown(answer)


            # ---------------------------------------------
            # Agent activity
            # ---------------------------------------------

            tool_messages = []

            for message in result["messages"]:

                if getattr(
                    message,
                    "type",
                    None
                ) == "tool":

                    tool_messages.append(
                        message
                    )


            if tool_messages:

                with st.expander(
                    "🛠️ Agent activity"
                ):

                    for message in tool_messages:

                        st.write(
                            f"Tool used: "
                            f"{message.name}"
                        )


        # -------------------------------------------------
        # Save assistant response
        # -------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )