# 🧠 DocuMind AI

### Intelligent Document & Workflow Agent

**Upload. Understand. Ask. Automate.**

DocuMind AI is an **agentic RAG application** that transforms uploaded PDF documents into an interactive AI knowledge base.

Instead of relying on a simple "chat with PDF" workflow, DocuMind combines **semantic retrieval, vector search, MMR retrieval, LLM reasoning, and tool calling** to let an AI agent decide how to work with a user's documents.

The project was built with a focus on **modularity, grounded responses, source transparency, and practical AI engineering**.

---

## 🚀 What DocuMind AI Can Do

* 📄 Upload and process multiple PDF documents
* ✂️ Split documents into meaningful chunks
* 🧠 Generate semantic embeddings using Hugging Face
* 🗄️ Store document vectors using Chroma
* 🔎 Retrieve relevant information using MMR search
* 🤖 Use an AI agent for tool-based reasoning
* 📚 Answer questions using uploaded documents
* 📝 Generate document summaries
* 📋 Extract requested information
* 📊 Provide document statistics
* 🔗 Display document sources and page references
* 🛠️ Show which tool the agent used
* 💬 Maintain conversational chat history
* 🔐 Keep API credentials outside the repository using environment variables

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │    Streamlit UI     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  PDF Processing     │
                    │  & Chunking         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ HuggingFace         │
                    │ Embeddings          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Chroma         │
                    │   Vector Store      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   MMR Retriever     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    AI Agent        │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
      search_documents   summarize_document   extract_information
                               │
                               ▼
                    document_statistics
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Groq LLM          │
                    │ GPT-OSS-120B        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Answer + Sources    │
                    │ + Tool Activity     │
                    └─────────────────────┘
```

---

## 🧩 Agent Tools

DocuMind currently provides four tools to the AI agent:

### 🔎 `search_documents`

Searches the uploaded document knowledge base and returns relevant document content along with source and page information.

### 📝 `summarize_document`

Provides document content to the agent for summarization.

### 📋 `extract_information`

Allows the agent to extract specific information requested by the user from document content.

### 📊 `document_statistics`

Provides statistics about the processed document collection, including documents, pages, and chunks.

The agent can decide which tool is appropriate based on the user's request.

---

## 🛠️ Technology Stack

| Technology         | Purpose                     |
| ------------------ | --------------------------- |
| Python             | Core application            |
| Streamlit          | Web interface               |
| LangChain          | RAG and agent orchestration |
| LangChain Groq     | LLM integration             |
| Groq               | LLM inference               |
| GPT-OSS-120B       | Language model              |
| Hugging Face       | Text embeddings             |
| `all-MiniLM-L6-v2` | Embedding model             |
| Chroma             | Vector database             |
| PyPDF              | PDF document loading        |
| Pydantic           | Structured data validation  |
| NumPy              | Numerical operations        |
| python-dotenv      | Environment configuration   |

---

## 📁 Project Structure

```text
DocuMind-AI/
│
├── app.py
│
├── src/
│   ├── __init__.py
│   ├── document_processor.py
│   ├── vector_store.py
│   ├── rag.py
│   ├── tools.py
│   └── agent.py
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

### Module Responsibilities

**`app.py`**
Handles the Streamlit interface, document processing workflow, chat interaction, source display, and agent activity.

**`document_processor.py`**
Loads uploaded PDFs, preserves document metadata, and creates text chunks.

**`vector_store.py`**
Creates Hugging Face embeddings, stores vectors in Chroma, and configures MMR retrieval.

**`rag.py`**
Contains the original grounded RAG answer-generation pipeline and relevance handling.

**`tools.py`**
Defines the tools available to the AI agent.

**`agent.py`**
Creates the DocuMind agent and connects the LLM with the available tools.

---

## 🔄 How It Works

### 1. Upload

The user uploads one or multiple PDF documents.

### 2. Process

The PDFs are loaded and split into smaller chunks while preserving metadata such as the original filename and page number.

### 3. Embed

Each chunk is converted into a semantic vector using:

```text
sentence-transformers/all-MiniLM-L6-v2
```

### 4. Store

The embeddings are stored in Chroma for efficient semantic retrieval.

### 5. Retrieve

When the user asks a question, the system retrieves relevant document chunks using **Maximum Marginal Relevance (MMR)**.

MMR helps balance relevance and diversity instead of simply returning highly similar duplicate chunks.

### 6. Agent Reasoning

The AI agent determines which available tool is appropriate for the user's request.

For example:

```text
"What does the contract say about payment?"
                ↓
        search_documents
```

or:

```text
"How many pages are in my documents?"
                ↓
        document_statistics
```

### 7. Generate

The retrieved information is provided to the Groq-powered LLM, which generates the final response.

### 8. Explain

DocuMind displays relevant source information and the tools used during the agent's execution.

---

## 🎯 Design Goals

This project was built around a few important principles:

### Grounded Answers

The system is designed to answer document-related questions using the user's uploaded information rather than blindly generating unsupported answers.

### Modularity

Instead of placing the entire application inside one large file, document processing, vector storage, RAG, tools, and agent logic are separated into dedicated modules.

### Tool-Based AI

The project explores how LLMs can move beyond simple text generation and **use tools to perform useful actions**.

### Transparency

The application exposes source information and agent activity so users can better understand where an answer came from and which capability was used.

### Practical Engineering

The project focuses on building a complete working system rather than only experimenting with individual AI techniques.

---

## 🧠 What I Learned Building This

Building DocuMind AI helped me understand how the individual components of modern AI applications connect together in a real system.

Some of the key areas I worked with include:

* Retrieval-Augmented Generation
* Semantic search
* Vector databases
* Embeddings
* MMR retrieval
* Prompt design
* LLM integration
* LangChain agents
* Tool calling
* Document processing
* Metadata management
* Source attribution
* Streamlit application development
* Environment and API-key security
* Modular Python architecture
* Debugging AI pipelines

One of the most valuable parts of the project was learning that building an AI application is not simply about connecting an LLM to a prompt.

**Retrieval quality, tool design, data flow, validation, error handling, and system architecture all matter.**

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Never commit your actual `.env` file or API key to GitHub.

A `.env.example` file is included as a safe template.

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/DocuMind-AI.git
cd DocuMind-AI
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create your environment file:

```text
.env
```

Add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Run the application:

```bash
streamlit run app.py
```

---

## 🧪 Example Use Cases

DocuMind can be adapted for many document-heavy workflows, including:

* 📑 Business reports
* 📜 Contracts
* 🏢 Company policies
* 📚 Research papers
* 👥 HR documents
* 💰 Financial documents
* 📋 Internal knowledge bases
* 📖 Technical documentation

---

## 🚧 Future Improvements

The current version establishes the core agentic RAG architecture.

Possible future improvements include:

* Structured extraction with stronger schema validation
* Multi-document comparison
* Better retrieval evaluation
* RAG evaluation metrics
* Hybrid keyword + semantic retrieval
* Reranking
* More advanced agent workflows
* Persistent document collections
* Authentication
* Document management
* Production deployment
* Observability and monitoring

---

## 💡 Why I Built This

I built DocuMind AI as a practical project to deepen my understanding of **AI engineering, RAG systems, and agentic applications**.

Rather than stopping at individual tutorials or isolated models, I wanted to understand how these technologies work together to solve a real-world problem.

The project evolved through testing, debugging, improving retrieval behavior, separating components into modules, and gradually introducing agent-based tool calling.

My goal was not simply to build a chatbot.

**The goal was to understand how to engineer an AI system.**

---

## 👨‍💻 About

I'm a Computer Science student and aspiring AI Engineer interested in:

* Artificial Intelligence
* Machine Learning
* Natural Language Processing
* Retrieval-Augmented Generation
* AI Agents
* Data Science
* AI-powered automation

I'm continuously building practical projects to strengthen my AI engineering skills and explore how modern AI systems can solve real-world problems.

---

## ⭐ If You Find This Project Interesting

Feel free to explore the code, experiment with the architecture, or suggest improvements.

**Built with curiosity, experimentation, and a lot of debugging. 🚀**
