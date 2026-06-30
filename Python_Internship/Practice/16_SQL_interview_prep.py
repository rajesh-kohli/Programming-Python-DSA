"""
==============================================================================
SQL Complete Tutorial & Interview Prep — From Foundations to MAANG-Ready
==============================================================================

This file is structured as a runnable tutorial using Python's built-in
sqlite3 module — zero installation required. Every query runs, every
concept is explained, every example teaches something distinct.

Target roles:  Forward Deployed Engineer, Data Scientist, AI Engineer
Target companies: Google, Meta, Amazon, Netflix, OpenAI, Anthropic, Databricks

How to use:
  - Run the whole file:   python 16_SQL_interview_prep.py
  - Run sections in VS Code:  select a %% block → Shift+Enter
  - Read the comments — they explain WHY, not just WHAT

Table of Contents:
  SETUP:     Database creation with realistic data
  Section 1: Basic SQL (Foundations)
  Section 2: Intermediate SQL (Joins, CTEs, Subqueries)
  Section 3: Advanced SQL (Window Functions — the crown jewel)
  Section 4: System Design & Optimization (conceptual)
  Section 5: Interview-Style Problems (10 problems, increasing difficulty)
  Section 6: Platform Differences (SQLite vs PostgreSQL vs BigQuery etc.)
  Section 7: Quick Reference Card (30 essential patterns)

IMPORTANT NOTE ON SQLite vs PostgreSQL:
  Most MAANG interviews use PostgreSQL syntax. SQLite is 95% compatible
  for learning purposes. Where they differ, this file notes the
  PostgreSQL equivalent so you're ready for whiteboard interviews.
"""

# %% Imports and Helper
import sqlite3
from datetime import datetime, timedelta

# =============================================================================
# HELPER FUNCTION: run(query) — executes SQL and prints results as a table
# =============================================================================
# We use this throughout the file. It handles:
#   - SELECT queries (prints results in a formatted table)
#   - INSERT/CREATE/UPDATE/DELETE queries (executes silently)
#   - Parameter substitution (pass params as second argument)

# We keep ONE persistent connection so all sections share the same database.
conn = sqlite3.connect(":memory:")  # in-memory DB — fast, no files to clean up
cursor = conn.cursor()

def run(query, params=None, show_all=True, limit=None):
    """
    Execute a SQL query and print results in a formatted table.

    Args:
        query:    SQL string to execute
        params:   tuple of parameters for ? placeholders
        show_all: if False, only print first 10 rows
        limit:    override max rows to display
    """
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        # If query returns rows (SELECT, EXPLAIN, PRAGMA, etc.), print them
        if cursor.description:
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()

            # Determine how many rows to show
            max_rows = limit if limit else (len(rows) if show_all else 10)
            display_rows = rows[:max_rows]

            # Calculate column widths (min 4 chars, max 30 chars)
            widths = []
            for i, col in enumerate(columns):
                col_width = len(str(col))
                for row in display_rows:
                    val_width = len(str(row[i]) if row[i] is not None else "NULL")
                    col_width = max(col_width, val_width)
                widths.append(min(max(col_width, 4), 30))

            # Print header
            header = " | ".join(str(col).ljust(w) for col, w in zip(columns, widths))
            separator = "-+-".join("-" * w for w in widths)
            print(header)
            print(separator)

            # Print rows
            for row in display_rows:
                values = []
                for val, w in zip(row, widths):
                    s = str(val) if val is not None else "NULL"
                    values.append(s.ljust(w))
                print(" | ".join(values))

            # Show row count
            if len(rows) > max_rows:
                print(f"... ({len(rows) - max_rows} more rows, {len(rows)} total)")
            else:
                print(f"({len(rows)} rows)")
            print()
        else:
            conn.commit()

    except sqlite3.Error as e:
        print(f"SQL Error: {e}")
        print(f"Query: {query[:200]}")
        print()


# =============================================================================
# SETUP: Create Tables with Realistic Data
# =============================================================================
# We create 6 tables that model a realistic tech company:
#   - departments: engineering org structure
#   - employees:   people with salaries, managers, hire dates
#   - products:    things the company sells
#   - customers:   people who buy things
#   - orders:      purchase transactions
#   - user_events: product analytics / clickstream data
#
# WHY these tables? Because 90% of SQL interview questions are about:
#   - Employee/salary problems (departments + employees)
#   - Revenue/sales problems (orders + products + customers)
#   - User behavior problems (user_events)

print("=" * 78)
print("SETUP: Creating database with realistic data")
print("=" * 78)
print()

# ----- Table 1: departments -----
run("""
CREATE TABLE departments (
    id          INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    budget      REAL NOT NULL,
    location    TEXT NOT NULL
)
""")

departments_data = [
    (1, 'Engineering',    5000000,  'San Francisco'),
    (2, 'Data Science',   3000000,  'San Francisco'),
    (3, 'Product',        2500000,  'New York'),
    (4, 'Marketing',      2000000,  'New York'),
    (5, 'Sales',          3500000,  'Chicago'),
    (6, 'HR',             1500000,  'San Francisco'),
    (7, 'Finance',        1800000,  'New York'),
    (8, 'Operations',     2200000,  'Seattle'),
]

cursor.executemany("INSERT INTO departments VALUES (?, ?, ?, ?)", departments_data)
conn.commit()

# ----- Table 2: employees -----
# manager_id is a self-referencing foreign key (employee's manager is also an employee)
# This is VERY common in interviews — hierarchical data!
run("""
CREATE TABLE employees (
    id          INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    department  TEXT NOT NULL,
    salary      REAL NOT NULL,
    hire_date   TEXT NOT NULL,
    manager_id  INTEGER,
    FOREIGN KEY (manager_id) REFERENCES employees(id)
)
""")

employees_data = [
    # Engineering (dept head: Alice, id=1)
    (1,  'Alice Johnson',    'Engineering',    185000, '2019-03-15', None),
    (2,  'Bob Smith',        'Engineering',    165000, '2020-01-10', 1),
    (3,  'Carol Williams',   'Engineering',    155000, '2020-06-22', 1),
    (4,  'David Brown',      'Engineering',    145000, '2021-02-14', 2),
    (5,  'Eve Davis',        'Engineering',    170000, '2019-08-01', 1),
    (6,  'Frank Miller',     'Engineering',    140000, '2022-03-10', 2),
    (7,  'Grace Lee',        'Engineering',    150000, '2021-09-05', 5),
    # Data Science (dept head: Henry, id=8)
    (8,  'Henry Wilson',     'Data Science',   175000, '2019-05-20', None),
    (9,  'Ivy Moore',        'Data Science',   160000, '2020-11-15', 8),
    (10, 'Jack Taylor',      'Data Science',   155000, '2021-01-08', 8),
    (11, 'Karen Anderson',   'Data Science',   145000, '2021-07-19', 9),
    (12, 'Leo Thomas',       'Data Science',   165000, '2020-04-01', 8),
    # Product
    (13, 'Mia Jackson',      'Product',        160000, '2019-09-12', None),
    (14, 'Noah White',       'Product',        140000, '2021-03-25', 13),
    (15, 'Olivia Harris',    'Product',        135000, '2022-01-18', 13),
    (16, 'Paul Martin',      'Product',        145000, '2020-08-30', 13),
    # Marketing
    (17, 'Quinn Garcia',     'Marketing',      130000, '2020-02-14', None),
    (18, 'Rachel Martinez',  'Marketing',      120000, '2021-05-10', 17),
    (19, 'Sam Robinson',     'Marketing',      115000, '2022-06-01', 17),
    (20, 'Tina Clark',       'Marketing',      125000, '2021-11-20', 17),
    # Sales
    (21, 'Uma Rodriguez',    'Sales',          140000, '2019-11-05', None),
    (22, 'Victor Lewis',     'Sales',          125000, '2020-07-15', 21),
    (23, 'Wendy Walker',     'Sales',          130000, '2021-04-22', 21),
    (24, 'Xavier Hall',      'Sales',          120000, '2022-02-28', 21),
    (25, 'Yara Allen',       'Sales',          135000, '2020-10-10', 21),
    # HR
    (26, 'Zoe Young',        'HR',             110000, '2020-01-20', None),
    (27, 'Aaron King',       'HR',             100000, '2021-08-15', 26),
    (28, 'Bella Wright',     'HR',              95000, '2022-05-01', 26),
    # Finance
    (29, 'Carlos Lopez',     'Finance',        135000, '2019-12-01', None),
    (30, 'Diana Hill',       'Finance',        120000, '2021-06-10', 29),
    # Operations
    (31, 'Ethan Scott',      'Operations',     130000, '2020-03-18', None),
    (32, 'Fiona Green',      'Operations',     115000, '2021-10-25', 31),
    (33, 'George Adams',     'Operations',     125000, '2022-01-05', 31),
    (34, 'Hannah Baker',     'Operations',     118000, '2022-07-12', 31),
    (35, 'Ian Nelson',       'Engineering',    155000, '2020-09-14', 1),
]

cursor.executemany("INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?)", employees_data)
conn.commit()

# ----- Table 3: products -----
run("""
CREATE TABLE products (
    id          INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    category    TEXT NOT NULL,
    price       REAL NOT NULL,
    stock       INTEGER NOT NULL
)
""")

products_data = [
    (1,  'Laptop Pro 16',       'Electronics',   1299.99, 150),
    (2,  'Wireless Mouse',      'Electronics',     29.99, 500),
    (3,  'Mechanical Keyboard', 'Electronics',     89.99, 300),
    (4,  'USB-C Hub',           'Electronics',     49.99, 400),
    (5,  'Monitor 27"',         'Electronics',    399.99, 200),
    (6,  'Standing Desk',       'Furniture',      599.99,  80),
    (7,  'Ergonomic Chair',     'Furniture',      449.99, 120),
    (8,  'Desk Lamp',           'Furniture',       39.99, 350),
    (9,  'Notebook Pack',       'Office',           9.99, 1000),
    (10, 'Pen Set',             'Office',           5.99, 800),
    (11, 'Webcam HD',           'Electronics',     79.99, 250),
    (12, 'Headphones',          'Electronics',    199.99, 180),
    (13, 'Phone Stand',         'Accessories',     19.99, 600),
    (14, 'Cable Organizer',     'Accessories',     14.99, 450),
    (15, 'Backpack',            'Accessories',     69.99, 220),
]

cursor.executemany("INSERT INTO products VALUES (?, ?, ?, ?, ?)", products_data)
conn.commit()

# ----- Table 4: customers -----
run("""
CREATE TABLE customers (
    id          INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    email       TEXT NOT NULL,
    city        TEXT NOT NULL,
    signup_date TEXT NOT NULL,
    tier        TEXT NOT NULL
)
""")

customers_data = [
    (1,  'John Doe',       'john@email.com',      'San Francisco', '2023-01-15', 'Gold'),
    (2,  'Jane Smith',     'jane@email.com',       'New York',      '2023-02-20', 'Silver'),
    (3,  'Mike Brown',     'mike@email.com',       'Chicago',       '2023-01-10', 'Gold'),
    (4,  'Sara Wilson',    'sara@email.com',       'Los Angeles',   '2023-03-05', 'Bronze'),
    (5,  'Tom Davis',      'tom@email.com',        'Seattle',       '2023-02-14', 'Silver'),
    (6,  'Lisa Anderson',  'lisa@email.com',       'San Francisco', '2023-04-01', 'Gold'),
    (7,  'James Taylor',   'james@email.com',      'New York',      '2023-01-22', 'Bronze'),
    (8,  'Emma Thomas',    'emma@email.com',       'Chicago',       '2023-05-10', 'Silver'),
    (9,  'Chris Jackson',  'chris@email.com',      'Los Angeles',   '2023-03-18', 'Gold'),
    (10, 'Amy White',      'amy@email.com',        'Seattle',       '2023-06-01', 'Bronze'),
    (11, 'Ryan Harris',    'ryan@email.com',       'San Francisco', '2023-04-15', 'Silver'),
    (12, 'Megan Martin',   'megan@email.com',      'New York',      '2023-07-20', 'Gold'),
    (13, 'Daniel Garcia',  'daniel@email.com',     'Chicago',       '2023-02-28', 'Silver'),
    (14, 'Sophia Martinez','sophia@email.com',     'Los Angeles',   '2023-08-05', 'Bronze'),
    (15, 'Kevin Robinson', 'kevin@email.com',      'Seattle',       '2023-05-25', 'Gold'),
    (16, 'Laura Clark',    'laura@email.com',      'San Francisco', '2023-01-05', 'Silver'),
    (17, 'Brian Lewis',    'brian@email.com',      'New York',      '2023-09-10', 'Bronze'),
    (18, 'Nicole Walker',  'nicole@email.com',     'Chicago',       '2023-06-15', 'Gold'),
    (19, 'Alex Hall',      'alex@email.com',       'Los Angeles',   '2023-03-30', 'Silver'),
    (20, 'Olivia Allen',   'olivia@email.com',     'Seattle',       '2023-10-01', 'Bronze'),
]

cursor.executemany("INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?)", customers_data)
conn.commit()

# ----- Table 5: orders -----
# Realistic order data spanning Jan 2024 - June 2024
run("""
CREATE TABLE orders (
    id          INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    product_id  INTEGER NOT NULL,
    quantity    INTEGER NOT NULL,
    order_date  TEXT NOT NULL,
    amount      REAL NOT NULL,
    status      TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
)
""")

orders_data = [
    (1,  1,  1,  1, '2024-01-05', 1299.99, 'completed'),
    (2,  1,  2,  2, '2024-01-05',   59.98, 'completed'),
    (3,  2,  5,  1, '2024-01-12',  399.99, 'completed'),
    (4,  3,  7,  1, '2024-01-15',  449.99, 'completed'),
    (5,  4,  9,  5, '2024-01-20',   49.95, 'completed'),
    (6,  5, 12,  1, '2024-01-25',  199.99, 'completed'),
    (7,  6,  3,  1, '2024-02-01',   89.99, 'completed'),
    (8,  7, 10,  3, '2024-02-05',   17.97, 'completed'),
    (9,  8,  6,  1, '2024-02-10',  599.99, 'completed'),
    (10, 9,  1,  1, '2024-02-14', 1299.99, 'completed'),
    (11, 10, 4,  2, '2024-02-18',   99.98, 'completed'),
    (12, 1,  3,  1, '2024-02-22',   89.99, 'completed'),
    (13, 2, 11,  1, '2024-02-28',   79.99, 'completed'),
    (14, 3,  8,  2, '2024-03-02',   79.98, 'completed'),
    (15, 11, 1,  1, '2024-03-05', 1299.99, 'completed'),
    (16, 12, 5,  1, '2024-03-08',  399.99, 'completed'),
    (17, 13, 7,  1, '2024-03-12',  449.99, 'shipped'),
    (18, 4, 12,  1, '2024-03-15',  199.99, 'completed'),
    (19, 5,  2,  3, '2024-03-18',   89.97, 'completed'),
    (20, 6, 15,  1, '2024-03-22',   69.99, 'completed'),
    (21, 14, 6,  1, '2024-03-25',  599.99, 'shipped'),
    (22, 15, 3,  2, '2024-03-28',  179.98, 'completed'),
    (23, 1, 12,  1, '2024-04-01',  199.99, 'completed'),
    (24, 7, 14,  4, '2024-04-05',   59.96, 'completed'),
    (25, 8,  1,  1, '2024-04-08', 1299.99, 'completed'),
    (26, 16, 5,  2, '2024-04-10',  799.98, 'completed'),
    (27, 9,  4,  1, '2024-04-14',   49.99, 'returned'),
    (28, 10, 7,  1, '2024-04-18',  449.99, 'completed'),
    (29, 17, 9,  10,'2024-04-20',   99.90, 'completed'),
    (30, 18, 11, 1, '2024-04-22',   79.99, 'completed'),
    (31, 2, 13,  2, '2024-04-25',   39.98, 'completed'),
    (32, 3,  1,  1, '2024-05-01', 1299.99, 'completed'),
    (33, 19, 6,  1, '2024-05-05',  599.99, 'shipped'),
    (34, 11, 2,  1, '2024-05-08',   29.99, 'completed'),
    (35, 12, 8,  3, '2024-05-10',  119.97, 'completed'),
    (36, 20, 15, 2, '2024-05-12',  139.98, 'completed'),
    (37, 4, 3,   1, '2024-05-15',   89.99, 'returned'),
    (38, 5, 1,   1, '2024-05-18', 1299.99, 'completed'),
    (39, 13, 4,  2, '2024-05-20',   99.98, 'completed'),
    (40, 6, 12,  1, '2024-05-22',  199.99, 'completed'),
    (41, 15, 5,  1, '2024-05-25',  399.99, 'completed'),
    (42, 1, 7,   1, '2024-06-01',  449.99, 'shipped'),
    (43, 8, 14,  2, '2024-06-05',   29.98, 'completed'),
    (44, 16, 1,  1, '2024-06-08', 1299.99, 'completed'),
    (45, 9, 3,   1, '2024-06-10',   89.99, 'completed'),
    (46, 18, 2,  2, '2024-06-12',   59.98, 'completed'),
    (47, 3, 6,   1, '2024-06-15',  599.99, 'completed'),
    (48, 11, 12, 1, '2024-06-18',  199.99, 'completed'),
    (49, 20, 9,  3, '2024-06-20',   29.97, 'pending'),
    (50, 7, 5,   1, '2024-06-25',  399.99, 'pending'),
]

cursor.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?)", orders_data)
conn.commit()

# ----- Table 6: user_events (clickstream / analytics data) -----
# This simulates product analytics data — the kind Data Scientists at
# Netflix, Spotify, or Meta analyze daily.
run("""
CREATE TABLE user_events (
    id               INTEGER PRIMARY KEY,
    user_id          INTEGER NOT NULL,
    event_type       TEXT NOT NULL,
    event_date       TEXT NOT NULL,
    duration_seconds INTEGER
)
""")

# Generate event data: logins, page_views, purchases, signups, searches
events_data = [
    # User 1: very active user
    (1,  1, 'login',     '2024-01-01', None),
    (2,  1, 'page_view', '2024-01-01', 45),
    (3,  1, 'search',    '2024-01-01', 12),
    (4,  1, 'purchase',  '2024-01-01', 120),
    (5,  1, 'login',     '2024-01-02', None),
    (6,  1, 'page_view', '2024-01-02', 30),
    (7,  1, 'login',     '2024-01-03', None),
    (8,  1, 'page_view', '2024-01-03', 60),
    (9,  1, 'purchase',  '2024-01-03', 90),
    (10, 1, 'login',     '2024-01-04', None),
    (11, 1, 'login',     '2024-01-05', None),
    # User 1 gap: skips Jan 6-7
    (12, 1, 'login',     '2024-01-08', None),
    (13, 1, 'page_view', '2024-01-08', 55),
    # User 2: moderate user
    (14, 2, 'login',     '2024-01-01', None),
    (15, 2, 'page_view', '2024-01-01', 20),
    (16, 2, 'login',     '2024-01-03', None),
    (17, 2, 'search',    '2024-01-03', 15),
    (18, 2, 'login',     '2024-01-05', None),
    (19, 2, 'page_view', '2024-01-05', 35),
    (20, 2, 'purchase',  '2024-01-05', 100),
    (21, 2, 'login',     '2024-01-06', None),
    (22, 2, 'login',     '2024-01-07', None),
    (23, 2, 'page_view', '2024-01-07', 40),
    # User 3: light user
    (24, 3, 'login',     '2024-01-02', None),
    (25, 3, 'page_view', '2024-01-02', 10),
    (26, 3, 'login',     '2024-01-10', None),
    (27, 3, 'search',    '2024-01-10', 8),
    (28, 3, 'login',     '2024-01-20', None),
    # User 4: churned user (signed up but barely used)
    (29, 4, 'login',     '2024-01-01', None),
    (30, 4, 'page_view', '2024-01-01', 5),
    # User 5: power user with purchases
    (31, 5, 'login',     '2024-01-01', None),
    (32, 5, 'page_view', '2024-01-01', 90),
    (33, 5, 'search',    '2024-01-01', 25),
    (34, 5, 'purchase',  '2024-01-01', 150),
    (35, 5, 'login',     '2024-01-02', None),
    (36, 5, 'page_view', '2024-01-02', 80),
    (37, 5, 'purchase',  '2024-01-02', 200),
    (38, 5, 'login',     '2024-01-03', None),
    (39, 5, 'login',     '2024-01-04', None),
    (40, 5, 'page_view', '2024-01-04', 70),
    # User 6-10: various patterns for analytics queries
    (41, 6, 'login',     '2024-01-05', None),
    (42, 6, 'page_view', '2024-01-05', 25),
    (43, 6, 'login',     '2024-01-06', None),
    (44, 7, 'login',     '2024-01-01', None),
    (45, 7, 'page_view', '2024-01-01', 15),
    (46, 7, 'search',    '2024-01-01', 10),
    (47, 7, 'login',     '2024-01-02', None),
    (48, 7, 'purchase',  '2024-01-02', 80),
    (49, 8, 'login',     '2024-01-03', None),
    (50, 8, 'page_view', '2024-01-03', 50),
    (51, 8, 'login',     '2024-01-04', None),
    (52, 8, 'search',    '2024-01-04', 20),
    (53, 9, 'login',     '2024-01-01', None),
    (54, 9, 'login',     '2024-01-02', None),
    (55, 9, 'page_view', '2024-01-02', 65),
    (56, 9, 'purchase',  '2024-01-02', 110),
    (57, 10,'login',     '2024-01-07', None),
    (58, 10,'page_view', '2024-01-07', 30),
    (59, 10,'login',     '2024-01-08', None),
    (60, 10,'page_view', '2024-01-08', 45),
]

cursor.executemany("INSERT INTO user_events VALUES (?, ?, ?, ?, ?)", events_data)
conn.commit()

print("Tables created. Let's verify:")
run("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
print("Row counts:")
for table in ['departments', 'employees', 'products', 'customers', 'orders', 'user_events']:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    print(f"  {table}: {cursor.fetchone()[0]} rows")
print()


# %% SECTION 1: Basic SQL (Foundations)
# =============================================================================
# SECTION 1: BASIC SQL — Foundations
# =============================================================================
# If you know nothing else, know THIS section cold.
# Every SQL interview starts here before going deeper.

print("=" * 78)
print("SECTION 1: BASIC SQL (Foundations)")
print("=" * 78)
print()

# ----- SELECT: Retrieve data from a table -----
# SELECT is the bread and butter. You'll use it in every single query.
# Think of it as: "Show me these columns from this table"

print("--- SELECT: Basic column selection ---")
# Select specific columns (ALWAYS prefer this over SELECT *)
# WHY: SELECT * is a code smell in production — it fetches unnecessary data,
# breaks when schema changes, and is slower for wide tables.
run("SELECT name, department, salary FROM employees LIMIT 5")

# ----- WHERE: Filter rows -----
# WHERE is your filter — it keeps only rows that match the condition.
# Think of it as: "Show me rows WHERE this condition is true"

print("--- WHERE: Filter by condition ---")
run("SELECT name, department, salary FROM employees WHERE department = 'Engineering'")

# ----- AND / OR: Combine conditions -----
# AND = both must be true (narrows results)
# OR  = either can be true (widens results)
# Use parentheses to control evaluation order!

print("--- AND/OR: Combine filters ---")
run("""
SELECT name, department, salary
FROM employees
WHERE department = 'Engineering'
  AND salary > 150000
""")

# Parentheses matter! Without them, AND binds before OR.
# This query: Engineering over 150k, OR anyone in Data Science
print("--- Parentheses in WHERE ---")
run("""
SELECT name, department, salary
FROM employees
WHERE (department = 'Engineering' AND salary > 150000)
   OR department = 'Data Science'
""")

# ----- IN: Match any value in a list -----
# IN is shorthand for multiple OR conditions.
# WHERE department IN ('A', 'B') is same as WHERE department = 'A' OR department = 'B'

print("--- IN: Match from a list ---")
run("""
SELECT name, department, salary
FROM employees
WHERE department IN ('Engineering', 'Data Science', 'Product')
ORDER BY salary DESC
LIMIT 5
""")

# ----- BETWEEN: Range check (inclusive on both ends!) -----
# BETWEEN is inclusive: BETWEEN 100000 AND 150000 includes both 100000 and 150000
# This trips people up in interviews — remember it's inclusive!

print("--- BETWEEN: Inclusive range filter ---")
run("""
SELECT name, department, salary
FROM employees
WHERE salary BETWEEN 140000 AND 160000
ORDER BY salary DESC
""")

# ----- LIKE: Pattern matching -----
# % = zero or more characters (wildcard)
# _ = exactly one character
# LIKE is case-sensitive in SQLite! (PostgreSQL has ILIKE for case-insensitive)

print("--- LIKE: Pattern matching ---")
# Names starting with 'A'
run("SELECT name FROM employees WHERE name LIKE 'A%'")

# Names with 'son' anywhere
print("--- LIKE: Contains pattern ---")
run("SELECT name FROM employees WHERE name LIKE '%son%'")

# ----- GROUP BY: Aggregate rows into groups -----
# GROUP BY collapses rows that share a value into a single summary row.
# CRITICAL RULE: Every column in SELECT must be either:
#   1. In the GROUP BY clause, OR
#   2. Inside an aggregate function (COUNT, SUM, AVG, MIN, MAX)
# Violating this rule is the #1 GROUP BY mistake in interviews.
#
# Visual - rows get sorted into buckets, then each bucket collapses to one row:
#
#   employees                    buckets (GROUP BY department)      result
#   +-------+------+            +----------------------------+
#   | Alice | Eng  | --+        | Eng:  [Alice, Bob, Carol]   | --> | Eng  | 3 | 133k |
#   | Bob   | Eng  | --+------> +----------------------------+
#   | Carol | Eng  | --+        | DS:   [Dave, Eve]           | --> | DS   | 2 | 120k |
#   | Dave  | DS   | --+------> +----------------------------+
#   | Eve   | DS   | --+
#   +-------+------+
#   5 rows in  -->  2 buckets  -->  2 rows out (one per group)

print("--- GROUP BY: Aggregate by department ---")
run("""
SELECT department,
       COUNT(*) as employee_count,
       ROUND(AVG(salary), 2) as avg_salary,
       MIN(salary) as min_salary,
       MAX(salary) as max_salary
FROM employees
GROUP BY department
ORDER BY avg_salary DESC
""")

# ----- HAVING: Filter groups (not rows) -----
# WHERE filters rows BEFORE grouping.
# HAVING filters groups AFTER grouping.
# INTERVIEW TIP: If asked "What's the difference between WHERE and HAVING?"
#   - WHERE filters individual rows before GROUP BY runs
#   - HAVING filters aggregated groups after GROUP BY runs
#   - You can't use aggregate functions in WHERE!

print("--- HAVING: Filter aggregated groups ---")
# Show only departments with avg salary > 130000
run("""
SELECT department,
       COUNT(*) as employee_count,
       ROUND(AVG(salary), 2) as avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > 130000
ORDER BY avg_salary DESC
""")

# ----- ORDER BY: Sort results -----
# ASC  = ascending (default, smallest first)
# DESC = descending (largest first)
# You can sort by multiple columns — it sorts by the first, then breaks ties with the second.

print("--- ORDER BY: Sort results ---")
run("""
SELECT name, department, salary
FROM employees
ORDER BY department ASC, salary DESC
LIMIT 10
""")

# ----- LIMIT / OFFSET: Pagination -----
# LIMIT N:          return only N rows
# OFFSET M:         skip the first M rows
# Together:         LIMIT N OFFSET M = skip M, then return N
# NOTE: PostgreSQL uses LIMIT/OFFSET. Oracle uses FETCH FIRST N ROWS ONLY.

print("--- LIMIT / OFFSET: Pagination ---")
# Page 2 (rows 6-10), assuming 5 per page
run("""
SELECT name, salary
FROM employees
ORDER BY salary DESC
LIMIT 5 OFFSET 5
""")

# ----- Aggregate functions: COUNT, SUM, AVG, MIN, MAX -----
# These are your statistical toolkit in SQL.
# COUNT(*) counts all rows, COUNT(column) counts non-NULL values.
# This distinction matters for columns with NULLs!

print("--- Aggregate Functions ---")
run("""
SELECT
    COUNT(*)           as total_employees,
    COUNT(manager_id)  as has_manager,
    SUM(salary)        as total_payroll,
    ROUND(AVG(salary), 2) as avg_salary,
    MIN(salary)        as lowest_salary,
    MAX(salary)        as highest_salary
FROM employees
""")

# ----- DISTINCT: Remove duplicate values -----
# DISTINCT removes duplicate rows from the result set.
# COUNT(DISTINCT column) counts unique values — very useful for analytics.

print("--- DISTINCT: Unique values ---")
run("SELECT DISTINCT department FROM employees ORDER BY department")

print("--- COUNT vs COUNT(DISTINCT) ---")
run("""
SELECT
    COUNT(city)          as total_entries,
    COUNT(DISTINCT city) as unique_cities
FROM customers
""")

# ----- NULL Handling: IS NULL, IS NOT NULL, COALESCE -----
# NULL is NOT a value — it means "unknown" or "missing".
# You CANNOT compare with = or !=. You MUST use IS NULL / IS NOT NULL.
# NULL = NULL is NOT true! (it evaluates to NULL, which is falsy)
#
# COALESCE(a, b, c) returns the first non-NULL argument.
# This is your go-to for providing default values.

print("--- NULL Handling ---")
# Find employees without a manager (department heads)
run("""
SELECT name, department, manager_id
FROM employees
WHERE manager_id IS NULL
""")

# Use COALESCE to replace NULL with a default
print("--- COALESCE: Replace NULL with default ---")
run("""
SELECT name,
       COALESCE(manager_id, 0) as manager_id_or_zero,
       COALESCE(CAST(manager_id AS TEXT), 'No Manager') as manager_label
FROM employees
WHERE manager_id IS NULL
""")

# ----- INNER JOIN: Combine rows from two tables -----
# JOIN connects rows from two tables based on a related column.
# INNER JOIN: only rows that match in BOTH tables (the default).
# Think of it as a Venn diagram — only the intersection.
#
# Visual - two circles, only the overlap survives:
#
#        employees              departments
#       /-----------\          /-----------\
#      /   Eng       \        /   Eng       \
#      |   DS    *****|******|***** DS      |
#      |   HR      *  |  INNER  *   Legal    |
#       \   Mktg     /  JOIN     \  Sales    /
#        \-----------/          \-----------/
#                       ^^^^^^^^
#                  only rows present
#                  in BOTH tables survive

print("--- INNER JOIN: Combine employees with departments ---")
run("""
SELECT e.name, e.department, d.budget, d.location
FROM employees e
INNER JOIN departments d ON e.department = d.name
ORDER BY d.budget DESC
LIMIT 8
""")

# ----- LEFT JOIN: Keep all rows from the left table -----
# LEFT JOIN: all rows from the LEFT table, matched rows from the RIGHT table.
# If no match exists in the right table, you get NULLs for right table columns.
# This is used constantly in analytics to preserve all base records.
#
# Visual - every LEFT row survives; unmatched RIGHT columns become NULL:
#
#   customers (LEFT)         orders (RIGHT)            LEFT JOIN result
#   +----+-------+           +----+-------------+      +-------+---------+
#   | id | name  |           | id | customer_id |      | name  | order   |
#   +----+-------+           +----+-------------+      +-------+---------+
#   | 1  | Alice | <-------- | 9  | 1           | ----> | Alice | 9       |
#   | 2  | Bob   |  no match +----+-------------+       | Bob   | NULL    |
#   +----+-------+                                      +-------+---------+
#   ALL rows from customers kept, even Bob who has no matching order.

print("--- LEFT JOIN: Keep all customers, even those without orders ---")
run("""
SELECT c.name, c.tier, COUNT(o.id) as order_count
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name, c.tier
ORDER BY order_count DESC
""")

# ----- CROSS JOIN: Every combination of rows -----
# CROSS JOIN produces the Cartesian product — every row in table A
# paired with every row in table B. Rarely used, but shows up in
# interviews for generating "all possible combinations."
# If A has 10 rows and B has 5 rows, CROSS JOIN gives 50 rows.

print("--- CROSS JOIN: All combinations (useful for generating date grids) ---")
run("""
SELECT d.name as department, t.tier
FROM departments d
CROSS JOIN (SELECT DISTINCT tier FROM customers) t
ORDER BY d.name, t.tier
LIMIT 12
""")

# ----- CAST(): Type conversion -----
# CAST converts data from one type to another.
# Common conversions: TEXT to INTEGER, REAL to INTEGER, etc.
# In PostgreSQL: you can also use :: syntax (e.g., salary::integer)

print("--- CAST: Type conversion ---")
run("""
SELECT name,
       salary,
       CAST(salary AS INTEGER) as salary_int,
       CAST(salary / 12 AS INTEGER) as monthly_int
FROM employees
LIMIT 5
""")


# %% SECTION 2: Intermediate SQL
# =============================================================================
# SECTION 2: INTERMEDIATE SQL
# =============================================================================
# This is where you separate yourself from beginners. Interviewers expect
# Data Scientists and FDEs to be fluent with everything in this section.

print()
print("=" * 78)
print("SECTION 2: INTERMEDIATE SQL")
print("=" * 78)
print()

# ----- LEFT JOIN revisited: Find unmatched rows -----
# The "anti-join" pattern: LEFT JOIN + WHERE right_table.id IS NULL
# finds rows in the left table with NO match in the right table.
# This is a classic interview pattern!

print("--- Anti-Join: Customers who never ordered ---")
# Which customers have never placed an order?
run("""
SELECT c.name, c.tier, c.signup_date
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.id IS NULL
""")
# If no rows returned, all customers have orders. That's OK — the pattern
# is what matters. In interviews, you'll use this constantly.

# ----- FULL OUTER JOIN workaround in SQLite -----
# SQLite does NOT support FULL OUTER JOIN directly.
# PostgreSQL does: SELECT * FROM A FULL OUTER JOIN B ON A.id = B.id
#
# The workaround uses UNION of LEFT JOINs in both directions.
# FULL OUTER JOIN = "keep ALL rows from BOTH tables, NULL where no match"
#
# Visual - two circles, EVERYTHING is kept, gaps filled with NULL:
#
#        team_a                  team_b
#       /-----------\           /-----------\
#      / Alice       \         /             \
#      |          ****|*******|****           |
#      |   Bob    *  matched *   Dave          |
#      |   Carol  *  (both)  *   Eve           |
#       \           /         \               /
#        \-----------/         \-----------/
#   Alice -> (NULL)        Bob -> Bob       Dave -> (NULL)
#                           Carol -> Carol                Eve -> (NULL)
#   left-only rows | matched rows (both sides) | right-only rows

print("--- FULL OUTER JOIN (SQLite workaround using UNION) ---")
# Let's create two small temp tables to demonstrate
run("CREATE TABLE team_a (name TEXT)")
run("CREATE TABLE team_b (name TEXT)")
run("INSERT INTO team_a VALUES ('Alice'), ('Bob'), ('Carol')")
run("INSERT INTO team_b VALUES ('Bob'), ('Carol'), ('Dave'), ('Eve')")

# This simulates FULL OUTER JOIN:
run("""
SELECT a.name as team_a, b.name as team_b
FROM team_a a
LEFT JOIN team_b b ON a.name = b.name

UNION

SELECT a.name as team_a, b.name as team_b
FROM team_b b
LEFT JOIN team_a a ON a.name = b.name
""")
# Notice: Alice (only in A), Dave/Eve (only in B), Bob/Carol (in both)

# Clean up temp tables
run("DROP TABLE team_a")
run("DROP TABLE team_b")

# ----- UNION, UNION ALL, INTERSECT, EXCEPT -----
# These are SET operations — they combine results from multiple queries.
#
# UNION:     combine results, remove duplicates (slower — has to deduplicate)
# UNION ALL: combine results, keep duplicates (faster — no deduplication)
# INTERSECT: only rows that appear in BOTH result sets
# EXCEPT:    rows in the first set that are NOT in the second set
#
# Rules:
#   1. Both queries must have the same number of columns
#   2. Corresponding columns must have compatible types
#   3. Column names come from the FIRST query

print("--- UNION vs UNION ALL ---")
# UNION removes duplicates
run("""
SELECT city FROM customers WHERE tier = 'Gold'
UNION
SELECT city FROM customers WHERE tier = 'Silver'
""")

# UNION ALL keeps duplicates (notice repeated cities)
print("--- UNION ALL (keeps duplicates) ---")
run("""
SELECT city FROM customers WHERE tier = 'Gold'
UNION ALL
SELECT city FROM customers WHERE tier = 'Silver'
""")

print("--- INTERSECT: Cities that have BOTH Gold and Silver customers ---")
run("""
SELECT city FROM customers WHERE tier = 'Gold'
INTERSECT
SELECT city FROM customers WHERE tier = 'Silver'
""")

print("--- EXCEPT: Cities with Gold customers but NO Bronze customers ---")
run("""
SELECT city FROM customers WHERE tier = 'Gold'
EXCEPT
SELECT city FROM customers WHERE tier = 'Bronze'
""")

# ----- CASE WHEN: Conditional logic inside SQL -----
# CASE WHEN is the SQL equivalent of if/elif/else.
# It's used for:
#   1. Bucketing continuous values into categories
#   2. Creating binary flags (1/0) for aggregation
#   3. Pivoting data (turning rows into columns)
# This is one of the MOST IMPORTANT constructs in interviews.

print("--- CASE WHEN: Salary bucketing ---")
# Bucket employees into salary tiers
run("""
SELECT name, salary,
    CASE
        WHEN salary >= 170000 THEN 'Senior'
        WHEN salary >= 140000 THEN 'Mid-Level'
        WHEN salary >= 110000 THEN 'Junior'
        ELSE 'Entry'
    END as salary_tier
FROM employees
ORDER BY salary DESC
LIMIT 10
""")

# CASE WHEN for aggregation (creating pivot-like summaries)
print("--- CASE WHEN: Conditional aggregation (pivot-like) ---")
run("""
SELECT department,
    COUNT(*) as total,
    SUM(CASE WHEN salary >= 150000 THEN 1 ELSE 0 END) as high_earners,
    SUM(CASE WHEN salary < 120000 THEN 1 ELSE 0 END) as below_120k,
    ROUND(
        100.0 * SUM(CASE WHEN salary >= 150000 THEN 1 ELSE 0 END) / COUNT(*),
        1
    ) as pct_high_earners
FROM employees
GROUP BY department
ORDER BY pct_high_earners DESC
""")

# CASE WHEN for feature engineering (useful for ML pipelines)
print("--- CASE WHEN: Feature engineering for ML ---")
run("""
SELECT name, hire_date,
    CASE
        WHEN julianday('now') - julianday(hire_date) > 365 * 4 THEN 'veteran'
        WHEN julianday('now') - julianday(hire_date) > 365 * 2 THEN 'experienced'
        ELSE 'new_hire'
    END as tenure_bucket,
    ROUND((julianday('now') - julianday(hire_date)) / 365.25, 1) as years_tenure
FROM employees
ORDER BY hire_date
LIMIT 8
""")

# ----- String Functions -----
# String manipulation comes up in data cleaning questions.
# SQLite supports most standard string functions.

print("--- String Functions ---")
run("""
SELECT
    name,
    UPPER(name) as upper_name,
    LOWER(name) as lower_name,
    LENGTH(name) as name_length,
    SUBSTR(name, 1, 5) as first_five,
    REPLACE(name, ' ', '_') as underscored
FROM employees
LIMIT 5
""")

# String concatenation: || in SQLite/PostgreSQL, CONCAT() in MySQL
print("--- String Concatenation (|| operator) ---")
run("""
SELECT
    name || ' (' || department || ')' as employee_info,
    '$' || CAST(CAST(salary AS INTEGER) AS TEXT) as formatted_salary
FROM employees
LIMIT 5
""")

# TRIM removes whitespace (or specified characters)
print("--- TRIM ---")
run("SELECT TRIM('   hello world   ') as trimmed")

# ----- Date Functions -----
# Date handling is one of the BIGGEST differences between SQL dialects.
# SQLite stores dates as TEXT in 'YYYY-MM-DD' format.
# strftime() is SQLite's Swiss Army knife for date manipulation.
#
# PostgreSQL equivalents (what you'll use in interviews):
#   SQLite: strftime('%Y', date)     → PostgreSQL: EXTRACT(YEAR FROM date)
#   SQLite: strftime('%m', date)     → PostgreSQL: EXTRACT(MONTH FROM date)
#   SQLite: DATE(date, '+30 days')   → PostgreSQL: date + INTERVAL '30 days'
#   SQLite: no DATE_TRUNC            → PostgreSQL: DATE_TRUNC('month', date)

print("--- Date Functions (SQLite strftime) ---")
run("""
SELECT
    order_date,
    strftime('%Y', order_date)    as year,
    strftime('%m', order_date)    as month,
    strftime('%Y-%m', order_date) as year_month,
    strftime('%w', order_date)    as day_of_week,
    DATE(order_date, '+30 days')  as plus_30_days,
    -- Days since order (like DATEDIFF in SQL Server)
    CAST(julianday('2024-06-30') - julianday(order_date) AS INTEGER) as days_ago
FROM orders
WHERE customer_id = 1
ORDER BY order_date
""")

# Date arithmetic for cohort analysis
print("--- Date Arithmetic: Months since signup ---")
run("""
SELECT
    name, signup_date,
    -- Months since signup (approximate, for grouping into cohorts)
    (strftime('%Y', '2024-06-30') - strftime('%Y', signup_date)) * 12
    + (strftime('%m', '2024-06-30') - strftime('%m', signup_date)) as months_since_signup
FROM customers
ORDER BY signup_date
LIMIT 10
""")

# ----- COALESCE and NULLIF -----
# COALESCE(a, b, c): returns the first non-NULL value
# NULLIF(a, b): returns NULL if a = b, otherwise returns a
# NULLIF is useful to avoid division by zero errors!

print("--- COALESCE: First non-NULL value ---")
run("""
SELECT
    event_type,
    duration_seconds,
    COALESCE(duration_seconds, 0) as duration_or_zero,
    COALESCE(CAST(duration_seconds AS TEXT), 'N/A') as duration_or_na
FROM user_events
WHERE user_id = 1
LIMIT 6
""")

print("--- NULLIF: Prevent division by zero ---")
# NULLIF returns NULL if both arguments are equal
# Dividing by NULL gives NULL instead of an error
run("""
SELECT
    department,
    COUNT(*) as total,
    SUM(CASE WHEN salary > 150000 THEN 1 ELSE 0 END) as high_earners,
    -- Without NULLIF, this would error if high_earners is 0
    ROUND(
        SUM(salary) * 1.0 /
        NULLIF(SUM(CASE WHEN salary > 150000 THEN 1 ELSE 0 END), 0),
        2
    ) as avg_salary_if_high
FROM employees
GROUP BY department
""")

# ----- Subqueries -----
# A subquery is a query nested inside another query.
# Three types:
#   1. Scalar subquery (returns single value) — used in WHERE or SELECT
#   2. Table subquery (returns rows) — used in FROM (becomes a "derived table")
#   3. Correlated subquery — references the outer query (runs once per outer row)
#
# Correlated subqueries are POWERFUL but SLOW — each outer row triggers
# the inner query. Prefer JOINs or CTEs when possible.
#
# Visual - the inner query runs first, its result feeds the outer query:
#
#   inner query                    outer query
#   +---------------------+        +--------------------------------+
#   | SELECT AVG(salary)  |        | SELECT name, salary             |
#   | FROM employees      | -----> | FROM employees                  |
#   +---------------------+ 125000 | WHERE salary > (125000)         |
#         runs first              +--------------------------------+
#                                          runs second, using that value

print("--- Scalar Subquery: Employees earning above average ---")
run("""
SELECT name, department, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees)
ORDER BY salary DESC
""")

print("--- Table Subquery (Derived Table): Department stats ---")
run("""
SELECT dept_stats.department, dept_stats.avg_salary, dept_stats.headcount
FROM (
    SELECT department,
           ROUND(AVG(salary), 2) as avg_salary,
           COUNT(*) as headcount
    FROM employees
    GROUP BY department
) dept_stats
WHERE dept_stats.headcount >= 4
ORDER BY dept_stats.avg_salary DESC
""")

print("--- Correlated Subquery: Employees earning above their department avg ---")
# For each employee, the subquery calculates THAT employee's department average.
# This runs the subquery once per employee row — which is why it's slow at scale.
run("""
SELECT e.name, e.department, e.salary,
    (SELECT ROUND(AVG(e2.salary), 2)
     FROM employees e2
     WHERE e2.department = e.department) as dept_avg
FROM employees e
WHERE e.salary > (
    SELECT AVG(e2.salary)
    FROM employees e2
    WHERE e2.department = e.department
)
ORDER BY e.department, e.salary DESC
""")

# ----- CTEs: Common Table Expressions (WITH clause) -----
# CTEs are named, reusable subqueries defined at the top of your query.
# They make complex queries MUCH more readable — think of them as
# "temporary named result sets."
#
# WHY CTEs matter in interviews:
#   - They show you can decompose complex problems
#   - Interviewers prefer CTEs over deeply nested subqueries
#   - They're easier to debug (test each CTE independently)
#   - Some problems REQUIRE CTEs (like recursive queries)
#
# Visual - each CTE is a named building block; later steps reuse earlier ones:
#
#   WITH dept_stats AS ( ... )      Step 1: build dept_stats
#        |
#        v
#        company_avg AS ( ... )     Step 2: build company_avg
#        |         |
#        v         v
#   SELECT ... FROM dept_stats CROSS JOIN company_avg   Step 3: final query
#
#   Compare to nested subqueries: everything crammed into one unreadable
#   blob. CTEs name each intermediate result so the query reads top to bottom.

print("--- CTE: Clean, readable multi-step query ---")
run("""
WITH dept_stats AS (
    -- Step 1: Calculate department-level statistics
    SELECT department,
           ROUND(AVG(salary), 2) as avg_salary,
           COUNT(*) as headcount,
           SUM(salary) as total_payroll
    FROM employees
    GROUP BY department
),
company_avg AS (
    -- Step 2: Calculate company-wide average
    SELECT ROUND(AVG(salary), 2) as company_avg_salary
    FROM employees
)
-- Step 3: Compare each department to the company average
SELECT ds.department,
       ds.headcount,
       ds.avg_salary,
       ca.company_avg_salary,
       ROUND(ds.avg_salary - ca.company_avg_salary, 2) as diff_from_avg,
       CASE
           WHEN ds.avg_salary > ca.company_avg_salary THEN 'Above Average'
           ELSE 'Below Average'
       END as status
FROM dept_stats ds
CROSS JOIN company_avg ca
ORDER BY ds.avg_salary DESC
""")

# ----- EXISTS and NOT EXISTS -----
# EXISTS checks if a subquery returns ANY rows. It's a boolean test.
# EXISTS is often faster than IN for large datasets because:
#   - EXISTS stops as soon as it finds the first match
#   - IN must evaluate the entire subquery first
#
# INTERVIEW TIP: Use EXISTS when checking "does a related row exist?"
#                 Use IN when matching against a small list of values.

print("--- EXISTS: Customers who HAVE placed orders ---")
run("""
SELECT c.name, c.tier
FROM customers c
WHERE EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.customer_id = c.id
)
LIMIT 10
""")
# Note: SELECT 1 is conventional — EXISTS only checks if rows exist,
# it doesn't care what columns you select.

print("--- NOT EXISTS: Departments with no employees earning > 170k ---")
run("""
SELECT d.name, d.budget
FROM departments d
WHERE NOT EXISTS (
    SELECT 1
    FROM employees e
    WHERE e.department = d.name
      AND e.salary > 170000
)
""")


# %% SECTION 3: Advanced SQL (Window Functions)
# =============================================================================
# SECTION 3: ADVANCED SQL — Window Functions
# =============================================================================
#
# Window functions are THE most important advanced SQL topic for MAANG
# interviews. They come up in nearly every Data Science and FDE interview
# at Google, Meta, Netflix, and Databricks.
#
# WHAT IS A WINDOW FUNCTION?
# -------------------------
# A window function performs a calculation across a SET of rows that are
# somehow related to the current row. That "set of rows" is the "window."
#
# KEY INSIGHT: Unlike GROUP BY, window functions DO NOT collapse rows.
# Each row keeps its identity — the window function just adds a new column.
#
# Think of it like this:
#   GROUP BY:         10 rows → 3 groups → 3 rows (collapsed)
#   Window function:  10 rows → 10 rows (each with an extra calculated column)
#
# SYNTAX:
#   function_name() OVER (
#       PARTITION BY column    -- optional: divide rows into groups
#       ORDER BY column        -- optional: define order within each group
#       frame_clause           -- optional: define which rows to include
#   )
#
# PARTITION BY vs GROUP BY:
#   GROUP BY:     SELECT dept, AVG(salary) → one row per dept (collapsed)
#   PARTITION BY: AVG(salary) OVER(PARTITION BY dept) → every row gets the avg
#
# Visual example with 6 employees in 2 departments:
#
#   name    | dept | salary | GROUP BY avg | OVER(PARTITION BY dept) avg
#   --------|------|--------|------------- |----------------------------
#   Alice   | Eng  | 150k   |             | 133k  (avg of Eng: 150+130+120)
#   Bob     | Eng  | 130k   |   → 133k    | 133k
#   Carol   | Eng  | 120k   |             | 133k
#   Dave    | DS   | 140k   |             | 120k  (avg of DS: 140+100)
#   Eve     | DS   | 100k   |   → 120k    | 120k
#
#   GROUP BY produces 2 rows. Window function produces 5 rows (all original rows kept).

print()
print("=" * 78)
print("SECTION 3: ADVANCED SQL (Window Functions)")
print("=" * 78)
print()

# ----- ROW_NUMBER(): Assign sequential numbers -----
# ROW_NUMBER() gives each row a unique number within its partition.
# If there are ties, it arbitrarily assigns different numbers.
# Common uses:
#   - "Find the top N per group" (the most common window function interview Q)
#   - Deduplication (keep row_number = 1, delete the rest)

print("--- ROW_NUMBER(): Rank employees within each department ---")
run("""
SELECT
    name,
    department,
    salary,
    ROW_NUMBER() OVER (
        PARTITION BY department
        ORDER BY salary DESC
    ) as salary_rank
FROM employees
ORDER BY department, salary_rank
""")

# The classic "Top N per group" pattern:
# INTERVIEW FAVORITE: "Find the highest-paid employee in each department"
print("--- ROW_NUMBER(): Top 2 earners per department ---")
run("""
WITH ranked AS (
    SELECT
        name, department, salary,
        ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rn
    FROM employees
)
SELECT name, department, salary
FROM ranked
WHERE rn <= 2
ORDER BY department, salary DESC
""")

# ----- RANK() vs DENSE_RANK() -----
# RANK():       tied values get the same rank, but it SKIPS the next number
# DENSE_RANK(): tied values get the same rank, DOES NOT skip
#
# Example with salaries [300, 300, 200, 100]:
#   RANK():       1, 1, 3, 4  (skips 2 because two items tied at 1)
#   DENSE_RANK(): 1, 1, 2, 3  (no gap — next unique value gets 2)
#   ROW_NUMBER(): 1, 2, 3, 4  (always unique, ties broken arbitrarily)
#
# INTERVIEW TIP: Interviewers love asking "What's the difference between
# RANK, DENSE_RANK, and ROW_NUMBER?" Make sure you can explain with an example.

print("--- RANK() vs DENSE_RANK() vs ROW_NUMBER() ---")
# Let's look at a case where there are ties
run("""
SELECT
    name, department, salary,
    ROW_NUMBER() OVER (ORDER BY salary DESC) as row_num,
    RANK()       OVER (ORDER BY salary DESC) as rank,
    DENSE_RANK() OVER (ORDER BY salary DESC) as dense_rank
FROM employees
ORDER BY salary DESC
LIMIT 15
""")
# Notice: when two employees have the same salary:
#   ROW_NUMBER: gives them different numbers (1, 2)
#   RANK: gives them the same number, skips next (1, 1, 3)
#   DENSE_RANK: gives them the same number, no skip (1, 1, 2)

# ----- LAG() and LEAD(): Access previous/next rows -----
# LAG(column, N):  value of column N rows BEFORE current row
# LEAD(column, N): value of column N rows AFTER current row
#
# These are essential for:
#   - Month-over-month growth
#   - Time between events
#   - Session analysis
#   - Detecting changes

print("--- LAG(): Month-over-month revenue ---")
run("""
WITH monthly_revenue AS (
    SELECT
        strftime('%Y-%m', order_date) as month,
        ROUND(SUM(amount), 2) as revenue
    FROM orders
    WHERE status != 'returned'
    GROUP BY strftime('%Y-%m', order_date)
)
SELECT
    month,
    revenue,
    LAG(revenue, 1) OVER (ORDER BY month) as prev_month_revenue,
    ROUND(
        (revenue - LAG(revenue, 1) OVER (ORDER BY month))
        / LAG(revenue, 1) OVER (ORDER BY month) * 100,
        1
    ) as mom_growth_pct
FROM monthly_revenue
ORDER BY month
""")

print("--- LEAD(): Time between consecutive events ---")
# How many days between each login for user 1?
run("""
SELECT
    user_id,
    event_date,
    LEAD(event_date, 1) OVER (
        PARTITION BY user_id
        ORDER BY event_date
    ) as next_event_date,
    CAST(
        julianday(LEAD(event_date, 1) OVER (
            PARTITION BY user_id ORDER BY event_date
        )) - julianday(event_date)
        AS INTEGER
    ) as days_until_next
FROM user_events
WHERE user_id = 1 AND event_type = 'login'
ORDER BY event_date
""")

# ----- SUM() OVER(): Running / Cumulative totals -----
# SUM(amount) OVER (ORDER BY date) gives a running total.
# This is the cumulative sum — each row includes the sum of all
# previous rows plus the current row.
#
# Without PARTITION BY: running total across ALL rows.
# With PARTITION BY: running total resets for each partition.

print("--- SUM() OVER(): Running total of revenue ---")
run("""
WITH monthly_revenue AS (
    SELECT
        strftime('%Y-%m', order_date) as month,
        ROUND(SUM(amount), 2) as revenue
    FROM orders
    WHERE status != 'returned'
    GROUP BY strftime('%Y-%m', order_date)
)
SELECT
    month,
    revenue,
    ROUND(SUM(revenue) OVER (ORDER BY month), 2) as cumulative_revenue
FROM monthly_revenue
ORDER BY month
""")

print("--- SUM() OVER(): Running total per customer ---")
run("""
SELECT
    customer_id,
    order_date,
    amount,
    ROUND(
        SUM(amount) OVER (
            PARTITION BY customer_id
            ORDER BY order_date
        ),
        2
    ) as customer_running_total
FROM orders
WHERE customer_id IN (1, 2, 3)
ORDER BY customer_id, order_date
""")

# ----- AVG() OVER(ROWS BETWEEN): Moving averages -----
# A moving average smooths out fluctuations in data.
# The ROWS BETWEEN clause defines the "window frame" — which rows
# relative to the current row should be included in the calculation.
#
# ROWS BETWEEN 2 PRECEDING AND CURRENT ROW = 3-row moving average
# (2 rows before + current row)
#
# Frame specifications:
#   UNBOUNDED PRECEDING: from the very first row of the partition
#   N PRECEDING:         N rows before current
#   CURRENT ROW:         the current row itself
#   N FOLLOWING:         N rows after current
#   UNBOUNDED FOLLOWING: to the very last row of the partition
#
# Default frame (when ORDER BY is specified): RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
# This means SUM() OVER(ORDER BY x) gives you a cumulative sum by default!
#
# Visual - the frame SLIDES along the ordered rows (3-row moving avg, "2 PRECEDING"):
#
#   month:    Jan    Feb    Mar    Apr    May
#   revenue:  100    120    140    90     110
#
#   row=Mar  [ 100    120  [ 140 ] ]                 avg(100,120,140) -> Mar
#   row=Apr           [ 120  [140    90 ] ]           avg(120,140, 90) -> Apr
#   row=May                  [ 140  [90  110] ]       avg(140, 90,110) -> May
#                                     ^^^^^^^ frame moves forward one row each time
#
#   Unlike GROUP BY (which collapses rows into buckets), the window frame
#   slides row-by-row and every original row survives in the output.

print("--- AVG() OVER(): 3-month moving average ---")
run("""
WITH monthly_revenue AS (
    SELECT
        strftime('%Y-%m', order_date) as month,
        ROUND(SUM(amount), 2) as revenue
    FROM orders
    WHERE status != 'returned'
    GROUP BY strftime('%Y-%m', order_date)
)
SELECT
    month,
    revenue,
    ROUND(
        AVG(revenue) OVER (
            ORDER BY month
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ),
        2
    ) as moving_avg_3m
FROM monthly_revenue
ORDER BY month
""")

# ----- FIRST_VALUE(), LAST_VALUE() -----
# FIRST_VALUE(column): value of column in the first row of the window
# LAST_VALUE(column):  value of column in the last row of the window
#
# GOTCHA with LAST_VALUE: The default frame is RANGE BETWEEN UNBOUNDED
# PRECEDING AND CURRENT ROW, which means LAST_VALUE returns the current
# row's value! You usually need to specify ROWS BETWEEN UNBOUNDED
# PRECEDING AND UNBOUNDED FOLLOWING.

print("--- FIRST_VALUE / LAST_VALUE ---")
run("""
SELECT
    name, department, salary,
    FIRST_VALUE(name) OVER (
        PARTITION BY department
        ORDER BY salary DESC
    ) as highest_paid_in_dept,
    LAST_VALUE(name) OVER (
        PARTITION BY department
        ORDER BY salary DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) as lowest_paid_in_dept
FROM employees
WHERE department IN ('Engineering', 'Data Science')
ORDER BY department, salary DESC
""")

# ----- NTILE(): Divide rows into N buckets -----
# NTILE(N) divides the ordered rows into N roughly equal groups.
# NTILE(4) = quartiles, NTILE(100) = percentiles
# Useful for: percentile analysis, A/B test group assignment, fairness

print("--- NTILE(): Salary quartiles ---")
run("""
SELECT
    name, department, salary,
    NTILE(4) OVER (ORDER BY salary) as salary_quartile,
    CASE NTILE(4) OVER (ORDER BY salary)
        WHEN 1 THEN 'Bottom 25%'
        WHEN 2 THEN '25-50%'
        WHEN 3 THEN '50-75%'
        WHEN 4 THEN 'Top 25%'
    END as quartile_label
FROM employees
ORDER BY salary
""")

# ----- Advanced Frame Specification -----
# Let's see different frames in action
print("--- Frame Specifications: Visual comparison ---")
run("""
WITH monthly_revenue AS (
    SELECT
        strftime('%Y-%m', order_date) as month,
        ROUND(SUM(amount), 2) as revenue
    FROM orders
    WHERE status != 'returned'
    GROUP BY strftime('%Y-%m', order_date)
)
SELECT
    month,
    revenue,
    -- Cumulative sum from the beginning (default with ORDER BY)
    ROUND(SUM(revenue) OVER (
        ORDER BY month
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ), 2) as cum_sum,
    -- 2-month trailing window (current + 1 preceding)
    ROUND(SUM(revenue) OVER (
        ORDER BY month
        ROWS BETWEEN 1 PRECEDING AND CURRENT ROW
    ), 2) as trailing_2m,
    -- Centered 3-month window (1 before + current + 1 after)
    ROUND(AVG(revenue) OVER (
        ORDER BY month
        ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
    ), 2) as centered_avg_3m
FROM monthly_revenue
ORDER BY month
""")

# ----- ROLLUP, CUBE, GROUPING SETS (PostgreSQL only — conceptual) -----
# These are PostgreSQL/SQL Server features for multi-level aggregation.
# SQLite does NOT support them, but they appear in interviews.
#
# ROLLUP: Creates subtotals + grand total
#   GROUP BY ROLLUP(department, tier)
#   Produces:  (department, tier), (department, NULL), (NULL, NULL)
#   → Individual groups, department subtotals, and a grand total
#
# CUBE: Creates ALL possible subtotal combinations
#   GROUP BY CUBE(department, tier)
#   Produces:  (department, tier), (department, NULL), (NULL, tier), (NULL, NULL)
#   → Every possible aggregation level
#
# GROUPING SETS: Specify exactly which groupings you want
#   GROUP BY GROUPING SETS ((department), (tier), ())
#   → Only the specific aggregations you list
#
# INTERVIEW ANSWER: "ROLLUP is hierarchical (like a subtotal report),
# CUBE gives all combinations, GROUPING SETS gives you full control."

print("--- ROLLUP / CUBE / GROUPING SETS (conceptual — PostgreSQL only) ---")
print("""
These are NOT supported in SQLite but frequently asked about in interviews.

  -- ROLLUP: subtotals per department + grand total
  SELECT department, tier, SUM(salary)
  FROM employees_ext
  GROUP BY ROLLUP(department, tier);

  -- Result:
  -- Engineering | Senior | 350000
  -- Engineering | Junior | 140000
  -- Engineering | NULL   | 490000   ← department subtotal
  -- Data Science| Senior | 175000
  -- Data Science| NULL   | 320000   ← department subtotal
  -- NULL        | NULL   | 810000   ← grand total

  -- CUBE: all combinations
  GROUP BY CUBE(department, tier)  -- adds (NULL, Senior), (NULL, Junior) etc.

  -- GROUPING SETS: custom combinations
  GROUP BY GROUPING SETS ((department), (tier), ())
""")


# %% SECTION 4: System Design & Optimization
# =============================================================================
# SECTION 4: SYSTEM DESIGN & OPTIMIZATION
# =============================================================================
#
# This section covers concepts that come up in system design rounds and
# performance-focused SQL questions. You can't always demo these in SQLite,
# but understanding them is critical for senior-level interviews.

print()
print("=" * 78)
print("SECTION 4: SYSTEM DESIGN & OPTIMIZATION")
print("=" * 78)
print()

# ----- EXPLAIN QUERY PLAN -----
# EXPLAIN shows HOW the database engine will execute your query.
# In interviews, you should be able to read a query plan and identify:
#   - Full table scans (SCAN TABLE — bad for large tables)
#   - Index usage (SEARCH TABLE USING INDEX — good)
#   - Join order and type

print("--- EXPLAIN QUERY PLAN ---")
run("EXPLAIN QUERY PLAN SELECT * FROM employees WHERE department = 'Engineering'")

# Let's create an index and see the difference
run("CREATE INDEX idx_emp_dept ON employees(department)")
print("--- After creating index on department ---")
run("EXPLAIN QUERY PLAN SELECT * FROM employees WHERE department = 'Engineering'")

# Composite index (multi-column)
run("CREATE INDEX idx_emp_dept_salary ON employees(department, salary)")
print("--- Composite index: department + salary ---")
run("""
EXPLAIN QUERY PLAN
SELECT * FROM employees
WHERE department = 'Engineering' AND salary > 150000
""")

# ----- Indexing Concepts -----
print("--- Indexing Concepts (Conceptual) ---")
print("""
B-TREE INDEXES (default in most databases)
==========================================
A B-tree index is a sorted data structure that allows O(log n) lookups.
Think of it like the index in the back of a textbook — instead of reading
every page, you jump straight to the right section.

Visual - without an index vs with a B-tree index:

  WITHOUT INDEX (full table scan, O(n)):
    [row1][row2][row3][row4] ... [row N]   <- must check every single row
     scan  scan  scan  scan        scan

  WITH B-TREE INDEX (O(log n)):
                  [ M ]                 <- start at root, compare
                 /     \\
            [ D ]       [ T ]           <- branch left/right, narrowing down
           /    \\       /    \\
        [B]    [F]   [Q]    [W]         <- a few hops reach the target row
                       ^
                  found it — no need to touch unrelated rows

WHEN TO CREATE AN INDEX:
  - Columns frequently used in WHERE clauses
  - Columns used in JOIN conditions
  - Columns used in ORDER BY (avoids sorting at query time)
  - Foreign keys (almost always worth indexing)

WHEN NOT TO INDEX:
  - Tables with very few rows (full scan is faster)
  - Columns with very low cardinality (e.g., boolean — only 2 values)
  - Columns that are frequently updated (indexes slow down writes)
  - Wide columns like TEXT/BLOB

COMPOSITE (MULTI-COLUMN) INDEXES:
  CREATE INDEX idx ON orders(customer_id, order_date);

  Rule: the LEFTMOST PREFIX must be used for the index to be effective.
  This index works for:
    WHERE customer_id = 5                     ✓ (uses leftmost column)
    WHERE customer_id = 5 AND order_date > X  ✓ (uses both columns)
  This index does NOT help:
    WHERE order_date > '2024-01-01'           ✗ (skips leftmost column)

COVERING INDEX:
  An index that includes ALL columns the query needs.
  The database can answer the query from the index alone without
  touching the actual table ("index-only scan").

  CREATE INDEX idx ON orders(customer_id, order_date, amount);
  SELECT order_date, amount FROM orders WHERE customer_id = 5;
  -- All needed columns are in the index → no table lookup!
""")

# ----- Partitioning Strategies -----
print("--- Partitioning Strategies (Conceptual) ---")
print("""
PARTITIONING: Splitting a large table into smaller physical pieces.
The database can then scan only the relevant partitions, skipping the rest.

TYPES OF PARTITIONING:

1. RANGE PARTITIONING (most common)
   Partition by date ranges — ideal for time-series data.
   Example: orders_2024_q1, orders_2024_q2, etc.
   Query WHERE order_date = '2024-03-15' → scans only Q1 partition.

2. HASH PARTITIONING
   Partition by hash of a column value — distributes data evenly.
   Good for: user_id-based partitioning when you want even distribution.
   Bad for: range queries (hash values aren't sequential).

3. LIST PARTITIONING
   Partition by explicit list of values.
   Example: partition by region: ('US', 'EU', 'APAC').
   Each query specifying region scans only that partition.

INTERVIEW TIP: When asked "How would you optimize a slow query on a
billion-row table?", partitioning by date is usually the right first answer.
""")

# ----- OLAP vs OLTP -----
print("--- OLAP vs OLTP ---")
print("""
OLTP (Online Transaction Processing)
=====================================
  Purpose:   Handle individual transactions (inserts, updates, deletes)
  Examples:  User registration, placing an order, updating a profile
  Databases: PostgreSQL, MySQL, SQLite
  Pattern:   Many small, fast queries touching a few rows each
  Schema:    Normalized (3NF) — minimize redundancy
  Indexing:  Indexes on primary keys, foreign keys, lookup columns
  Users:     Application backends, APIs

OLAP (Online Analytical Processing)
====================================
  Purpose:   Analyze large datasets for business intelligence
  Examples:  "What was total revenue by region last quarter?"
  Databases: BigQuery, Snowflake, Redshift, Databricks
  Pattern:   Few large queries scanning millions/billions of rows
  Schema:    Denormalized — star schema / snowflake schema
  Storage:   Column-oriented (only reads needed columns)
  Users:     Data analysts, data scientists, business stakeholders

KEY INSIGHT FOR INTERVIEWS:
  If they ask about building a dashboard or analytics query → think OLAP.
  If they ask about handling user requests in real-time → think OLTP.
  Modern data stacks: OLTP source → ETL pipeline → OLAP warehouse.
""")

# ----- Row-Oriented vs Column-Oriented Storage -----
print("--- Row-Oriented vs Column-Oriented Storage ---")
print("""
ROW-ORIENTED (PostgreSQL, MySQL, SQLite)
========================================
  Data is stored row by row on disk:
  [Alice, Eng, 150k] [Bob, Eng, 130k] [Carol, DS, 140k]

  Fast for: SELECT * FROM users WHERE id = 42  (one row, all columns)
  Slow for: SELECT AVG(salary) FROM users      (needs to read every row)

COLUMN-ORIENTED (BigQuery, Redshift, Snowflake, ClickHouse)
============================================================
  Data is stored column by column on disk:
  Names:    [Alice, Bob, Carol, ...]
  Depts:    [Eng, Eng, DS, ...]
  Salaries: [150k, 130k, 140k, ...]

  Fast for: SELECT AVG(salary) FROM users   (reads only salary column)
  Slow for: SELECT * FROM users WHERE id=42 (must assemble from many columns)

  Additional benefits of columnar storage:
  - COMPRESSION: same-type values in a column compress extremely well
                (e.g., run-length encoding for repeated department names)
  - VECTORIZED EXECUTION: modern CPUs can process arrays of same-type values
                          much faster than mixed-type rows

THIS IS WHY BigQuery can scan 1TB in seconds — it only reads the columns
you actually need, and those columns are heavily compressed.
""")

# ----- Join Algorithms -----
print("--- Join Algorithms (How Databases Execute JOINs) ---")
print("""
1. NESTED LOOP JOIN
   For each row in table A, scan ALL rows in table B.
   Complexity: O(n * m)
   Best when: one table is very small, or there's an index on the join column.
   Think: two nested for loops.

2. HASH JOIN
   Build a hash table from the smaller table, then probe it with the larger table.
   Complexity: O(n + m)
   Best when: joining two large tables with equality conditions (=).
   Most common join algorithm in modern databases.

3. MERGE JOIN (Sort-Merge Join)
   Sort both tables by the join column, then merge them like merge sort.
   Complexity: O(n log n + m log m) for sorting, O(n + m) for merging.
   Best when: both tables are already sorted (e.g., by a clustered index).
   Required for: inequality joins, range joins.

INTERVIEW TIP: When asked "Why is this JOIN slow?", think about:
  1. Is there an index on the join column? (If not: nested loop → add index)
  2. Are both tables large? (hash join is best for large-large equi-joins)
  3. Is it an inequality join? (can't use hash join — needs merge or nested loop)
""")

# ----- Common Performance Anti-Patterns -----
print("--- Common Performance Anti-Patterns ---")
print("""
1. SELECT * (never in production)
   - Reads unnecessary columns → more I/O, more network transfer
   - Breaks when schema changes (new columns appear unexpectedly)
   - Prevents covering index optimization
   Fix: explicitly list only the columns you need.

2. FUNCTIONS ON INDEXED COLUMNS
   BAD:  WHERE YEAR(order_date) = 2024
         (can't use index — function applied to every row)
   GOOD: WHERE order_date >= '2024-01-01' AND order_date < '2025-01-01'
         (range scan on index — much faster)

3. CORRELATED SUBQUERIES
   BAD:  SELECT *, (SELECT AVG(salary) FROM emp e2 WHERE e2.dept = e1.dept)
         (runs inner query once per outer row)
   GOOD: Use a CTE or JOIN with a pre-aggregated table.

4. NOT IN WITH NULLS
   WHERE id NOT IN (SELECT manager_id FROM employees)
   If manager_id has ANY NULL values, the entire NOT IN returns no rows!
   Fix: Use NOT EXISTS instead, or filter NULLs: NOT IN (SELECT ... WHERE x IS NOT NULL)

5. ORDER BY + LIMIT WITHOUT INDEX
   SELECT * FROM orders ORDER BY created_at DESC LIMIT 10;
   Without an index on created_at, the DB must sort ALL rows, then return 10.
   With an index: it just reads the last 10 entries from the index.

6. IMPLICIT TYPE CONVERSION
   WHERE varchar_column = 12345
   The DB may convert every row's varchar to int for comparison → full scan.
   Fix: WHERE varchar_column = '12345'
""")

# ----- Write vs Read Optimization Tradeoffs -----
print("--- Write vs Read Optimization Tradeoffs ---")
print("""
Every optimization decision in databases is a tradeoff between reads and writes.

MORE INDEXES:
  + Faster reads (lookups, joins, sorts)
  - Slower writes (every INSERT/UPDATE/DELETE must update all indexes)
  - More storage space

DENORMALIZATION:
  + Faster reads (no joins needed — data is pre-joined)
  - Slower writes (must update data in multiple places)
  - Risk of data inconsistency (same data stored twice)

MATERIALIZED VIEWS:
  + Instant reads (pre-computed results)
  - Must be refreshed (stale data between refreshes)
  - Storage cost

RULE OF THUMB:
  Read-heavy workloads (analytics, dashboards): optimize for reads
  Write-heavy workloads (logging, IoT): minimize indexes, use append-only patterns
  Mixed workloads: separate OLTP (writes) from OLAP (reads) with a data pipeline
""")


# %% SECTION 5: Interview-Style Problems
# =============================================================================
# SECTION 5: INTERVIEW-STYLE PROBLEMS
# =============================================================================
# 10 problems, increasing difficulty. Each has:
#   - Problem statement (what an interviewer would say)
#   - Company/role context
#   - Hints
#   - Solution with detailed explanation

print()
print("=" * 78)
print("SECTION 5: INTERVIEW-STYLE PROBLEMS (10 Problems)")
print("=" * 78)
print()

# -------------------------------------------------------------------------
# PROBLEM 1: Find Duplicate Records
# -------------------------------------------------------------------------
print("=" * 60)
print("PROBLEM 1: Find Duplicate Records")
print("=" * 60)
print("""
PROBLEM:  Find all products that have been ordered by the same customer
          more than once. Show the customer, product, and number of orders.

COMPANY:  Amazon, Google (Data Analyst / Data Scientist)
ROLE:     This is a warm-up question — should take 2-3 minutes.
          Tests: GROUP BY, HAVING, JOIN

HINTS:
  - GROUP BY customer_id AND product_id
  - Use HAVING to filter groups with count > 1
  - JOIN to get human-readable names
""")

print("SOLUTION:")
run("""
SELECT
    c.name as customer,
    p.name as product,
    COUNT(*) as times_ordered,
    ROUND(SUM(o.amount), 2) as total_spent
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN products p ON o.product_id = p.id
GROUP BY o.customer_id, o.product_id
HAVING COUNT(*) > 1
ORDER BY times_ordered DESC
""")
print("EXPLANATION: GROUP BY (customer_id, product_id) creates a group for")
print("each unique customer-product pair. HAVING COUNT(*) > 1 keeps only")
print("the pairs where the customer ordered that product more than once.")
print()

# -------------------------------------------------------------------------
# PROBLEM 2: Second Highest Salary per Department
# -------------------------------------------------------------------------
print("=" * 60)
print("PROBLEM 2: Second Highest Salary per Department")
print("=" * 60)
print("""
PROBLEM:  For each department, find the employee with the SECOND highest
          salary. If a department has fewer than 2 employees, exclude it.

COMPANY:  Meta, Google, Amazon (all levels)
ROLE:     Classic interview question — tests window functions.

HINTS:
  - Use DENSE_RANK() instead of ROW_NUMBER() to handle ties correctly
  - CTE + filter pattern: rank in CTE, filter in outer query
  - Think about edge cases: what if two people tie for #1?
""")

print("SOLUTION:")
run("""
WITH ranked AS (
    SELECT
        name,
        department,
        salary,
        DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) as salary_rank
    FROM employees
)
SELECT name, department, salary, salary_rank
FROM ranked
WHERE salary_rank = 2
ORDER BY department
""")
print("EXPLANATION: DENSE_RANK() handles ties correctly. If two employees")
print("tie for #1, the next employee gets rank 2 (not 3 like RANK() would give).")
print("We use PARTITION BY department to rank within each department separately.")
print()

# -------------------------------------------------------------------------
# PROBLEM 3: Consecutive Login Days (Gaps and Islands)
# -------------------------------------------------------------------------
print("=" * 60)
print("PROBLEM 3: Consecutive Login Days (Gaps and Islands)")
print("=" * 60)
print("""
PROBLEM:  Find the longest streak of consecutive login days for each user.

COMPANY:  Netflix, Spotify, Meta (Data Science / Analytics)
ROLE:     This is a HARD problem. The "gaps and islands" technique is one of
          the most advanced SQL patterns tested in interviews.

HINTS:
  - Get distinct login dates per user
  - Use ROW_NUMBER() to assign sequential numbers
  - Subtract ROW_NUMBER from the date — consecutive dates produce the same value!
  - Group by that "island ID" to find streak lengths
""")

print("SOLUTION:")
run("""
WITH login_dates AS (
    -- Step 1: Get distinct login dates per user
    SELECT DISTINCT user_id, event_date
    FROM user_events
    WHERE event_type = 'login'
),
with_rn AS (
    -- Step 2: Assign row numbers ordered by date within each user
    SELECT
        user_id,
        event_date,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_date) as rn
    FROM login_dates
),
with_island AS (
    -- Step 3: The key insight!
    -- For consecutive dates, (date - row_number) gives the same value.
    -- Example:
    --   Jan 1 (rn=1): 1 - 1 = 0  → island "Dec 31"
    --   Jan 2 (rn=2): 2 - 2 = 0  → island "Dec 31" (SAME! → consecutive)
    --   Jan 3 (rn=3): 3 - 3 = 0  → island "Dec 31" (SAME! → consecutive)
    --   Jan 5 (rn=4): 5 - 4 = 1  → island "Jan 1"  (DIFFERENT → new streak)
    SELECT
        user_id,
        event_date,
        DATE(event_date, '-' || rn || ' days') as island_id
    FROM with_rn
),
streaks AS (
    -- Step 4: Group by island to find streak length and dates
    SELECT
        user_id,
        MIN(event_date) as streak_start,
        MAX(event_date) as streak_end,
        COUNT(*) as streak_length
    FROM with_island
    GROUP BY user_id, island_id
)
-- Step 5: Find the longest streak per user
SELECT
    user_id,
    streak_start,
    streak_end,
    streak_length as consecutive_days
FROM streaks
WHERE (user_id, streak_length) IN (
    SELECT user_id, MAX(streak_length)
    FROM streaks
    GROUP BY user_id
)
ORDER BY consecutive_days DESC
""")
print("EXPLANATION: The gaps-and-islands technique uses the difference between")
print("a row's date and its row number. For consecutive dates, this difference")
print("is constant — creating an 'island ID'. Non-consecutive dates break the")
print("pattern and start a new island. This is elegant and efficient.")
print()

# -------------------------------------------------------------------------
# PROBLEM 4: Year-over-Year Growth Percentage
# -------------------------------------------------------------------------
print("=" * 60)
print("PROBLEM 4: Year-over-Year (Month-over-Month) Growth")
print("=" * 60)
print("""
PROBLEM:  Calculate month-over-month revenue growth for the business.
          Show each month's revenue, previous month's revenue, and
          the growth percentage.

COMPANY:  All MAANG, Databricks, Stripe (Analytics / Data Science)
ROLE:     Tests: CTE, LAG(), percentage calculation

HINTS:
  - Aggregate revenue by month first (CTE)
  - Use LAG() to get previous month's value
  - Growth = (current - previous) / previous * 100
  - Handle the first month (no previous) with COALESCE or CASE
""")

print("SOLUTION:")
run("""
WITH monthly AS (
    SELECT
        strftime('%Y-%m', order_date) as month,
        ROUND(SUM(amount), 2) as revenue,
        COUNT(DISTINCT customer_id) as unique_customers,
        COUNT(*) as order_count
    FROM orders
    WHERE status IN ('completed', 'shipped')
    GROUP BY strftime('%Y-%m', order_date)
)
SELECT
    month,
    revenue,
    unique_customers,
    order_count,
    LAG(revenue) OVER (ORDER BY month) as prev_revenue,
    CASE
        WHEN LAG(revenue) OVER (ORDER BY month) IS NULL THEN 'N/A'
        ELSE CAST(
            ROUND(
                (revenue - LAG(revenue) OVER (ORDER BY month))
                / LAG(revenue) OVER (ORDER BY month) * 100,
                1
            ) AS TEXT
        ) || '%'
    END as mom_growth
FROM monthly
ORDER BY month
""")
print("EXPLANATION: LAG(revenue) OVER (ORDER BY month) gets the previous row's")
print("revenue. For the first month, LAG returns NULL, so we handle that with CASE.")
print("Growth formula: (current - previous) / previous * 100.")
print()

# -------------------------------------------------------------------------
# PROBLEM 5: Retention / Cohort Analysis
# -------------------------------------------------------------------------
print("=" * 60)
print("PROBLEM 5: Retention / Cohort Analysis")
print("=" * 60)
print("""
PROBLEM:  For each user, determine their signup month (cohort). Then
          calculate what percentage of each cohort was still active
          (placed an order) in subsequent months.

COMPANY:  Netflix, Meta, Spotify, Anthropic (Growth / Data Science)
ROLE:     This is a CRITICAL question for growth-focused roles.
          Tests: CTEs, date arithmetic, self-joins, percentage calculation

HINTS:
  - Define cohort as signup month
  - Define "active" as placing an order in a given month
  - Calculate months since signup for each order
  - Group by cohort and period to get retention rates
""")

print("SOLUTION:")
run("""
WITH cohorts AS (
    -- Step 1: Assign each customer to a cohort (signup month)
    SELECT
        id as customer_id,
        strftime('%Y-%m', signup_date) as cohort_month
    FROM customers
),
activity AS (
    -- Step 2: For each order, calculate months since the customer signed up
    SELECT DISTINCT
        o.customer_id,
        c.cohort_month,
        strftime('%Y-%m', o.order_date) as activity_month,
        -- Months between signup and order
        (CAST(strftime('%Y', o.order_date) AS INTEGER) - CAST(strftime('%Y', cu.signup_date) AS INTEGER)) * 12
        + (CAST(strftime('%m', o.order_date) AS INTEGER) - CAST(strftime('%m', cu.signup_date) AS INTEGER))
        as months_since_signup
    FROM orders o
    JOIN cohorts c ON o.customer_id = c.customer_id
    JOIN customers cu ON o.customer_id = cu.id
    WHERE o.status != 'returned'
),
cohort_sizes AS (
    -- Step 3: Count customers in each cohort
    SELECT cohort_month, COUNT(*) as cohort_size
    FROM cohorts
    GROUP BY cohort_month
)
-- Step 4: Calculate retention rate for each cohort at each period
SELECT
    a.cohort_month,
    cs.cohort_size,
    a.months_since_signup as period,
    COUNT(DISTINCT a.customer_id) as active_users,
    ROUND(
        100.0 * COUNT(DISTINCT a.customer_id) / cs.cohort_size,
        1
    ) as retention_pct
FROM activity a
JOIN cohort_sizes cs ON a.cohort_month = cs.cohort_month
WHERE a.months_since_signup BETWEEN 0 AND 6
GROUP BY a.cohort_month, cs.cohort_size, a.months_since_signup
ORDER BY a.cohort_month, a.months_since_signup
LIMIT 25
""")
print("EXPLANATION: Cohort analysis groups users by when they signed up, then")
print("tracks what percentage remain active over time. This is the core metric")
print("for subscription businesses (Netflix, Spotify) and growth teams at MAANG.")
print()

# -------------------------------------------------------------------------
# PROBLEM 6: Cumulative Revenue by Month
# -------------------------------------------------------------------------
print("=" * 60)
print("PROBLEM 6: Cumulative Revenue by Month")
print("=" * 60)
print("""
PROBLEM:  Show each month's revenue alongside the cumulative (running)
          total. Also show what percentage of the total annual revenue
          each month contributes.

COMPANY:  Amazon, Databricks, Stripe (Finance / Analytics)
ROLE:     Tests: SUM() OVER(), window frames, percentage calculation

HINTS:
  - Aggregate by month first
  - SUM() OVER(ORDER BY month) for running total
  - Divide each month by the grand total for percentage
""")

print("SOLUTION:")
run("""
WITH monthly AS (
    SELECT
        strftime('%Y-%m', order_date) as month,
        ROUND(SUM(amount), 2) as revenue
    FROM orders
    WHERE status != 'returned'
    GROUP BY strftime('%Y-%m', order_date)
),
with_totals AS (
    SELECT
        month,
        revenue,
        ROUND(SUM(revenue) OVER (ORDER BY month), 2) as cumulative_revenue,
        SUM(revenue) OVER () as grand_total  -- OVER() with no ORDER BY = total of all rows
    FROM monthly
)
SELECT
    month,
    revenue,
    cumulative_revenue,
    ROUND(100.0 * revenue / grand_total, 1) as pct_of_total,
    ROUND(100.0 * cumulative_revenue / grand_total, 1) as cumulative_pct
FROM with_totals
ORDER BY month
""")
print("EXPLANATION: SUM() OVER(ORDER BY month) gives a running total.")
print("SUM() OVER() with no ORDER BY or PARTITION BY gives the grand total")
print("across all rows — useful for calculating percentages.")
print()

# -------------------------------------------------------------------------
# PROBLEM 7: Users Who Did Event A but Not Event B
# -------------------------------------------------------------------------
print("=" * 60)
print("PROBLEM 7: Users Who Did A but Not B")
print("=" * 60)
print("""
PROBLEM:  Find users who logged in but NEVER made a purchase.

COMPANY:  Meta, Netflix, Anthropic (Product Analytics / Growth)
ROLE:     Tests understanding of set operations and conversion funnels.
          There are MULTIPLE correct approaches — interviewers want to
          see you discuss tradeoffs.

HINTS:
  - Approach 1: LEFT JOIN + IS NULL
  - Approach 2: NOT EXISTS
  - Approach 3: EXCEPT
  - Approach 4: NOT IN (but watch out for NULLs!)
""")

print("SOLUTION (all 4 approaches):")

# Approach 1: LEFT JOIN + IS NULL (most intuitive)
print("--- Approach 1: LEFT JOIN ---")
run("""
SELECT DISTINCT logins.user_id
FROM user_events logins
LEFT JOIN user_events purchases
    ON logins.user_id = purchases.user_id
    AND purchases.event_type = 'purchase'
WHERE logins.event_type = 'login'
  AND purchases.user_id IS NULL
ORDER BY logins.user_id
""")

# Approach 2: NOT EXISTS (often most efficient)
print("--- Approach 2: NOT EXISTS ---")
run("""
SELECT DISTINCT user_id
FROM user_events
WHERE event_type = 'login'
  AND NOT EXISTS (
      SELECT 1
      FROM user_events ue2
      WHERE ue2.user_id = user_events.user_id
        AND ue2.event_type = 'purchase'
  )
ORDER BY user_id
""")

# Approach 3: EXCEPT (cleanest, set-based thinking)
print("--- Approach 3: EXCEPT ---")
run("""
SELECT DISTINCT user_id FROM user_events WHERE event_type = 'login'
EXCEPT
SELECT DISTINCT user_id FROM user_events WHERE event_type = 'purchase'
""")

print("EXPLANATION: All three approaches give the same result. In interviews:")
print("  - LEFT JOIN: shows you understand joins deeply")
print("  - NOT EXISTS: often fastest (stops at first match)")
print("  - EXCEPT: cleanest, shows set-based thinking")
print("  - NOT IN: avoid due to NULL issues (if subquery returns NULL, no rows match)")
print()

# -------------------------------------------------------------------------
# PROBLEM 8: Median Calculation in SQL
# -------------------------------------------------------------------------
print("=" * 60)
print("PROBLEM 8: Median Calculation in SQL")
print("=" * 60)
print("""
PROBLEM:  Calculate the median salary for each department.
          SQL has no built-in MEDIAN() function (except in some dialects).

COMPANY:  Google, Meta, Databricks (Data Science)
ROLE:     Tests: creative problem-solving, window functions, edge cases.
          The median is the middle value when sorted. For even counts,
          it's the average of the two middle values.

HINTS:
  - Use ROW_NUMBER() to rank rows
  - Use COUNT() to find total rows per group
  - The median is at position (count+1)/2 for odd, or avg of count/2 and count/2+1 for even
  - PostgreSQL has PERCENTILE_CONT(0.5) — mention this in interviews
""")

print("SOLUTION:")
run("""
WITH ranked AS (
    SELECT
        department,
        salary,
        ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary) as rn,
        COUNT(*) OVER (PARTITION BY department) as cnt
    FROM employees
)
SELECT
    department,
    ROUND(AVG(salary), 2) as median_salary
FROM ranked
WHERE rn IN (
    -- For odd count: middle element (e.g., cnt=5 → rn=3)
    -- For even count: two middle elements (e.g., cnt=6 → rn=3,4)
    (cnt + 1) / 2,       -- floor((cnt+1)/2) — handles odd
    (cnt + 2) / 2        -- ceil((cnt+1)/2) — handles even
)
GROUP BY department
ORDER BY median_salary DESC
""")
print("EXPLANATION: For a sorted list of N values:")
print("  Odd N:  median = value at position (N+1)/2")
print("  Even N: median = average of values at positions N/2 and N/2+1")
print("  We select both positions and AVG them — this works for both cases.")
print("  In PostgreSQL, use: PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary)")
print()

# -------------------------------------------------------------------------
# PROBLEM 9: Pivot / Unpivot Data
# -------------------------------------------------------------------------
print("=" * 60)
print("PROBLEM 9: Pivot / Unpivot Data")
print("=" * 60)
print("""
PROBLEM:  Create a pivot table showing order counts by customer tier
          and product category. Rows = categories, Columns = tiers.

COMPANY:  Amazon, Databricks (Analytics / BI)
ROLE:     Tests: CASE WHEN for pivoting, understanding of data reshaping

HINTS:
  - Use CASE WHEN inside aggregate functions
  - Each desired column becomes a SUM(CASE WHEN tier = 'X' THEN 1 ELSE 0 END)
  - PostgreSQL has CROSSTAB(), but CASE WHEN works everywhere
""")

print("SOLUTION (Pivot with CASE WHEN):")
run("""
SELECT
    p.category,
    SUM(CASE WHEN c.tier = 'Gold'   THEN 1 ELSE 0 END) as gold_orders,
    SUM(CASE WHEN c.tier = 'Silver' THEN 1 ELSE 0 END) as silver_orders,
    SUM(CASE WHEN c.tier = 'Bronze' THEN 1 ELSE 0 END) as bronze_orders,
    COUNT(*) as total_orders
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN products p ON o.product_id = p.id
GROUP BY p.category
ORDER BY total_orders DESC
""")

# Pivot: monthly revenue by product category
print("--- Bonus: Monthly revenue pivot ---")
run("""
SELECT
    strftime('%Y-%m', o.order_date) as month,
    ROUND(SUM(CASE WHEN p.category = 'Electronics' THEN o.amount ELSE 0 END), 2) as electronics,
    ROUND(SUM(CASE WHEN p.category = 'Furniture'   THEN o.amount ELSE 0 END), 2) as furniture,
    ROUND(SUM(CASE WHEN p.category = 'Office'      THEN o.amount ELSE 0 END), 2) as office,
    ROUND(SUM(CASE WHEN p.category = 'Accessories' THEN o.amount ELSE 0 END), 2) as accessories,
    ROUND(SUM(o.amount), 2) as total
FROM orders o
JOIN products p ON o.product_id = p.id
WHERE o.status != 'returned'
GROUP BY strftime('%Y-%m', o.order_date)
ORDER BY month
""")
print("EXPLANATION: SQL doesn't have a native PIVOT keyword in most dialects.")
print("The CASE WHEN approach works everywhere and is the expected answer in interviews.")
print("In PostgreSQL: use CROSSTAB(). In BigQuery/Snowflake: PIVOT keyword exists.")
print()

# -------------------------------------------------------------------------
# PROBLEM 10: Top N per Group
# -------------------------------------------------------------------------
print("=" * 60)
print("PROBLEM 10: Running Top-N per Group")
print("=" * 60)
print("""
PROBLEM:  For each product category, find the top 3 products by total
          revenue generated. Show the category, product name, total revenue,
          and its rank within the category.

COMPANY:  Google, Amazon, Netflix (all levels)
ROLE:     The "Top N per Group" pattern is the SINGLE MOST common window
          function interview question. You MUST know this cold.

HINTS:
  - Aggregate revenue per product first
  - Use ROW_NUMBER() or DENSE_RANK() partitioned by category
  - Filter to rank <= 3 in the outer query
  - Use CTE for readability
""")

print("SOLUTION:")
run("""
WITH product_revenue AS (
    -- Step 1: Total revenue per product
    SELECT
        p.id as product_id,
        p.name as product_name,
        p.category,
        ROUND(SUM(o.amount), 2) as total_revenue,
        COUNT(*) as order_count
    FROM products p
    LEFT JOIN orders o ON p.id = o.product_id AND o.status != 'returned'
    GROUP BY p.id, p.name, p.category
),
ranked AS (
    -- Step 2: Rank products within each category by revenue
    SELECT
        category,
        product_name,
        total_revenue,
        order_count,
        ROW_NUMBER() OVER (
            PARTITION BY category
            ORDER BY total_revenue DESC
        ) as revenue_rank
    FROM product_revenue
)
-- Step 3: Filter to top 3 per category
SELECT category, product_name, total_revenue, order_count, revenue_rank
FROM ranked
WHERE revenue_rank <= 3
ORDER BY category, revenue_rank
""")
print("EXPLANATION: This is the standard Top-N-per-Group pattern:")
print("  1. Aggregate the metric (revenue per product)")
print("  2. Rank within each group (ROW_NUMBER PARTITION BY category)")
print("  3. Filter (WHERE rank <= N)")
print("  This 3-step pattern works for ANY 'top N per group' problem.")
print()


# %% SECTION 6: Platform Differences
# =============================================================================
# SECTION 6: PLATFORM DIFFERENCES
# =============================================================================
# Different SQL engines have different syntax. Interviews may use any of these.
# This reference helps you translate between them.

print()
print("=" * 78)
print("SECTION 6: PLATFORM DIFFERENCES")
print("=" * 78)
print()

print("""
====================================================================================
FEATURE           | SQLite            | PostgreSQL         | MySQL
====================================================================================
Date truncate     | strftime('%Y-%m', | DATE_TRUNC('month',| DATE_FORMAT(d,
  to month        |   date_col)       |   date_col)        |   '%Y-%m')
----------------------------------------------------------------------------------
Extract year      | strftime('%Y',    | EXTRACT(YEAR FROM  | YEAR(date_col)
                  |   date_col)       |   date_col)        |
----------------------------------------------------------------------------------
Date add          | DATE(d, '+N days')| d + INTERVAL       | DATE_ADD(d,
                  |                   |   'N days'         |   INTERVAL N DAY)
----------------------------------------------------------------------------------
Date diff (days)  | julianday(d1) -   | d1 - d2            | DATEDIFF(d1, d2)
                  |   julianday(d2)   | (returns integer)  |
----------------------------------------------------------------------------------
Current date      | DATE('now')       | CURRENT_DATE       | CURDATE()
----------------------------------------------------------------------------------
Current timestamp | DATETIME('now')   | NOW()              | NOW()
----------------------------------------------------------------------------------
String concat     | col1 || col2      | col1 || col2       | CONCAT(col1, col2)
----------------------------------------------------------------------------------
Substring         | SUBSTR(s, pos, n) | SUBSTRING(s FROM   | SUBSTRING(s, pos, n)
                  |                   |   pos FOR n)       |
----------------------------------------------------------------------------------
Case-insensitive  | LIKE (default     | ILIKE              | LIKE (default
  pattern match   |   case-sensitive) |                    |   case-insensitive!)
----------------------------------------------------------------------------------
LIMIT / OFFSET    | LIMIT N OFFSET M  | LIMIT N OFFSET M   | LIMIT M, N  (reversed!)
                  |                   | or FETCH FIRST N   |   or LIMIT N OFFSET M
----------------------------------------------------------------------------------
FULL OUTER JOIN   | Not supported     | Supported          | Not supported
                  | (use UNION trick) |                    | (use UNION trick)
----------------------------------------------------------------------------------
Boolean type      | 0 / 1 (integer)   | TRUE / FALSE       | 0 / 1 (tinyint)
----------------------------------------------------------------------------------
Auto-increment    | AUTOINCREMENT     | SERIAL /           | AUTO_INCREMENT
                  |                   | GENERATED ALWAYS   |
----------------------------------------------------------------------------------
Upsert            | INSERT OR REPLACE | INSERT ... ON      | INSERT ... ON
                  |                   | CONFLICT DO UPDATE | DUPLICATE KEY UPDATE
----------------------------------------------------------------------------------
Window functions  | Supported (3.25+) | Fully supported    | Supported (8.0+)
----------------------------------------------------------------------------------
CTEs (WITH)       | Supported (3.8+)  | Fully supported    | Supported (8.0+)
----------------------------------------------------------------------------------
Recursive CTEs    | Supported         | Supported          | Supported (8.0+)
----------------------------------------------------------------------------------
JSON support      | json_extract()    | jsonb, ->, ->>     | JSON_EXTRACT(), ->
----------------------------------------------------------------------------------
Array type        | Not supported     | ARRAY[], unnest()  | Not supported
----------------------------------------------------------------------------------
ROLLUP / CUBE     | Not supported     | Supported          | ROLLUP only (8.0+)
----------------------------------------------------------------------------------
Median function   | Not built-in      | PERCENTILE_CONT    | Not built-in
                  |                   | (0.5) WITHIN GROUP |
====================================================================================


====================================================================================
FEATURE           | BigQuery           | Snowflake          | Databricks SQL
====================================================================================
Date truncate     | DATE_TRUNC(d,      | DATE_TRUNC('month',| DATE_TRUNC('month',
  to month        |   MONTH)           |   d)               |   d)
----------------------------------------------------------------------------------
Extract year      | EXTRACT(YEAR       | EXTRACT(YEAR FROM  | YEAR(d) or
                  |   FROM d)          |   d)               |   EXTRACT(YEAR FROM d)
----------------------------------------------------------------------------------
Date add          | DATE_ADD(d,        | DATEADD('day',     | DATE_ADD(d, N)
                  |   INTERVAL N DAY)  |   N, d)            |
----------------------------------------------------------------------------------
Date diff         | DATE_DIFF(d1,d2,   | DATEDIFF('day',    | DATEDIFF(d1, d2)
                  |   DAY)             |   d1, d2)          |
----------------------------------------------------------------------------------
String concat     | CONCAT(a, b) or || | col1 || col2       | CONCAT(a, b) or ||
----------------------------------------------------------------------------------
LIMIT             | LIMIT N            | LIMIT N            | LIMIT N
----------------------------------------------------------------------------------
Window functions  | Fully supported    | Fully supported    | Fully supported
----------------------------------------------------------------------------------
QUALIFY clause    | Supported          | Supported          | Supported
  (filter window  | (filter on window  |                    |
   function)      |  result directly)  |                    |
----------------------------------------------------------------------------------
Nested/repeated   | ARRAY, STRUCT,     | VARIANT, ARRAY,    | ARRAY, STRUCT,
  types           | UNNEST()           | OBJECT, FLATTEN()  |   MAP
----------------------------------------------------------------------------------
PIVOT keyword     | Not supported      | PIVOT / UNPIVOT    | PIVOT / UNPIVOT
----------------------------------------------------------------------------------
Median function   | PERCENTILE_CONT    | MEDIAN()           | PERCENTILE(col, 0.5)
                  | (0.5) or APPROX   |                    |
----------------------------------------------------------------------------------
Storage model     | Columnar           | Columnar           | Columnar (Delta Lake)
====================================================================================


QUALIFY CLAUSE (BigQuery, Snowflake, Databricks)
=================================================
QUALIFY is a game-changer — it lets you filter on window function results
directly, without needing a CTE or subquery.

Instead of:
  WITH ranked AS (
      SELECT *, ROW_NUMBER() OVER(PARTITION BY dept ORDER BY salary DESC) as rn
      FROM employees
  )
  SELECT * FROM ranked WHERE rn = 1;

You can write:
  SELECT *
  FROM employees
  QUALIFY ROW_NUMBER() OVER(PARTITION BY dept ORDER BY salary DESC) = 1;

Much cleaner! Know this for Databricks and Google interviews.
""")


# %% SECTION 7: Quick Reference Card
# =============================================================================
# SECTION 7: QUICK REFERENCE CARD — 30 Essential SQL Patterns
# =============================================================================
# Print this, put it on your wall, review it before every interview.

print()
print("=" * 78)
print("SECTION 7: QUICK REFERENCE CARD — 30 Essential SQL Patterns")
print("=" * 78)
print()

print("""
==========================================================================
 #  | PATTERN                        | WHEN TO USE
==========================================================================
 1  | SELECT col1, col2 FROM t       | Basic column selection
    | WHERE condition                 |
--------------------------------------------------------------------------
 2  | GROUP BY col                    | Aggregate rows into groups
    | HAVING agg_func() > N           | Filter groups (not rows)
--------------------------------------------------------------------------
 3  | LEFT JOIN t2 ON t1.id=t2.fk    | Keep all rows from left table
    | WHERE t2.id IS NULL             | Anti-join: find unmatched rows
--------------------------------------------------------------------------
 4  | INNER JOIN t2 ON t1.id=t2.fk   | Only matching rows from both
--------------------------------------------------------------------------
 5  | COALESCE(col, default)          | Replace NULL with a default value
--------------------------------------------------------------------------
 6  | CASE WHEN x THEN a             | Conditional logic / bucketing
    |      WHEN y THEN b ELSE c END  |
--------------------------------------------------------------------------
 7  | WITH cte AS (SELECT ...)       | Named temporary result set (CTE)
    | SELECT * FROM cte               | Makes complex queries readable
--------------------------------------------------------------------------
 8  | ROW_NUMBER() OVER(PARTITION    | Assign unique rank within groups
    |   BY grp ORDER BY col)          | #1 use: top-N per group
--------------------------------------------------------------------------
 9  | RANK() / DENSE_RANK() OVER()  | Rank with tie handling
    |                                 | RANK skips, DENSE_RANK doesn't
--------------------------------------------------------------------------
10  | LAG(col) OVER(ORDER BY date)  | Get previous row's value
    | LEAD(col) OVER(ORDER BY date) | Get next row's value
    |                                 | Use: growth rates, time gaps
--------------------------------------------------------------------------
11  | SUM(col) OVER(ORDER BY date)  | Running / cumulative total
--------------------------------------------------------------------------
12  | AVG(col) OVER(ROWS BETWEEN    | Moving average
    |   N PRECEDING AND CURRENT ROW) |
--------------------------------------------------------------------------
13  | NTILE(4) OVER(ORDER BY col)   | Divide into N equal buckets
    |                                 | NTILE(4) = quartiles
--------------------------------------------------------------------------
14  | SUM(CASE WHEN cond THEN 1     | Conditional count / pivot
    |   ELSE 0 END)                  | "How many rows match X?"
--------------------------------------------------------------------------
15  | COUNT(DISTINCT col)            | Count unique values
--------------------------------------------------------------------------
16  | UNION / UNION ALL              | Combine result sets
    |                                 | UNION deduplicates, ALL keeps dupes
--------------------------------------------------------------------------
17  | EXCEPT                         | Rows in A not in B (set difference)
--------------------------------------------------------------------------
18  | EXISTS (SELECT 1 FROM ...)     | Check if related rows exist
    |                                 | Often faster than IN
--------------------------------------------------------------------------
19  | NOT IN (SELECT col FROM t      | Exclude matching values
    |   WHERE col IS NOT NULL)        | ALWAYS filter NULLs in subquery!
--------------------------------------------------------------------------
20  | NULLIF(denominator, 0)         | Prevent division by zero
    |                                 | Returns NULL if denominator is 0
--------------------------------------------------------------------------
21  | FIRST_VALUE(col) OVER(         | First value in the window
    |   PARTITION BY grp ORDER BY x) | Last: use UNBOUNDED FOLLOWING frame
--------------------------------------------------------------------------
22  | DATE_TRUNC('month', date)      | Truncate date to period (PostgreSQL)
    | strftime('%Y-%m', date)         | SQLite equivalent
--------------------------------------------------------------------------
23  | WHERE date >= '2024-01-01'     | Date range filter (index-friendly)
    |   AND date < '2025-01-01'      | NEVER use YEAR(date) = 2024
--------------------------------------------------------------------------
24  | SELECT *, rn FROM (            | Top-N per group pattern
    |   SELECT *, ROW_NUMBER()       | 1. Rank in subquery/CTE
    |     OVER(PARTITION BY grp      | 2. Filter in outer query
    |     ORDER BY val DESC) as rn   | Most common window function Q
    | ) WHERE rn <= N                |
--------------------------------------------------------------------------
25  | Correlated subquery:           | Per-row calculation referencing
    | (SELECT AGG FROM t2            |   the outer query
    |  WHERE t2.grp = t1.grp)       | Slow but powerful — prefer CTE/JOIN
--------------------------------------------------------------------------
26  | INSERT INTO ... SELECT ...     | Insert results of a query
    | FROM source_table              | Bulk data movement
--------------------------------------------------------------------------
27  | CREATE INDEX idx               | Speed up WHERE, JOIN, ORDER BY
    | ON table(col1, col2)           | Leftmost prefix rule for composites
--------------------------------------------------------------------------
28  | EXPLAIN (ANALYZE)              | See how the DB executes your query
    | SELECT ...                     | Look for: Seq Scan → add index
--------------------------------------------------------------------------
29  | Gaps and Islands:              | Find consecutive date streaks
    | DATE - ROW_NUMBER() = island   | Login streaks, price changes
--------------------------------------------------------------------------
30  | Self-join:                     | Compare rows within the same table
    | FROM t a JOIN t b              | Manager-employee, sequential events
    | ON a.manager_id = b.id        |
==========================================================================
""")


# =============================================================================
# CLEANUP
# =============================================================================
conn.close()
print("=" * 78)
print("DATABASE CONNECTION CLOSED. Tutorial complete!")
print("=" * 78)
print()
print("NEXT STEPS FOR INTERVIEW PREP:")
print("  1. Re-do problems 3, 5, 8 from memory (they're the hardest)")
print("  2. Practice on LeetCode SQL (problems 175-185 cover MAANG basics)")
print("  3. Practice on StrataScratch or DataLemur for company-specific questions")
print("  4. Time yourself: easy = 5 min, medium = 10 min, hard = 15 min")
print("  5. Learn PostgreSQL-specific syntax (QUALIFY, DATE_TRUNC, PERCENTILE_CONT)")
print("  6. For Databricks/Snowflake roles: study QUALIFY and columnar storage")
print()
