"""
==============================================================================
Object Oriented Programming (OOP) — Complete Guide for Interviews
==============================================================================

Object Oriented Programming - coding a real-world problem by using object-oriented principles
Object Oriented Design - mapping the real-world problem into object-oriented principles

- Python is not purely OOP (you can write procedural code too)
- A language is purely OOP if EVERYTHING is an object (Java, C# are closer)
- Python supports OOP but also allows functional and procedural styles

OOP Principles (the 4 pillars):
    1. Encapsulation  — bundling data + methods together, controlling access
    2. Abstraction    — hiding complex details, showing only what's necessary
    3. Inheritance    — creating new classes from existing ones (code reuse)
    4. Polymorphism   — same interface, different behavior

OOP is very useful when building complex software:
    - C/C++ built Unix OS using OOP principles
    - Every major framework (Django, Flask, React) uses OOP internally
    - Database ORMs, game engines, GUI frameworks — all OOP

Table of Contents:
    Section 1:  Why OOP? The NVT Technique
    Section 2:  Classes and Objects — The Basics
    Section 3:  The __init__ Constructor and self
    Section 4:  Instance Variables vs Class Variables
    Section 5:  Methods (Instance, Class, Static)
    Section 6:  Encapsulation & Access Control
    Section 7:  Inheritance
    Section 8:  Polymorphism
    Section 9:  Magic/Dunder Methods
    Section 10: @property Decorator (Getters & Setters)
    Section 11: Composition vs Inheritance
    Section 12: Abstract Classes
    Section 13: Real-World OOP Design Example
    Section 14: Interview Questions & Practice
"""


# =============================================================================
# SECTION 1: Why OOP? The NVT Technique
# =============================================================================

# ----- When to use OOP vs Procedural code -----
#
# Procedural (functions only):
#   Good for: scripts, data pipelines, small utilities, one-off analysis
#   Example: a script that reads a CSV and computes statistics
#
# OOP (classes + objects):
#   Good for: large systems, reusable components, modeling real-world entities
#   Example: a web app with Users, Orders, Products, Payments
#
# Rule of thumb: if you have MULTIPLE related pieces of data that share
# behavior, use a class. If it's a one-shot operation, use a function.

# ----- NVT Technique (Noun Verb Technique) -----
#
# This is how you design OOP systems from a problem statement:
#
# Example: Build a website for a driving school
# Requirements:
# - Customer will come to the website
# - Customer will register on the website
# - They will book a slot (there can be multiple slots)
# - Customer selects from multiple slots which get added to the cart
# - They will make a payment
# - Registration is successful
#
# Step 1: Identify NOUNS → these become CLASSES
#   Customer, Slot, Cart, Payment, Registration
#
# Step 2: Identify VERBS → these become METHODS
#   register(), book(), add_to_cart(), make_payment()
#
# Step 3: Identify ADJECTIVES/PROPERTIES → these become ATTRIBUTES
#   customer_name, customer_email, slot_time, slot_date, cart_items, amount
#
# This technique works for ANY interview design question:
#   "Design a parking lot"  → Car, ParkingSpot, ParkingLot, Ticket
#   "Design a library"      → Book, Member, Librarian, Loan
#   "Design Twitter"        → User, Tweet, Timeline, Notification


# =============================================================================
# SECTION 2: Classes and Objects — The Basics
# =============================================================================

# ----- What is a Class? -----
#
# A class is a USER-DEFINED DATA TYPE — a blueprint/template for creating objects.
# It bundles DATA (attributes) and BEHAVIOR (methods) together.
#
#   class = blueprint      (like an architect's plan for a house)
#   object = instance      (like the actual house built from that plan)
#
# You can create MANY objects from ONE class, just like building
# many houses from the same blueprint.

# In Python, EVERYTHING is an object:
a = 5
print(type(a))       # <class 'int'> — 'a' is an object of the 'int' class
print(type("hello")) # <class 'str'> — strings are objects of the 'str' class

# dir() shows all methods and attributes available on a class/object:
# dir(int)   # shows __add__, __mul__, bit_length, etc.
# dir(str)   # shows upper, lower, split, join, etc.

# ----- Simplest class -----

class Dog:
    pass   # 'pass' means "empty body" — placeholder

# Creating objects (also called "instantiation"):
dog1 = Dog()   # dog1 is an OBJECT (instance) of the Dog class
dog2 = Dog()   # dog2 is a DIFFERENT object of the same class

print(type(dog1))         # <class '__main__.Dog'>
print(dog1 is dog2)       # False — they are separate objects in memory
print(id(dog1), id(dog2)) # different memory addresses

# ----- Class with attributes and methods -----

class Dog2:
    # This is a METHOD — a function defined inside a class
    def bark(self):     # 'self' refers to the specific object calling this method
        print("Woof!")

    def sit(self):
        print("*sits down*")

my_dog = Dog2()
my_dog.bark()    # Output: Woof!
my_dog.sit()     # Output: *sits down*

# The DOT (.) operator is how you access an object's methods and attributes:
#   object.method()     — call a method
#   object.attribute    — access data

print()


# =============================================================================
# SECTION 3: The __init__ Constructor and 'self'
# =============================================================================

# ----- What is __init__? -----
#
# __init__ is a SPECIAL METHOD called the CONSTRUCTOR.
# It runs AUTOMATICALLY when you create a new object.
# You do NOT call it yourself — Python calls it for you.
#
# Purpose: initialize the object's attributes (set up its initial state).

# ----- What is 'self'? -----
#
# 'self' is a reference to THE SPECIFIC OBJECT being created/used.
# When you write self.name = "Buddy", you're saying:
#   "THIS particular object's name attribute is 'Buddy'"
#
# 'self' is NOT a keyword — it's a convention. You could name it anything,
# but ALWAYS use 'self'. Every method in a class must have 'self' as
# its first parameter.
#
# Think of it this way:
#   class Dog:
#       def bark(self):    ← self = whichever dog object called .bark()
#
#   dog1.bark()  → self = dog1
#   dog2.bark()  → self = dog2

class Employee:
    def __init__(self, eid, ename, esalary):
        # These are INSTANCE ATTRIBUTES — each object gets its own copy
        self.eid = eid          # self.eid belongs to THIS specific employee
        self.ename = ename      # self.ename belongs to THIS specific employee
        self.esalary = esalary

    def display(self):
        print(f"ID: {self.eid}, Name: {self.ename}, Salary: ${self.esalary:,}")

# Creating objects — __init__ runs automatically for each
emp1 = Employee(5301, "Mayur", 50000)
emp2 = Employee(5302, "Priya", 65000)

emp1.display()   # ID: 5301, Name: Mayur, Salary: $50,000
emp2.display()   # ID: 5302, Name: Priya, Salary: $65,000

# Each object has its OWN copy of the attributes:
print(emp1.ename)   # Mayur
print(emp2.ename)   # Priya — different object, different data

# ----- Why put code in __init__? -----
#
# We keep code inside the constructor whose control we don't want to give
# to the users. It runs automatically — no choice.
#
# Analogy: When you turn on a computer:
#   1. BIOS setup runs automatically (you don't control it)
#   2. Bootstrap program loads the OS into RAM
#   These are like __init__ — they run without you asking.
#
# Analogy: ATM Machine:
#   When you insert a card, authentication starts automatically.
#   You don't manually call "authenticate()" — the machine does it.

print()


# =============================================================================
# SECTION 4: Instance Variables vs Class Variables
# =============================================================================

# ----- Instance Variables -----
# Defined with self.variable_name inside __init__
# Each object gets its OWN copy
# Changing one object's variable does NOT affect other objects

# ----- Class Variables -----
# Defined OUTSIDE __init__, directly in the class body
# SHARED by ALL objects of that class
# Changing it affects ALL objects (unless overridden on an instance)

class Employee2:
    # CLASS VARIABLE — shared by all employees
    company = "Google"
    employee_count = 0

    def __init__(self, name, salary):
        # INSTANCE VARIABLES — unique to each employee
        self.name = name
        self.salary = salary
        Employee2.employee_count += 1   # increment the shared counter

    def display(self):
        # Can access both instance and class variables
        print(f"{self.name} works at {Employee2.company}, earns ${self.salary:,}")

e1 = Employee2("Alice", 150000)
e2 = Employee2("Bob", 130000)
e3 = Employee2("Charlie", 145000)

e1.display()   # Alice works at Google, earns $150,000
e2.display()   # Bob works at Google, earns $130,000

print(f"Total employees: {Employee2.employee_count}")   # 3

# Changing the class variable affects ALL objects:
Employee2.company = "Meta"
e1.display()   # Alice works at Meta
e2.display()   # Bob works at Meta

# ----- When to use which? -----
# Instance variable: data that differs per object (name, salary, ID)
# Class variable: data shared across all objects (company name, count, tax rate)

print()


# =============================================================================
# SECTION 5: Methods — Instance, Class, and Static
# =============================================================================

class MathUtils:
    pi = 3.14159   # class variable

    def __init__(self, value):
        self.value = value   # instance variable

    # ----- Instance Method -----
    # Has access to the instance (self) AND the class
    # Use when: the method needs to read/modify instance data
    def double(self):
        return self.value * 2

    # ----- Class Method -----
    # Uses @classmethod decorator. First param is 'cls' (the class itself)
    # Has access to class variables but NOT instance variables
    # Use when: the method works with class-level data, or as an alternative constructor
    @classmethod
    def circle_area(cls, radius):
        return cls.pi * radius ** 2   # uses class variable 'pi'

    # ----- Static Method -----
    # Uses @staticmethod decorator. No 'self' or 'cls' parameter
    # Has NO access to instance or class data
    # Use when: the method is logically related to the class but doesn't
    # need any instance/class data. It's just a regular function living inside the class.
    @staticmethod
    def add(a, b):
        return a + b

m = MathUtils(5)
print(m.double())                    # 10 (instance method — uses self.value)
print(MathUtils.circle_area(7))      # 153.93... (class method — uses cls.pi)
print(MathUtils.add(3, 4))           # 7 (static method — no self or cls needed)

# ----- Interview tip -----
# | Method Type | First Param | Can Access          | Use For                    |
# |-------------|-------------|---------------------|----------------------------|
# | Instance    | self        | Instance + Class    | Most methods               |
# | Class       | cls         | Class only          | Factory methods, counters  |
# | Static      | (none)      | Neither             | Utility/helper functions   |

print()


# =============================================================================
# SECTION 6: Encapsulation & Access Control
# =============================================================================

# Encapsulation = bundling data + methods AND controlling access to that data.
#
# In Python, there are NO truly private variables (unlike Java/C++).
# Instead, we use NAMING CONVENTIONS to signal access levels:
#
#   public:     name         → accessible from anywhere
#   protected:  _name        → "don't touch from outside" (convention, not enforced)
#   private:    __name       → name mangling makes it harder to access (but not impossible)

class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner          # PUBLIC: anyone can read/write
        self._account_type = "Savings"  # PROTECTED: convention says "internal use"
        self.__balance = balance    # PRIVATE: name-mangled to _BankAccount__balance

    # Public method to safely access private data
    def get_balance(self):
        return self.__balance

    # Public method to safely modify private data (with validation)
    def deposit(self, amount):
        if amount <= 0:
            print("Deposit must be positive!")
            return
        self.__balance += amount
        print(f"Deposited ${amount:,}. New balance: ${self.__balance:,}")

    def withdraw(self, amount):
        if amount > self.__balance:
            print("Insufficient funds!")
            return
        self.__balance -= amount
        print(f"Withdrew ${amount:,}. New balance: ${self.__balance:,}")

acc = BankAccount("Alice", 10000)

# Public: works fine
print(acc.owner)              # Alice

# Protected: works but convention says don't use externally
print(acc._account_type)      # Savings (no error, but bad practice)

# Private: raises AttributeError
# print(acc.__balance)        # AttributeError: 'BankAccount' has no attribute '__balance'

# But you CAN access it via name mangling (Python doesn't truly enforce privacy):
print(acc._BankAccount__balance)   # 10000 (works but NEVER do this)

# The RIGHT way: use the public methods
print(acc.get_balance())      # 10000
acc.deposit(5000)             # Deposited $5,000. New balance: $15,000
acc.withdraw(3000)            # Withdrew $3,000. New balance: $12,000
acc.withdraw(50000)           # Insufficient funds!

# ----- Why encapsulation matters -----
# Without it: anyone can do acc.balance = -999999 (invalid state!)
# With it: all changes go through deposit/withdraw which validate the data.
# This is called "data hiding" — one of the OOP principles.

print()


# =============================================================================
# SECTION 7: Inheritance — Code Reuse Through Hierarchy
# =============================================================================

# Inheritance lets you create a NEW class based on an EXISTING class.
# The new class inherits all attributes and methods from the parent.
#
#   Parent class (superclass, base class) → has the shared code
#   Child class (subclass, derived class) → inherits + extends/overrides
#
# Analogy: Animal is a parent. Dog and Cat are children.
# Both Dog and Cat can eat() and sleep() (inherited from Animal),
# but Dog barks and Cat meows (their own methods).

# ----- Single Inheritance -----

class Animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species

    def speak(self):
        print(f"{self.name} makes a sound")

    def info(self):
        print(f"{self.name} is a {self.species}")


class Dog3(Animal):   # Dog3 INHERITS from Animal
    def __init__(self, name, breed):
        # super() calls the parent's __init__
        # This avoids duplicating the initialization code
        super().__init__(name, species="Dog")
        self.breed = breed   # Dog-specific attribute

    # METHOD OVERRIDING: replacing the parent's method with a new version
    def speak(self):
        print(f"{self.name} says: Woof!")

    # Dog-specific method (not in Animal)
    def fetch(self):
        print(f"{self.name} fetches the ball!")


class Cat(Animal):
    def __init__(self, name, indoor):
        super().__init__(name, species="Cat")
        self.indoor = indoor

    def speak(self):
        print(f"{self.name} says: Meow!")


dog = Dog3("Rex", "German Shepherd")
cat = Cat("Whiskers", True)

dog.info()    # Rex is a Dog       (inherited from Animal)
dog.speak()   # Rex says: Woof!    (overridden in Dog3)
dog.fetch()   # Rex fetches the ball!  (Dog-specific)

cat.info()    # Whiskers is a Cat  (inherited from Animal)
cat.speak()   # Whiskers says: Meow!  (overridden in Cat)

# isinstance() checks if an object is an instance of a class (or its parent)
print(isinstance(dog, Dog3))      # True
print(isinstance(dog, Animal))    # True (Dog3 IS an Animal)
print(isinstance(dog, Cat))       # False

# issubclass() checks class hierarchy
print(issubclass(Dog3, Animal))   # True
print(issubclass(Cat, Animal))    # True

print()

# ----- Multilevel Inheritance -----
# Grandparent → Parent → Child

class Vehicle:
    def __init__(self, brand):
        self.brand = brand

class Car(Vehicle):
    def __init__(self, brand, model):
        super().__init__(brand)
        self.model = model

class ElectricCar(Car):
    def __init__(self, brand, model, battery_kwh):
        super().__init__(brand, model)
        self.battery_kwh = battery_kwh

    def display(self):
        print(f"{self.brand} {self.model} — {self.battery_kwh}kWh battery")

tesla = ElectricCar("Tesla", "Model 3", 75)
tesla.display()   # Tesla Model 3 — 75kWh battery

print()

# ----- Multiple Inheritance -----
# A class can inherit from MORE THAN ONE parent class.
# Python uses MRO (Method Resolution Order) to decide which parent's method to call.

class Flyable:
    def fly(self):
        print("I can fly!")

class Swimmable:
    def swim(self):
        print("I can swim!")

class Duck(Animal, Flyable, Swimmable):
    def __init__(self, name):
        super().__init__(name, species="Duck")

    def speak(self):
        print(f"{self.name} says: Quack!")

donald = Duck("Donald")
donald.speak()   # Donald says: Quack!
donald.fly()     # I can fly!     (from Flyable)
donald.swim()    # I can swim!    (from Swimmable)

# MRO (Method Resolution Order) — the order Python searches for methods:
print(Duck.__mro__)
# Duck → Animal → Flyable → Swimmable → object

print()


# =============================================================================
# SECTION 8: Polymorphism — Same Interface, Different Behavior
# =============================================================================

# Polymorphism = "many forms"
# The SAME method name behaves DIFFERENTLY depending on the object.
#
# We already saw this: dog.speak() → "Woof", cat.speak() → "Meow"
# Same method name, different behavior. That's polymorphism.

# ----- Polymorphism with a common interface -----

def make_animal_speak(animal):
    """This function works with ANY animal — it doesn't care which type."""
    animal.speak()   # calls the appropriate version based on the object's class

make_animal_speak(dog)      # Rex says: Woof!
make_animal_speak(cat)      # Whiskers says: Meow!
make_animal_speak(donald)   # Donald says: Quack!

# This is powerful because make_animal_speak() doesn't need to know
# the specific type. It just calls .speak() and the right version runs.
# This is called "duck typing" in Python: "If it walks like a duck
# and quacks like a duck, treat it as a duck."

# ----- Operator Overloading -----
# Python lets you define how operators (+, -, ==, <, etc.) work on your objects.

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        """Define what + does for Vector objects."""
        return Vector(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        """Define what == does for Vector objects."""
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        """Define how the object looks when printed."""
        return f"Vector({self.x}, {self.y})"

v1 = Vector(1, 2)
v2 = Vector(3, 4)
v3 = v1 + v2          # calls v1.__add__(v2)
print(v3)              # Vector(4, 6)
print(v1 == v2)        # False
print(v1 == Vector(1, 2))  # True

print()


# =============================================================================
# SECTION 9: Magic/Dunder Methods (Double UNDERscore)
# =============================================================================

# Dunder methods are special methods surrounded by double underscores.
# Python calls them automatically in specific situations.
#
# | Method         | Called When                    | Example               |
# |----------------|--------------------------------|-----------------------|
# | __init__       | Object is created              | obj = MyClass()       |
# | __str__        | str(obj) or print(obj)         | print(obj)            |
# | __repr__       | repr(obj) or in REPL           | >>> obj               |
# | __len__        | len(obj)                       | len(my_list)          |
# | __eq__         | obj1 == obj2                   | a == b                |
# | __lt__         | obj1 < obj2                    | a < b                 |
# | __add__        | obj1 + obj2                    | a + b                 |
# | __getitem__    | obj[key]                       | lst[0]                |
# | __contains__   | item in obj                    | 5 in my_set           |
# | __iter__       | for item in obj                | for x in obj:         |
# | __del__        | Object is garbage collected     | del obj               |

class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def __str__(self):
        """Human-readable string (for print and str())."""
        return f"'{self.title}' by {self.author}"

    def __repr__(self):
        """Developer-readable string (for debugging, REPL)."""
        return f"Book('{self.title}', '{self.author}', {self.pages})"

    def __len__(self):
        """What len() returns for this object."""
        return self.pages

    def __eq__(self, other):
        """When are two books considered equal?"""
        return self.title == other.title and self.author == other.author

    def __lt__(self, other):
        """What does < mean for books? Compare by page count."""
        return self.pages < other.pages

book1 = Book("Clean Code", "Robert Martin", 464)
book2 = Book("Python Crash Course", "Eric Matthes", 544)
book3 = Book("Clean Code", "Robert Martin", 464)

print(book1)           # 'Clean Code' by Robert Martin  ← __str__
print(repr(book2))     # Book('Python Crash Course', 'Eric Matthes', 544)  ← __repr__
print(len(book1))      # 464  ← __len__
print(book1 == book3)  # True  ← __eq__
print(book1 < book2)   # True  ← __lt__ (464 < 544)

# Now we can even sort books!
books = [book2, book1]
books.sort()   # uses __lt__ to compare
print([str(b) for b in books])  # Clean Code first (fewer pages)

print()


# =============================================================================
# SECTION 10: @property Decorator — Pythonic Getters & Setters
# =============================================================================

# In Java/C++, you write explicit getter/setter methods:
#   get_name(), set_name(value)
#
# In Python, we use @property to make attribute access look natural
# while still controlling it behind the scenes.

class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius   # protected attribute

    @property
    def celsius(self):
        """Getter: called when you READ obj.celsius"""
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        """Setter: called when you WRITE obj.celsius = value"""
        if value < -273.15:
            raise ValueError("Temperature below absolute zero is not possible!")
        self._celsius = value

    @property
    def fahrenheit(self):
        """Computed property: calculated from celsius, not stored."""
        return self._celsius * 9/5 + 32

temp = Temperature(25)
print(temp.celsius)      # 25     ← calls the getter
print(temp.fahrenheit)   # 77.0   ← computed property

temp.celsius = 100       # calls the setter (validates!)
print(temp.fahrenheit)   # 212.0

# temp.celsius = -300    # Would raise ValueError!

# The beauty: from the outside, celsius and fahrenheit look like regular
# attributes. But behind the scenes, they're method calls with validation.

print()


# =============================================================================
# SECTION 11: Composition vs Inheritance
# =============================================================================

# ----- "Has-a" (Composition) vs "Is-a" (Inheritance) -----
#
# Inheritance: Dog IS AN Animal → class Dog(Animal)
# Composition: Car HAS AN Engine → Engine is an attribute of Car
#
# Rule of thumb: prefer composition over inheritance.
# Composition is more flexible and avoids deep inheritance chains.

class Engine:
    def __init__(self, horsepower, fuel_type):
        self.horsepower = horsepower
        self.fuel_type = fuel_type

    def start(self):
        print(f"{self.fuel_type} engine ({self.horsepower}hp) starting... Vroom!")

class Car2:
    def __init__(self, brand, model, engine):
        self.brand = brand
        self.model = model
        self.engine = engine   # COMPOSITION: Car HAS an Engine

    def drive(self):
        self.engine.start()
        print(f"{self.brand} {self.model} is driving!")

v8 = Engine(450, "Gasoline")
mustang = Car2("Ford", "Mustang", v8)
mustang.drive()
# Output:
#   Gasoline engine (450hp) starting... Vroom!
#   Ford Mustang is driving!

# The Engine is a separate, reusable component.
# You could put the same engine in a different car, or swap engines.
# This flexibility is why composition is often preferred.

print()


# =============================================================================
# SECTION 12: Abstract Classes
# =============================================================================

# An abstract class is a class that CAN'T be instantiated directly.
# It defines a TEMPLATE — child classes MUST implement certain methods.
#
# Use case: you want to enforce that all subclasses implement specific methods.

from abc import ABC, abstractmethod

class Shape(ABC):   # ABC = Abstract Base Class
    @abstractmethod
    def area(self):
        """Every shape MUST implement area(). No choice."""
        pass

    @abstractmethod
    def perimeter(self):
        """Every shape MUST implement perimeter()."""
        pass

    def describe(self):
        """Non-abstract method — inherited as-is."""
        print(f"This shape has area {self.area():.2f} and perimeter {self.perimeter():.2f}")


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2

    def perimeter(self):
        return 2 * 3.14159 * self.radius


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


# shape = Shape()   # TypeError: Can't instantiate abstract class!

circle = Circle(5)
rect = Rectangle(4, 6)

circle.describe()   # This shape has area 78.54 and perimeter 31.42
rect.describe()     # This shape has area 24.00 and perimeter 20.00

# Polymorphism with abstract classes:
shapes = [Circle(3), Rectangle(4, 5), Circle(7)]
total_area = sum(s.area() for s in shapes)
print(f"Total area of all shapes: {total_area:.2f}")

print()


# =============================================================================
# SECTION 13: Real-World OOP Design Example — E-Commerce System
# =============================================================================

# Let's apply everything to design a mini e-commerce system.
# This is the kind of design question you'd get in interviews.

class Product:
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

    def is_available(self):
        return self.stock > 0

    def __repr__(self):
        return f"{self.name} (${self.price:.2f})"


class CartItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    @property
    def subtotal(self):
        return self.product.price * self.quantity

    def __repr__(self):
        return f"{self.product.name} x{self.quantity} = ${self.subtotal:.2f}"


class ShoppingCart:
    def __init__(self):
        self.items = []   # COMPOSITION: Cart HAS items

    def add(self, product, quantity=1):
        if product.stock < quantity:
            print(f"Not enough stock for {product.name}!")
            return
        # Check if product already in cart
        for item in self.items:
            if item.product is product:
                item.quantity += quantity
                return
        self.items.append(CartItem(product, quantity))

    def remove(self, product_name):
        self.items = [item for item in self.items if item.product.name != product_name]

    @property
    def total(self):
        return sum(item.subtotal for item in self.items)

    def display(self):
        if not self.items:
            print("Cart is empty!")
            return
        print("--- Shopping Cart ---")
        for item in self.items:
            print(f"  {item}")
        print(f"  TOTAL: ${self.total:.2f}")

    def checkout(self):
        if not self.items:
            print("Nothing to checkout!")
            return
        for item in self.items:
            item.product.stock -= item.quantity
        total = self.total
        self.items.clear()
        print(f"Order placed! Total charged: ${total:.2f}")
        return total


# ----- Using the system -----
laptop = Product("MacBook Pro", 2499.99, 10)
phone = Product("iPhone 16", 999.99, 25)
case = Product("Phone Case", 29.99, 100)

cart = ShoppingCart()
cart.add(laptop)
cart.add(phone, 2)
cart.add(case, 3)
cart.display()
# --- Shopping Cart ---
#   MacBook Pro x1 = $2499.99
#   iPhone 16 x2 = $1999.98
#   Phone Case x3 = $89.97
#   TOTAL: $4589.94

cart.checkout()   # Order placed! Total charged: $4589.94
print(f"Laptops remaining in stock: {laptop.stock}")  # 9

print()


# =============================================================================
# SECTION 14: Interview Questions & Practice
# =============================================================================

# ----- Common OOP Interview Questions -----
#
# Q: What are the 4 pillars of OOP?
# A: Encapsulation (bundling data + methods + access control),
#    Abstraction (hiding complexity, showing simple interface),
#    Inheritance (creating classes from existing ones),
#    Polymorphism (same interface, different behavior).
#
# Q: What's the difference between a class and an object?
# A: A class is a blueprint/template. An object is an instance created from that blueprint.
#    class Dog is the blueprint; my_dog = Dog("Rex") creates an actual dog object.
#
# Q: What is 'self' in Python?
# A: 'self' is a reference to the current instance. When you call obj.method(),
#    Python passes obj as the first argument (self) automatically.
#
# Q: What's the difference between __str__ and __repr__?
# A: __str__ is for end users (human-readable). __repr__ is for developers
#    (unambiguous, ideally can recreate the object). print() uses __str__,
#    the REPL uses __repr__.
#
# Q: What is the difference between composition and inheritance?
# A: Inheritance = "is-a" (Dog is an Animal). Composition = "has-a" (Car has an Engine).
#    Prefer composition — it's more flexible and avoids tight coupling.
#
# Q: What is method resolution order (MRO)?
# A: The order Python searches for a method in multiple inheritance.
#    Uses C3 linearization. Check with ClassName.__mro__ or ClassName.mro().
#
# Q: Can you have truly private variables in Python?
# A: No. Python uses name mangling (__var → _ClassName__var) to make it harder
#    to access, but it's not truly private. Python philosophy: "We're all
#    consenting adults here."
#
# Q: What are abstract classes and when would you use them?
# A: Abstract classes can't be instantiated. They define a contract that
#    subclasses MUST follow. Use when you want to enforce that all subclasses
#    implement specific methods (e.g., all Shapes must have area()).
#
# Q: What is the diamond problem?
# A: In multiple inheritance, if A inherits from B and C, and both B and C
#    inherit from D, there's ambiguity about which path to follow.
#    Python solves this with MRO (C3 linearization).

# ----- Practice Exercises -----
#
# Exercise 1: Library System
#   Create classes: Book (title, author, isbn, available),
#   Member (name, member_id, borrowed_books),
#   Library (books, members, borrow_book(), return_book())
#
# Exercise 2: Bank System
#   Create classes: Account (with deposit, withdraw, transfer methods),
#   SavingsAccount (with interest calculation — inherits from Account),
#   CheckingAccount (with overdraft limit — inherits from Account)
#
# Exercise 3: School System
#   Create: Person (name, age), Student(Person) with grades,
#   Teacher(Person) with subjects, Classroom with students and teacher.
#   Implement GPA calculation and class average.
#
# Exercise 4: Design a Parking Lot (common interview question)
#   Classes: ParkingLot, ParkingSpot (small/medium/large),
#   Vehicle (Car, Motorcycle, Truck — inherit from Vehicle),
#   Ticket (entry_time, exit_time, calculate_fee())


# =============================================================================
# Quick Reference — OOP Concepts at a Glance
# =============================================================================

# | Concept              | What It Is                                          |
# |----------------------|-----------------------------------------------------|
# | Class                | Blueprint for objects (user-defined type)            |
# | Object               | Instance of a class (actual data in memory)          |
# | __init__             | Constructor — runs automatically on creation         |
# | self                 | Reference to the current instance                   |
# | Instance variable    | Data unique to each object (self.x)                 |
# | Class variable       | Data shared by all objects (ClassName.x)             |
# | Instance method      | Regular method with self — accesses instance data    |
# | @classmethod         | Method with cls — accesses class data only           |
# | @staticmethod        | Utility function inside a class — no self or cls     |
# | Encapsulation        | Bundle data + methods, control access (_x, __x)      |
# | Inheritance          | Child class gets parent's attributes and methods     |
# | super()              | Call parent class's method from child                |
# | Method overriding    | Child replaces parent's method with its own          |
# | Polymorphism         | Same method name, different behavior per class       |
# | Abstract class       | Template class that can't be instantiated (ABC)      |
# | @property            | Make method look like attribute access                |
# | Composition          | "Has-a" — object contains another object             |
# | Dunder methods       | __str__, __repr__, __add__, __eq__, __len__, etc.    |
# | MRO                  | Method Resolution Order for multiple inheritance     |
# | isinstance()         | Check if object is instance of a class               |
# | issubclass()         | Check if class is subclass of another                |
