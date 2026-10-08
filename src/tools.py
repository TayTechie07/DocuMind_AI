from langchain_core.tools import tool


def create_tools(retriever, documents):
    """
    Create agent-ready tools using the current
    document knowledge base.
    """

    @tool
    def search_documents(query: str) -> str:
        """
        Search the uploaded documents for information
        relevant to the user's question.
        """

        if not query.strip():
            return "Please provide a search query."

        results = retriever.invoke(query)

        if not results:
            return (
                "No relevant information was found "
                "in the uploaded documents."
            )

        formatted_results = []

        for index, document in enumerate(
            results,
            start=1
        ):

            source = document.metadata.get(
                "source",
                "Unknown document"
            )

            page = document.metadata.get(
                "page",
                None
            )

            if isinstance(page, int):
                page_number = page + 1
            else:
                page_number = "Unknown"

            formatted_results.append(
                f"""
Source {index}
Document: {source}
Page: {page_number}

Content:
{document.page_content}
"""
            )

        return "\n\n".join(formatted_results)


    @tool
    def summarize_document(document_text: str) -> str:
        """
        Prepare document content for summarization.
        The agent will use the LLM to generate the summary.
        """

        if not document_text.strip():
            return "No document content was provided."

        return (
            "Document content available for summarization:\n\n"
            + document_text
        )


    @tool
    def extract_information(
        document_text: str,
        fields: list[str]
    ) -> str:
        """
        Prepare document content and requested fields
        for structured information extraction.
        """

        if not document_text.strip():
            return "No document content was provided."

        if not fields:
            return "No fields were specified for extraction."

        requested_fields = ", ".join(fields)

        return (
            "Extract the following information from the "
            "document:\n"
            f"{requested_fields}\n\n"
            "Document content:\n"
            f"{document_text}"
        )


    @tool
    def document_statistics() -> str:
        """
        Return statistics about the uploaded documents.
        """

        if not documents:
            return "No documents have been processed."

        document_names = set()
        pages = set()

        for document in documents:

            source = document.metadata.get(
                "source",
                "Unknown document"
            )

            page = document.metadata.get(
                "page",
                None
            )

            document_names.add(source)

            if page is not None:
                pages.add(
                    (source, page)
                )

        return (
            f"Documents: {len(document_names)}\n"
            f"Pages: {len(pages)}\n"
            f"Chunks: {len(documents)}"
        )


    return [
        search_documents,
        summarize_document,
        extract_information,
        document_statistics
    ]