import numpy as np
from langchain_core.prompts import ChatPromptTemplate


def generate_answer(llm, retriever, question):
    """
    Retrieve relevant documents and generate
    a grounded answer using the LLM.
    """

    # Retrieve candidate documents using MMR
    documents = retriever.invoke(question)

    if not documents:
        return (
            "I don't know based on the uploaded documents.",
            []
        )

    # Get embedding model from the vector store
    embedding_model = retriever.vectorstore._embedding_function

    # Embed the user's question
    question_embedding = np.array(
        embedding_model.embed_query(question)
    )

    # Embed retrieved documents
    document_embeddings = embedding_model.embed_documents(
        [
            document.page_content
            for document in documents
        ]
    )

    # Calculate cosine similarity
    relevant_documents = []

    for document, document_embedding in zip(
        documents,
        document_embeddings
    ):

        document_embedding = np.array(
            document_embedding
        )

        similarity = np.dot(
            question_embedding,
            document_embedding
        ) / (
            np.linalg.norm(question_embedding)
            * np.linalg.norm(document_embedding)
        )

        # Relevance threshold
        if similarity >= 0.35:
            relevant_documents.append(document)

    # No sufficiently relevant documents
    if not relevant_documents:

        return (
            "I don't know based on the uploaded documents.",
            []
        )

    # Create context only from relevant documents
    context = "\n\n".join(
        document.page_content
        for document in relevant_documents
    )

    # Prompt
    template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are DocuMind AI, an intelligent document assistant.

Answer the user's question using ONLY the
information provided in the document context.

If the answer cannot be found in the context,
say:

"I don't know based on the uploaded documents."

Do not use outside knowledge.

Document context:
{context}
"""
            ),
            (
                "human",
                "{question}"
            )
        ]
    )

    prompt = template.invoke(
        {
            "context": context,
            "question": question
        }
    )

    # Generate answer
    response = llm.invoke(prompt)

    return response.content, relevant_documents