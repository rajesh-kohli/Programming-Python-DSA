"""
OOP Practice File
=================
This file combines OOP theory, data structure implementations, and small real-world
examples that are commonly covered in class.

Core OOP concepts covered:
- class and object
- attributes and methods
- constructor (__init__)
- self reference
- encapsulation
- inheritance
- polymorphism

Data structures covered:
- Stack (LIFO)
- Queue (FIFO)
- Undirected Graph
- Directed Graph

Other concepts covered:
- Prefix / Postfix (Polish notation) expression evaluation
- Friend recommendation system (graph + OOP combined)

Useful real-world use cases:
- Browser back/forward navigation -> Stack
- Customer service / print queue -> Queue
- Social networks / friend recommendations -> Graph
- Banking application -> OOP class design
- Compilers / expression evaluators -> Postfix/Prefix notation
"""

# -------------------------------------------------------------------
# 1. OOP Basics
# -------------------------------------------------------------------
"""
Class:
A class is a blueprint for creating objects.

Object:
An object is an instance of a class.

Constructor (__init__):
A special method that runs automatically when an object is created.
It is used to initialize attributes.

self:
A reference to the current object. It lets us access attributes and methods
inside the class.

Encapsulation:
Protecting internal data and allowing access through controlled methods.
This is why we often use methods like deposit(), withdraw(), etc.

Visual - one class, many independent objects:

    class BankAccount        account1 = BankAccount("Ravi", 1000)
    (the blueprint)          account2 = BankAccount("Asha", 500)
    +----------------+
    | account_holder |       account1            account2
    | _balance       |       +---------------+   +---------------+
    | deposit()      |  -->  | Ravi  | 1000  |   | Asha  | 500   |
    | withdraw()     |       +---------------+   +---------------+
    | get_balance()  |       (its own _balance)  (its own _balance)
    +----------------+

Each object gets its own copy of the attributes, but they all share
the same methods defined on the class. `self` is what lets a method
know *which* object's data to work on.
"""


class BankAccount:
    def __init__(self, account_holder, balance=0):
        """Create a bank account with an account holder and balance."""
        self.account_holder = account_holder
        self._balance = balance  # protected attribute

    def deposit(self, amount):
        """Deposit money into the account."""
        if amount > 0:
            self._balance += amount
            return f"Deposited {amount}. New balance: {self._balance}"
        return "Amount must be positive"

    def withdraw(self, amount):
        """Withdraw money if enough balance is available."""
        if amount > 0 and amount <= self._balance:
            self._balance -= amount
            return f"Withdrew {amount}. Remaining balance: {self._balance}"
        return "Insufficient balance"

    def get_balance(self):
        """Return the current balance."""
        return self._balance


class Student:
    def __init__(self, name, marks):
        """Create a student object with a name and marks."""
        self.name = name
        self.marks = marks

    def add_mark(self, mark):
        """Add a new mark to the student record."""
        self.marks.append(mark)

    def calculate_average(self):
        """Return the average of all marks."""
        if not self.marks:
            return 0
        return sum(self.marks) / len(self.marks)

    def is_passing(self):
        """Return True if the average is above 40."""
        return self.calculate_average() >= 40


# -------------------------------------------------------------------
# 2. Stack (LIFO)
# -------------------------------------------------------------------
"""
A stack follows the LIFO principle:
Last In, First Out.

Visual (push 10, 20, 30 -> pop returns 30 first):

    push(10)   push(20)   push(30)     pop() -> 30
    +----+     +----+     +----+       +----+
    |    |     |    |     | 30 | top   |    |
    +----+     +----+     +----+       +----+
    |    |     | 20 | top | 20 |       | 20 | top
    +----+     +----+     +----+       +----+
    | 10 | top | 10 |     | 10 |       | 10 |
    +----+     +----+     +----+       +----+

Only the top is ever touched - that's what makes it O(1).

Use cases:
- Undo/Redo in editors
- Browser back button
- Function call stack
- Checking balanced parentheses in expressions
"""


class Stack:
    def __init__(self):
        """Initialize an empty stack."""
        self.items = []

    def push(self, element):
        """Add an element to the top of the stack."""
        self.items.append(element)

    def pop(self):
        """Remove and return the top element if the stack is not empty."""
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack")
        return self.items.pop()

    def peek(self):
        """Return the top element without removing it."""
        if self.is_empty():
            return None
        return self.items[-1]

    def is_empty(self):
        """Return True if the stack has no elements."""
        return len(self.items) == 0

    def size(self):
        """Return the number of elements in the stack."""
        return len(self.items)

    def display(self):
        """Return the current contents of the stack."""
        return self.items


def is_balanced(expression):
    """Check if parentheses in an expression are balanced."""
    stack = Stack()
    pairs = {')': '(', ']': '[', '}': '{'}

    for char in expression:
        if char in '([{':
            stack.push(char)
        elif char in ')]}':
            if stack.is_empty() or stack.pop() != pairs[char]:
                return False

    return stack.is_empty()


# -------------------------------------------------------------------
# 3. Queue (FIFO)
# -------------------------------------------------------------------
"""
A queue follows the FIFO principle:
First In, First Out.

Visual (enqueue A, B, C -> dequeue returns A first):

    FRONT                          BACK
    +-----+     +-----+     +-----+
    |  A  | <-- |  B  | <-- |  C  |   <- new items enqueue() here
    +-----+     +-----+     +-----+
       |
       v
    dequeue() removes from the FRONT -> "A" leaves first

Stack pops/pushes one end; a queue adds at the back and removes
from the front - that's the whole difference to remember.

Use cases:
- Customer service queues
- Print jobs
- Message buffering
- Scheduling tasks in order
"""


from collections import deque


class Queue:
    def __init__(self):
        """Initialize an empty queue."""
        self.items = deque()

    def enqueue(self, element):
        """Add an element to the end of the queue."""
        self.items.append(element)

    def dequeue(self):
        """Remove and return the first element if the queue is not empty."""
        if self.is_empty():
            raise IndexError("Cannot dequeue from an empty queue")
        return self.items.popleft()

    def peek(self):
        """Return the first element without removing it."""
        if self.is_empty():
            return None
        return self.items[0]

    def is_empty(self):
        """Return True if the queue has no elements."""
        return len(self.items) == 0

    def size(self):
        """Return the number of elements in the queue."""
        return len(self.items)

    def display(self):
        """Return the current contents of the queue."""
        return list(self.items)


# -------------------------------------------------------------------
# 4. Graphs
# -------------------------------------------------------------------
"""
Graphs are used to represent connections between objects.

Undirected graph (A-B means the connection works both ways):
Use case: social networks / friendships

        A --- B
              |
              C --- D

    graph = {
        "A": ["B"],
        "B": ["A", "C"],
        "C": ["B", "D"],
        "D": ["C"],
    }

Directed graph (A -> B means only A points to B, not the reverse):
Use case: web pages / routes / dependencies

        A --> B --> C
        |___________^

    graph = {
        "A": ["B", "C"],
        "B": ["C"],
        "C": [],
    }

Both are stored the same way in code: a dict where each key maps to
a list of its neighbors (an "adjacency list"). The only difference is
whether add_edge() writes the connection in one direction or both.
"""


class UndirectedGraph:
    def __init__(self):
        self.graph = {}

    def add_vertex(self, node):
        if node not in self.graph:
            self.graph[node] = []

    def add_edge(self, node1, node2):
        self.add_vertex(node1)
        self.add_vertex(node2)
        if node2 not in self.graph[node1]:
            self.graph[node1].append(node2)
        if node1 not in self.graph[node2]:
            self.graph[node2].append(node1)

    def has_edge(self, node1, node2):
        return node2 in self.graph.get(node1, [])

    def get_neighbors(self, node):
        return self.graph.get(node, [])

    def display(self):
        return self.graph

    def find_path(self, start, end):
        """Find a path between two nodes using BFS."""
        if start == end:
            return [start]

        visited = {start}
        queue = deque([[start]])

        while queue:
            path = queue.popleft()
            current = path[-1]

            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    if neighbor == end:
                        return new_path
                    visited.add(neighbor)
                    queue.append(new_path)

        return None


class DirectedGraph:
    def __init__(self):
        self.graph = {}

    def add_vertex(self, node):
        if node not in self.graph:
            self.graph[node] = []

    def add_edge(self, from_node, to_node):
        self.add_vertex(from_node)
        self.add_vertex(to_node)
        if to_node not in self.graph[from_node]:
            self.graph[from_node].append(to_node)

    def has_edge(self, from_node, to_node):
        return to_node in self.graph.get(from_node, [])

    def display(self):
        return self.graph


# -------------------------------------------------------------------
# 5. Facebook-style Friend Recommendation (OOP use case)
# -------------------------------------------------------------------
"""
This is a very relevant OOP use case.
We model each person as an object and use methods to connect people and
recommend new friends based on mutual connections.

Idea:
If Alice is friends with Bob and Carol, and Bob is also friends with David,
then David could be suggested to Alice as a potential friend
(Alice and David share two mutual friends, so David ranks highest).

        Bob --- Alice --- Carol
         |                  |
        David -------------+

    Alice's direct friends:      Bob, Carol
    Friends-of-friends (David):  reached via Bob AND via Carol -> score 2
    -> recommend_friends("Alice") suggests David first
"""


class Person:
    def __init__(self, name):
        self.name = name
        self.friends = []

    def add_friend(self, friend):
        """Add a new friend if it does not already exist."""
        if friend not in self.friends:
            self.friends.append(friend)

    def show_friends(self):
        """Return the names of all friends."""
        return [friend.name for friend in self.friends]


class SocialNetwork:
    def __init__(self):
        self.people = {}

    def add_person(self, person):
        """Add a person to the network if they are not already present."""
        if person.name not in self.people:
            self.people[person.name] = person

    def connect(self, person1, person2):
        """Create a friendship between two people."""
        self.add_person(person1)
        self.add_person(person2)
        person1.add_friend(person2)
        person2.add_friend(person1)

    def recommend_friends(self, person_name):
        """Suggest friends based on mutual connections."""
        person = self.people.get(person_name)
        if person is None:
            return []

        recommendations = {}
        for friend in person.friends:
            for mutual_friend in friend.friends:
                if mutual_friend.name != person.name and mutual_friend not in person.friends:
                    recommendations[mutual_friend.name] = (
                        recommendations.get(mutual_friend.name, 0) + 1
                    )

        return sorted(recommendations.items(), key=lambda item: item[1], reverse=True)


# -------------------------------------------------------------------
# 6. Prefix, Postfix, and Polish Notation (extra DSA concept)
# -------------------------------------------------------------------
"""
Polish notation is a way of writing expressions without parentheses.
There are three common forms:
- Prefix: operator before operands  -> + a b
- Infix: operator between operands  -> a + b
- Postfix: operator after operands  -> a b +

Visual - the expression 5 + (2 * 3) as an expression tree:

            +
           / \
          5   *
             / \
            2   3

    Read the tree root-to-leaf for prefix:   + 5 * 2 3
    Read the tree leaf-to-root for postfix:  5 2 3 * +

Walking through evaluate_postfix("5 2 3 * +") with a stack:

    token  action          stack
    5      push            [5]
    2      push            [5, 2]
    3      push             [5, 2, 3]
    *      pop 3, pop 2 -> push 2*3=6   [5, 6]
    +      pop 6, pop 5 -> push 5+6=11  [11]   <- final answer

evaluate_prefix walks the tokens in reverse for the same reason: the
operator comes first, so you need both operands already on the stack
before you reach it.

Why it is useful:
- It removes the need for parentheses in many cases.
- It is commonly used in compilers and expression evaluators.
"""


class ExpressionEvaluator:
    def __init__(self):
        self.stack = []

    def evaluate_prefix(self, expression):
        """Evaluate a prefix expression like + 5 * 2 3."""
        tokens = expression.split()
        self.stack = []

        for token in reversed(tokens):
            if token.isdigit():
                self.stack.append(int(token))
            else:
                if len(self.stack) < 2:
                    raise ValueError("Invalid prefix expression")
                a = self.stack.pop()
                b = self.stack.pop()

                if token == '+':
                    self.stack.append(a + b)
                elif token == '-':
                    self.stack.append(a - b)
                elif token == '*':
                    self.stack.append(a * b)
                elif token == '/':
                    self.stack.append(a // b)

        return self.stack[-1]

    def evaluate_postfix(self, expression):
        """Evaluate a postfix expression like 5 2 3 * +."""
        tokens = expression.split()
        self.stack = []

        for token in tokens:
            if token.isdigit():
                self.stack.append(int(token))
            else:
                if len(self.stack) < 2:
                    raise ValueError("Invalid postfix expression")
                b = self.stack.pop()
                a = self.stack.pop()

                if token == '+':
                    self.stack.append(a + b)
                elif token == '-':
                    self.stack.append(a - b)
                elif token == '*':
                    self.stack.append(a * b)
                elif token == '/':
                    self.stack.append(a // b)

        return self.stack[-1]


# -------------------------------------------------------------------
# 7. Inheritance and Polymorphism (extra OOP concept)
# -------------------------------------------------------------------
"""
Inheritance:
A child class can reuse the features of a parent class.

Polymorphism:
Different classes can have methods with the same name, but they behave differently.
"""


class Vehicle:
    def __init__(self, name):
        self.name = name

    def start(self):
        return f"{self.name} is starting"

    def stop(self):
        return f"{self.name} is stopping"


class Car(Vehicle):
    def drive(self):
        return f"{self.name} is driving"


class Bike(Vehicle):
    def ride(self):
        return f"{self.name} is riding"


# -------------------------------------------------------------------
# 8. Example Usage / Demo
# -------------------------------------------------------------------
if __name__ == "__main__":
    print("=== OOP Basics ===")
    account = BankAccount("Ravi", 1000)
    print(account.deposit(500))
    print(account.withdraw(300))
    print("Current balance:", account.get_balance())

    student = Student("Asha", [70, 80, 90])
    print("Student average:", student.calculate_average())
    print("Passing?", student.is_passing())

    print("\n=== Stack Demo ===")
    s = Stack()
    s.push(10)
    s.push(20)
    s.push(30)
    print("Stack:", s.display())
    print("Peek:", s.peek())
    print("Pop:", s.pop())
    print("Balanced expression?", is_balanced("({[a+b]})"))
    print("Unbalanced expression?", is_balanced("({[a+b]"))

    print("\n=== Queue Demo ===")
    q = Queue()
    q.enqueue("A")
    q.enqueue("B")
    q.enqueue("C")
    print("Queue:", q.display())
    print("Dequeued:", q.dequeue())

    print("\n=== Undirected Graph Demo ===")
    ug = UndirectedGraph()
    ug.add_edge("A", "B")
    ug.add_edge("B", "C")
    ug.add_edge("C", "D")
    print("Graph:", ug.display())
    print("Path from A to D:", ug.find_path("A", "D"))

    print("\n=== Directed Graph Demo ===")
    dg = DirectedGraph()
    dg.add_edge("A", "B")
    dg.add_edge("B", "C")
    dg.add_edge("A", "C")
    print("Graph:", dg.display())

    print("\n=== Facebook-style Friend Recommendation ===")
    alice = Person("Alice")
    bob = Person("Bob")
    carol = Person("Carol")
    david = Person("David")

    network = SocialNetwork()
    network.connect(alice, bob)
    network.connect(alice, carol)
    network.connect(bob, david)
    network.connect(carol, david)

    print("Alice's friends:", alice.show_friends())
    print("Recommended friends for Alice:", network.recommend_friends("Alice"))

    print("\n=== Prefix/Postfix Evaluation ===")
    evaluator = ExpressionEvaluator()
    print("Prefix result:", evaluator.evaluate_prefix("+ 5 * 2 3"))
    print("Postfix result:", evaluator.evaluate_postfix("5 2 3 * +"))

    print("\n=== Inheritance Demo ===")
    car = Car("Honda")
    bike = Bike("Yamaha")
    print(car.start())
    print(car.drive())
    print(bike.start())
    print(bike.ride())
