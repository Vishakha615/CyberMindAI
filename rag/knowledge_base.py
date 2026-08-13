from rag.vector_store import (
    add_document,
    get_document_count
)


CYBERSECURITY_CONTENT = """
Cybersecurity is the practice of protecting computer systems,
networks, applications and data from unauthorized access,
misuse and attacks.

The three fundamental principles of information security are
Confidentiality, Integrity and Availability, commonly known as CIA.

Confidentiality means that information should only be accessible
to authorized individuals.

Integrity means that information should remain accurate and
should not be modified without authorization.

Availability means that authorized users should be able to
access systems and information when needed.

Authentication is the process of verifying the identity of
a user or system.

Authorization determines what an authenticated user is allowed
to access or perform.

A firewall is a security control that monitors and controls
network traffic according to defined security rules.
"""


def initialize_knowledge_base():

    count = get_document_count()

    print("Current ChromaDB document count:", count)

    if count == 0:

        added = add_document(
            CYBERSECURITY_CONTENT,
            "cybersecurity_basics.txt"
        )

        print(
            f"Knowledge base initialized: {added} chunks"
        )