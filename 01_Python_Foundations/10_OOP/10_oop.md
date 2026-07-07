# Module 10: Object-Oriented Programming (OOP)

OOP is a paradigm for organizing code by grouping related data and behavior into "Objects".

## Why OOP? The NVT Technique
To design an OOP system from a problem statement, use the **Noun-Verb Technique (NVT)**:
1. **Nouns** become Classes (e.g., Customer, Cart)
2. **Adjectives/Properties** become Attributes (e.g., name, price)
3. **Verbs** become Methods (e.g., register(), add_item())

## The 4 Pillars of OOP

```mermaid
mindmap
  root((OOP))
    Encapsulation
      (Bundling data + methods)
      (Controlling access)
    Abstraction
      (Hiding complexity)
      (Showing simple interface)
    Inheritance
      (Code reuse)
      (Parent-Child relationship)
    Polymorphism
      (Same interface, different behavior)
      (Method overriding)
```

## The `__init__` Process
When you create an object (`dog = Dog()`), Python automatically calls the `__init__` constructor method to initialize it.

```mermaid
sequenceDiagram
    participant User
    participant Python
    participant Object
    
    User->>Python: dog = Dog("Rex")
    Python->>Object: Create raw object in memory
    Python->>Object: __init__(self, "Rex")
    Note over Object: self.name = "Rex"
    Object-->>User: Return initialized object reference
```

## Method Types

| Method Type | Decorator | First Arg | Can access instance data? | Can access class data? |
| --- | --- | --- | --- | --- |
| **Instance** | None | `self` | Yes | Yes |
| **Class** | `@classmethod` | `cls` | No | Yes |
| **Static** | `@staticmethod`| None | No | No |

## Composition vs Inheritance

| Feature | Inheritance ("is-a") | Composition ("has-a") |
| --- | --- | --- |
| **Relationship** | ElectricCar *is a* Car | Car *has an* Engine |
| **Coupling** | Very tight (child breaks if parent changes) | Loose (swap engines easily) |
| **Liskov Principle**| Child must be able to completely replace parent | N/A |
| **Preference** | Use sparingly | Prefer over inheritance |

## Multiple Inheritance and MRO
Python supports inheriting from multiple classes. If multiple parents have the same method, Python uses the Method Resolution Order (MRO) to decide which one to call.

```mermaid
classDiagram
    class A
    class B
    class C
    class D
    
    A <|-- B
    A <|-- C
    B <|-- D
    C <|-- D
    
    note for D "Diamond Problem.\nMRO is D -> B -> C -> A"
```

## Real-World Example: Bank System

```mermaid
classDiagram
    class BankAccount {
        -_balance: float
        +deposit(amount)
        +withdraw(amount)
    }
    class SavingsAccount {
        +interest_rate: float
        +apply_interest()
    }
    class CheckingAccount {
        +overdraft_limit: float
        +withdraw(amount)
    }
    
    BankAccount <|-- SavingsAccount
    BankAccount <|-- CheckingAccount
```
