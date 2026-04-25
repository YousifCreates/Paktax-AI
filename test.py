import os
os.environ['PYTHONPATH'] = '.'
from chain.qa_chain_openai import ask

print("Ask a question about Pakistani income tax (or type 'exit' to quit)")

while True:
    question = input("You: ")
    if question.lower() == 'exit':
        break

    answer = ask(question)
    print("PakTax AI: ", answer)