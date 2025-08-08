Real Wrestling News — MVP

Stack: FastAPI, SQLAlchemy, JWT; SQLite for dev/test, Postgres-ready; Minimal HTML/JS frontend.

Quickstart
1) Make the setup script executable:
   ```bash
   chmod +x run.sh
   ```
2) Run the application:
   ```bash
   ./run.sh
   ```
3) Access the app:
   - UI: http://localhost:8000/static/index.html
   - API Docs: http://localhost:8000/docs

Typical Dev Workflow
- Register & Login
- Promote to admin (dev only): POST `/auth/promote_self` (use API docs)
- Trigger ingestion: POST `/admin/ingest` (also auto-polls every ~15 min)
- View & vote in the UI

Endpoints
- Auth
  - POST `/auth/register` { email, password }
  - POST `/auth/login` (x-www-form-urlencoded: username, password)
  - POST `/auth/promote_self` (dev only)
- Articles & Voting
  - GET `/articles` [tag, source_id, limit]
  - POST `/articles` (auth)
  - POST `/vote` (auth) { article_id, direction: up|down|clear }
- Admin
  - GET `/admin/sources`
  - POST `/admin/sources` (admin)
  - POST `/admin/ingest` (admin)

Environment
- Configure via `.env` (not committed). Supported variables (prefixed with APP_):
  - `APP_DATABASE_URL` (default `sqlite:///./dev.db`)
  - `APP_JWT_SECRET_KEY` (CHANGE IN PROD)
  - `APP_ENVIRONMENT` (`dev`, `test`, `prod`)

Credibility
- Wilson lower bound blended with source score; thresholds configurable via env.

Tests
- Coming soon with pytest.


