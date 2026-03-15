# Decision Engine – Inbank

This project implements a simple loan decision engine based on the credit scoring algorithm described in the assignment.

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
# Mocked Registry Data

For simplicity, the external registry is mocked with hardcoded data:

| Personal Code | Scenario | Credit Modifier |
|---------------|----------|----------------|
| 49002010965 | User with debt | - |
| 49002010976 | Segment 1 | 100 |
| 49002010987 | Segment 2 | 300 |
| 49002010998 | Segment 3 | 1000 |

If a user has debt, the loan is automatically rejected.

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

# Feedback on the Assignment

One thing I would improve in the assignment is how the requested loan amount is used.

Currently, the decision engine always returns the maximum possible amount based on the credit modifier and loan period, regardless of the amount requested by the user.

In a real-world system, the requested amount would likely influence the decision process. For example, the system could first check whether the requested amount can be approved and only return the maximum possible amount if the requested one is too high.

