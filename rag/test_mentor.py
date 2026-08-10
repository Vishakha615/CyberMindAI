from services.rag_service import ask_cybermind


question = input(
    "Ask CyberMind AI: "
)


answer, sources = ask_cybermind(question)


print("\n🤖 CyberMind AI\n")
print(answer)


print("\n📚 Sources:")

for source in sources:

    print("-", source)