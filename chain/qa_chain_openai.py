import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from rag.retriever import get_retriever

# Disable ChromaDB telemetry
os.environ["ANONYMIZED_TELEMETRY"] = "False"

# Load environment variables
load_dotenv()

# Chat history store
chat_history = []


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def get_qa_chain():
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.3
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are PakTax AI, an expert FBR (Federal Board of Revenue)
tax assistant for Pakistan. You help Pakistani citizens understand and file
their income tax returns.

STRICT RULES:
1. Only answer questions related to Pakistani income tax, FBR policies, and tax filing.
2. Always base your answers on the provided FBR document context below.
3. If the answer is not clearly in the context, use the context clues available
   and provide the best possible answer based on FBR documents. Only say you 
   could not find it if the context has absolutely no relevant information.
4. Never guess or make up tax figures, slabs, or deadlines.
5. Never give a final tax liability number — tell the user to verify with the 
   official FBR calculator at fbr.gov.pk.
6. Respond in the same language the user writes in — Urdu, Roman Urdu, or English.
7. Be warm, patient, and encouraging — many users are filing for the first time.
8. Keep responses clear and simple — avoid complex legal language.
9. When tax slabs or rates are present in the context, always present them in a
   clear numbered table format for easy reading.

CONTEXT FROM FBR DOCUMENTS:
{context}"""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])

    retriever = get_retriever()

    chain = (
        {
            "context": (lambda x: x["input"]) | retriever | format_docs,
            "chat_history": lambda x: x["chat_history"],
            "input": lambda x: x["input"]
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain


def ask(question):
    global chat_history
    chain = get_qa_chain()

    answer = chain.invoke({
        "input": question,
        "chat_history": chat_history
    })

    # Update chat history
    chat_history.append(HumanMessage(content=question))
    chat_history.append(AIMessage(content=answer))

    return answer


if __name__ == "__main__":
    print("=== Testing QA Chain ===")
    test_question = "What are the income tax slabs for salaried individuals in Pakistan for tax year 2024-25?"
    print(f"\nQuestion: {test_question}\n")
    answer = ask(test_question)
    print(f"Answer:\n{answer}")