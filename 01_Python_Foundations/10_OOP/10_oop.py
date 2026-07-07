# =============================================================================
# SECTION 1: Classes, Objects, and Variables
# =============================================================================
# NVT Example: Design a Library
# Nouns -> Book, Member. Verbs -> borrow, return.

class Dog:
    # CLASS VARIABLE: Shared across ALL instances of the class
    species = "Canis familiaris"

    def __init__(self, name, age):
        # INSTANCE VARIABLES: Unique to each object (created using 'self')
        self.name = name
        self.age = age

# =============================================================================
# SECTION 2: The Three Types of Methods
# =============================================================================

class MathUtils:
    history = []  # Class variable

    def __init__(self, value):
        self.value = value

    # 1. INSTANCE METHOD (takes self)
    def multiply(self, factor):
        result = self.value * factor
        MathUtils.history.append(f"Multiplied by {factor}")
        return result

    # 2. CLASS METHOD (takes cls)
    @classmethod
    def get_history(cls):
        return cls.history

    # 3. STATIC METHOD (takes neither self nor cls)
    @staticmethod
    def is_even(number):
        return number % 2 == 0

# =============================================================================
# SECTION 3: Encapsulation & @property
# =============================================================================

class Employee:
    def __init__(self, name, salary):
        self.name = name
        # The double underscore name-mangles the variable to make it "private"
        self.__salary = salary

    @property
    def salary(self):
        """Getter for salary"""
        return self.__salary

    @salary.setter
    def salary(self, new_salary):
        """Setter with validation"""
        if new_salary < 0:
            raise ValueError("Salary cannot be negative")
        self.__salary = new_salary

# =============================================================================
# SECTION 4: Inheritance, Polymorphism, and MRO
# =============================================================================

class Animal:
    def speak(self):
        return "Some generic sound"

class Cat(Animal):
    # Method Overriding (Polymorphism)
    def speak(self):
        return "Meow!"

class Bird(Animal):
    def speak(self):
        return "Tweet!"

class A:
    def show(self): print("A")
class B(A):
    def show(self): print("B")
class C(A):
    def show(self): print("C")
class D(B, C):
    pass

# =============================================================================
# SECTION 5: Magic/Dunder Methods
# =============================================================================

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        # Support for v1 + v2
        return Vector(self.x + other.x, self.y + other.y)

    def __str__(self):
        # Human-readable string for print()
        return f"Vector({self.x}, {self.y})"

    def __eq__(self, other):
        # Support for v1 == v2
        return self.x == other.x and self.y == other.y

# =============================================================================
# SECTION 6: Abstract Base Classes (ABC)
# =============================================================================
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, w, h):
        self.w = w
        self.h = h
    
    def area(self):
        return self.w * self.h

# =============================================================================
# SECTION 7: Real-World Example (Bank Account)
# =============================================================================

class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance  # Protected

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount

    def withdraw(self, amount):
        if 0 < amount <= self._balance:
            self._balance -= amount
            return True
        return False

class SavingsAccount(BankAccount):
    def __init__(self, owner, balance, interest_rate):
        super().__init__(owner, balance)  # Call parent constructor
        self.interest_rate = interest_rate

    def apply_interest(self):
        interest = self._balance * (self.interest_rate / 100)
        self.deposit(interest)

class CheckingAccount(BankAccount):
    def __init__(self, owner, balance, overdraft_limit):
        super().__init__(owner, balance)
        self.overdraft_limit = overdraft_limit

    # Overriding the parent's withdraw method
    def withdraw(self, amount):
        if 0 < amount <= (self._balance + self.overdraft_limit):
            self._balance -= amount
            return True
        return False

if __name__ == "__main__":
    print("--- 1. Class vs Instance Variables ---")
    dog1 = Dog("Rex", 3)
    dog2 = Dog("Buddy", 5)

    print(f"Dog1: {dog1.name}, Species: {dog1.species}")
    print(f"Dog2: {dog2.name}, Species: {dog2.species}")

    # Changing the class variable updates it for all (future) accesses!
    Dog.species = "Canis lupus familiaris"
    print(f"After class update -> Dog1 Species: {dog1.species}")

    print("\n--- 2. Method Types ---")
    math_obj = MathUtils(10)
    print(f"Instance Method output: {math_obj.multiply(5)}")
    print(f"Class Method output: {MathUtils.get_history()}")
    print(f"Static Method output: {MathUtils.is_even(10)}")

    print("\n--- 3. Encapsulation ---")
    emp = Employee("Alice", 50000)
    print(f"Initial Salary: {emp.salary}")  # Calls the getter
    
    emp.salary = 60000  # Calls the setter
    print(f"Updated Salary: {emp.salary}")
    
    try:
        emp.salary = -100  # Fails validation
    except ValueError as e:
        print(f"Validation caught error: {e}")

    print("\n--- 4. Inheritance and Polymorphism ---")
    # Polymorphism: same method name 'speak', different behavior
    animals = [Cat(), Bird(), Animal()]
    for a in animals:
        print(f"{type(a).__name__} says: {a.speak()}")

    print("\n--- 5. Method Resolution Order (MRO) ---")
    print(f"MRO for D: {[cls.__name__ for cls in D.__mro__]}")
    d_obj = D()
    d_obj.show()  # Prints B because D -> B -> C -> A

    print("\n--- 6. Magic Methods ---")
    v1 = Vector(2, 3)
    v2 = Vector(4, 5)
    v3 = v1 + v2  # Calls __add__
    print(f"v1 + v2 = {v3}")  # Calls __str__
    print(f"v3 == Vector(6, 8)? {v3 == Vector(6, 8)}")  # Calls __eq__

    print("\n--- 7. Abstract Classes ---")
    rect = Rectangle(4, 5)
    print(f"Rectangle Area: {rect.area()}")

    print("\n--- 8. Real-World Design ---")
    savings = SavingsAccount("Alice", 1000, 5.0)
    savings.apply_interest()
    print(f"Savings Balance after interest: {savings.balance}")

    checking = CheckingAccount("Bob", 500, 200)
    print(f"Checking withdrawal of 600 successful? {checking.withdraw(600)}")
    print(f"Checking Balance: {checking.balance}")

# === PRACTICE ZONE ===
# Implement these from scratch:

class AnimalPractice:
    """Implement: __init__(name, species), speak() method, __str__"""
    pass

class DogPractice(AnimalPractice):
    """Override speak() to return 'Woof!'"""
    pass

class ShapePractice(ABC):
    """Abstract base with abstract area() and perimeter() methods"""
    pass
