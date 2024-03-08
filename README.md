# React Frontend with Azure AI Promptflow and AI Search

This project consists of a backend and frontend. The backend is written in Python and the frontend is a React application.

## Backend

The backend is located in the `backend/` directory. It uses a flow-based approach to handle chat conversations, with each step of the flow defined in the `backend/flow/` directory. The flow is defined in `backend/flow/flow.dag.yaml`.

The backend also includes a `.gitignore` file that specifies files and directories that should not be tracked by Git.

## Frontend

The frontend is located in the `frontend/` directory. It is a React application created with Create React App. For more information on how to work with this application, refer to the `frontend/README.md`.

The frontend also includes a `.gitignore` file that specifies files and directories that should not be tracked by Git.

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
