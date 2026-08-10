from rag import ask_question


question = "How long is the internship?"

result = ask_question(question)

print("\nANSWER:")
print(result["answer"])

print("\nSOURCES:")
for source in result["sources"]:
    print("-", source)