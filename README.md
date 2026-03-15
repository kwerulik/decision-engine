# Decision Engine – Inbank

# Project Structure

```
decision-engine
│
├── backend
│   ├── main.py
│   ├── test_main.py
│   └── requirements.txt
│
├── frontend
│   ├── index.html
│   ├── app.js
│   └── style.css
│
├── .gitignore
└── README.md
```

Backend contains the API and decision logic.

Frontend is a very simple interface that allows submitting loan applications to the API.

---

# Decision Logic

The assignment provided the following scoring formula:

```
credit_score = (credit_modifier / loan_amount) * loan_period
```

Decision rule:

```
score >= 1 → loan approved
score < 1 → loan rejected
```

Instead of iterating through possible loan values, the inequality can be simplified mathematically:

```
loan_amount <= credit_modifier * loan_period
```

This means the **maximum approvable loan amount** can be calculated directly as:

```
max_amount = credit_modifier * loan_period
```


If the calculated amount is below the minimum allowed loan (2000€), the system tries to find a **longer loan period** that satisfies the condition.

If no valid combination exists within the allowed limits, the application is rejected.

---

# Tech Stack

Backend

* Python
* FastAPI
* Pydantic
* Pytest

Frontend

* HTML
* JavaScript
* CSS

---

# Running the Project

## 1. Start the backend

```
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

The API will run at:

```
http://127.0.0.1:8000
```

---

## 2. API Documentation

FastAPI automatically generates API documentation:

```
http://127.0.0.1:8000/docs
```

---

## 3. Run the frontend

Simply open:

```
frontend/index.html
```

in your browser.

The frontend sends requests to the backend API and displays the decision.

---

# Running Tests

```
cd backend
pytest
```

Tests verify several scenarios:

* user with existing debt
* approval with adjusted loan period
* standard approval
* maximum loan cap
* invalid personal code
* validation errors

---


