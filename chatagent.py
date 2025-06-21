import os
from dotenv import load_dotenv
from datetime import datetime
from langchain import hub
from langchain.agents import Tool, AgentExecutor, initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.messages import HumanMessage, AIMessage
from langchain.chains import RetrievalQA
from langchain_chroma import Chroma
from google.cloud import firestore
from langchain_google_firestore import FirestoreChatMessageHistory
from verify_email import verify_email
from pydantic import BaseModel, Field

# load environment variables
load_dotenv()


class UserDetails(BaseModel):
    name: str = Field(description="The name of the user")
    email: str = Field(description="The email of the user")
    phone: str = Field(description="The phone number of the user")
    appointment_date: str = Field(description="Date of the appointment.")

#firestore steup
PROJECT_ID = os.getenv("PROJECT_ID")
SESSION_ID = os.getenv("SESSION_ID")
COLLECTION_NAME_1 = "chat_history"
COLLECTION_NAME_2 = "customer_appointments"

client = firestore.Client(project=PROJECT_ID)

chat_history = FirestoreChatMessageHistory(
    session_id=SESSION_ID,
    collection=COLLECTION_NAME_1,
    client=client
)

user_appointments = FirestoreChatMessageHistory(
    session_id=SESSION_ID,
    collection=COLLECTION_NAME_2,
    client=client
)

#initialize llm and embedding model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

#initialize the chroma vectorstore
current_dir = os.path.dirname(os.path.abspath(__file__))
db_dir = os.path.join(current_dir, "db")
persistent_directory = os.path.join(db_dir, "chroma_db")

db = Chroma(persist_directory=persistent_directory, embedding_function=embeddings)
retriever = db.as_retriever(search_type="similarity_score_threshold", search_kwargs={"k": 5, "score_threshold": 0.5})

retrieval_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

#search_tool
def search_documents(query):
    return retrieval_chain.invoke(query)

search_tool = Tool(
    name="search_documents",
    func=search_documents,
    description="Use this tool to answer user questions based on uploaded documents."
)

# tool to get current datetime
def get_current_time():
    return f"The current system time is {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."

date_tool = Tool(
    name="get_current_date_time",
    func=get_current_time,
    description="Use this to get the current system time and date."
)

# tool to book appointment
def book_appointment(query):
    
    #extract name, email, phonenumber and appointment date using llm
    detail_extractor = llm.with_structured_output(UserDetails)
    details = detail_extractor.invoke(query)

    #validate the email and phone num
    email = details.email
    phone = details.phone
    if not verify_email(email) or not (phone.startswith("9") and len(phone) == 10): #simple phonenumber verificaiton logic.
        return "Invalid email or phone number format. Please try again."

    #store appointment details
    formatted = f"Name: {details.name}, Email: {email}, Phone: {phone}, Appointment Date: {details.appointment_date}"
    user_appointments.add_user_message(HumanMessage(content=formatted))
    return "Appointment booked!\n" + formatted

book_tool = Tool(
    name="book_appointment",
    func=book_appointment,
    description="Use this tool to book an appointment. Include name, email, phone number, and appointment date in the message."
)

#specify available tools for agent
tools = [search_tool, book_tool, date_tool]

#initialize agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

#chatbot loop
print("\nDocument Search and Appointment Booking Chatbot:\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ['quit', 'exit', 'bye']:
        print("ChatBot: Thank you for using the chatbot!")
        break

    result = agent.invoke(user_input)
    print("ChatBot:", result['output'])
