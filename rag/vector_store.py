'''import os
import chromadb

from rag.chunking import split_text
from rag.embeddings import create_embeddings


CHROMA_PATH = "chroma_db"

COLLECTION_NAME = "cybermind_knowledge"


client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)


print("Chroma collection:", COLLECTION_NAME)
print("Document count:", collection.count())


def add_document(
    document_text,
    source_name
):

    chunks = split_text(document_text)

    if not chunks:
        return 0

    embeddings = create_embeddings(chunks)

    ids = []

    metadatas = []

    for index in range(len(chunks)):

        ids.append(
            f"{source_name}_{index}"
        )

        metadatas.append(
            {
                "source": source_name,
                "chunk": index
            }
        )

    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return len(chunks)


def search_documents(
    query,
    top_k=3
):

    query_embedding = create_embeddings(
        [query]
    )[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results


def get_document_count():

    return collection.count()'''





import os
import chromadb

from rag.chunking import split_text
from rag.embeddings import create_embeddings


CHROMA_PATH = "chroma_db"

COLLECTION_NAME = "cybermind_knowledge"


client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)

print("Chroma collection:", COLLECTION_NAME)
print("Document count:", collection.count())

def add_document(
    document_text,
    source_name
):

    chunks = split_text(document_text)

    if not chunks:
        return 0

    embeddings = create_embeddings(chunks)

    ids = []

    metadatas = []

    for index in range(len(chunks)):

        ids.append(
            f"{source_name}_{index}"
        )

        metadatas.append(
            {
                "source": source_name,
                "chunk": index
            }
        )

    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return len(chunks)


'''def search_documents(
    query,
    top_k=3
):

    query_embedding = create_embeddings(
        [query]
    )[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results'''
    
    
def search_documents(query, top_k=3):

    query_embedding = create_embeddings([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    print("QUERY:", query)
    print("DOCUMENTS:", results.get("documents"))
    print("METADATAS:", results.get("metadatas"))
    print("DISTANCES:", results.get("distances"))

    return results


def get_document_count():

    return collection.count()
