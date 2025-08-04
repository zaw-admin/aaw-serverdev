# aaw-serverdev

Prototype server for AAW AI code assistant running a local model.

## Structure
- `host_server/` – FastAPI application providing code analysis with key-based access and task scheduling.
- `host_server/static/` – web GUIs for users (`index.html`) and admins (`admin.html`).
- `requirements.txt` – Python dependencies.

## Running
1. Set allowed keys (comma separated) and optional concurrency:
   ```bash
   export ALLOWED_KEYS="demo-key"
   export MAX_CONCURRENCY=2  # optional
   ```
2. Start the server:
   ```bash
   uvicorn host_server.main:app --reload
   ```
   On startup the application pulls the latest `main` branch and installs dependencies
   from `requirements.txt` automatically.
3. User interface: open [http://localhost:8000](http://localhost:8000).
4. Admin dashboard: open [http://localhost:8000/admin](http://localhost:8000/admin) for resource usage and active users.

The server loads a local Hugging Face model (`distilgpt2` by default) to analyze submitted code. Requests are queued via an internal semaphore so multiple users can be handled concurrently without manual intervention. An admin endpoint allows updating concurrency limits on the fly.
