from rag.vector_store import collection


print(
    "Total documents/chunks:",
    collection.count()
)


data = collection.get(
    include=[
        "documents",
        "metadatas"
    ]
)


for index, document in enumerate(
    data["documents"]
):

    print("\n" + "=" * 60)

    print(
        "ID:",
        data["ids"][index]
    )

    print(
        "Source:",
        data["metadatas"][index]["source"]
    )

    print(
        "Chunk:",
        data["metadatas"][index]["chunk"]
    )

    print(
        "Document:",
        document
    )