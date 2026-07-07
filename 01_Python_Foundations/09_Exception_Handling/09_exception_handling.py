# =============================================================================
# SECTION 1: Basic Exception Handling
# =============================================================================
import os

if __name__ == "__main__":
    print("--- 1. FileNotFoundError ---")
    try:
        with open("non_existent_magic.txt", "r") as f:
            content = f.read()
    except FileNotFoundError as e:
        print(f"Caught an error! The file doesn't exist. Details: {e}")

    print("\n--- 2. ValueError and ZeroDivisionError ---")
    try:
        # ValueError simulation
        num = int("not_a_number") 
    except ValueError as e:
        print(f"ValueError caught: Cannot convert string to integer. Details: {e}")

    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        print(f"ZeroDivisionError caught: You can't divide by zero! Details: {e}")

    print("\n--- 3. Multiple Except Blocks (IndexError) ---")
    lst = [10, 20, 30]
    index = 5
    
    try:
        print(f"Trying to access index {index}...")
        val = lst[index]
    except IndexError as e:
        print(f"IndexError caught: Index out of bounds. Details: {e}")
    except Exception as e:
        # Fallback for anything else
        print(f"Generic exception caught: {e}")

# =============================================================================
# SECTION 2: Try / Except / Else / Finally
# =============================================================================

    print("\n--- 4. Full try/except/else/finally Flow (KeyError) ---")
    employee_info = {"Alice": "Engineer", "Bob": "Designer"}
    name = "unknown_person"
    
    try:
        print(f"Looking up {name}...")
        role = employee_info[name]
    except KeyError:
        print(f"KeyError: {name} is not in the database.")
    else:
        # This block ONLY runs if there was NO exception in the try block
        print(f"Success! Role is {role}")
    finally:
        # This block ALWAYS runs. Perfect for closing files or releasing resources.
        print("Database lookup complete (finally block executed).")

# =============================================================================
# SECTION 3: Bugs, Bad Practices, and Fixes
# =============================================================================

    print("\n--- 5. The Bare Except Warning ---")
    # BAD PRACTICE:
    # try:
    #     do_something()
    # except:
    #     pass
    # Why? It catches KeyboardInterrupt (Ctrl+C), making the program impossible to stop manually!
    
    # *** BUG (Original code snippet):
    # response = input("Yes or no?").lower  <-- Missing parentheses!
    # if response == 'yes': ...
    #
    # *** FIX:
    response_simulated = "Yes".lower()
    print(f"Fixed string method: {response_simulated}")

# =============================================================================
# SECTION 4: Custom Exceptions and Chaining
# =============================================================================

    print("\n--- 6. Custom Exceptions ---")
    
    # Define a custom exception by inheriting from Exception
    class InsufficientFundsError(Exception):
        pass

    class BankAccount:
        def __init__(self, balance):
            self.balance = balance
            
        def withdraw(self, amount):
            if amount > self.balance:
                raise InsufficientFundsError(f"Cannot withdraw {amount}. Balance is only {self.balance}.")
            self.balance -= amount
            return self.balance

    account = BankAccount(100)
    try:
        account.withdraw(500)
    except InsufficientFundsError as e:
        print(f"Custom Error Caught: {e}")

    print("\n--- 7. Exception Chaining ---")
    # Sometimes you catch one error but want to raise a different, more descriptive one.
    try:
        try:
            val = int("hello")
        except ValueError as original_error:
            # The 'from' keyword chains the exceptions together in the traceback
            raise RuntimeError("Failed to process user input") from original_error
    except RuntimeError as e:
        print(f"Caught chained exception: {e}")
        print(f"The original cause was: {e.__cause__}")

# =============================================================================
# SECTION 5: The `with` Statement
# =============================================================================

    print("\n--- 8. The `with` Statement (Context Manager) ---")
    # Create a temp file
    with open("temp_demo.txt", "w") as f:
        f.write("Hello context managers!")
        # File is automatically closed here!
        
    with open("temp_demo.txt", "r") as f:
        print("File contents:", f.read())
        
    # Cleanup
    os.remove("temp_demo.txt")

# === PRACTICE ZONE ===
def safe_divide(a, b):
    """Return a/b. Return None and print a helpful message if b is 0."""
    pass

def get_list_element(lst, index):
    """Return lst[index]. Return None if index is out of bounds."""
    pass
