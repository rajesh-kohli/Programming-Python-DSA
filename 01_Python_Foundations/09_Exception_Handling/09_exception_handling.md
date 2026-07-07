# Module 09: Exception Handling

Exceptions are Python's way of dealing with errors that happen while a program is running (runtime errors). Instead of crashing immediately, Python gives you a chance to "catch" the error and recover.

## The `try` Block Lifecycle

```mermaid
flowchart TD
    Try[Execute code in 'try' block] --> Error{Did an error occur?}
    Error -- Yes --> Except[Execute 'except' block]
    Error -- No --> Else[Execute 'else' block]
    Except --> Finally[Execute 'finally' block]
    Else --> Finally
    Finally --> Done[Continue program execution]
```
- **`try`**: Code that might fail.
- **`except`**: Code that runs *only* if an exception occurs.
- **`else`**: Code that runs *only* if NO exception occurred.
- **`finally`**: Code that ALWAYS runs, regardless of what happened (used for cleanup).

## Exception Hierarchy
In Python, all exceptions inherit from `BaseException`. You should generally catch specific exceptions rather than a generic one.

```mermaid
classDiagram
    BaseException <|-- Exception
    BaseException <|-- KeyboardInterrupt
    Exception <|-- ArithmeticError
    Exception <|-- LookupError
    Exception <|-- ValueError
    ArithmeticError <|-- ZeroDivisionError
    LookupError <|-- IndexError
    LookupError <|-- KeyError
```

## The "Net Width" Comparison
Why shouldn't you just use a bare `except:` to catch everything?

| Syntax | What it catches | Good Idea? | Reason |
| --- | --- | --- | --- |
| `except FileNotFoundError:` | Only missing files | **YES** | You know exactly what went wrong and how to fix it. |
| `except Exception as e:` | Almost all errors | **OKAY** | Good as a final fallback, lets you log the error `e`. |
| `except:` | ABSOLUTELY EVERYTHING | **NO!** | Catches `SystemExit` and `KeyboardInterrupt` (Ctrl+C). You literally can't stop the program. |

## The `with` Statement (Context Managers)
When working with external resources (files, network connections), you must remember to close them, even if an error occurs. The `with` statement handles this automatically.

```mermaid
sequenceDiagram
    participant Code
    participant ContextManager
    participant Resource
    
    Code->>ContextManager: with open("file.txt") as f:
    activate ContextManager
    ContextManager->>Resource: __enter__()
    Note over Code,Resource: Code executes...
    Code->>ContextManager: block ends (or exception raised)
    ContextManager->>Resource: __exit__()
    deactivate ContextManager
    Note over Resource: Resource safely closed!
```
