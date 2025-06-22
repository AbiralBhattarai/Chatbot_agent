# Document Search and Appointment Booking Chatbot

## Installation

1. Clone the repository:
```
git clone https://github.com/AbiralBhattarai/Chatbot_agent.git
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

3. Set up the environment variables:
   - Create a `.env` file in the project directory.
   - Add the following variables to the `.env` file:
     ```
     PROJECT_ID=your-google-cloud-project-id
     SESSION_ID=your-session-id
     GOOGLE_API_KEY = your-google-gemini-api-key
     ```

4. Ensure you have the necessary Google Cloud credentials set up for Firestore and Google Generative AI.

## Usage
1. Additional txt or pdf documents can be added to the docs folder. Run the `vectorize.py` script to vectorize the documents which enables the chatbot to search the documents.

2. Run the `chatagent.py ` script to start the chatbot:
```
python chatagent.py
```

3. The chatbot will start running, and you can interact with it by typing your messages in the console.

4. The chatbot supports the following functionalities:
   - **Document Search**: The chatbot can search for relevant documents based on your query and provide the information from those documents.
   - **Appointment Booking**: The chatbot can help you book an appointment by extracting the necessary details (name, email, phone number, and appointment date) from your input. You can type in the date as Next Monday,etc and the chatbot will use the date_tool to find the accurate date.

5. To exit the chatbot, type `quit`, `exit`, `end`, or `bye`.

## Technologies Used

- [Google Generative AI](https://ai.google.dev/)  
  Used for natural language understanding and generation via the Gemini (Generative AI) model.

- [LangChain](https://docs.langchain.com/)  
  A framework for building applications with LLMs, used to orchestrate tools, memory, agents, and prompts.

- [Google Firestore](https://firebase.google.com/docs/firestore)  
  A scalable NoSQL cloud database used to store chat history and customer appointment details in real time.

- [Chroma](https://docs.trychroma.com/)  
  An open-source embedding-based vector database for storing and retrieving relevant documents using similarity search.

- [verify-email](https://pypi.org/project/verify-email/)  
  A Python package used to verify and validate email addresses before processing.


## Contributing

If you would like to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your forked repository.
5. Submit a pull request to the main repository.

