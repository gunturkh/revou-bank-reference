# RevoBank API Usage Guide

This document provides instructions for using the RevoBank RESTful API.

## Setup and Running

1. Install dependencies using uv:
   ```
   uv pip install -r requirements.txt
   ```

2. Initialize the database with test data:
   ```
   python init_db.py
   ```

3. Run the application:
   ```
   python run.py
   ```

## Authentication

Most endpoints require authentication. To authenticate:

1. Create a new user account or use a test account:
   - Username: `johndoe`
   - Password: `password123`

2. Login to obtain a JWT token:
   ```
   curl -X POST -H "Content-Type: application/json" -d '{"username":"johndoe","password":"password123"}' http://localhost:5000/users/login
   ```

3. Use the token in subsequent requests:
   ```
   curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:5000/users/me
   ```

## API Endpoints

### User Management

#### Create a new user
```
POST /users
Content-Type: application/json

{
  "username": "newuser",
  "email": "user@example.com",
  "password": "securepassword",
  "first_name": "New",
  "last_name": "User"
}
```

#### Get current user profile
```
GET /users/me
Authorization: Bearer YOUR_TOKEN
```

#### Update current user profile
```
PUT /users/me
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "first_name": "Updated",
  "last_name": "Name"
}
```

### Account Management

#### Get all accounts
```
GET /accounts
Authorization: Bearer YOUR_TOKEN
```

#### Get account by ID
```
GET /accounts/1
Authorization: Bearer YOUR_TOKEN
```

#### Create a new account
```
POST /accounts
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "account_type": "savings",
  "initial_balance": 1000.0
}
```

#### Update an account
```
PUT /accounts/1
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "account_type": "checking",
  "is_active": true
}
```

#### Delete an account
```
DELETE /accounts/1
Authorization: Bearer YOUR_TOKEN
```

### Transaction Management

#### Get all transactions
```
GET /transactions
Authorization: Bearer YOUR_TOKEN
```

Optionally filter by account or transaction type:
```
GET /transactions?account_id=1&type=deposit
Authorization: Bearer YOUR_TOKEN
```

#### Get transaction by ID
```
GET /transactions/1
Authorization: Bearer YOUR_TOKEN
```

#### Create deposit transaction
```
POST /transactions
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "transaction_type": "deposit",
  "amount": 500.0,
  "to_account_id": 1,
  "description": "Salary deposit"
}
```

#### Create withdrawal transaction
```
POST /transactions
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "transaction_type": "withdrawal",
  "amount": 200.0,
  "from_account_id": 1,
  "description": "ATM withdrawal"
}
```

#### Create transfer transaction
```
POST /transactions
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "transaction_type": "transfer",
  "amount": 300.0,
  "from_account_id": 1,
  "to_account_id": 2,
  "description": "Monthly savings"
}
```

## Testing with Postman or Insomnia

1. Create a new request in Postman/Insomnia
2. Set the appropriate HTTP method and URL
3. Add headers (Content-Type, Authorization)
4. Add request body if needed
5. Send the request and check the response 