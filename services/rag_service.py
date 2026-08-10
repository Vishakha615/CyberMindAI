from rag.vector_store import search_documents

from services.llm_service import (
    generate_mentor_response
)


def ask_cybermind(question):

    # -----------------------------------------
    # Retrieve relevant knowledge
    # -----------------------------------------

    results = search_documents(
        question,
        top_k=3
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    if not documents:

        return (
            "I couldn't find relevant information "
            "in my cybersecurity knowledge base.",
            []
        )

    # -----------------------------------------
    # Build context
    # -----------------------------------------

    context_parts = []

    for index, document in enumerate(
        documents
    ):

        source = metadatas[index].get(
            "source",
            "Unknown"
        )

        context_parts.append(
            f"Source: {source}\n"
            f"{document}"
        )

    context = "\n\n".join(
        context_parts
    )

    # -----------------------------------------
    # Generate answer
    # -----------------------------------------

    answer = generate_mentor_response(
        question,
        context
    )

    sources = [
        metadata.get(
            "source",
            "Unknown"
        )
        for metadata in metadatas
    ]

    return answer, sources




def get_relevant_context(
    question,
    top_k=5
):

    results = search_documents(
        question,
        top_k=top_k
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    context_parts = []

    for index, document in enumerate(
        documents
    ):

        source = metadatas[index].get(
            "source",
            "Unknown"
        )

        context_parts.append(
            f"Source: {source}\n"
            f"{document}"
        )

    return "\n\n".join(
        context_parts
    )