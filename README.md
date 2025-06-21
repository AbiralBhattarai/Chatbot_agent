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

1. Run the `chatagent.py ` script to start the chatbot:
```
python chatagent.py
```

2. The chatbot will start running, and you can interact with it by typing your messages in the console.

3. The chatbot supports the following functionalities:
   - **Document Search**: The chatbot can search for relevant documents based on your query and provide the information from those documents.
   - **Appointment Booking**: The chatbot can help you book an appointment by extracting the necessary details (name, email, phone number, and appointment date) from your input. You can type in the date as Next Monday,etc and the chatbot will use the date_tool to find the accurate date.

4. To exit the chatbot, type `quit`, `exit`, `end`, or `bye`.

## API

The chatbot uses the following APIs and tools:

- **Google Generative AI**: The chatbot uses the Google Generative AI model for natural language processing and generation.
- **Google Firestore**: The chatbot uses Google Firestore to store the chat history and customer appointment details.
- **Chroma**: The chatbot uses the Chroma vector store to store and retrieve relevant documents.
- **Verify-email**: Used to verify the email.

## Contributing

If you would like to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your forked repository.
5. Submit a pull request to the main repository.

