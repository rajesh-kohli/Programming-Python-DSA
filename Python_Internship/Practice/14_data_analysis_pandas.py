"""
==============================================================================
Pandas Complete Tutorial & Practice — From Zero to Interview-Ready
==============================================================================

This file is structured as a runnable tutorial. Each section builds on the
previous one. Run sections individually in VS Code (select → Shift+Enter)
or run the whole file.

Table of Contents:
  Section 1:  What is Pandas? Series vs DataFrame
  Section 2:  Creating DataFrames (from dicts, lists, CSV)
  Section 3:  Inspecting Data (head, info, describe, shape, dtypes)
  Section 4:  Selecting Data (loc, iloc, boolean indexing)
  Section 5:  Filtering & Querying
  Section 6:  Adding, Renaming, Dropping Columns
  Section 7:  Sorting
  Section 8:  Handling Missing Data (NaN)
  Section 9:  GroupBy & Aggregation (the most important section)
  Section 10: Merge, Join, Concat (combining DataFrames)
  Section 11: Apply, Map, Lambda (custom transformations)
  Section 12: String Operations
  Section 13: DateTime Operations
  Section 14: Pivot Tables & Crosstab
  Section 15: Window Functions (rolling, cumsum)
  Section 16: Reading & Writing Files (CSV, Excel, JSON)
  Section 17: Method Chaining (writing clean Pandas code)
  Section 18: Performance Tips
  Section 19: Practice Exercises (10 exercises with solutions)
  Section 20: Interview-Style Problems (Applied Scientist / FDE)
  Section 21: Capstone — Customer Transaction Analysis
"""

# %% Imports
import os
import numpy as np
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

print("Pandas version:", pd.__version__)
print()


# %% SECTION 1: What is Pandas? Series vs DataFrame
# =============================================================================
# SECTION 1: What is Pandas? Series vs DataFrame
# =============================================================================

# Pandas is a Python library for data manipulation and analysis.
# It provides two core data structures:
#
#   Series:    a 1D labeled array (like a column in a spreadsheet)
#   DataFrame: a 2D labeled table  (like a spreadsheet or SQL table)
#
# Think of a DataFrame as a dictionary of Series — each column is a Series.

# ----- Series -----
s = pd.Series([10, 20, 30, 40], index=["a", "b", "c", "d"])
e = pd.Series([10, 20, 30, 40]) # when you don't assign index, it assigns 0,1,2..

print("--- Series ---")
print(s)
print(e)  #notice indexing
print("Type:", type(s))
print("Access by label: s['b'] =", s["b"])        # 20
print("Access by position: s[1] =", s.iloc[1]) 
print(e[:-1]) # all elements upto/except the last element
print(e[:2]) # the way list indexing works, e.g e[2] doesn't work with series
print(e.iloc[2]) #only iloc works when we haven't assigned labels
print("Type:", type(e))
print()

# ----- DataFrame -----
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
    "city": ["NYC", "LA", "Chicago"]
})
print("--- DataFrame ---")
print(df)
print("Shape:", df.shape)     # (3, 3) = 3 rows, 3 columns
print()

# %% SECTION 2: Creating DataFrames
# =============================================================================
# SECTION 2: Creating DataFrames
# =============================================================================

# ----- From a dictionary of lists (most common) -----
df1 = pd.DataFrame({
    "product": ["Laptop", "Phone", "Tablet"],
    "price": [999, 699, 499],
    "stock": [50, 200, 150]
})

# ----- From a list of dictionaries (each dict = one row) -----
df2 = pd.DataFrame([
    {"name": "Alice", "score": 85},
    {"name": "Bob", "score": 92},
    {"name": "Charlie", "score": 78}
])

# ----- From a NumPy array -----
df3 = pd.DataFrame(
    np.random.randint(1, 100, size=(4, 3)),
    columns=["A", "B", "C"]
)

print("--- From dict ---")
print(df1)
print("\n--- From list of dicts ---")
print(df2)
print("\n--- From NumPy array ---")
print(df3)
print()

# %% SECTION 3: Inspecting Data — The First Things You Do With Any Dataset
# =============================================================================
# SECTION 3: Inspecting Data — The First Things You Do With Any Dataset
# =============================================================================

# Let's create a realistic dataset to work with throughout the tutorial.
np.random.seed(42)
n = 100
sales = pd.DataFrame({
    "date": pd.date_range("2026-01-01", periods=n, freq="D"),
    "customer_id": np.random.choice(["C001", "C002", "C003", "C004", "C005"], n),
    "amount": np.round(np.random.uniform(10, 500, n), 2),
    "product_category": np.random.choice(["Electronics", "Clothing", "Groceries", "Books"], n),
    "quantity": np.random.randint(1, 10, n),
    "city": np.random.choice(["NYC", "LA", "Chicago", "Houston", "Phoenix"], n)
})
# Add some NaN values for later exercises
sales.loc[3, "amount"] = np.nan # nan fpr amount at index numbered 3 (not index number 3)
sales.loc[7, "city"] = np.nan
sales.loc[15, "amount"] = np.nan

print("=" * 60)
print("SECTION 3: Inspecting Data")
print("=" * 60)

# ----- Essential inspection functions -----

print("\n--- df.head(5) — first 5 rows ---")
print(sales.head())

print("\n--- df.tail(3) — last 3 rows ---")
print(sales.tail(3))

print("\n--- df.shape — (rows, columns) ---")
print(sales.shape)  # (100, 6)

print("\n--- df.columns — column names ---")
print(sales.columns.tolist())

print("\n--- df.dtypes — data type of each column ---")
print(sales.dtypes)

print("\n--- df.info() — summary including non-null counts and memory ---")
sales.info()

print("\n--- df.describe() — statistics for numeric columns ---")
print(sales.describe())

# describe() gives: count, mean, std, min, 25%, 50% (median), 75%, max
# For interviews: describe() is usually your FIRST call to understand distributions.
#
# ----- How to READ describe() output — The Checklist -----
#
# | What to check                    | What it tells you                            |
# |----------------------------------|----------------------------------------------|
# | count differs between columns?   | Missing data in specific columns             |
# | mean vs 50% (median)             | Skewness — if mean >> median, right-skewed   |
# | std relative to mean             | How variable the data is (std/mean > 1 = very spread) |
# | min and max                      | Range, and whether extreme outliers exist     |
# | 25% to 75% (IQR)                | Where the "middle half" of your data lives   |
# | min far from 25%?                | Possible low-end outliers                    |
# | max far from 75%?                | Possible high-end outliers                   |
#
# ----- Example observations from our sales data -----
#
# 1. count: amount is 98 but quantity is 100
#    → 2 rows have NaN in 'amount'. Always check count mismatches first.
#
# 2. mean ≈ 50% (median) for amount (251 vs 241)
#    → Close values means the distribution is roughly SYMMETRIC (no extreme skew).
#    → If mean were much higher than median, a few very large values would be
#      pulling the average up (right-skew). If mean << median, left-skew.
#
# 3. mean date = 50% date
#    → Our dates are evenly spaced (pd.date_range with freq="D"), so mean and
#      median are identical. In real data they'd differ — e.g., if most transactions
#      happened in January with a few in April, median would be in January but
#      mean would be pulled toward April.
#
# 4. std for date is NaN
#    → Pandas can't compute standard deviation for datetime. This is normal.
#
# ----- What is Standard Deviation (std)? -----
#
# std measures HOW SPREAD OUT the values are from the mean.
#   Low std  = values are clustered close to the mean (consistent)
#   High std = values are spread far from the mean (variable)
#
# For amount: mean = 251, std = 132
#   ~68% of values fall within 1 std of the mean: 251 ± 132 = $119 to $383
#   ~95% of values fall within 2 std of the mean: 251 ± 264 = -$13 to $515
#   Anything beyond 2 std is unusual (that's why anomaly detection flags |z| > 2)
#
# Practical shortcut: std / mean = coefficient of variation (CV)
#   Here: 132 / 251 = 0.53 → transactions vary by ~53% from average (quite variable)
#   CV < 0.1 = very consistent, CV > 0.5 = highly variable
#
# For quantity: mean = 4.71, std = 2.60
#   Typical range: ~2 to ~7 → matches the 25%-75% percentiles (2 to 7)

print("\n--- df.nunique() — number of unique values per column ---")
print(sales.nunique())

print("\n--- df['column'].value_counts() — frequency of each value ---")
print(sales["product_category"].value_counts())
print()

# %% SECTION 4: Selecting Data — loc, iloc, and Boolean Indexing
# =============================================================================
# SECTION 4: Selecting Data — loc, iloc, and Boolean Indexing
# =============================================================================

print("=" * 60)
print("SECTION 4: Selecting Data")
print("=" * 60)

# ----- Selecting columns -----
# Single column → returns a Series
amounts = sales["amount"]
type(amounts) #series
print(amounts[0:5])
amounts[4] # 191.7 - Tries to guess. It defaults to checking for a label named 4 first.
amounts.iloc[4] # 191.7 - Looks strictly at the integer position (the 5th item in line)
amounts.loc[4] # 191.7 - Looks strictly at the label index named 4

## all three commands return the same value: 191.7 - reasons mentioned above

## Major difference between list and series is:
# A Python list only has hidden, automatic positional index numbers (0, 1, 2, 3...)
# A pandas Series is actually two distinct arrays joined together: a list of Labels (the Index) and a list of Values.

"""
Here are two crucial examples showing where your list analogy breaks down.
1. Custom Labels (Non-numeric)
You can change a Series index to words, dates, or strings. A list can never do this.

"""

# Python List
my_list = [100, 200, 300]
# my_list['apple'] -> ERROR! Lists only accept integers.

# Pandas Series with custom index labels
my_series = pd.Series([100, 200, 300], index=['apple', 'banana', 'cherry'])

print(my_series['banana'])  # Returns 200 (using label)
print(my_series.iloc[1])    # Returns 200 (using position)

"""
2. Shuffled or Out-of-Order Numerical Labels

This is where the biggest bugs happen. Imagine you sort or filter your data, 
and the rows change order, but keep their original labels.
"""

# A Series where labels are shuffled/not matching positions
s = pd.Series([10, 20, 30], index=[2, 0, 1])

print(s.iloc[0])  # Returns 10 -> The first item in the physical list
print(s.loc[0])   # Returns 20 -> The item whose explicit label is 0
print(s[0])       # Returns 20 -> Chose the label, NOT the position!

"""
If this were a standard Python list, [0] would always give you the first item (10). 
In pandas, it gives you 20 because it prioritized the label.
"""


# Multiple columns → returns a DataFrame
subset = sales[["customer_id", "amount", "product_category"]]
print(subset.head(10))

# ----- loc: select by LABEL (row/column names) -----
# loc[row_label, column_label]
print("\n--- loc examples ---")
print("Row 0, all columns:\n", sales.loc[0])
print("\nRows 0-2, specific columns:")
print(sales.loc[0:2, ["customer_id", "amount"]])

# ----- iloc: select by INTEGER POSITION -----
# iloc[row_position, column_position]
print("\n--- iloc examples ---")
print("First 3 rows, first 2 columns:")
print(sales.iloc[:3, :2])
print("\nLast row:")
print(sales.iloc[-1])

# ----- KEY DIFFERENCE -----
# loc[0:2]  → includes row 2 (label-based, inclusive on both ends)
# iloc[0:2] → excludes row 2 (position-based, exclusive on the end, like Python slicing)

# ----- Boolean indexing (MOST IMPORTANT — used everywhere) -----
# Create a boolean mask, then use it to filter rows
print("\n--- Boolean indexing ---")
expensive = sales[sales["amount"] > 400]


print(sales.head())

print(f"Transactions over $400: {len(expensive)} rows")

print(expensive.head())

Groceries_sales = sales[sales["product_category"] == 'Groceries']

print(Groceries_sales)
print()

# %% SECTION 5: Filtering & Querying
# =============================================================================
# SECTION 5: Filtering & Querying
# =============================================================================

print("=" * 60)
print("SECTION 5: Filtering & Querying")
print("=" * 60)

# ----- Single condition -----
electronics = sales[sales["product_category"] == "Electronics"]
print(f"\nElectronics transactions: {len(electronics)}")

# ----- Multiple conditions (use & for AND, | for OR, ~ for NOT) -----
# IMPORTANT: wrap each condition in parentheses!
expensive_electronics = sales[
    (sales["product_category"] == "Electronics") & (sales["amount"] > 300)
]
print(f"Electronics over $300: {len(expensive_electronics)}")

# ----- isin() — check if value is in a list -----
big_cities = sales[sales["city"].isin(["NYC", "LA"])]
print(f"NYC or LA transactions: {len(big_cities)}")

# ----- between() — range filter -----
mid_range = sales[sales["amount"].between(100, 300)]
print(f"Amount between 100-300: {len(mid_range)}")

# ----- str.contains() — partial string matching -----
c_customers = sales[sales["customer_id"].str.contains("C00")]
print(f"Customers matching 'C00': {len(c_customers)}")

# ----- .query() — SQL-like syntax (cleaner for complex filters) -----
result = sales.query("amount > 200 and city == 'NYC'")
print(f"NYC transactions over $200: {len(result)}")

# ----- Negation with ~ -----
not_groceries = sales[~(sales["product_category"] == "Groceries")]
print(f"Non-grocery transactions: {len(not_groceries)}")
print()

# %% SECTION 6: Adding, Renaming, Dropping Columns
# =============================================================================
# SECTION 6: Adding, Renaming, Dropping Columns
# =============================================================================

print("=" * 60)
print("SECTION 6: Column Operations")
print("=" * 60)

df_copy = sales.copy()  # always work on a copy to avoid modifying the original

# ----- Add a new column -----
df_copy["total"] = df_copy["amount"] * df_copy["quantity"]
df_copy["is_expensive"] = df_copy["amount"] > 200

# ----- Rename columns -----
df_renamed = df_copy.rename(columns={"amount": "sale_amount", "city": "location"})
print("\nRenamed columns:", df_renamed.columns.tolist())

# ----- Drop columns -----
df_dropped = df_copy.drop(columns=["is_expensive", "total"])
print("After dropping 2 columns:", df_dropped.columns.tolist())

# ----- Insert a column at a specific position -----
df_copy.insert(1, "year", 2026)
print("After insert at position 1:", df_copy.columns.tolist())
print()

# %% SECTION 7: Sorting
# =============================================================================
# SECTION 7: Sorting
# =============================================================================

print("=" * 60)
print("SECTION 7: Sorting")
print("=" * 60)

# ----- Sort by one column -----
by_amount = sales.sort_values("amount", ascending=False)
print("\nTop 5 by amount:")
print(by_amount.head())

# ----- Sort by multiple columns -----
by_cat_amount = sales.sort_values(
    ["product_category", "amount"],
    ascending=[True, False]  # category A-Z, amount high-to-low within each
)
print("\nSorted by category then amount (desc):")
print(by_cat_amount.head(8))

# ----- nlargest / nsmallest — faster than sort + head for top-N -----
top5 = sales.nlargest(5, "amount")
bottom5 = sales.nsmallest(5, "amount")
print("\nTop 5 amounts:")
print(top5[["customer_id", "amount"]])
print()

# %% SECTION 8: Handling Missing Data (NaN)
# =============================================================================
# SECTION 8: Handling Missing Data (NaN)
# =============================================================================

print("=" * 60)
print("SECTION 8: Missing Data")
print("=" * 60)

# We added NaN values to rows 3, 7, 15 earlier.

# ----- Detect missing values -----
print("\nMissing values per column:")
print(sales.isnull().sum())

print("\nRows with any missing value:")
print(sales[sales.isnull().any(axis=1)])

# ----- Drop rows with missing values -----
cleaned = sales.dropna()
print(f"\nAfter dropna: {len(sales)} → {len(cleaned)} rows")

# ----- Drop rows where a SPECIFIC column is missing -----
cleaned2 = sales.dropna(subset=["amount"])
print(f"After dropna(subset=['amount']): {len(cleaned2)} rows")

# ----- Fill missing values -----
filled_zero = sales["amount"].fillna(0)          # fill with 0
filled_mean = sales["amount"].fillna(sales["amount"].mean())   # fill with mean
filled_ffill = sales["city"].ffill()              # forward fill (use previous value)

print(f"\nOriginal NaN count in 'amount': {sales['amount'].isnull().sum()}")
print(f"After fillna(mean): {filled_mean.isnull().sum()}")

# ----- Interview tip -----
# Always explain your missing data strategy:
#   - Drop: when missing is <5% and random
#   - Fill with mean/median: numeric data, when distribution matters
#   - Fill with mode: categorical data
#   - Forward/backward fill: time series data
#   - Flag it: create a separate 'is_missing' column and fill with a value
print()

# %% SECTION 9: GroupBy & Aggregation — THE MOST IMPORTANT SECTION
# =============================================================================
# SECTION 9: GroupBy & Aggregation — THE MOST IMPORTANT SECTION
# =============================================================================

print("=" * 60)
print("SECTION 9: GroupBy & Aggregation")
print("=" * 60)

# GroupBy splits the data into groups, applies a function, and combines results.
# Think of it as: SQL's GROUP BY + aggregate functions.
#
# Pattern: df.groupby("column")["value_column"].agg_function()

# ----- Basic groupby -----
print("\n--- Total sales by category ---")
cat_totals = sales.groupby("product_category")["amount"].sum()
print(cat_totals)

print("\n--- Average amount by city ---")
city_avg = sales.groupby("city")["amount"].mean()
print(city_avg.round(2))

# ----- Multiple aggregations with .agg() -----
print("\n--- Multiple aggregations ---")
cat_stats = sales.groupby("product_category")["amount"].agg(["sum", "mean", "count", "min", "max"])
print(cat_stats.round(2))

# ----- Aggregate different columns differently -----
print("\n--- Different aggs per column ---")
multi_agg = sales.groupby("product_category").agg(
    total_sales=("amount", "sum"),
    avg_quantity=("quantity", "mean"),
    num_transactions=("customer_id", "count"),
    unique_customers=("customer_id", "nunique")
)
print(multi_agg.round(2))

# ----- Group by multiple columns -----
print("\n--- Group by category AND city ---")
cat_city = sales.groupby(["product_category", "city"])["amount"].sum()
print(cat_city.head(10))

# ----- reset_index() — convert grouped result back to a regular DataFrame -----
cat_city_df = cat_city.reset_index()
cat_city_df.columns = ["category", "city", "total"]
print("\nAs a flat DataFrame:")
print(cat_city_df.head())

# ----- transform() — apply agg but keep original shape -----
# Useful for adding a group-level stat as a new column
sales_with_avg = sales.copy()
sales_with_avg["category_avg"] = sales.groupby("product_category")["amount"].transform("mean")
print("\n--- transform: category average added to each row ---")
print(sales_with_avg[["product_category", "amount", "category_avg"]].head())

# ----- filter() — keep only groups that meet a condition -----
# Keep only categories with more than 20 transactions
popular = sales.groupby("product_category").filter(lambda g: len(g) > 20)
print(f"\nCategories with >20 transactions: {popular['product_category'].nunique()} categories, {len(popular)} rows")
print()

# %% SECTION 10: Merge, Join, Concat — Combining DataFrames
# =============================================================================
# SECTION 10: Merge, Join, Concat — Combining DataFrames
# =============================================================================

print("=" * 60)
print("SECTION 10: Merge, Join, Concat")
print("=" * 60)

# ----- Create two sample tables -----
customers = pd.DataFrame({
    "customer_id": ["C001", "C002", "C003", "C004", "C005", "C006"],
    "name": ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank"],
    "tier": ["Gold", "Silver", "Gold", "Bronze", "Silver", "Gold"]
})

orders = pd.DataFrame({
    "order_id": [1, 2, 3, 4, 5],
    "customer_id": ["C001", "C002", "C001", "C007", "C003"],
    "amount": [250, 180, 320, 90, 410]
})

# ----- merge (like SQL JOIN) -----
# inner join: only matching rows from both
inner = pd.merge(orders, customers, on="customer_id", how="inner")
print("\n--- INNER JOIN ---")
print(inner)
# C007 dropped (not in customers), C004/C005/C006 dropped (not in orders)

# left join: all rows from left, matching from right
left = pd.merge(orders, customers, on="customer_id", how="left")
print("\n--- LEFT JOIN ---")
print(left)
# C007 kept with NaN for name/tier

# right join: all rows from right, matching from left
right = pd.merge(orders, customers, on="customer_id", how="right")
print("\n--- RIGHT JOIN ---")
print(right)
# C004/C005/C006 kept with NaN for order_id/amount

# outer join: all rows from both
outer = pd.merge(orders, customers, on="customer_id", how="outer")
print("\n--- OUTER JOIN ---")
print(outer)

# ----- concat: stack DataFrames vertically or horizontally -----
df_jan = pd.DataFrame({"month": ["Jan", "Jan"], "sales": [100, 200]})
df_feb = pd.DataFrame({"month": ["Feb", "Feb"], "sales": [150, 250]})

stacked = pd.concat([df_jan, df_feb], ignore_index=True)
print("\n--- concat (vertical stack) ---")
print(stacked)
print()

# %% SECTION 11: Apply, Map, Lambda — Custom Transformations
# =============================================================================
# SECTION 11: Apply, Map, Lambda — Custom Transformations
# =============================================================================

print("=" * 60)
print("SECTION 11: Apply, Map, Lambda")
print("=" * 60)

df_apply = sales[["customer_id", "amount", "quantity"]].head(5).copy()

# ----- apply on a column (Series.apply) — element-wise -----
df_apply["amount_tier"] = df_apply["amount"].apply(
    lambda x: "High" if x > 300 else "Medium" if x > 100 else "Low"
)
print("\n--- apply with lambda ---")
print(df_apply)

# ----- apply on a DataFrame (row-wise with axis=1) -----
df_apply["revenue"] = df_apply.apply(lambda row: row["amount"] * row["quantity"], axis=1)
print("\n--- apply row-wise ---")
print(df_apply)

# ----- map — for mapping values using a dictionary -----
tier_map = {"C001": "Gold", "C002": "Silver", "C003": "Gold", "C004": "Bronze", "C005": "Silver"}
df_apply["tier"] = df_apply["customer_id"].map(tier_map)
print("\n--- map with dictionary ---")
print(df_apply)

# ----- replace — substitute specific values -----
df_replace = df_apply.copy()
df_replace["amount_tier"] = df_replace["amount_tier"].replace({"High": "Premium", "Low": "Budget"})
print("\n--- replace ---")
print(df_replace[["amount", "amount_tier"]])

# ----- When to use what -----
# apply():   for complex logic, row-wise operations, custom functions
# map():     for simple 1-to-1 value substitution from a dict or function
# replace(): for replacing specific values
# vectorized ops: ALWAYS prefer df["a"] * df["b"] over apply when possible (10-100x faster)
print()

# %% SECTION 12: String Operations
# =============================================================================
# SECTION 12: String Operations
# =============================================================================

print("=" * 60)
print("SECTION 12: String Operations")
print("=" * 60)

names = pd.Series(["  Alice Smith  ", "bob jones", "CHARLIE BROWN", "Diana Prince", None])

print("Original:", names.tolist())
print("lower:   ", names.str.lower().tolist())
print("upper:   ", names.str.upper().tolist())
print("title:   ", names.str.title().tolist())
print("strip:   ", names.str.strip().tolist())
print("contains:", names.str.contains("o", na=False).tolist())
print("len:     ", names.str.len().tolist())
print("split:   ", names.str.strip().str.split(" ").tolist())

# Extract first name
print("1st name:", names.str.strip().str.split(" ").str[0].tolist())
print()

# %% SECTION 13: DateTime Operations
# =============================================================================
# SECTION 13: DateTime Operations
# =============================================================================

print("=" * 60)
print("SECTION 13: DateTime Operations")
print("=" * 60)

# Our 'sales' DataFrame already has a datetime column.
# If it were a string, convert with: pd.to_datetime(df["date"])

print("Date column dtype:", sales["date"].dtype)

# ----- Extract components -----
sales_dt = sales.copy()
sales_dt["year"] = sales_dt["date"].dt.year
sales_dt["month"] = sales_dt["date"].dt.month
sales_dt["day_name"] = sales_dt["date"].dt.day_name()
sales_dt["week"] = sales_dt["date"].dt.isocalendar().week

print("\n--- Extracted date parts ---")
print(sales_dt[["date", "year", "month", "day_name", "week"]].head())

# ----- Resample: group by time periods -----
# First set date as index
ts = sales.set_index("date")

weekly = ts["amount"].resample("W").sum()
print("\n--- Weekly total sales ---")
print(weekly.head())

monthly = ts["amount"].resample("ME").agg(["sum", "mean", "count"])
print("\n--- Monthly stats ---")
print(monthly)

# ----- Filter by date range -----
jan_sales = sales[(sales["date"] >= "2026-01-01") & (sales["date"] < "2026-02-01")]
print(f"\nJanuary transactions: {len(jan_sales)}")
print()

# %% SECTION 14: Pivot Tables & Crosstab
# =============================================================================
# SECTION 14: Pivot Tables & Crosstab
# =============================================================================

print("=" * 60)
print("SECTION 14: Pivot Tables & Crosstab")
print("=" * 60)

# ----- pivot_table: like Excel pivot tables -----
pivot = sales.pivot_table(
    values="amount",
    index="product_category",
    columns="city",
    aggfunc="sum",
    fill_value=0
)
print("\n--- Pivot: total sales by category × city ---")
print(pivot.round(2))

# With margins (row/column totals)
pivot_margins = sales.pivot_table(
    values="amount",
    index="product_category",
    aggfunc=["sum", "mean", "count"],
    margins=True
)
print("\n--- Pivot with margins ---")
print(pivot_margins.round(2))

# ----- crosstab: frequency table -----
ct = pd.crosstab(sales["product_category"], sales["city"])
print("\n--- Crosstab: count of transactions by category × city ---")
print(ct)

# Normalize to get proportions
ct_pct = pd.crosstab(sales["product_category"], sales["city"], normalize="index")
print("\n--- Crosstab (% within each category) ---")
print(ct_pct.round(3))
print()

# %% SECTION 15: Window Functions (rolling, cumsum, rank)
# =============================================================================
# SECTION 15: Window Functions (rolling, cumsum, rank)
# =============================================================================

print("=" * 60)
print("SECTION 15: Window Functions")
print("=" * 60)

ts_sorted = sales.sort_values("date").copy()

# ----- Rolling (moving) average -----
ts_sorted["rolling_7d_avg"] = ts_sorted["amount"].rolling(window=7, min_periods=1).mean()
print("\n--- 7-day rolling average ---")
print(ts_sorted[["date", "amount", "rolling_7d_avg"]].head(10))

# ----- Cumulative sum -----
ts_sorted["cumulative_sales"] = ts_sorted["amount"].cumsum()
print("\n--- Cumulative sales ---")
print(ts_sorted[["date", "amount", "cumulative_sales"]].head(10))

# ----- rank() -----
ranked = sales.copy()
ranked["amount_rank"] = ranked["amount"].rank(ascending=False, method="dense")
print("\n--- Ranked by amount ---")
print(ranked.nsmallest(5, "amount_rank")[["customer_id", "amount", "amount_rank"]])

# ----- pct_change() — period-over-period change -----
daily_totals = sales.groupby("date")["amount"].sum().sort_index()
daily_pct = daily_totals.pct_change()
print("\n--- Day-over-day % change ---")
print(daily_pct.head(10).round(3))
print()

# %% SECTION 16: Reading & Writing Files
# =============================================================================
# SECTION 16: Reading & Writing Files
# =============================================================================

print("=" * 60)
print("SECTION 16: Reading & Writing Files")
print("=" * 60)

# ----- CSV -----
# df = pd.read_csv("file.csv")
# df = pd.read_csv("file.csv", usecols=["col1", "col2"])   # read only specific columns
# df = pd.read_csv("file.csv", nrows=1000)                  # read only first 1000 rows
# df = pd.read_csv("file.csv", dtype={"id": str})           # specify column types
# df.to_csv("output.csv", index=False)                      # save without row numbers

# ----- Excel -----
# df = pd.read_excel("file.xlsx", sheet_name="Sheet1")
# df.to_excel("output.xlsx", index=False)

# ----- JSON -----
# df = pd.read_json("file.json")
# df.to_json("output.json", orient="records")

# ----- Parquet (fast, compressed — preferred for large datasets) -----
# df = pd.read_parquet("file.parquet")
# df.to_parquet("output.parquet")

# ----- SQL -----
# import sqlite3
# conn = sqlite3.connect("database.db")
# df = pd.read_sql("SELECT * FROM table_name", conn)
# df.to_sql("table_name", conn, if_exists="replace", index=False)

print("See code comments for read/write examples.")
print("Key tip: use parquet for large datasets (10x faster than CSV, 5x smaller).")
print()

# %% SECTION 17: Method Chaining — Writing Clean Pandas Code
# =============================================================================
# SECTION 17: Method Chaining — Writing Clean Pandas Code
# =============================================================================

print("=" * 60)
print("SECTION 17: Method Chaining")
print("=" * 60)

# Method chaining lets you write a sequence of operations as one expression.
# This is the Pandas equivalent of a SQL query.

# ----- Without chaining (messy) -----
# temp = sales[sales["amount"] > 100]
# temp = temp.groupby("product_category")["amount"].sum()
# temp = temp.reset_index()
# temp.columns = ["category", "total"]
# temp = temp.sort_values("total", ascending=False)

# ----- With chaining (clean) -----
result = (
    sales
    [sales["amount"] > 100]
    .groupby("product_category")["amount"]
    .sum()
    .reset_index()
    .rename(columns={"product_category": "category", "amount": "total"})
    .sort_values("total", ascending=False)
)
print("\n--- Method chaining result ---")
print(result)

# ----- Use .assign() to add columns in a chain -----
result2 = (
    sales
    .assign(revenue=lambda df: df["amount"] * df["quantity"])
    .groupby("product_category")
    .agg(total_revenue=("revenue", "sum"), avg_revenue=("revenue", "mean"))
    .round(2)
    .sort_values("total_revenue", ascending=False)
)
print("\n--- assign + groupby chain ---")
print(result2)
print()

# %% SECTION 18: Performance Tips
# =============================================================================
# SECTION 18: Performance Tips
# =============================================================================

# 1. Use VECTORIZED operations, not loops:
#    BAD:  for i, row in df.iterrows(): df.loc[i, "new"] = row["a"] * 2
#    GOOD: df["new"] = df["a"] * 2

# 2. Use .query() for complex filters (can be faster than boolean indexing)

# 3. Use categorical dtype for low-cardinality string columns:
#    df["category"] = df["category"].astype("category")
#    Reduces memory by 90%+ for columns with few unique values

# 4. Use read_csv with usecols and dtype to avoid loading unnecessary data

# 5. For large datasets (>1GB), consider:
#    - Parquet instead of CSV (faster I/O, smaller files)
#    - Chunked reading: pd.read_csv("big.csv", chunksize=10000)
#    - Polars library (Rust-based, 10x faster than Pandas)

# %% SECTION 19: Practice Exercises (with solutions)
# =============================================================================
# SECTION 19: Practice Exercises (with solutions)
# =============================================================================

print("=" * 60)
print("SECTION 19: Practice Exercises")
print("=" * 60)

# Use the 'sales' DataFrame for all exercises.
# Try solving each one BEFORE looking at the solution below it.

# ----- Exercise 1 -----
# Find the total quantity sold per product category.
print("\n--- Ex 1: Total quantity per category ---")
ex1 = sales.groupby("product_category")["quantity"].sum().sort_values(ascending=False)
print(ex1)

# ----- Exercise 2 -----
# Find the customer who made the most transactions (by count).
print("\n--- Ex 2: Customer with most transactions ---")
ex2 = sales["customer_id"].value_counts().head(1)
print(ex2)

# ----- Exercise 3 -----
# Calculate the average amount per transaction for each city,
# but only include cities with more than 15 transactions.
print("\n--- Ex 3: Avg amount for cities with >15 transactions ---")
ex3 = (
    sales.groupby("city")
    .agg(avg_amount=("amount", "mean"), count=("amount", "count"))
    .query("count > 15")
    .round(2)
)
print(ex3)

# ----- Exercise 4 -----
# Create a column 'amount_pct_of_total' showing each transaction's
# amount as a percentage of the total sales.
print("\n--- Ex 4: Each transaction as % of total ---")
ex4 = sales.copy()
ex4["amount_pct_of_total"] = (ex4["amount"] / ex4["amount"].sum() * 100).round(3)
print(ex4[["customer_id", "amount", "amount_pct_of_total"]].head())

# ----- Exercise 5 -----
# For each customer, find their MOST purchased product category.
print("\n--- Ex 5: Most purchased category per customer ---")
ex5 = (
    sales.groupby(["customer_id", "product_category"])
    .size()
    .reset_index(name="count")
    .sort_values("count", ascending=False)
    .drop_duplicates(subset="customer_id")
    [["customer_id", "product_category", "count"]]
)
print(ex5)

# ----- Exercise 6 -----
# Calculate the percentage of total sales that each category represents.
print("\n--- Ex 6: Category share of total sales ---")
ex6 = (
    sales.groupby("product_category")["amount"]
    .sum()
    .pipe(lambda s: (s / s.sum() * 100).round(2))
    .sort_values(ascending=False)
)
print(ex6)

# ----- Exercise 7 -----
# Find all transactions where the amount is above the average for that category.
print("\n--- Ex 7: Above-average transactions within each category ---")
sales_temp = sales.copy()
sales_temp["cat_avg"] = sales.groupby("product_category")["amount"].transform("mean")
ex7 = sales_temp[sales_temp["amount"] > sales_temp["cat_avg"]]
print(f"{len(ex7)} transactions above their category average")
print(ex7[["customer_id", "product_category", "amount", "cat_avg"]].head())

# ----- Exercise 8 -----
# Create a cross-tabulation showing avg amount by customer × category.
print("\n--- Ex 8: Avg amount by customer × category ---")
ex8 = sales.pivot_table(
    values="amount", index="customer_id",
    columns="product_category", aggfunc="mean"
).round(2)
print(ex8)

# ----- Exercise 9 -----
# Find the date with the highest total sales.
print("\n--- Ex 9: Date with highest total sales ---")
ex9 = sales.groupby("date")["amount"].sum().idxmax()
print(f"Best day: {ex9}, Total: ${sales.groupby('date')['amount'].sum().max():.2f}")

# ----- Exercise 10 -----
# For each customer, calculate the running total of their purchases over time.
print("\n--- Ex 10: Running total per customer ---")
ex10 = (
    sales.sort_values("date")
    .assign(running_total=sales.sort_values("date").groupby("customer_id")["amount"].cumsum())
)
print(ex10[["date", "customer_id", "amount", "running_total"]].head(10))
print()

# %% SECTION 20: Interview-Style Problems (Applied Scientist / FDE)
# =============================================================================
# SECTION 20: Interview-Style Problems (Applied Scientist / FDE)
# =============================================================================

print("=" * 60)
print("SECTION 20: Interview-Style Problems")
print("=" * 60)

# These are the types of Pandas questions asked in Applied Scientist
# and Forward Deployed Engineer interviews.

# ----- Problem 1: Cohort Retention -----
# "Given transaction data, for each customer find their first purchase month,
#  then check if they made a purchase in the following month."
print("\n--- Interview Q1: Cohort — first purchase month per customer ---")
cohort = sales.copy()
cohort["month"] = cohort["date"].dt.to_period("M")
first_purchase = cohort.groupby("customer_id")["month"].min().reset_index()
first_purchase.columns = ["customer_id", "cohort_month"]
print(first_purchase)

# ----- Problem 2: Year-over-Year Growth -----
# "Calculate the month-over-month growth rate of total sales."
print("\n--- Interview Q2: Month-over-month growth ---")
monthly_sales = sales.set_index("date")["amount"].resample("ME").sum()
mom_growth = monthly_sales.pct_change() * 100
print(pd.DataFrame({"total": monthly_sales, "growth_pct": mom_growth.round(2)}))

# ----- Problem 3: Pareto Analysis (80/20 rule) -----
# "What percentage of customers account for 80% of total sales?"
print("\n--- Interview Q3: Pareto — which customers drive 80% of sales ---")
cust_sales = (
    sales.groupby("customer_id")["amount"]
    .sum()
    .sort_values(ascending=False)
)
cust_sales_pct = (cust_sales.cumsum() / cust_sales.sum() * 100).round(2)
pareto_df = pd.DataFrame({
    "total_sales": cust_sales.round(2),
    "cumulative_pct": cust_sales_pct
})
print(pareto_df)
customers_for_80 = (cust_sales_pct <= 80).sum() + 1
print(f"\n{customers_for_80} out of {len(cust_sales)} customers account for ~80% of sales")

# ----- Problem 4: RFM Analysis -----
# "Compute Recency, Frequency, Monetary value for each customer."
print("\n--- Interview Q4: RFM Analysis ---")
reference_date = sales["date"].max() + pd.Timedelta(days=1)
rfm = sales.groupby("customer_id").agg(
    recency=("date", lambda x: (reference_date - x.max()).days),
    frequency=("date", "count"),
    monetary=("amount", "sum")
).round(2)
print(rfm)

# ----- Problem 5: Detect Anomalies -----
# "Flag transactions where the amount is more than 2 standard deviations
#  from the mean of that product category."
print("\n--- Interview Q5: Anomaly detection ---")
stats = sales.groupby("product_category")["amount"].agg(["mean", "std"])
anomalies = sales.merge(stats, left_on="product_category", right_index=True)
anomalies["z_score"] = (anomalies["amount"] - anomalies["mean"]) / anomalies["std"]
flagged = anomalies[anomalies["z_score"].abs() > 2]
print(f"Anomalous transactions (|z| > 2): {len(flagged)}")
if len(flagged) > 0:
    print(flagged[["date", "customer_id", "amount", "product_category", "z_score"]].head())

# ----- Problem 6: Basket Analysis -----
# "For each transaction date × customer, what categories did they buy together?"
print("\n--- Interview Q6: What categories are bought together ---")
baskets = (
    sales.groupby(["date", "customer_id"])["product_category"]
    .apply(lambda x: ", ".join(sorted(x.unique())))
    .reset_index()
    .rename(columns={"product_category": "basket"})
)
multi_category = baskets[baskets["basket"].str.contains(",")]
print(f"Multi-category baskets: {len(multi_category)}")
print(multi_category.head())
print()

# %% SECTION 21: Capstone — Customer Transaction Analysis
# =============================================================================
# SECTION 21: Capstone — Customer Transaction Analysis
# =============================================================================

print("=" * 60)
print("SECTION 21: Capstone — Transaction Analysis from CSV")
print("=" * 60)

REQUIRED_COLUMNS = {"date", "customer_id", "amount", "product_category"}


def load_transactions(filepath: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{filepath}' not found.")

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    return df


def total_sales_by_category(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("product_category")["amount"]
        .sum()
        .reset_index()
        .rename(columns={"amount": "total_sales"})
        .sort_values("total_sales", ascending=False)
    )


def top_customers(df: pd.DataFrame, n: int = 3) -> pd.DataFrame:
    return (
        df.groupby("customer_id")["amount"]
        .sum()
        .reset_index()
        .rename(columns={"amount": "total_amount"})
        .nlargest(n, "total_amount")
    )


def save_results(category_sales: pd.DataFrame, top_custs: pd.DataFrame, filepath: str):
    with open(filepath, "w") as f:
        f.write("Total Sales by Product Category\n")
        category_sales.to_csv(f, index=False)
        f.write("\nTop 3 Customers by Total Amount\n")
        top_custs.to_csv(f, index=False)


csv_path = os.path.join(SCRIPT_DIR, "transactions.csv")
if os.path.exists(csv_path):
    txn = load_transactions(csv_path)

    category_sales = total_sales_by_category(txn)
    print("\nTotal Sales by Product Category:")
    print(category_sales.to_string(index=False))

    top_custs = top_customers(txn, n=3)
    print("\nTop 3 Customers by Total Amount:")
    print(top_custs.to_string(index=False))

    output_path = os.path.join(SCRIPT_DIR, "analysis.csv")
    save_results(category_sales, top_custs, output_path)
    print(f"\nResults saved to {output_path}")
else:
    print(f"\nSkipping capstone: {csv_path} not found.")
    print("Create a transactions.csv with columns: date, customer_id, amount, product_category")


# =============================================================================
# Quick Reference Card — Functions You'll Use 90% of the Time
# =============================================================================

# | Task                    | Function                                          |
# |-------------------------|---------------------------------------------------|
# | Read data               | pd.read_csv(), pd.read_excel(), pd.read_parquet() |
# | First look              | df.head(), df.shape, df.info(), df.describe()     |
# | Select columns          | df["col"], df[["col1", "col2"]]                   |
# | Filter rows             | df[df["col"] > value], df.query("col > value")    |
# | Sort                    | df.sort_values("col"), df.nlargest(5, "col")      |
# | Group + aggregate       | df.groupby("col")["val"].sum()                    |
# | Multiple aggs           | df.groupby("col").agg(name=("col", "func"))       |
# | Join tables             | pd.merge(df1, df2, on="key", how="left")          |
# | Stack tables            | pd.concat([df1, df2])                             |
# | Missing data            | df.isnull().sum(), df.fillna(), df.dropna()        |
# | Add columns             | df["new"] = ..., df.assign(new=lambda df: ...)     |
# | Apply function          | df["col"].apply(func), df.apply(func, axis=1)     |
# | Pivot table             | df.pivot_table(values, index, columns, aggfunc)    |
# | Time grouping           | df.resample("M").sum()                             |
# | Rolling window          | df["col"].rolling(7).mean()                        |
# | Cumulative              | df["col"].cumsum()                                 |
# | Rank                    | df["col"].rank()                                   |
# | Save                    | df.to_csv(), df.to_parquet(), df.to_excel()        |
