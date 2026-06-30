"""
==============================================================================
Flask REST API — User Registration Endpoint (Complete Tutorial)
==============================================================================

This file teaches you how to build a REST API from scratch.
From Python basics (loops, conditionals, functions), this will
bridge the gap to web development and backend engineering.

We'll build a /register endpoint that accepts user signups.

----- WHAT IS THE INTENTION OF THIS USE-CASE? -----

Almost every web application needs user registration:
  - Instagram: you sign up with email/username/password
  - Netflix: you create an account before watching
  - Amazon: you register before buying

This use-case teaches you how the SERVER SIDE works. When you click
"Sign Up" on a website, the frontend sends your data to a backend API
like the one we're building here. The backend:
  1. Receives the data
  2. Validates it (is the email real? is the password strong?)
  3. Stores it in a database
  4. Sends back a success or error response

This is a FOUNDATIONAL skill for any backend or full-stack role.
Every interview for Applied Scientist, Forward Deployed Engineer,
or Software Engineer will test whether you can build, reason about,
and debug API endpoints like this.
"""


# =============================================================================
# PART 1: CONCEPTS — What Are APIs, REST, Flask, Endpoints?
# =============================================================================

# ----- What is an API? -----
#
# API = Application Programming Interface
#
# An API is a CONTRACT between two pieces of software. It says:
#   "If you send me data in THIS format, I'll send you back data in THAT format."
#
# Real-world analogy:
#   You (client) go to a restaurant. You don't walk into the kitchen.
#   Instead, you talk to a WAITER (the API). You give your ORDER (request),
#   and the waiter brings back your FOOD (response).
#
#   Client  →  API  →  Server/Database
#   (you)     (waiter)  (kitchen)
#
# Examples of APIs you use every day:
#   - Google Maps API: your app sends an address, gets back coordinates
#   - Stripe API: your app sends payment info, gets back confirmation
#   - Twitter API: your app sends a query, gets back tweets
#
#
# ----- What is REST? -----
#
# REST = Representational State Transfer
#
# REST is a set of RULES for how APIs should work. A "RESTful API" follows
# these conventions:
#
# 1. Use HTTP METHODS to indicate what action you want:
#    | Method | Purpose          | Example                          |
#    |--------|------------------|----------------------------------|
#    | GET    | Read/retrieve    | GET /users → list all users      |
#    | POST   | Create new       | POST /users → create a new user  |
#    | PUT    | Update (replace) | PUT /users/5 → update user #5    |
#    | PATCH  | Update (partial) | PATCH /users/5 → change one field|
#    | DELETE | Remove           | DELETE /users/5 → delete user #5 |
#
# 2. Use URLs (endpoints) to identify RESOURCES:
#    /users, /products, /orders — these are the "nouns"
#    The HTTP method is the "verb"
#
# 3. Use HTTP STATUS CODES to indicate the result:
#    | Code | Meaning               | When to use                      |
#    |------|-----------------------|----------------------------------|
#    | 200  | OK                    | Successful GET/PUT/PATCH         |
#    | 201  | Created               | Successful POST (new resource)   |
#    | 400  | Bad Request           | Invalid input from client        |
#    | 401  | Unauthorized          | Not logged in                    |
#    | 403  | Forbidden             | Logged in but no permission      |
#    | 404  | Not Found             | Resource doesn't exist           |
#    | 500  | Internal Server Error | Bug on the server side           |
#
# 4. Send and receive data as JSON:
#    JSON = JavaScript Object Notation — looks like a Python dictionary:
#    {"username": "alice", "email": "alice@example.com"}
#
#
# ----- What is an Endpoint? -----
#
# An endpoint is a specific URL + HTTP method combination.
# Think of it as ONE specific action the API can perform.
#
#   POST /register  → this is ONE endpoint (creates a new user)
#   GET /users      → this is ANOTHER endpoint (lists all users)
#   DELETE /users/5 → this is ANOTHER endpoint (deletes user #5)
#
#
# ----- What is Flask? -----
#
# Flask is a Python FRAMEWORK for building web applications and APIs.
# A framework gives you pre-built tools so you don't start from scratch.
#
# Flask is called a "micro-framework" because it's minimal — it gives you
# just enough to handle HTTP requests and responses. You add what you need.
#
# Other Python frameworks:
#   Django  — "batteries included", bigger, more opinionated
#   FastAPI — modern, async, auto-generates API documentation
#
# Flask is the best starting point because it's simple and explicit.
#
#
# ----- What is a POST Request? -----
#
# When a client (browser, mobile app, another service) wants to CREATE
# something, it sends a POST request with data in the BODY.
#
# Example — what the client sends:
#
#   POST /register HTTP/1.1
#   Content-Type: application/json
#
#   {
#       "username": "alice",
#       "email": "alice@example.com",
#       "password": "secure123"
#   }
#
# The server receives this, processes it, and sends back a RESPONSE:
#
#   HTTP/1.1 201 Created
#   Content-Type: application/json
#
#   {
#       "message": "User registered successfully",
#       "user": {"username": "alice", "email": "alice@example.com"}
#   }
#
#
# ----- What is JSON? -----
#
# JSON is the standard format for sending data over APIs.
# It looks exactly like a Python dictionary:
#
#   Python dict:  {"name": "Alice", "age": 25}
#   JSON:         {"name": "Alice", "age": 25}
#
# Flask converts between Python dicts and JSON automatically.
#
#
# ----- What are Decorators? (used heavily in Flask) -----
#
# A decorator is a line starting with @ placed ABOVE a function.
# It WRAPS the function with extra behavior without changing the function itself.
#
# In Flask, @app.route("/register", methods=["POST"]) is a decorator that says:
#   "Register this function to handle POST requests to /register"
#
# Think of it as: sticking a label on a function that says
#   "Hey Flask, when someone visits /register, call ME!"
#
# Without the decorator, Flask wouldn't know which function to call
# when a request comes in.


# =============================================================================
# PART 2: THE CODE — User Registration API
# =============================================================================

# 're' is Python's built-in module for Regular Expressions (regex).
# Regex is a pattern-matching language for strings.
# We use it here to validate email format and check for digits in passwords.
import re

# Flask: the web framework that handles HTTP requests and responses.
# request: an object that contains the data the client sent (headers, body, URL, etc.)
# jsonify: a helper that converts a Python dict into a proper JSON HTTP response.
from flask import Flask, request, jsonify

# ----- Create the Flask application -----
# Flask(__name__) creates a new Flask app instance.
# __name__ is a special Python variable that equals "__main__" when you run the file directly.
# Flask uses it to determine the root path for finding templates and static files.
app = Flask(__name__)


# =============================================================================
# Helper Functions — Validation Logic
# =============================================================================

def is_valid_email(email: str) -> bool:
    """
    Check if the email string matches a valid email pattern.
    Returns True if valid, False if not.
    """
    # This is a REGEX (regular expression) pattern.
    # Regex is like a search template — it describes what a valid email looks like.
    #
    # Let's break down r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    #
    #   r'...'                  → "raw string" — tells Python not to interpret backslashes
    #                              (without r, you'd need \\ instead of \)
    #   ^                       → "start of string" — match must begin at the start
    #   [a-zA-Z0-9._%+-]       → a "character class" — matches any ONE of these characters:
    #                              a-z (lowercase), A-Z (uppercase), 0-9 (digits),
    #                              . _ % + - (special chars allowed in email usernames)
    #   +                       → "one or more" of the preceding character class
    #                              so [a-zA-Z0-9._%+-]+ means "one or more valid username chars"
    #   @                       → matches the literal @ symbol (every email has one)
    #   [a-zA-Z0-9.-]+         → domain name — one or more letters, digits, dots, or hyphens
    #                              e.g., "gmail", "mail.company"
    #   \.                      → matches a literal dot (\ escapes the dot because . in regex
    #                              normally means "any character")
    #   [a-zA-Z]{2,}           → top-level domain — at least 2 letters
    #                              e.g., "com", "org", "io", "co.uk"
    #   $                       → "end of string" — nothing else allowed after this
    #
    # Example matches:    alice@gmail.com ✓   bob.smith@company.co.uk ✓
    # Example non-matches: @gmail.com ✗   alice@ ✗   alice@.com ✗   alice.com ✗
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # re.match(pattern, string) tries to match the pattern against the string.
    # Returns a Match object if it matches, or None if it doesn't.
    # "is not None" converts this to True/False.
    return re.match(pattern, email) is not None


def is_valid_password(password: str) -> list[str]:
    """
    Check password strength. Returns a list of error messages.
    Empty list = password is valid.
    """
    errors = []  # start with empty list — we'll add errors as we find them

    # Check 1: minimum length
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")

    # Check 2: must contain at least one digit
    #
    # re.search(pattern, string) scans the ENTIRE string for the pattern.
    #   (unlike re.match which only checks the START of the string)
    #
    # r'\d' is a regex pattern that means "any single digit" (0-9).
    #   \d is shorthand for [0-9]
    #
    # re.search(r'\d', password) returns:
    #   - A Match object if ANY digit is found anywhere in the password
    #   - None if there are NO digits at all
    #
    # So: not re.search(r'\d', password)
    #   = not None  → True   (when no digit found → password is WEAK)
    #   = not Match → False  (when digit found → password is OK)
    #
    # Example:
    #   re.search(r'\d', "secure123") → Match (found '1') → not Match = False → no error
    #   re.search(r'\d', "abcdefgh") → None (no digit)    → not None  = True  → add error
    if not re.search(r'\d', password):
        errors.append("Password must contain at least one number")

    return errors  # empty list means all checks passed


def validate_registration(data: dict) -> list[str]:
    """
    Validate all registration fields at once.
    Collects ALL errors (not just the first one) — better user experience
    because the user can fix everything in one attempt.

    Args:
        data: the parsed JSON body from the request (a Python dict)

    Returns:
        A list of error message strings. Empty list = no errors.
    """
    errors = []

    # --- Check that all required fields exist and aren't empty ---
    required_fields = ["username", "email", "password"]
    for field in required_fields:
        # "field not in data" → the key doesn't exist in the dict at all
        #    e.g., data = {"username": "alice"}  →  "email" not in data = True
        #
        # "not data[field]" → the key exists but the value is empty/falsy
        #    e.g., data = {"email": ""}  →  not "" = True (empty string is falsy)
        #    Also catches: None, 0, False
        if field not in data or not data[field]:
            errors.append(f"'{field}' is required")

    # If required fields are missing, return early.
    # We can't validate email format if there's no email field at all!
    if errors:
        return errors

    # --- Validate username ---
    # .strip() removes leading/trailing whitespace: "  alice  " → "alice"
    username = data["username"].strip()
    if len(username) < 3:
        errors.append("Username must be at least 3 characters long")

    # --- Validate email format ---
    if not is_valid_email(data["email"]):
        errors.append("Invalid email format")

    # --- Validate password strength ---
    password_errors = is_valid_password(data["password"])
    # .extend() adds ALL items from one list into another list.
    # Unlike .append() which would add the list AS a single item:
    #   errors.append(["err1", "err2"])  → errors = [..., ["err1", "err2"]]  (nested — wrong!)
    #   errors.extend(["err1", "err2"])  → errors = [..., "err1", "err2"]     (flat — correct!)
    errors.extend(password_errors)

    return errors


# =============================================================================
# PART 3: THE ENDPOINT — POST /register
# =============================================================================

# @app.route() is a DECORATOR — it tells Flask:
#   "When someone sends a request to THIS URL with THIS method, run THIS function."
#
# @app.route("/register", methods=["POST"]) means:
#   - URL path: /register  (the full URL will be http://127.0.0.1:5000/register)
#   - Only accepts POST requests (not GET, PUT, DELETE)
#   - If someone tries GET /register, Flask automatically returns 405 Method Not Allowed
#
# The function below (register) is called a "view function" or "route handler".
# Flask calls it automatically when a matching request arrives.

@app.route("/register", methods=["POST"])
def register():
    """
    Register a new user.

    Expects JSON body:
        {
            "username": "alice",
            "email": "alice@example.com",
            "password": "secure123"
        }

    Returns:
        201: User registered successfully
        400: Validation errors
    """

    # ----- Step 1: Get the JSON data from the request -----

    # 'request' is a global Flask object — it's automatically populated with
    # the data from the incoming HTTP request (headers, body, URL params, etc.)
    # You don't create it — Flask creates it for you.
    #
    # request.get_json() does two things:
    #   1. Reads the raw body of the request (a string of JSON text)
    #   2. Parses it into a Python dictionary using json.loads() internally
    #
    # Example: if the client sent '{"username":"alice","email":"a@b.com","password":"abc123456"}'
    #   then data = {"username": "alice", "email": "a@b.com", "password": "abc123456"}
    #
    # Returns None if:
    #   - The client didn't set Content-Type: application/json
    #   - The body is not valid JSON (e.g., missing quotes, trailing commas)
    data = request.get_json()

    # Guard clause: if data is None, the request body wasn't valid JSON.
    # We return immediately with a 400 Bad Request error.
    # This prevents a crash when we try to access data["username"] on None.
    if data is None:
        # jsonify(dict) converts a Python dict to a proper HTTP response with:
        #   - Content-Type: application/json header
        #   - The dict serialized as a JSON string in the response body
        #
        # The ", 400" after jsonify() sets the HTTP status code.
        # Flask's return format: return (response_body, status_code)
        return jsonify({"error": "Request body must be valid JSON"}), 400

    # ----- Step 2: Validate the input -----
    errors = validate_registration(data)  # returns a list of error strings

    if errors:  # if the list is non-empty (has at least one error)
        return jsonify({"errors": errors}), 400  # 400 = Bad Request

    # ----- Step 3: Process the registration -----
    # In a real application, you would:
    #   1. Hash the password (NEVER store plain text passwords)
    #   2. Save the user to a database
    #   3. Send a confirmation email
    #   4. Return a session token or JWT
    #
    # For this tutorial, we just build the response data.

    # Build a user dict with cleaned data.
    # .strip() removes whitespace: "  alice  " → "alice"
    # .lower() converts to lowercase: "Alice@Gmail.COM" → "alice@gmail.com"
    # We intentionally do NOT include the password in the response (security).
    user = {
        "username": data["username"].strip(),
        "email": data["email"].strip().lower()
    }

    # ----- Step 4: Return success response -----
    # 201 = "Created" — the standard status code when a new resource is created.
    # We return the created user data so the client can confirm what was saved.
    return jsonify({
        "message": "User registered successfully",
        "user": user
    }), 201


# =============================================================================
# PART 4: HEALTH CHECK ENDPOINT — GET /health
# =============================================================================

# A health check endpoint is standard practice in production.
# Monitoring tools (like AWS CloudWatch, Datadog, Kubernetes) ping this
# endpoint every few seconds to confirm the server is running.
# If it stops responding, alerts are triggered.

@app.route("/health", methods=["GET"])
def health_check():
    # This is the simplest possible endpoint — just returns "I'm alive".
    # 200 = OK (the default status code, but we're being explicit).
    return jsonify({"status": "healthy"}), 200


# =============================================================================
# PART 5: ERROR HANDLERS — Catch unexpected errors gracefully
# =============================================================================

# These catch errors that happen ANYWHERE in the app, not just in /register.
# Without these, Flask would return HTML error pages — useless for an API client
# that expects JSON. These ensure we ALWAYS return JSON.

# @app.errorhandler(404) is a decorator that says:
# "Whenever a 404 error occurs anywhere in the app, call this function instead
#  of showing Flask's default HTML error page."
# The 'error' parameter receives the exception object (we don't use it here,
# but Flask requires the function to accept it).

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed"}), 405


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


# =============================================================================
# PART 6: RUN THE SERVER
# =============================================================================

if __name__ == "__main__":
    # __name__ == "__main__" means: "only run this block when the file is
    # executed directly (python file.py), NOT when it's imported by another file."
    # This is important because test files will import this module without
    # wanting to start the server.

    # debug=True means:
    #   1. Auto-restarts the server when you change code (hot reload)
    #   2. Shows detailed error messages in the browser/response
    #   3. NEVER use debug=True in production (security risk — exposes internals)
    #
    # port=5000 is the default Flask port.
    # After running, the server listens at: http://127.0.0.1:5000
    #
    # 127.0.0.1 = "localhost" = your own machine
    # (no one else on the internet can reach it — safe for development)

    print("=" * 60)
    print("Starting Flask server...")
    print("Server will run at: http://127.0.0.1:5000")
    print("=" * 60)
    print()
    print("Test with these curl commands in a NEW terminal:")
    print()
    print("1. Health check (should return 200):")
    print('   curl http://127.0.0.1:5000/health')
    print()
    print("2. Successful registration (should return 201):")
    print('   curl -X POST http://127.0.0.1:5000/register \\')
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"username":"alice","email":"alice@example.com","password":"secure123"}\'')
    print()
    print("3. Missing fields (should return 400):")
    print('   curl -X POST http://127.0.0.1:5000/register \\')
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"username":"alice"}\'')
    print()
    print("4. Bad email + weak password (should return 400):")
    print('   curl -X POST http://127.0.0.1:5000/register \\')
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"username":"alice","email":"not-an-email","password":"short"}\'')
    print()
    print("5. Wrong method (should return 405):")
    print('   curl http://127.0.0.1:5000/register')
    print()
    print("Press Ctrl+C to stop the server.")
    print("=" * 60)

    # app.run() starts Flask's built-in development server.
    # This is a BLOCKING call — the program stays here until you press Ctrl+C.
    # The server sits in a loop: wait for request → process → respond → repeat.
    app.run(debug=True, port=5000)


# =============================================================================
# PART 7: HOW TO TEST THIS (step by step)
# =============================================================================

# 1. Run this file:
#      python 15_API_endpoint_Python_usecase.py
#    The server starts and waits for requests.
#
# 2. Open a SECOND terminal (the first one is busy running the server).
#
# 3. Use 'curl' to send requests.
#    curl is a command-line tool that sends HTTP requests.
#    Think of it as a text-based browser.
#
#    -X POST          → use the POST method (default is GET)
#    -H "..."         → set a Header (Content-Type tells server we're sending JSON)
#    -d '{"key":"val"}'  → the Data (body) to send
#
#    # Successful registration
#    curl -X POST http://127.0.0.1:5000/register \
#      -H "Content-Type: application/json" \
#      -d '{"username":"alice","email":"alice@example.com","password":"secure123"}'
#
#    Expected response:
#    {
#      "message": "User registered successfully",
#      "user": {"email": "alice@example.com", "username": "alice"}
#    }
#
#    # Validation errors
#    curl -X POST http://127.0.0.1:5000/register \
#      -H "Content-Type: application/json" \
#      -d '{"username":"a","email":"bad","password":"short"}'
#
#    Expected response:
#    {
#      "errors": [
#        "Username must be at least 3 characters long",
#        "Invalid email format",
#        "Password must be at least 8 characters long",
#        "Password must contain at least one number"
#      ]
#    }
#
# 4. You can also test with Python (using the 'requests' library):
#
#    import requests
#    response = requests.post("http://127.0.0.1:5000/register", json={
#        "username": "alice",
#        "email": "alice@example.com",
#        "password": "secure123"
#    })
#    print(response.status_code)  # 201
#    print(response.json())       # the JSON response as a Python dict


# =============================================================================
# PART 8: WHAT'S MISSING FOR PRODUCTION? (Interview Discussion Points)
# =============================================================================

# This is a learning example. In a real production system, you'd need:
#
# 1. PASSWORD HASHING
#    NEVER store passwords as plain text.
#    Use bcrypt or argon2 to hash passwords before storing:
#      from werkzeug.security import generate_password_hash
#      hashed = generate_password_hash(password)
#    Hashing is ONE-WAY — you can verify a password against the hash,
#    but you can't reverse the hash to get the password back.
#
# 2. DATABASE
#    Store users in a real database (PostgreSQL, MySQL, MongoDB).
#    Use an ORM like SQLAlchemy to interact with it from Python:
#      db.session.add(new_user)
#      db.session.commit()
#    Our code currently doesn't persist anything — restart = data gone.
#
# 3. DUPLICATE CHECKING
#    Before creating a user, check if the email/username already exists:
#      if User.query.filter_by(email=email).first():
#          return error "Email already registered"
#
# 4. AUTHENTICATION & TOKENS
#    After registration, issue a JWT (JSON Web Token) or session token.
#    The client sends this token with every subsequent request to prove
#    they're logged in:
#      Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
#
# 5. RATE LIMITING
#    Prevent abuse — e.g., max 5 registration attempts per minute per IP.
#    Use Flask-Limiter:
#      @limiter.limit("5 per minute")
#
# 6. INPUT SANITIZATION
#    Prevent SQL injection and XSS attacks.
#    Never insert user input directly into SQL queries.
#    ORMs handle this automatically.
#
# 7. HTTPS
#    Always use HTTPS in production (encrypted communication).
#    In development, HTTP is fine (localhost only).
#
# 8. LOGGING
#    Log every request for debugging and audit trails:
#      app.logger.info(f"New registration: {username}")
#
# 9. CORS (Cross-Origin Resource Sharing)
#    If your frontend (React, etc.) is on a different domain than your API,
#    you need CORS headers. Use Flask-CORS:
#      from flask_cors import CORS
#      CORS(app)
#
# 10. ENVIRONMENT VARIABLES
#     Never hardcode secrets (database passwords, API keys) in code.
#     Use environment variables:
#       import os
#       SECRET_KEY = os.environ["SECRET_KEY"]
#
# 11. TESTING
#     Write automated tests using pytest + Flask's test client:
#       def test_register_success(client):
#           response = client.post("/register", json={...})
#           assert response.status_code == 201
#
# 12. API DOCUMENTATION
#     Use Swagger/OpenAPI to document your endpoints.
#     FastAPI generates this automatically; for Flask, use flask-restx.


# =============================================================================
# PART 9: KEY CONCEPTS SUMMARY — For Interview Reference
# =============================================================================

# ----- The Request-Response Cycle -----
#
#   Client                          Server (Flask)
#     |                                 |
#     |  POST /register                 |
#     |  {"username": "alice", ...}     |
#     | ------------------------------> |
#     |                                 |  1. Parse JSON body
#     |                                 |  2. Validate input
#     |                                 |  3. Process (save to DB)
#     |                                 |  4. Build response
#     |  201 Created                    |
#     |  {"message": "success", ...}    |
#     | <------------------------------ |
#
#
# ----- Flask Key Concepts -----
#
# | Concept            | What it does                                      |
# |--------------------|---------------------------------------------------|
# | Flask(__name__)    | Creates the app                                   |
# | @app.route()       | Maps a URL + method to a Python function          |
# | request            | Object containing the incoming request data       |
# | request.get_json() | Parses the JSON body into a Python dict           |
# | jsonify()          | Converts a Python dict to a JSON HTTP response    |
# | return ..., 201    | The second value is the HTTP status code           |
# | @app.errorhandler  | Catches specific HTTP errors globally             |
# | app.run()          | Starts the development server (blocking call)     |
#
#
# ----- HTTP Methods Cheat Sheet -----
#
# | Method | SQL Equivalent | Example                |
# |--------|----------------|------------------------|
# | GET    | SELECT         | Fetch user profile     |
# | POST   | INSERT         | Create new user        |
# | PUT    | UPDATE (full)  | Replace entire profile |
# | PATCH  | UPDATE (part)  | Change just the email  |
# | DELETE | DELETE         | Remove user account    |
#
#
# ----- Common Interview Questions About REST APIs -----
#
# Q: What's the difference between PUT and PATCH?
# A: PUT replaces the ENTIRE resource. PATCH updates only the fields you send.
#    PUT /users/5 with {"name": "Bob"} would DELETE all other fields.
#    PATCH /users/5 with {"name": "Bob"} would only change the name.
#
# Q: What's the difference between 401 and 403?
# A: 401 = "Who are you?" (not authenticated — need to log in)
#    403 = "I know who you are, but you can't do this" (not authorized)
#
# Q: Why return errors as JSON instead of plain text?
# A: The client (frontend app) needs to PARSE the response programmatically.
#    JSON is structured and easy to parse. Plain text requires string matching.
#
# Q: Why validate on the server even if the frontend validates too?
# A: Never trust the client. Anyone can bypass frontend validation by sending
#    requests directly (with curl, Postman, or a script). Server validation
#    is the ONLY validation that matters for security.
#
# Q: What is idempotency?
# A: An operation is idempotent if doing it multiple times has the same effect
#    as doing it once. GET, PUT, DELETE are idempotent. POST is NOT —
#    sending POST /register twice would try to create TWO users.


# =============================================================================
# PART 10: PRACTICE USE-CASES — Build These for Interview Prep
# =============================================================================

# Below are 4 additional API use-cases. Each one teaches a different concept.
# Try building them yourself first, then check the solution code.
# You can add these routes to the same Flask app above.


# ---------------------------------------------------------------------------
# USE-CASE 2: To-Do List API (CRUD — Create, Read, Update, Delete)
# ---------------------------------------------------------------------------
#
# This is the most common interview exercise. It tests ALL HTTP methods.
#
# Endpoints:
#   GET    /todos        → list all todos
#   POST   /todos        → create a new todo
#   PUT    /todos/<id>   → update a todo (mark complete, change title)
#   DELETE /todos/<id>   → delete a todo
#
# <id> in the URL is a PATH PARAMETER — Flask extracts it for you.
#
# CRUD <-> HTTP METHOD MENTAL MODEL:
#
#   GET /todos          ---->  [ {id:1,...}, {id:2,...} ]   Read  (list)
#   POST /todos         ---->  todos.append(new_todo)        Create
#   PUT /todos/<id>     ---->  find id, mutate fields         Update
#   DELETE /todos/<id>  ---->  remove matching id             Delete
#
#   This is the same CRUD pattern behind almost every resource-based API
#   (todos, products, users, orders...) -- once you know this shape, you
#   can guess the endpoints of most REST APIs you'll encounter.

# In-memory storage (list of dicts). In production, this would be a database.
todos = []
next_id = 1  # auto-incrementing ID


@app.route("/todos", methods=["GET"])
def get_todos():
    """Return all todos. Optionally filter by ?status=complete"""
    # request.args is a dict of URL query parameters.
    # e.g., GET /todos?status=complete → request.args = {"status": "complete"}
    # .get("status") returns the value or None if not present.
    status_filter = request.args.get("status")

    if status_filter:
        # List comprehension: filter todos where status matches
        filtered = [t for t in todos if t["status"] == status_filter]
        return jsonify(filtered), 200

    return jsonify(todos), 200


@app.route("/todos", methods=["POST"])
def create_todo():
    """Create a new todo item."""
    global next_id  # needed to modify the module-level variable inside a function

    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "'title' is required"}), 400

    # Build the new todo with an auto-generated ID and default status
    todo = {
        "id": next_id,
        "title": data["title"],
        "status": "pending"  # new todos start as pending
    }
    todos.append(todo)   # add to our in-memory list
    next_id += 1          # increment for the next todo

    return jsonify(todo), 201


@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    """
    Update a todo by its ID.

    <int:todo_id> is a URL path parameter with type conversion.
    Flask extracts the number from the URL and passes it as an integer.
    e.g., PUT /todos/3 → todo_id = 3 (int, not string)
    """
    data = request.get_json()

    # Find the todo with matching ID using a loop
    # (in production, you'd do: todo = Todo.query.get(todo_id))
    for todo in todos:
        if todo["id"] == todo_id:
            # .get("key", default) returns the value if key exists,
            # otherwise returns the default (the current value — no change)
            todo["title"] = data.get("title", todo["title"])
            todo["status"] = data.get("status", todo["status"])
            return jsonify(todo), 200

    # If we get here, no todo was found with that ID
    return jsonify({"error": f"Todo {todo_id} not found"}), 404


@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    """Delete a todo by its ID."""
    global todos  # needed because we're reassigning the list

    original_count = len(todos)
    # List comprehension that keeps everything EXCEPT the matching ID
    todos = [t for t in todos if t["id"] != todo_id]

    if len(todos) == original_count:
        # Nothing was removed — the ID didn't exist
        return jsonify({"error": f"Todo {todo_id} not found"}), 404

    # 200 with a confirmation message (some APIs use 204 No Content instead)
    return jsonify({"message": f"Todo {todo_id} deleted"}), 200

# Test commands for the To-Do API:
#   curl -X POST http://127.0.0.1:5000/todos -H "Content-Type: application/json" -d '{"title":"Buy groceries"}'
#   curl -X POST http://127.0.0.1:5000/todos -H "Content-Type: application/json" -d '{"title":"Learn Flask"}'
#   curl http://127.0.0.1:5000/todos
#   curl -X PUT http://127.0.0.1:5000/todos/1 -H "Content-Type: application/json" -d '{"status":"complete"}'
#   curl -X DELETE http://127.0.0.1:5000/todos/2
#   curl http://127.0.0.1:5000/todos


# ---------------------------------------------------------------------------
# USE-CASE 3: Calculator API (Query Parameters)
# ---------------------------------------------------------------------------
#
# This teaches a different way to pass data: URL query parameters instead of JSON body.
# Query params are key-value pairs after the ? in a URL:
#   GET /calculate?a=10&b=5&operation=add
#
# When to use query params vs JSON body:
#   Query params: for simple GET requests, filters, search
#   JSON body: for POST/PUT with complex data

@app.route("/calculate", methods=["GET"])
def calculate():
    """
    Perform arithmetic: GET /calculate?a=10&b=5&operation=add

    Supports: add, subtract, multiply, divide
    """
    # request.args.get() retrieves query parameters from the URL.
    # They always come as STRINGS, so we need to convert to float.
    a = request.args.get("a")       # string or None
    b = request.args.get("b")       # string or None
    operation = request.args.get("operation")  # string or None

    # Validate: all three parameters are required
    if not all([a, b, operation]):
        return jsonify({
            "error": "Missing parameters. Required: a, b, operation",
            "example": "/calculate?a=10&b=5&operation=add"
        }), 400

    # Convert strings to numbers. try/except handles invalid input like "abc".
    try:
        a = float(a)
        b = float(b)
    except ValueError:
        return jsonify({"error": "'a' and 'b' must be numbers"}), 400

    # Perform the calculation based on the operation
    operations = {
        "add": a + b,
        "subtract": a - b,
        "multiply": a * b,
    }

    if operation == "divide":
        if b == 0:
            return jsonify({"error": "Cannot divide by zero"}), 400
        result = a / b
    elif operation in operations:
        result = operations[operation]
    else:
        return jsonify({
            "error": f"Unknown operation: '{operation}'",
            "supported": ["add", "subtract", "multiply", "divide"]
        }), 400

    return jsonify({
        "a": a, "b": b,
        "operation": operation,
        "result": result
    }), 200

# Test commands for Calculator API:
#   curl "http://127.0.0.1:5000/calculate?a=10&b=5&operation=add"
#   curl "http://127.0.0.1:5000/calculate?a=10&b=5&operation=divide"
#   curl "http://127.0.0.1:5000/calculate?a=10&b=0&operation=divide"
#   curl "http://127.0.0.1:5000/calculate?a=hello&b=5&operation=add"


# ---------------------------------------------------------------------------
# USE-CASE 4: Login Endpoint (Authentication Pattern)
# ---------------------------------------------------------------------------
#
# This pairs with the /register endpoint. After a user registers,
# they need to LOG IN to access protected resources.
#
# In production, you'd check the password hash against the database.
# Here we use a hardcoded "database" to show the pattern.

# Simulated user database (in production: real database with hashed passwords)
fake_user_db = {
    "alice": {"email": "alice@example.com", "password_hash": "secure123"},
    "bob": {"email": "bob@example.com", "password_hash": "password456"}
}

@app.route("/login", methods=["POST"])
def login():
    """
    Authenticate a user.

    Expects JSON: {"username": "alice", "password": "secure123"}
    Returns: 200 with a (fake) token, or 401 Unauthorized
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    username = data.get("username", "").strip().lower()
    password = data.get("password", "")

    # Check if user exists
    if username not in fake_user_db:
        # SECURITY: don't say "user not found" — that tells attackers which
        # usernames exist. Use a generic message for both wrong user and wrong password.
        return jsonify({"error": "Invalid username or password"}), 401

    # Check password (in production: compare hashes, not plain text)
    user = fake_user_db[username]
    if user["password_hash"] != password:
        return jsonify({"error": "Invalid username or password"}), 401

    # Authentication successful — return a fake token
    # In production, this would be a JWT created with a secret key
    return jsonify({
        "message": "Login successful",
        "token": "fake-jwt-token-abc123",  # in production: jwt.encode(...)
        "user": {"username": username, "email": user["email"]}
    }), 200

# Test commands for Login API:
#   curl -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -d '{"username":"alice","password":"secure123"}'
#   curl -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -d '{"username":"alice","password":"wrong"}'
#   curl -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -d '{"username":"nobody","password":"abc"}'


# ---------------------------------------------------------------------------
# USE-CASE 5: Search/Filter Endpoint (Pagination)
# ---------------------------------------------------------------------------
#
# Real APIs return thousands of results. You can't send them all at once.
# PAGINATION splits results into pages: "show me page 2 of 10 items per page."
#
# This is a VERY common interview topic and production pattern.

# Simulated product catalog
products = [
    {"id": i, "name": f"Product {i}", "category": ["Electronics", "Books", "Clothing"][i % 3], "price": round(10 + i * 7.5, 2)}
    for i in range(1, 51)  # 50 products
]

@app.route("/products", methods=["GET"])
def search_products():
    """
    Search and filter products with pagination.

    Query params:
      category: filter by category (optional)
      min_price: minimum price filter (optional)
      max_price: maximum price filter (optional)
      page: page number, default 1
      per_page: items per page, default 10

    Example: GET /products?category=Books&page=1&per_page=5
    """
    # --- Get filter parameters ---
    category = request.args.get("category")
    min_price = request.args.get("min_price", type=float)  # type=float auto-converts
    max_price = request.args.get("max_price", type=float)

    # --- Get pagination parameters ---
    # type=int tells Flask to convert the string to int automatically
    # default= is used if the parameter isn't provided
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    # Clamp per_page to prevent abuse (requesting 1 million items)
    per_page = min(per_page, 50)

    # --- Apply filters ---
    # Start with all products, then narrow down
    results = products

    if category:
        results = [p for p in results if p["category"].lower() == category.lower()]
    if min_price is not None:
        results = [p for p in results if p["price"] >= min_price]
    if max_price is not None:
        results = [p for p in results if p["price"] <= max_price]

    # --- Apply pagination ---
    # Calculate which slice of the results to return
    # Page 1, per_page=10: items 0-9
    # Page 2, per_page=10: items 10-19
    #
    # PAGINATION WINDOW DIAGRAM (per_page=10, 50 total items):
    #
    #   items:  [0..9][10..19][20..29][30..39][40..49]
    #            page1  page2   page3   page4   page5
    #
    #   page=2 -> start = (2-1)*10 = 10, end = 10+10 = 20 -> slice [10:20]
    #   This is just Python list slicing applied to a "window" of the data,
    #   so the client only ever receives one page's worth of results.
    total = len(results)
    start = (page - 1) * per_page  # page 1 → start at 0, page 2 → start at 10
    end = start + per_page
    page_results = results[start:end]  # Python list slicing

    return jsonify({
        "data": page_results,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": (total + per_page - 1) // per_page  # ceiling division
        }
    }), 200

# Test commands for Search/Pagination API:
#   curl "http://127.0.0.1:5000/products"
#   curl "http://127.0.0.1:5000/products?category=Books"
#   curl "http://127.0.0.1:5000/products?min_price=50&max_price=100"
#   curl "http://127.0.0.1:5000/products?page=2&per_page=5"
#   curl "http://127.0.0.1:5000/products?category=Electronics&page=1&per_page=3"


# =============================================================================
# PART 11: PRACTICE CHALLENGES — Try These Yourself
# =============================================================================

# These are progressively harder. Build them by adding more @app.route() functions.
#
# Challenge 1 (Easy): Word Counter
#   POST /wordcount with {"text": "hello world hello"}
#   Return: {"word_count": 3, "unique_words": 2, "frequencies": {"hello": 2, "world": 1}}
#
# Challenge 2 (Medium): URL Shortener
#   POST /shorten with {"url": "https://very-long-url.com/path/to/page"}
#   Return: {"short_code": "abc123", "short_url": "http://127.0.0.1:5000/abc123"}
#   GET /abc123 → redirect to the original URL
#   Hint: use a dict to map short codes to long URLs, uuid.uuid4().hex[:6] for codes
#
# Challenge 3 (Medium): Leaderboard
#   POST /scores with {"player": "alice", "score": 150}
#   GET /leaderboard → returns top 10 players sorted by score (descending)
#   GET /leaderboard?player=alice → returns alice's rank and score
#
# Challenge 4 (Hard): Rate Limiter
#   Build middleware that limits each IP to 10 requests per minute.
#   Return 429 Too Many Requests if exceeded.
#   Hint: use a dict mapping IP → list of timestamps, check window of last 60 seconds
#   Access client IP with: request.remote_addr
