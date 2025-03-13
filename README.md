# RevoBank RESTful API

A RESTful API for the RevoBank application with User, Account, and Transaction management.

## Features

- **User Management**: Create, retrieve, and update user profiles
- **Account Management**: Create, retrieve, update, and delete bank accounts
- **Transaction Management**: Process and retrieve transaction records

## Setup and Installation

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies using uv:
   ```
   uv pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python app.py
   ```

## API Endpoints

### User Management
- `POST /users`: Create a new user account
- `GET /users/me`: Retrieve current user profile
- `PUT /users/me`: Update current user profile

### Account Management
- `GET /accounts`: List all accounts
- `GET /accounts/:id`: Get account details
- `POST /accounts`: Create a new account
- `PUT /accounts/:id`: Update account details
- `DELETE /accounts/:id`: Delete an account

### Transaction Management
- `GET /transactions`: List all transactions
- `GET /transactions/:id`: Get transaction details
- `POST /transactions`: Create a new transaction # revou-bank-reference
