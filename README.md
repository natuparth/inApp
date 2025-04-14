# IMDB Clone App

This project is a full-stack application with a FastAPI backend and a React frontend using Material UI. It mimics a simplified version of the IMDB platform with movie and actor search functionalities.

## How to Run the Application

### Frontend (React UI)

Navigate to the `ui` folder, install dependencies, and start the development server:

```bash
cd ui
npm install
npm run dev
```

This will start the frontend on [http://localhost:5173](http://localhost:5173) by default.

### Backend (FastAPI)

Navigate to the `backend` folder and start the FastAPI server:

```bash
cd backend
uvicorn main:app --reload
```

Or, if you're using a custom command:

```bash
fastapi dev main.py
```

This will start the backend on [http://localhost:8000](http://localhost:8000), and the Swagger UI will be available at [http://localhost:8000/docs](http://localhost:8000/docs).

## Project Structure

```
/project-root
│
├── backend/        # FastAPI backend
│   └── main.py     # FastAPI entrypoint
│
└── ui/             # React frontend
    └── src/        # React components
```

## Notes

- Make sure your backend is running before using features on the frontend that depend on API calls.
- The backend uses token-based authentication via OAuth2.
- Swagger docs can be used to interact with API endpoints.

---

