import os

from rag.vector_store import add_document


DOCUMENTS_PATH = "rag/documents"


def build_knowledge_base():

    total_chunks = 0

    for filename in os.listdir(
        DOCUMENTS_PATH
    ):

        if not filename.endswith(".txt"):
            continue

        file_path = os.path.join(
            DOCUMENTS_PATH,
            filename
        )

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            text = file.read()

        chunks_added = add_document(
            text,
            filename
        )

        total_chunks += chunks_added

        print(
            f"✅ {filename}: "
            f"{chunks_added} chunks"
        )

    print(
        f"\n🎉 Total chunks: {total_chunks}"
    )


if __name__ == "__main__":

    build_knowledge_base()