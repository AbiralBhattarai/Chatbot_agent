import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage
from langchain_chroma import Chroma
from google.cloud import firestore
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda,RunnableBranch
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_firestore import FirestoreChatMessageHistory
from pydantic import BaseModel,Field
from datetime import datetime
from verify_email import verify_email

class UserDetails(BaseModel):
    """Information about the customer."""
    name:str = Field(description="The name of the user")
    email:str = Field(description="The email of the user")
    phone: str = Field(description="The phone number of the user")
    appointment_date: str = Field(description="Date of the appointment.")

def get_system_time(format: str = "%Y-%m-%d %H:%M:%S"):
        """Get the current system time in the given format"""
        return datetime.now().strftime(format)
     

load_dotenv()
PROJECT_ID = "langchain-15031"
SESSION_ID = "user_session_1"
COLLECTION_NAME_1 = "chat_history"
COLLECTION_NAME_2 = "customer_appointments"

print("Initializing firestore client")
client = firestore.Client(project=PROJECT_ID)

print("Initializing FirestoreChatMessageHistory")

chat_history= FirestoreChatMessageHistory(
        session_id=SESSION_ID,
        collection=COLLECTION_NAME_1,
        client=client
)

user_appointments = FirestoreChatMessageHistory(
        session_id=SESSION_ID,
        collection=COLLECTION_NAME_2,
        client=client
)

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

print("\nDocument Search and Appointment Booking Chatbot: \n")


classification_prompt_template = ChatPromptTemplate.from_messages([
    ('system','Classify user input:'),
    ('human',"Classify this query into either document_search or book_appointment or not_sure: {query}.The only answers should be one word: Either document_search or book_appointment or not_sure.")
])

classification_chain = classification_prompt_template|llm|StrOutputParser()

while True:
    query = input("You:")
    if query.lower() in ['quit','exit','end','bye']:
        print('Thank you for using the chatbot!')
        break
    response = classification_chain.invoke({"query": query})
    print(response)
    if response =='document_search':
        relevant_docs = retriever.invoke(query)
        combined_input = (
            "Here are some documents that might help answer the user query:" + 
            query + "\n\nRelevant docs:\n\n".join([doc.page_content for doc in relevant_docs]) + "\n\n Please answer the query based on above docs\n\n"
            + "If unsure about the answer, reply with I'm not sure about that."
        )
        human_message = HumanMessage(content=combined_input)
        chat_history.add_user_message(human_message)
        result = llm.invoke(chat_history.messages)
        response = result.content
        chat_history.add_ai_message(AIMessage(content=response))
        print("ChatBot: ",response)
    elif(response == 'book_appointment'):
        details = input("Enter your name,email,phone_number and appointment date:")
        messages = [
            ("system", f"You are an assistant that extracts structured user details."),
            ("system", f"Today's date is: {get_system_time()}."),
            ("human", f"The user has input: {details}. Please extract the name, email, phone number, and appointment date."),
        ]

        detail_extractor_llm = llm.with_structured_output(UserDetails)
        response = detail_extractor_llm.invoke(messages)
        name = response.name
        email = response.email
        phone_num = response.phone
        appointment_date = response.appointment_date
        while True:
            if verify_email(email) and (phone_num.startswith('9') and len(phone_num)==10):
                print("Email and Phone verified!")
                break
            else:
                print("\nInvalid Email and Phone number!\n Please re-enter:\n")
                email = input("Enter email: ")
                phone_num = input("Enter phone number: ")
        formatted = f"Name:{name}, Email:{email}, Phone number:{phone_num}, Appointment Date: {appointment_date}"
        user_appointments.add_user_message(HumanMessage(content=formatted))
        print("\nAppointment_booked!!\n\nAppointment Details:\n"+formatted+'\n\n')

    else:
        print("I'm not sure about that.")

