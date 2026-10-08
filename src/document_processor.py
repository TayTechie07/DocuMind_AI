import os
import tempfile

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def process_documents(uploaded_files):
    """
    Load uploaded PDF files and split them into chunks.
    """

    all_chunks = []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )

    for uploaded_file in uploaded_files:

        temp_path = None

        try:

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as temp_file:

                temp_file.write(
                    uploaded_file.getvalue()
                )

                temp_path = temp_file.name

            # Load PDF
            loader = PyPDFLoader(temp_path)

            documents = loader.load()

            # Add original filename to metadata
            for document in documents:

                document.metadata["source"] = (
                    uploaded_file.name
                )

            # Split into chunks
            chunks = splitter.split_documents(
                documents
            )

            all_chunks.extend(chunks)

        finally:

            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)

    return all_chunks