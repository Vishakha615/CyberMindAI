from rag.vector_store import search_documents


query = input(
    "Ask a cybersecurity question: "
)


results = search_documents(
    query,
    top_k=3
)


print("\n🔎 Retrieved Knowledge:\n")


documents = results["documents"][0]

metadatas = results["metadatas"][0]

distances = results["distances"][0]


for index in range(
    len(documents)
):

    print(
        f"\nResult {index + 1}"
    )

    print(
        "Source:",
        metadatas[index]["source"]
    )

    print(
        "Distance:",
        distances[index]
    )

    print(
        "Content:",
        documents[index]
    )