# Project Specification: Smart Business Assistant

## 1. Project Overview
The **Smart Business Assistant** is a production-quality, AI-powered business management platform designed for small businesses. It integrates billing management, financial analytics, and a natural language AI assistant to help business owners track their finances, visualize growth, and make data-driven decisions.

### Tech Stack
- **Backend:** FastAPI (Python 3.13)
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Data Validation:** Pydantic
- **Frontend:** Streamlit
- **Visualization:** Plotly
- **AI Integration:** OpenAI-compatible API via FreeLLMAPI

---

## 2. Functional Requirements

### 2.1 Billing & Invoice Management
- **Invoice Creation:** Generate professional invoices with line items, taxes, and discounts.
- **Client Management:** Maintain a directory of clients with contact and billing details.
- **Payment Tracking:** Mark invoices as paid, pending, or overdue.
- **Billing History:** View and filter historical billing data.

### 2.2 Financial Analytics
- **Revenue Tracking:** Real-time visualization of total revenue over time.
- **Expense Analysis:** Categorized tracking of business expenditures.
- **Profit/Loss Dashboards:** Interactive Plotly charts showing net profit margins.
- **Cash Flow Forecasting:** Basic trend analysis based on historical data.

### 2.3 AI Business Assistant
- **Natural Language Querying:** Ask questions about business performance (e.g., "Who is my highest paying client this month?").
- **Report Generation:** Automatically summarize monthly financial health.
- **Business Advice:** Get suggestions on cost-cutting or revenue growth based on data.
- **Context-Awareness:** The AI uses RAG (Retrieval-Augmented Generation) to access real-time database records.

### 2.4 User Management
- **Authentication:** Secure login and registration.
- **Authorization:** Role-based access control (Admin vs. Staff).
- **Profile Management:** Manage business details and preferences.

---

## 3. Non-Functional Requirements
- **Maintainability:** Adherence to strict coding standards (type hints, small functions).
- **Scalability:** Modular architecture allowing for easy addition of new features.
- **Performance:** Optimized SQL queries and asynchronous API endpoints.
- **Security:** JWT-based authentication and protection against common OWASP vulnerabilities.
- **Reliability:** Comprehensive error handling and logging.

---

## 4. Folder Structure
```text
Smart Business Assistant/
├── Backend/
│   ├── app/
│   │   ├── api/            # API route handlers (v1)
│   │   ├── core/           # Configuration, security, and constants
│   │   ├── crud/           # Create, Read, Update, Delete logic
│   │   ├── models/         # SQLAlchemy database models
│   │   ├── schemas/        # Pydantic data models
│   │   ├── services/       # Business logic and AI orchestration
│   │   └── db/             # Database session and engine setup
│   ├── tests/              # Backend unit and integration tests
│   ├── requirements.txt    # Project dependencies
│   └── main.py             # FastAPI entry point
├── Frontend/
│   ├── pages/              # Streamlit multi-page application files
│   ├── components/         # Reusable UI components
│   ├── utils/              # API client and helper functions
│   └── app.py              # Streamlit main entry point
├── Database/
│   └── migrations/         # Alembic database migration scripts
├── Docs/
│   └── PROJECT_SPEC.md     # This specification document
└── Tests/                  # End-to-end integration tests
```

---

## 5. Database Overview
**Database:** PostgreSQL

### Key Entities
- **User:** `id, email, hashed_password, full_name, role, created_at`
- **BusinessProfile:** `id, user_id, business_name, currency, tax_id, address`
- **Client:** `id, business_id, name, email, phone, address`
- **Invoice:** `id, client_id, invoice_number, date, due_date, status (Paid/Pending/Overdue), total_amount`
- **InvoiceItem:** `id, invoice_id, description, quantity, unit_price, total`
- **Transaction:** `id, business_id, amount, type (Income/Expense), category, date, description`

---

## 6. Backend Architecture
- **Layered Pattern:**
    - **API Layer:** FastAPI handles request routing, validation (Pydantic), and response formatting.
    - **Service Layer:** Orchestrates complex business logic and interacts with the AI service.
    - **Data Access Layer:** SQLAlchemy ORM manages all interactions with PostgreSQL.
- **Asynchronous I/O:** Extensive use of `async/await` for database and API calls to ensure high concurrency.
- **Dependency Injection:** FastAPI's `Depends` for managing database sessions and authentication.

---

## 7. Frontend Architecture
- **Framework:** Streamlit for rapid development of a data-centric UI.
- **State Management:** Use of `st.session_state` to maintain user sessions and API tokens.
- **Visualization:** Plotly for interactive, responsive financial charts.
- **Modular Design:** Separate pages for Dashboard, Billing, Clients, and AI Chat.

---

## 8. API Architecture
- **Style:** RESTful API.
- **Versioning:** `/api/v1/` prefix for all endpoints.
- **Authentication:** Bearer Token (JWT) in the Authorization header.
- **Data Format:** JSON for all requests and responses.
- **Error Handling:** Standardized JSON error responses with appropriate HTTP status codes.

---

## 9. AI Assistant Architecture
- **LLM Provider:** FreeLLMAPI (OpenAI-compatible).
- **RAG Pipeline:**
    1. **Query Analysis:** LLM determines if the user is asking for data or general advice.
    2. **Context Retrieval:** If data is needed, the system executes specific SQL queries via the CRUD layer.
    3. **Prompt Augmentation:** The retrieved data is injected into the prompt as context.
    4. **Response Generation:** The LLM generates a human-readable answer based on the provided business data.
- **Prompt Engineering:** System prompts define the AI as a "Professional Business Consultant."

---

## 10. Development Milestones
- [ ] **Milestone 1: Foundation**
    - Project scaffolding, Database schema design, and Environment setup.
- [ ] **Milestone 2: Core Backend**
    - User authentication, Client and Invoice CRUD APIs.
- [ ] **Milestone 3: Basic Frontend**
    - Streamlit integration, Login page, and Billing management UI.
- [ ] **Milestone 4: Analytics Engine**
    - Transaction tracking and Plotly dashboard implementation.
- [ ] **Milestone 5: AI Integration**
    - FreeLLMAPI integration and RAG pipeline for business data.
- [ ] **Milestone 6: Polishing & Testing**
    - End-to-end testing, bug fixes, and production optimization.

---

## 11. Coding Standards
- **Language:** Python 3.13.
- **Type Safety:** Mandatory type hints for all function signatures.
- **Function Length:** Maximum 50 lines per function to ensure readability.
- **Validation:** Pydantic for all input/output data validation.
- **ORM:** SQLAlchemy for all database operations (no raw SQL unless optimized).
- **Style:** PEP 8 compliance.
- **Documentation:** Docstrings for all public-facing services and API endpoints.

---

## 12. Future Improvements
- **Automated Invoicing:** Scheduled invoice generation and email delivery.
- **Multi-Currency Support:** Automatic exchange rate conversion for international clients.
- **Advanced Forecasting:** Machine Learning models for predicting future revenue trends.
- **Third-Party Integration:** Syncing with Stripe, PayPal, or QuickBooks.