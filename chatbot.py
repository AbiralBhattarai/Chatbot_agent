import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda,RunnableBranch
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()
llm = ChatGoogleGenerativeAI(model = "gemini-2.0-flash")

current_dir = os.path.dirname(os.path.abspath(__file__))

db_dir = os.path.join(current_dir,"db")
persistent_directory = os.path.join(db_dir,"chroma_db")

embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")

db = Chroma(persist_directory=persistent_directory,embedding_function=embeddings)
retriever = db.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k":5,"score_threshold":0.5}
)

print("\nDocument Search Chatbot: \n")

chat_history = []
chat_history.append(("system","You are a helpful chatbot that answers users query based on the provided documents."))
while True:
    query = input("You:")
    if query.lower() in ['quit','exit','end','bye']:
        print('Thank you for using the chatbot!')
        break
    relevant_docs = retriever.invoke(query)
    combined_input = (
        "Here are some documents that might help answer the user query:" + 
        query + "\n\nRelevant docs:\n\n".join([doc.page_content for doc in relevant_docs]) + "\n\n Please answer the query based on above docs\n\n"
        + "If unsure about the answer, reply with I'm not sure about that."
    )
    human_message = HumanMessage(content=combined_input)
    chat_history.append(human_message)
    result = llm.invoke(chat_history)
    response = result.content
    chat_history.append(AIMessage(content=response))
    print("ChatBot: ",response)


    