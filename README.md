# Promtflow Orchestration of React/Python/Postgres Web App with Response Rating Feature

This project consists of a backend and frontend. The backend is written in Python and the frontend is a React application.

## Backend

The backend is located in the `backend/` directory. It uses a flow-based approach to handle chat conversations, with each step of the flow defined in the `backend/flow/` directory. The flow is defined in `backend/flow/flow.dag.yaml`.

The backend also includes a `.gitignore` file that specifies files and directories that should not be tracked by Git.

### Database

The backend uses SQLAlchemy as an ORM and it defines several models in [`backend/models.py`](backend/models.py). To set up the database, you need to run the `init_db.py` script:

python backend/init_db.py

This will create the necessary tables in the database.

### Rating Feature (backend)

The backend provides an endpoint to rate chat messages. This is implemented in the rate_chat function in backend/app.py. The rating is stored in the Rating model defined in backend/models.py.

### Overview of the PromptFlow Package

The promptflow package is designed to manage and execute a series of tasks in a conversational AI workflow. It uses a JSON configuration file to define the flow of tasks and their dependencies.

**Key Components**

1. Flow Detail (flow.detail.json): This file contains the details of the AI assistant's capabilities, the prompt to be used, and the parameters for the AI model.

2. Flow Tools (flow.tools.json): This file defines the tools used in the flow. Each tool has a type (e.g., Python function, LLM), inputs, and a source file or function.

3. Python Scripts: Scripts like FormatRetrievedDocuments.py, FormatConversation.py, and FormatReply.py are used to format the conversation history, retrieved documents, and the AI's reply.

4. Jinja2 Templates: Templates like DetermineReply.jinja2 are used to generate the prompt for the AI model.

5. Azure OpenAI GPT-4 Turbo (AzureOpenAI.chat): This is the AI model used to generate the reply.

**Workflow**

1. The conversation history and retrieved documents are formatted using the respective Python scripts.

2. The prompt for the AI model is generated using the Jinja2 template.

3. The AI model generates a reply based on the prompt.

4. The reply is formatted using the FormatReply.py script.

5. The formatted reply is returned to the user.

Please refer to the respective files for more detailed information:

- Flow Detail: backend/flow/.promptflow/flow.detail.json
- Flow Tools: backend/flow/.promptflow/flow.tools.json
- Python Scripts: backend/flow/
- Jinja2 Templates: backend/flow/
- Azure OpenAI GPT-4 Turbo: backend/flow/.promptflow/flow.tools.json (under AzureOpenAI.chat)

## Frontend

The frontend is located in the `frontend/` directory. It is a React application created with Create React App. For more information on how to work with this application, refer to the `frontend/README.md`.

The frontend also includes a `.gitignore` file that specifies files and directories that should not be tracked by Git.

### Rating Feature (frontend)

The frontend provides a way for users to rate chat messages. This is implemented in the rateResponse function in frontend/src/components/Chat.js.

## Getting Started

To get started with this project:

1. Clone the repository.
2. Install the backend dependencies by running `pip install -r backend/requirements.txt`.
3. Install the frontend dependencies by running `npm install` in the `frontend/` directory.
4. Start the backend by running `python backend/main.py`.
5. Start the frontend by running `npm start` in the `frontend/` directory.

## Contributing

Contributions are welcome. Please open an issue to discuss your idea or submit a pull request.

## License

This project is licensed under the terms of the MIT license.
