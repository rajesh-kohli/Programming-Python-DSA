###############################################################################
#              OOP Use Cases — Data Structures & Real-World Design            #
###############################################################################

"""
This file applies OOP concepts from 17_OOP.py to practical problems.
Topics covered:
    Section 1:  Stack — LIFO Data Structure
    Section 2:  Queue Implemented Using Two Stacks
    Section 3:  Stack Implemented Using Queue
    Section 4:  Linked List
    Section 5:  Min Stack (Stack that tracks minimum in O(1))
    Section 6:  Browser History (real-world stack use case)
    Section 7:  Task Scheduler (real-world queue use case)
    Section 8:  LRU Cache (linked list + hash map)
    Section 9:  Document Distance (cosine similarity)
    Section 10: Plagiarism Detection (4 versions)
    Section 11: Interview Q&A

Pre-requisites: 17_OOP.py (classes, dunder methods, encapsulation, inheritance)
"""

import math
from collections import deque, OrderedDict, Counter


# =============================================================================
# SECTION 1: Stack — LIFO Data Structure
# =============================================================================

# ----- What is a Stack? -----
#
# A Stack is a linear data structure that follows LIFO order:
#   Last In, First Out — the last element pushed is the first one popped.
#
# Real-life analogy: a stack of plates
#   - You put a new plate on TOP  (push)
#   - You take a plate from TOP   (pop)
#   - You look at the top plate   (peek)
#   You NEVER take from the bottom while the top exists.
#
# ----- Visual -----
#
#   push(10)   push(20)   push(30)   pop()    peek()
#   ┌────┐     ┌────┐     ┌────┐     ┌────┐   ┌────┐
#   │ 10 │     │ 20 │     │ 30 │◄TOP │ 20 │◄  │ 20 │◄ returns 20 (no pop)
#   └────┘     │ 10 │     │ 20 │     │ 10 │   │ 10 │
#              └────┘     │ 10 │     └────┘   └────┘
#                         └────┘    30 removed
#
# ----- Core operations and time complexity -----
#
#   push(x)  — add x to the top            O(1)
#   pop()    — remove and return top        O(1)
#   peek()   — look at top without removing O(1)
#   is_empty()— check if stack has elements O(1)
#   size()   — number of elements           O(1)
#
# Python list works perfectly as a stack:
#   list.append()  → push
#   list.pop()     → pop (from end by default)
#
# ----- Why use a class instead of just a list? -----
# A raw list lets you do list[0], list.insert(), list.sort() etc. — those
# aren't valid stack operations and could corrupt the LIFO invariant.
# Wrapping it in a class ENFORCES the interface: only push/pop/peek are allowed.
# This is encapsulation in action.

print("===== SECTION 1: Stack =====")

class Stack:
    """
    LIFO stack backed by a Python list.
    All operations are O(1) amortized.
    """

    def __init__(self):
        self._data = []          # underscore = "private by convention"

    def push(self, item):
        """Add item to the top of the stack."""
        self._data.append(item)

    def pop(self):
        """Remove and return the top item.  Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._data.pop()   # list.pop() removes from the END (top)

    def peek(self):
        """Return the top item without removing it."""
        if self.is_empty():
            raise IndexError("peek on empty stack")
        return self._data[-1]     # last element = top of stack

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def size(self) -> int:
        return len(self._data)

    def __repr__(self):
        # Show bottom → top so the visual matches the push order
        return f"Stack(bottom→top): {self._data}"


# --- Demo ---
s = Stack()
s.push(10)
s.push(20)
s.push(30)
print(s)                    # Stack(bottom→top): [10, 20, 30]
print("peek:", s.peek())    # 30
print("pop:", s.pop())      # 30
print(s)                    # Stack(bottom→top): [10, 20]
print("size:", s.size())    # 2


# =============================================================================
# SECTION 2: Queue Implemented Using Two Stacks
# =============================================================================

# ----- What is a Queue? -----
#
# A Queue follows FIFO order: First In, First Out.
# Real-life analogy: a line at a ticket counter.
#   - People join at the BACK  (enqueue)
#   - People leave from FRONT  (dequeue)
#
# ----- The Problem -----
# Implement a queue using only stack operations (push / pop / peek / is_empty).
# This is a classic interview question testing your understanding of both
# data structures.
#
# ----- Intuition -----
# A stack reverses the order of elements (LIFO).
# Two reversals restore the original order (FIFO).
#
# Use two stacks:
#   inbox  (stack1) — all new elements go here (enqueue is O(1))
#   outbox (stack2) — elements leave from here (dequeue)
#
# When outbox is EMPTY and we need to dequeue:
#   Pour everything from inbox into outbox (this reverses the order once).
#   Now the oldest element (first enqueued) is on TOP of outbox → pop it.
#
# ----- Visual Walkthrough -----
#
#   enqueue(1), enqueue(2), enqueue(3)
#
#   inbox:  [1, 2, 3]  (3 on top)       outbox: []
#
#   dequeue() called:
#     outbox is empty → pour inbox into outbox:
#       pop 3 from inbox → push 3 to outbox
#       pop 2 from inbox → push 2 to outbox
#       pop 1 from inbox → push 1 to outbox
#
#   inbox:  []     outbox: [3, 2, 1]  (1 on top)
#                                      ↑ THIS is the front of the queue
#   pop from outbox → returns 1  ✓  (first element in, first element out)
#
#   enqueue(4), enqueue(5)
#   inbox:  [4, 5]    outbox: [3, 2]   (2 on top)
#
#   dequeue() → outbox not empty → pop 2 → returns 2 ✓
#   dequeue() → outbox not empty → pop 3 → returns 3 ✓
#   dequeue() → outbox empty → pour inbox:  outbox becomes [5, 4]
#             → pop 4 → returns 4 ✓
#
# ----- Time Complexity Analysis -----
#
#   enqueue: O(1) always — just push to inbox
#   dequeue: O(1) AMORTISED — sounds expensive but here's why:
#     Each element is moved at most ONCE from inbox to outbox over its lifetime.
#     If you do n enqueues and n dequeues total:
#       - n pushes to inbox      → n operations
#       - n moves inbox→outbox   → n operations
#       - n pops from outbox     → n operations
#       Total = 3n operations for 2n method calls → O(1) per call on average
#     This "spreading cost across many calls" is amortised analysis.
#
#   Space: O(n) — elements live in one of the two stacks at any time
#
# ----- Why not just use collections.deque? -----
# In production you absolutely would. This problem tests whether you
# UNDERSTAND data structures — the constraint forces you to think about
# reversals and amortised complexity.
#
# ----- Common Mistake: Wrong else placement -----
#
# A buggy version seen in class:
#
#   def dequeue(self):
#       if len(self.stack2) == 0:
#           i = 0
#           while i < len(self.stack1):      # i never increments — relies on
#               self.stack2.append(           # pop() shrinking the list to exit
#                   self.stack1.pop())
#       else:
#           print("queue is empty cannot remove")   # ← BUG: fires when stack2
#       return self.stack2.pop(), self.stack2       #   is NOT empty (has items!)
#
# What's wrong:
#   1. else fires when stack2 HAS items — that is the NORMAL dequeue path,
#      not the empty case. "queue is empty" is printed when it shouldn't be.
#   2. The actual empty check is MISSING — when both stacks are empty the
#      function falls through to self.stack2.pop() and crashes with IndexError.
#   3. i = 0 / while i < len(...) works only because pop() shrinks the list,
#      but it's misleading. Use "while self.stack1:" instead.
#
# Fixed structure:
#
#   def dequeue(self):
#       if len(self.stack2) == 0:
#           if len(self.stack1) == 0:        # ← correct empty check: BOTH empty
#               print("queue is empty, cannot remove")
#               return
#           while self.stack1:               # pour stack1 → stack2
#               self.stack2.append(self.stack1.pop())
#       return self.stack2.pop()             # stack2 now has front at top

print("\n===== SECTION 2: Queue Using Two Stacks =====")

class QueueUsingStacks:
    """
    FIFO queue implemented with two stacks.
    enqueue: O(1)
    dequeue: O(1) amortised
    """

    def __init__(self):
        self._inbox  = Stack()   # receives all new elements
        self._outbox = Stack()   # serves all dequeue requests

    def enqueue(self, item):
        """Add item to the back of the queue.  O(1)"""
        self._inbox.push(item)

    def _refill_outbox(self):
        """Pour inbox into outbox — only called when outbox is empty."""
        while not self._inbox.is_empty():
            self._outbox.push(self._inbox.pop())
        # After this, outbox's top = oldest element (front of queue)

    def dequeue(self):
        """Remove and return the front item.  O(1) amortised."""
        if self._outbox.is_empty():
            if self._inbox.is_empty():
                raise IndexError("dequeue from empty queue")
            self._refill_outbox()
        return self._outbox.pop()

    def front(self):
        """Peek at the front item without removing it."""
        if self._outbox.is_empty():
            if self._inbox.is_empty():
                raise IndexError("front of empty queue")
            self._refill_outbox()
        return self._outbox.peek()

    def is_empty(self) -> bool:
        return self._inbox.is_empty() and self._outbox.is_empty()

    def size(self) -> int:
        return self._inbox.size() + self._outbox.size()

    def __repr__(self):
        # Reconstruct logical front→back order for display only
        outbox_items = list(reversed(self._outbox._data))  # front first
        inbox_items  = self._inbox._data                   # oldest first
        return f"Queue(front→back): {outbox_items + inbox_items}"


# --- Demo ---
q = QueueUsingStacks()
q.enqueue(1)
q.enqueue(2)
q.enqueue(3)
print(q)                      # Queue(front→back): [1, 2, 3]
print("front:", q.front())    # 1
print("dequeue:", q.dequeue()) # 1
print("dequeue:", q.dequeue()) # 2
q.enqueue(4)
q.enqueue(5)
print(q)                      # Queue(front→back): [3, 4, 5]
print("dequeue:", q.dequeue()) # 3


# =============================================================================
# SECTION 3: Stack Implemented Using Queue
# =============================================================================

# ----- Problem -----
# Implement a stack (LIFO) using only queue operations: enqueue and dequeue.
# You cannot peek at or index into the queue directly.
#
# ----- Why is this trickier than Queue-using-Stacks? -----
# A queue forces FIFO — the oldest element comes out first.
# A stack needs the NEWEST element to come out first.
# To get the newest element to the front of a queue, we have to ROTATE
# all the older elements behind it after every push.
#
# ----- Two Approaches -----
#
#   Approach A — Two queues, costly push:
#     push(x): enqueue x into q2, pour all of q1 into q2, swap q1 and q2
#     pop():   dequeue from q1  (front = most recently pushed)
#     push: O(n)   pop: O(1)
#
#   Approach B — One queue, costly push (cleaner, fewer moving parts):
#     push(x): enqueue x, then rotate the other (size-1) elements to the back
#              → x ends up at the FRONT (top of the logical stack)
#     pop():   dequeue from front  (always the most recently pushed)
#     push: O(n)   pop: O(1)
#
# Both have the same complexity. We implement both below.
#
# ─────────────────────────────────────────────────────────────────────────────
# APPROACH A — Two Queues
# ─────────────────────────────────────────────────────────────────────────────
#
# ----- Visual Walkthrough -----
#
#   push(10):
#     enqueue 10 → q2=[10]
#     q1 is empty, nothing to pour
#     swap → q1=[10], q2=[]
#
#   push(20):
#     enqueue 20 → q2=[20]
#     pour q1 into q2: dequeue 10, enqueue 10 → q2=[20, 10]
#     swap → q1=[20, 10], q2=[]
#     front of q1 = 20 = top of stack ✓
#
#   push(30):
#     enqueue 30 → q2=[30]
#     pour q1 into q2: dequeue 20→q2, dequeue 10→q2 → q2=[30, 20, 10]
#     swap → q1=[30, 20, 10], q2=[]
#     front of q1 = 30 = top of stack ✓
#
#   pop() → dequeue from q1 → 30 ✓
#   pop() → dequeue from q1 → 20 ✓
#   pop() → dequeue from q1 → 10 ✓
#
# ─────────────────────────────────────────────────────────────────────────────
# APPROACH B — One Queue (rotate after push)
# ─────────────────────────────────────────────────────────────────────────────
#
# ----- Visual Walkthrough -----
#
#   push(10): enqueue → q=[10]  (size=1, rotate 0 times)
#
#   push(20): enqueue → q=[10, 20]
#             rotate 1 time (size-1 = 1):
#               dequeue 10, enqueue 10 → q=[20, 10]
#             front = 20 = top ✓
#
#   push(30): enqueue → q=[20, 10, 30]
#             rotate 2 times (size-1 = 2):
#               dequeue 20, enqueue 20 → q=[10, 30, 20]
#               dequeue 10, enqueue 10 → q=[30, 20, 10]
#             front = 30 = top ✓
#
#   pop() → dequeue → 30 ✓
#   pop() → dequeue → 20 ✓
#
# Key insight: every push moves x to the front by cycling all older elements
# behind it. The queue always holds elements in stack order (newest at front).
#
# ----- Time Complexity -----
#
#   Approach A:  push O(n) — pours all n elements from q1 to q2
#                pop  O(1) — simple dequeue
#   Approach B:  push O(n) — rotates n-1 elements
#                pop  O(1) — simple dequeue
#
#   Space: O(n) — all n elements live in one queue at a time

print("\n===== SECTION 3: Stack Using Queue =====")

# ── Approach A: Two Queues ──

class StackUsingTwoQueues:
    """
    LIFO stack using two queues.
    push: O(n)  |  pop/peek: O(1)
    """

    def __init__(self):
        self._q1 = deque()   # main queue — front = top of stack
        self._q2 = deque()   # helper queue used only during push

    def push(self, val):
        """Push val onto the stack.  O(n)"""
        # Step 1: put new element into q2 first (it must be at the front after swap)
        self._q2.append(val)
        # Step 2: pour all of q1 into q2 (older elements go behind the new one)
        while self._q1:
            self._q2.append(self._q1.popleft())
        # Step 3: swap — q1 becomes the updated queue with new element at front
        self._q1, self._q2 = self._q2, self._q1
        # q2 is now empty (ready for next push)

    def pop(self):
        """Remove and return the top element.  O(1)"""
        if not self._q1:
            raise IndexError("pop from empty stack")
        return self._q1.popleft()   # front of q1 = top of stack

    def peek(self):
        """Return the top element without removing it.  O(1)"""
        if not self._q1:
            raise IndexError("peek on empty stack")
        return self._q1[0]

    def is_empty(self) -> bool:
        return not self._q1

    def __repr__(self):
        # q1[0] is the top; display top→bottom
        return f"Stack(top→bottom): {list(self._q1)}"


# --- Demo: Approach A ---
print("  -- Approach A: Two Queues --")
stk_a = StackUsingTwoQueues()
for v in [10, 20, 30]:
    stk_a.push(v)
    print(f"  push({v}) → {stk_a}")
print(f"  peek: {stk_a.peek()}")          # 30
print(f"  pop:  {stk_a.pop()}")           # 30
print(f"  pop:  {stk_a.pop()}")           # 20
print(f"  after pops → {stk_a}")          # [10]


# ── Approach B: One Queue ──

class StackUsingOneQueue:
    """
    LIFO stack using a single queue.
    After each push, rotate so the new element sits at the front.
    push: O(n)  |  pop/peek: O(1)
    """

    def __init__(self):
        self._q = deque()

    def push(self, val):
        """Push val onto the stack.  O(n)"""
        self._q.append(val)                   # new element goes to the back first
        rotations = len(self._q) - 1          # number of older elements
        for _ in range(rotations):
            self._q.append(self._q.popleft()) # cycle each older element to the back
        # after rotations, val is at the front (top of stack)

    def pop(self):
        """Remove and return the top element.  O(1)"""
        if not self._q:
            raise IndexError("pop from empty stack")
        return self._q.popleft()

    def peek(self):
        """Return the top element without removing it.  O(1)"""
        if not self._q:
            raise IndexError("peek on empty stack")
        return self._q[0]

    def is_empty(self) -> bool:
        return not self._q

    def __repr__(self):
        return f"Stack(top→bottom): {list(self._q)}"


# --- Demo: Approach B ---
print("\n  -- Approach B: One Queue --")
stk_b = StackUsingOneQueue()
for v in [10, 20, 30]:
    stk_b.push(v)
    print(f"  push({v}) → {stk_b}")
print(f"  peek: {stk_b.peek()}")          # 30
print(f"  pop:  {stk_b.pop()}")           # 30
print(f"  pop:  {stk_b.pop()}")           # 20
print(f"  after pops → {stk_b}")          # [10]


# =============================================================================
# SECTION 4: Linked List   (was Section 3)
# =============================================================================

# ----- What is a Linked List? -----
#
# A sequence of NODES where each node holds:
#   - data  : the value stored
#   - next  : a reference (pointer) to the next node
#
# The list itself just tracks the HEAD node.
# There is no index-based access — you must traverse from the head.
#
# ----- Visual -----
#
#   head
#    │
#    ▼
#   ┌──────┬──────┐    ┌──────┬──────┐    ┌──────┬──────┐
#   │  10  │  ●───┼───►│  20  │  ●───┼───►│  30  │ None │
#   └──────┴──────┘    └──────┴──────┘    └──────┴──────┘
#    Node(10)            Node(20)            Node(30)
#
# ----- Linked List vs Array (Python list) -----
#
#   Operation          Array (list)     Linked List
#   ─────────────────────────────────────────────────
#   Access by index    O(1)             O(n)   ← traverse from head
#   Insert at front    O(n) (shift)     O(1)   ← just update head
#   Insert at end      O(1) amortised   O(n) or O(1) with tail pointer
#   Delete from front  O(n) (shift)     O(1)
#   Search             O(n)             O(n)
#   Memory             contiguous       scattered (each node allocated separately)
#
# When to use a linked list:
#   - Frequent insert/delete at the FRONT or MIDDLE
#   - When you don't need random access by index
#   - Implementing stacks, queues, LRU caches

print("\n===== SECTION 4: Linked List =====")

class Node:
    """A single node in a singly linked list."""
    def __init__(self, data):
        self.data = data
        self.next = None   # will point to the next Node object, or None

    def __repr__(self):
        return f"Node({self.data})"


class LinkedList:
    """
    Singly linked list with common operations.
    """

    def __init__(self):
        self.head = None    # empty list: head points to nothing
        self._size = 0

    # ----- Insert operations -----

    def prepend(self, data):
        """Insert at the FRONT.  O(1)"""
        new_node = Node(data)
        new_node.next = self.head   # new node points to old head
        self.head = new_node        # head now points to new node
        self._size += 1

    def append(self, data):
        """Insert at the END.  O(n)"""
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:   # walk to the last node
                current = current.next
            current.next = new_node            # last node now points to new node
        self._size += 1

    def insert_after(self, target_data, data):
        """Insert after the first node with target_data.  O(n)"""
        current = self.head
        while current:
            if current.data == target_data:
                new_node = Node(data)
                new_node.next = current.next   # new node → whatever was after current
                current.next = new_node         # current → new node
                self._size += 1
                return
            current = current.next
        raise ValueError(f"{target_data} not found in list")

    # ----- Delete operations -----

    def delete(self, data):
        """Remove the first node with the given data.  O(n)

        Visual: delete node with value 20

        Before:  head→[10]→[20]→[30]→None

        We need the node BEFORE [20] (which is [10]).
        Set [10].next = [20].next = [30].

        After:   head→[10]→[30]→None
        [20] is now unreferenced → garbage collected.
        """
        if self.head is None:
            raise ValueError("delete from empty list")

        # Special case: deleting the head node
        if self.head.data == data:
            self.head = self.head.next
            self._size -= 1
            return

        # General case: find the node BEFORE the one we want to delete
        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next   # skip over the target node
                self._size -= 1
                return
            current = current.next
        raise ValueError(f"{data} not found in list")

    # ----- Search -----

    def search(self, data) -> bool:
        """Return True if data exists in the list.  O(n)"""
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False

    # ----- Reversal -----

    def reverse(self):
        """Reverse the linked list in-place.  O(n) time, O(1) space.

        Idea: walk the list, flipping each node's .next to point BACKWARD.

        Use three pointers:
          prev    — the node we just processed (starts as None)
          current — the node we're processing now
          nxt     — the node we'll process next (saved before we overwrite current.next)

        Visual on [10]→[20]→[30]→None:

        Step 1: prev=None, current=10, nxt=20
                10.next = None  (was 20)
                prev=10, current=20

        Step 2: prev=10, current=20, nxt=30
                20.next = 10
                prev=20, current=30

        Step 3: prev=20, current=30, nxt=None
                30.next = 20
                prev=30, current=None  → loop ends

        head = prev = 30
        Result: [30]→[20]→[10]→None  ✓
        """
        prev = None
        current = self.head
        while current:
            nxt = current.next    # save next before overwriting
            current.next = prev   # flip the pointer
            prev = current        # advance prev
            current = nxt         # advance current
        self.head = prev          # prev is now the new head (last original node)

    def to_list(self) -> list:
        """Convert to a Python list for easy printing.  O(n)"""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def __len__(self):
        return self._size

    def __repr__(self):
        nodes = self.to_list()
        return " → ".join(str(n) for n in nodes) + " → None"


# --- Demo ---
ll = LinkedList()
ll.append(10)
ll.append(20)
ll.append(30)
ll.prepend(5)
print(ll)                       # 5 → 10 → 20 → 30 → None
ll.insert_after(20, 25)
print(ll)                       # 5 → 10 → 20 → 25 → 30 → None
print("search 25:", ll.search(25))    # True
print("search 99:", ll.search(99))    # False
ll.delete(25)
print(ll)                       # 5 → 10 → 20 → 30 → None
ll.reverse()
print("reversed:", ll)          # 30 → 20 → 10 → 5 → None


# =============================================================================
# SECTION 5: Min Stack — Track Minimum in O(1)
# =============================================================================

# ----- Problem -----
# Design a stack that supports push, pop, peek, AND get_min() in O(1) time.
#
# Naive approach: get_min() scans all elements → O(n). Too slow.
#
# ----- Key Insight -----
# Each element that gets pushed was pushed at a point in time when the stack
# looked a certain way. Track "what was the minimum AT THE TIME this element
# was pushed" alongside the element itself.
#
# When you pop an element, the minimum reverts to what it was before that push.
#
# Implementation: maintain a SECOND stack (min_stack) that mirrors the main
# stack. When we push x, we push min(x, current_min) onto min_stack.
# When we pop, we pop from BOTH stacks.
#
# ----- Visual -----
#
#   push(5):  data=[5]        min_stack=[5]         min=5
#   push(3):  data=[5,3]      min_stack=[5,3]       min=3
#   push(7):  data=[5,3,7]    min_stack=[5,3,3]     min=3
#   push(2):  data=[5,3,7,2]  min_stack=[5,3,3,2]   min=2
#   pop():    data=[5,3,7]    min_stack=[5,3,3]     min=3  ✓ (2 removed, min reverts)
#   get_min() → peek min_stack → 3  ✓
#
# Time:  O(1) for all operations
# Space: O(n) extra for the min_stack (doubles memory, but constant multiplier)

print("\n===== SECTION 5: Min Stack =====")

class MinStack:
    """
    Stack with O(1) get_min().
    Uses an auxiliary stack to track the running minimum.
    """

    def __init__(self):
        self._data    = []   # main stack
        self._min_stk = []   # tracks minimum at each level

    def push(self, val: int):
        self._data.append(val)
        # Running min: either val itself (if smaller) or the current min
        current_min = val if not self._min_stk else min(val, self._min_stk[-1])
        self._min_stk.append(current_min)

    def pop(self) -> int:
        if not self._data:
            raise IndexError("pop from empty MinStack")
        self._min_stk.pop()   # keep both stacks in sync
        return self._data.pop()

    def peek(self) -> int:
        if not self._data:
            raise IndexError("peek on empty MinStack")
        return self._data[-1]

    def get_min(self) -> int:
        """Return the current minimum in O(1)."""
        if not self._min_stk:
            raise IndexError("get_min on empty MinStack")
        return self._min_stk[-1]

    def __repr__(self):
        return f"MinStack data={self._data}  mins={self._min_stk}"


# --- Demo ---
ms = MinStack()
for v in [5, 3, 7, 2]:
    ms.push(v)
    print(f"push({v})  →  {ms}  →  min={ms.get_min()}")
print("pop:", ms.pop())
print(f"after pop  →  {ms}  →  min={ms.get_min()}")


# =============================================================================
# SECTION 6: Browser History — Real-World Stack Use Case
# =============================================================================

# ----- Problem -----
# Implement the back/forward buttons of a web browser.
#
# Rules:
#   - visit(url): navigate to a new page
#       → clears ALL forward history (just like a real browser)
#   - back():  go to the previous page
#   - forward(): go to the next page (only if you went back first)
#
# ----- Why two stacks? -----
#
#   back_stack   — pages you CAN go back to
#   forward_stack— pages you CAN go forward to
#
#   visit(url):
#     push current page onto back_stack
#     set current = url
#     CLEAR forward_stack  (new navigation kills forward history)
#
#   back():
#     push current onto forward_stack
#     current = back_stack.pop()
#
#   forward():
#     push current onto back_stack
#     current = forward_stack.pop()
#
# ----- Visual -----
#
#   start at "google.com"
#
#   visit("youtube.com"):
#     back=[google]  current=youtube  fwd=[]
#
#   visit("github.com"):
#     back=[google, youtube]  current=github  fwd=[]
#
#   back():
#     back=[google]  current=youtube  fwd=[github]
#
#   back():
#     back=[]  current=google  fwd=[github, youtube]
#
#   forward():
#     back=[google]  current=youtube  fwd=[github]
#
#   visit("stackoverflow.com"):    ← new visit clears forward!
#     back=[google, youtube]  current=stackoverflow  fwd=[]

print("\n===== SECTION 6: Browser History =====")

class BrowserHistory:

    def __init__(self, homepage: str):
        self._current  = homepage
        self._back_stk = Stack()
        self._fwd_stk  = Stack()

    def visit(self, url: str):
        """Navigate to url, clearing all forward history."""
        self._back_stk.push(self._current)
        self._current = url
        # Clear forward history — new navigation invalidates it
        self._fwd_stk = Stack()
        print(f"  visit({url!r})  →  current={self._current!r}")

    def back(self) -> str:
        """Go back one page. Returns the page landed on."""
        if self._back_stk.is_empty():
            print("  back() — nothing to go back to")
            return self._current
        self._fwd_stk.push(self._current)
        self._current = self._back_stk.pop()
        print(f"  back()          →  current={self._current!r}")
        return self._current

    def forward(self) -> str:
        """Go forward one page. Returns the page landed on."""
        if self._fwd_stk.is_empty():
            print("  forward() — nothing to go forward to")
            return self._current
        self._back_stk.push(self._current)
        self._current = self._fwd_stk.pop()
        print(f"  forward()       →  current={self._current!r}")
        return self._current

    def current_page(self) -> str:
        return self._current


# --- Demo ---
browser = BrowserHistory("google.com")
browser.visit("youtube.com")
browser.visit("github.com")
browser.visit("stackoverflow.com")
browser.back()
browser.back()
browser.forward()
browser.visit("reddit.com")      # clears forward history
browser.forward()                # nothing to forward to


# =============================================================================
# SECTION 7: Task Scheduler — Real-World Queue Use Case
# =============================================================================

# ----- Problem -----
# A task scheduler receives tasks from multiple sources and processes them
# in the order they arrive (FIFO).
# Each task has a name, a priority (but in this simple version we process
# strictly in arrival order), and a status.
#
# This models how operating systems schedule processes, how web servers
# handle HTTP requests, or how a print spooler queues print jobs.
#
# ----- Design -----
# Task (data class): name, task_id, status
# TaskScheduler: uses collections.deque (Python's O(1) FIFO queue)
#   add_task(task)    — enqueue
#   process_next()    — dequeue and run
#   pending_count()   — how many tasks are waiting

print("\n===== SECTION 7: Task Scheduler =====")

class Task:
    _id_counter = 0   # class variable — shared across all Task instances

    def __init__(self, name: str):
        Task._id_counter += 1
        self.task_id = Task._id_counter
        self.name    = name
        self.status  = "pending"

    def execute(self):
        """Simulate running the task."""
        self.status = "done"
        print(f"    [Task #{self.task_id}] '{self.name}' executed ✓")

    def __repr__(self):
        return f"Task(#{self.task_id} '{self.name}' [{self.status}])"


class TaskScheduler:
    """
    FIFO task queue.
    Uses collections.deque for O(1) append (right) and popleft (left).
    """

    def __init__(self):
        self._queue: deque[Task] = deque()

    def add_task(self, name: str) -> Task:
        """Create and enqueue a task.  Returns the Task object."""
        task = Task(name)
        self._queue.append(task)
        print(f"  Scheduled: {task}")
        return task

    def process_next(self):
        """Dequeue and execute the oldest task."""
        if not self._queue:
            print("  No tasks to process.")
            return
        task = self._queue.popleft()   # O(1) — that's why we use deque, not list
        task.execute()

    def process_all(self):
        """Process every task in order."""
        while self._queue:
            self.process_next()

    def pending_count(self) -> int:
        return len(self._queue)

    def __repr__(self):
        return f"TaskScheduler({list(self._queue)})"


# --- Demo ---
scheduler = TaskScheduler()
scheduler.add_task("Send welcome email")
scheduler.add_task("Generate report")
scheduler.add_task("Backup database")
scheduler.add_task("Send alert")
print(f"  Pending: {scheduler.pending_count()}")
print("  Processing all tasks:")
scheduler.process_all()
print(f"  Pending after processing: {scheduler.pending_count()}")


# =============================================================================
# SECTION 8: LRU Cache
# =============================================================================

# ----- What is an LRU Cache? -----
#
# LRU = Least Recently Used.
# A cache with a fixed capacity that evicts the LEAST RECENTLY USED item
# when it's full and a new item needs to be added.
#
# Real-world uses:
#   - CPU caches  — keep recently used memory pages
#   - Browser cache — keep recently viewed web content
#   - Database query cache — keep recent query results
#   - CDN edge caches
#
# ----- Operations needed -----
#   get(key)         → return cached value or -1 if not found    O(1)
#   put(key, value)  → insert/update; evict LRU if at capacity  O(1)
#
# ----- Why is this hard? -----
# We need:
#   1. O(1) lookup by key        → hash map (dict)
#   2. O(1) track of usage order → doubly linked list
#      (move recently used to front, evict from back in O(1))
#
# ----- Data structure: Hash Map + Doubly Linked List -----
#
#  dict maps key → Node in the doubly linked list
#  DLL keeps nodes in MOST-recently-used → LEAST-recently-used order
#
#  Dummy head (MRU end) and dummy tail (LRU end) simplify edge cases.
#
# ----- Visual (capacity = 3) -----
#
#   put(1, A):  head ↔ [1:A] ↔ tail
#   put(2, B):  head ↔ [2:B] ↔ [1:A] ↔ tail     (2 is most recent)
#   put(3, C):  head ↔ [3:C] ↔ [2:B] ↔ [1:A] ↔ tail
#   get(1):     move 1 to front
#               head ↔ [1:A] ↔ [3:C] ↔ [2:B] ↔ tail
#   put(4, D):  capacity full! evict LRU = [2:B] (nearest to tail)
#               head ↔ [4:D] ↔ [1:A] ↔ [3:C] ↔ tail
#
# ----- Note on Python's OrderedDict -----
# Python's collections.OrderedDict remembers insertion order AND supports
# move_to_end(), making LRU Cache trivial to implement cleanly.
# Knowing both approaches matters for interviews.

print("\n===== SECTION 8: LRU Cache =====")

class LRUCache:
    """
    LRU Cache using OrderedDict.
    OrderedDict.move_to_end(key, last=False) → moves to FRONT (MRU end)
    OrderedDict.popitem(last=False)           → removes FRONT (LRU end when we keep MRU at end)

    Convention used here: MOST recently used → end (last=True is default)
    So evict from the FRONT (last=False in popitem).
    """

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("capacity must be > 0")
        self.capacity = capacity
        self._cache: OrderedDict = OrderedDict()

    def get(self, key) -> int:
        """Return cached value or -1.  Marks key as most recently used."""
        if key not in self._cache:
            return -1
        self._cache.move_to_end(key)   # move to end = mark as MRU
        return self._cache[key]

    def put(self, key, value):
        """Insert or update.  Evicts LRU if over capacity."""
        if key in self._cache:
            self._cache.move_to_end(key)   # updating = using it
        self._cache[key] = value
        if len(self._cache) > self.capacity:
            evicted_key, _ = self._cache.popitem(last=False)  # remove LRU (front)
            print(f"    evicted key={evicted_key!r} (LRU)")

    def __repr__(self):
        items = list(self._cache.items())
        order = " ← ".join(f"{k}:{v}" for k, v in reversed(items))
        return f"LRUCache(MRU→LRU: {order})"


# --- Demo ---
lru = LRUCache(capacity=3)
lru.put(1, "A")
lru.put(2, "B")
lru.put(3, "C")
print(lru)                        # MRU→LRU: 3:C ← 2:B ← 1:A
print("get(1):", lru.get(1))      # A  (1 becomes MRU)
print(lru)                        # MRU→LRU: 1:A ← 3:C ← 2:B
lru.put(4, "D")                   # evicts 2:B (LRU)
print(lru)                        # MRU→LRU: 4:D ← 1:A ← 3:C
print("get(2):", lru.get(2))      # -1 (evicted)
print("get(3):", lru.get(3))      # C


# =============================================================================
# SECTION 9: Document Distance
# =============================================================================

# ----- Problem -----
# Given two text documents, how similar are they?
#
#   Doc1 = "I love Programming"
#   Doc2 = "I love Programming"
#
# For identical documents the answer is obvious, but the same algorithm works
# for any pair of documents — which is how search engines, plagiarism detectors,
# and recommendation systems work under the hood.
#
# ----- Core Idea: Documents as Vectors -----
# Represent each document as a WORD FREQUENCY VECTOR.
# Every unique word across both documents is one "axis" (dimension).
# The count of that word in a document is its value on that axis.
#
#   Vocabulary: {I, love, Programming}
#
#             I    love   Programming
#   Doc1  = [ 1,    1,       1       ]
#   Doc2  = [ 1,    1,       1       ]
#
# These are points in 3-D space. Two identical documents are the SAME POINT.
# The "distance" between documents = the ANGLE between their vectors.
#
# ----- Why angle instead of straight-line distance? -----
# "I love Programming" and "I love Programming I love Programming" are the
# same content but different lengths. Straight-line distance (Euclidean)
# would say they're different. Angle-based distance says 0° — identical. ✓
# The angle doesn't care about how many times you repeated the document,
# only about the MIX of words — that's what captures meaning.
#
# ----- Cosine Similarity Formula -----
#
#              A · B
#   cos(θ) = ─────────
#             |A| × |B|
#
#   where:
#     A · B = dot product = Σ (A[word] × B[word])   for each shared word
#     |A|   = magnitude   = √( Σ A[word]² )
#     |B|   = magnitude   = √( Σ B[word]² )
#
#   Interpretation:
#     cos(θ) = 1.0  →  θ = 0°   →  identical
#     cos(θ) = 0.0  →  θ = 90°  →  completely different (no words in common)
#     0 < cos(θ) < 1  →  θ between 0° and 90°  →  partially similar
#
#   Document distance = θ = arccos( cos(θ) )
#
# ----- What does arccos mean? -----
#
# arccos is the INVERSE of cosine.
# cos      takes an ANGLE  → gives a NUMBER  (between 0 and 1)
# arccos   takes a NUMBER  → gives the ANGLE back
#
# So if cos(θ) = 0.667, you ask: "what angle has a cosine of 0.667?"
# arccos answers that question.
#
#   cos(θ) = 1.0  →  arccos(1.0) = 0°    (identical)
#   cos(θ) = 0.5  →  arccos(0.5) = 60°   (moderately different)
#   cos(θ) = 0.0  →  arccos(0.0) = 90°   (completely different)
#
# Why do we bother converting to an angle at all?
# Because angles are more intuitive than raw numbers.
# "0.667 similarity" is hard to judge at a glance.
# "48.2° apart" immediately tells you: halfway between identical and
# completely different — you know it's borderline without thinking hard.
#
# The pipeline in code is:
#
#   cos_sim = dot / (|A| × |B|)          → e.g. 0.667  (just a number)
#   angle   = math.degrees(               → e.g. 48.2°  (the actual distance)
#               math.acos(cos_sim))
#
# The formula notation "arccos( cos(θ) )" just shows the relationship —
# in practice you only ever have cos_sim (the number), and arccos gives
# you the meaningful angle to report.
#
# ----- Step-by-Step Walkthrough -----
#
#   Doc1 = "I love Programming"   word_freq = {i:1, love:1, programming:1}
#   Doc2 = "I love Programming"   word_freq = {i:1, love:1, programming:1}
#
#   Step 1 — Dot product:
#     i×i + love×love + programming×programming = 1×1 + 1×1 + 1×1 = 3
#
#   Step 2 — Magnitudes:
#     |Doc1| = √(1² + 1² + 1²) = √3 ≈ 1.732
#     |Doc2| = √(1² + 1² + 1²) = √3 ≈ 1.732
#
#   Step 3 — Cosine similarity:
#     cos(θ) = 3 / (√3 × √3) = 3/3 = 1.0
#
#   Step 4 — Angle (document distance):
#     θ = arccos(1.0) = 0°   →   IDENTICAL ✓
#
# ----- Another Example: Partial Overlap -----
#
#   Doc1 = "I love Programming"   → {i:1, love:1, programming:1}
#   Doc3 = "I love Python"        → {i:1, love:1, python:1}
#
#   Vocabulary: {i, love, programming, python}
#
#             i    love  prog  python
#   Doc1  = [ 1,    1,    1,    0   ]
#   Doc3  = [ 1,    1,    0,    1   ]
#
#   Dot product = 1×1 + 1×1 + 1×0 + 0×1 = 2   (only "i" and "love" shared)
#   |Doc1| = √3 ≈ 1.732    |Doc3| = √3 ≈ 1.732
#   cos(θ) = 2 / 3 ≈ 0.667
#   θ = arccos(0.667) ≈ 48.2°   →   somewhat similar
#
# ----- Yet Another: Almost No Overlap -----
#
#   Doc1 = "I love Programming"   → {i:1, love:1, programming:1}
#   Doc4 = "I hate Java"          → {i:1, hate:1, java:1}
#
#   Dot product = 1×1 = 1   (only "I" shared)
#   cos(θ) = 1/3 ≈ 0.333
#   θ ≈ 70.5°   →   mostly different

print("\n===== SECTION 9: Document Distance =====")


class Document:
    """
    Represents a text document as a word frequency vector.
    Normalises to lowercase and splits on whitespace.
    """

    def __init__(self, text: str):
        self.text = text
        self.word_freq: Counter = self._build_freq_vector(text)

    def _build_freq_vector(self, text: str) -> Counter:
        """Count occurrences of each (lowercased) word."""
        words = text.lower().split()
        return Counter(words)

    def __repr__(self):
        return f"Document({self.text!r}  freq={dict(self.word_freq)})"


class DocumentDistance:
    """
    Computes the angular distance between two Documents using
    their word-frequency vectors and cosine similarity.

    Methods:
        dot_product()        — Σ (A[w] × B[w]) for shared words
        magnitude(doc)       — √( Σ freq² )
        cosine_similarity()  — dot / (|A| × |B|),  range [0, 1]
        distance_degrees()   — arccos(cosine),      range [0°, 90°]
        are_similar(thresh)  — True if angle < threshold
        report()             — print full breakdown
    """

    def __init__(self, doc1: Document, doc2: Document):
        self.doc1 = doc1
        self.doc2 = doc2

    def dot_product(self) -> float:
        """
        Multiply matching word counts and sum them.
        Words that appear in only ONE document contribute 0 (missing × anything = 0).

        Time: O(min(|V1|, |V2|)) where V1, V2 are the vocabulary sizes.
        """
        total = 0.0
        for word, count in self.doc1.word_freq.items():
            if word in self.doc2.word_freq:
                total += count * self.doc2.word_freq[word]
        return total

    def magnitude(self, doc: Document) -> float:
        """
        Length of the frequency vector = √( Σ count² ).
        This is the L2 norm (Euclidean length) of the vector.
        """
        return math.sqrt(sum(c ** 2 for c in doc.word_freq.values()))

    def cosine_similarity(self) -> float:
        """
        cos(θ) = dot(A, B) / (|A| × |B|)
        Returns a value in [0.0, 1.0].
        Returns 0.0 if either document is empty (no words).
        """
        dot  = self.dot_product()
        mag1 = self.magnitude(self.doc1)
        mag2 = self.magnitude(self.doc2)
        if mag1 == 0 or mag2 == 0:
            return 0.0
        return dot / (mag1 * mag2)

    def distance_degrees(self) -> float:
        """
        Document distance = angle between vectors, in degrees.
        θ = arccos( cos(θ) )
        0°  → identical
        90° → completely different
        """
        cos_sim = self.cosine_similarity()
        # Clamp to [-1, 1] to guard against floating-point rounding errors
        # e.g., cosine might be 1.0000000002 due to float arithmetic
        cos_sim = max(-1.0, min(1.0, cos_sim))
        return math.degrees(math.acos(cos_sim))

    def are_similar(self, threshold_degrees: float = 45.0) -> bool:
        """
        Heuristic: treat documents as 'similar' if the angle is below threshold.
        Default threshold = 45° (half of the 0°–90° range).
        Adjust for stricter (lower) or looser (higher) matching.
        """
        return self.distance_degrees() <= threshold_degrees

    def report(self):
        """Print a human-readable similarity breakdown."""
        dot  = self.dot_product()
        mag1 = self.magnitude(self.doc1)
        mag2 = self.magnitude(self.doc2)
        cos  = self.cosine_similarity()
        dist = self.distance_degrees()
        print(f"  Doc1 : {self.doc1.text!r}")
        print(f"  Doc2 : {self.doc2.text!r}")
        print(f"  Freq1: {dict(self.doc1.word_freq)}")
        print(f"  Freq2: {dict(self.doc2.word_freq)}")
        print(f"  ── Calculation ──────────────────────────────")
        print(f"  Dot product       : {dot:.4f}")
        print(f"  |Doc1|            : {mag1:.4f}  (√{sum(c**2 for c in self.doc1.word_freq.values())})")
        print(f"  |Doc2|            : {mag2:.4f}  (√{sum(c**2 for c in self.doc2.word_freq.values())})")
        print(f"  Cosine similarity : {cos:.4f}   (1.0 = identical, 0.0 = different)")
        print(f"  Document distance : {dist:.2f}°  (0° = identical, 90° = different)")
        similar_label = "YES ✓" if self.are_similar() else "NO ✗"
        print(f"  Similar? (< 45°)  : {similar_label}")
        print()


# --- Demo 1: Identical documents ---
print("  ── Case 1: Identical ──────────────────────────────")
d1 = Document("I love Programming")
d2 = Document("I love Programming")
DocumentDistance(d1, d2).report()

# --- Demo 2: Same subject, one word different ---
print("  ── Case 2: One word different ─────────────────────")
d3 = Document("I love Python")
DocumentDistance(d1, d3).report()

# --- Demo 3: Same opener, different topic ---
print("  ── Case 3: Mostly different ───────────────────────")
d4 = Document("I hate Java")
DocumentDistance(d1, d4).report()

# --- Demo 4: Completely no overlap ---
print("  ── Case 4: No shared words ────────────────────────")
d5 = Document("cats eat fish")
DocumentDistance(d1, d5).report()

# --- Demo 5: Repeated content (length should NOT matter) ---
print("  ── Case 5: Same content, repeated (angle should = 0°) ──")
d6 = Document("I love Programming I love Programming")
DocumentDistance(d1, d6).report()


# -----------------------------------------------------------------------------
# Instructor-style version — same algorithm, simpler code
# -----------------------------------------------------------------------------
#
# Instead of two separate classes (Document + DocumentDistance), one class
# receives the raw strings directly and does everything internally.
# No type hints, no Counter — just plain dicts and a manual loop.
# This is closer to what you'd write under interview time pressure.

class Document_distance:

    def __init__(self, doc1, doc2):
        # Split each document into a list of words
        # "I love Programming" → ['I', 'love', 'Programming']
        self.lst1 = doc1.split()
        self.lst2 = doc2.split()

    def word_freq(self, lst):
        """
        Build a frequency dictionary from a word list.
        ['I', 'love', 'I'] → {'i': 2, 'love': 1}

        Logic: for each word, lowercase it, then either
          - add it to the dict with count 1 (first time seen), or
          - increment its count (seen before)
        """
        freq = {}
        for word in lst:
            word = word.lower()          # treat 'I' and 'i' as the same word
            if word in freq:
                freq[word] += 1
            else:
                freq[word] = 1
        return freq

    def dot_product(self, freq1, freq2):
        """
        Σ (freq1[word] × freq2[word])  for every word shared by both docs.
        Words in only one document don't contribute (missing × anything = 0).
        """
        result = 0
        for word in freq1:
            if word in freq2:
                result += freq1[word] * freq2[word]
        return result

    def magnitude(self, freq):
        """
        Length of the frequency vector = √( Σ count² )
        Uses ** 0.5 instead of math.sqrt — same thing, no import needed.
        """
        total = 0
        for count in freq.values():
            total += count ** 2
        return total ** 0.5

    def similarity(self):
        """
        Cosine similarity = dot(A,B) / (|A| × |B|)
        Returns a number between 0 (different) and 1 (identical).
        """
        freq1 = self.word_freq(self.lst1)
        freq2 = self.word_freq(self.lst2)
        dot  = self.dot_product(freq1, freq2)
        mag1 = self.magnitude(freq1)
        mag2 = self.magnitude(freq2)
        if mag1 == 0 or mag2 == 0:    # guard: empty document → no similarity
            return 0
        return dot / (mag1 * mag2)

    def distance(self):
        """
        Document distance = arccos(cosine similarity), converted to degrees.
        0°  → identical
        90° → completely different
        """
        cos_sim = self.similarity()
        cos_sim = max(-1.0, min(1.0, cos_sim))   # clamp for floating-point safety
        return math.degrees(math.acos(cos_sim))


# --- Demo (instructor style) ---
print("  ── Instructor-style class ─────────────────────────")
pairs = [
    ("I love Programming", "I love Programming"),   # identical
    ("I love Programming", "I love Python"),         # one word different
    ("I love Programming", "I hate Java"),           # mostly different
]
for doc1_text, doc2_text in pairs:
    dd = Document_distance(doc1_text, doc2_text)
    cos  = dd.similarity()
    dist = dd.distance()
    print(f"  {doc1_text!r:25} vs {doc2_text!r:20}")
    print(f"    cos={cos:.4f}  angle={dist:.2f}°  {'similar ✓' if dist < 45 else 'different ✗'}")


# =============================================================================
# SECTION 10: Plagiarism Detection
# =============================================================================

# ----- Problem -----
# Given a submitted text and a source document, check what percentage of
# words in the text appear in the document. If > 50%, flag it as plagiarised.
#
# ----- Why is this different from Document Distance? -----
# Document Distance (Section 9) measures how SIMILAR two documents are as
# a whole — it's symmetric (A vs B = B vs A).
#
# Plagiarism is DIRECTIONAL — we ask: "what % of the SUBMITTED text's words
# appear in the SOURCE?" A short copy-paste into a long essay might score
# low similarity overall but 100% plagiarism on the copied portion.
#
# ----- Four Approaches (increasing sophistication) -----
#
#   Version 1 — Word overlap (instructor style):
#     For each word in text, check if it appears in document.
#     Simple O(n×m) scan using a list.
#
#   Version 2 — Set-based word overlap (faster):
#     Convert document to a set for O(1) lookup instead of O(m) scan.
#     Same result, much faster for large documents.
#
#   Version 3 — Jaccard similarity:
#     |words in BOTH| / |words in EITHER|
#     Symmetric measure of overlap between unique word sets.
#
#   Version 4 — N-gram (phrase) matching:
#     Instead of single words, check if CONSECUTIVE WORD SEQUENCES (phrases)
#     from the text appear in the document. Much harder to fool by
#     just replacing a few words.
#
# ----- Visual: Word Overlap -----
#
#   text     = "Python is a great programming language"
#   document = "Python is the most popular programming language in the world"
#
#   Word-by-word check:
#     Python      → in doc? YES ✓
#     is          → in doc? YES ✓
#     a           → in doc? NO  ✗
#     great       → in doc? NO  ✗
#     programming → in doc? YES ✓
#     language    → in doc? YES ✓
#
#   matched = 4 out of 6 words = 66.7%  → PLAGIARISED (> 50%)
#
# ----- Visual: N-gram (bigram) matching -----
#
#   text     = "Python is great"
#   bigrams from text = [("python","is"), ("is","great")]
#
#   document = "Python is the best"
#   bigrams from doc  = [("python","is"), ("is","the"), ("the","best")]
#
#   ("python","is") → in doc bigrams? YES ✓
#   ("is","great")  → in doc bigrams? NO  ✗
#
#   1 out of 2 bigrams matched = 50%
#   Phrase-level check is stricter — just sharing individual words isn't enough.

print("\n===== SECTION 10: Plagiarism Detection =====")


# ── Version 1: Instructor style — word overlap with a list ──────────────────
#
# Straightforward: loop over each word in text, scan the document list.
# Time: O(n × m)  — for every word in text (n), scan all of document (m)
# This is fine for short texts but slow for large documents (use Version 2).

class Plagiarism:

    def __init__(self, text, document):
        self.text     = text.lower().split()      # submitted text as word list
        self.document = document.lower().split()  # source document as word list

    def check(self):
        """Count how many words in text also appear in document."""
        count = 0
        for word in self.text:
            if word in self.document:   # O(m) scan each time — list lookup
                count += 1
        percentage = (count / len(self.text)) * 100
        verdict = "PLAGIARISED 🚨" if percentage > 50 else "Original ✓"
        print(f"  {percentage:.1f}% word overlap — {verdict}")
        return percentage


# ── Version 2: Set-based — same idea, O(1) lookup ───────────────────────────
#
# Converting the document to a set makes each lookup O(1) instead of O(m).
# For a 10,000-word document, this is ~10,000× faster per word checked.
#
# Time: O(n + m)  — O(m) once to build set, O(1) per word in text (n words)
# Space: O(m) extra for the set
#
# ----- Why does a set give O(1) lookup? -----
# A set stores words in a hash table. Python computes a hash of the word
# and jumps directly to that bucket — no scanning needed.
# A list has no such structure, so Python checks every element: O(m).

class PlagiarismFast:

    def __init__(self, text, document):
        self.text_words = text.lower().split()
        self.doc_set    = set(document.lower().split())  # O(m) to build, O(1) per lookup

    def check(self):
        count = sum(1 for word in self.text_words if word in self.doc_set)
        percentage = (count / len(self.text_words)) * 100
        verdict = "PLAGIARISED 🚨" if percentage > 50 else "Original ✓"
        print(f"  {percentage:.1f}% word overlap (fast set lookup) — {verdict}")
        return percentage


# ── Version 3: Jaccard Similarity ───────────────────────────────────────────
#
# Jaccard similarity measures overlap between two SETS of unique words.
#
#              |A ∩ B|          words in BOTH text and document
#   J(A,B) = ─────────  =  ──────────────────────────────────────
#              |A ∪ B|          words in EITHER text or document
#
# Unlike Version 1/2, Jaccard is SYMMETRIC (order doesn't matter)
# and only counts each unique word once (ignores repetition).
#
# ----- Visual -----
#
#   text     words = {python, is, great}
#   document words = {python, is, popular, language}
#
#   intersection (∩) = {python, is}           → 2 words
#   union        (∪) = {python, is, great, popular, language}  → 5 words
#
#   Jaccard = 2/5 = 0.40  →  40% — not plagiarised (< 50%)
#
# Range: 0.0 (no overlap) to 1.0 (identical word sets)

class PlagiarismJaccard:

    def __init__(self, text, document):
        self.text_set = set(text.lower().split())
        self.doc_set  = set(document.lower().split())

    def jaccard_similarity(self):
        intersection = self.text_set & self.doc_set   # words in both
        union        = self.text_set | self.doc_set   # words in either
        if not union:
            return 0.0
        return len(intersection) / len(union)

    def check(self):
        score      = self.jaccard_similarity()
        percentage = score * 100
        verdict    = "PLAGIARISED 🚨" if percentage > 50 else "Original ✓"
        print(f"  Jaccard = {score:.4f}  ({percentage:.1f}%) — {verdict}")
        print(f"  Shared words : {self.text_set & self.doc_set}")
        return percentage


# ── Version 4: N-gram (phrase) matching ─────────────────────────────────────
#
# Single-word matching is easy to fool:
#   Original: "Python is a great language"
#   Paraphrased: "Python is an excellent language"  → still 3/5 words match
#
# N-gram matching checks consecutive SEQUENCES of n words (phrases).
#   n=1 → unigrams (same as Version 1)
#   n=2 → bigrams  ("python is", "is a", "a great" ...)
#   n=3 → trigrams ("python is a", "is a great" ...)
#
# Harder to paraphrase AND still match — you'd have to change the entire
# phrase structure, not just swap one word.
#
# ----- How to build n-grams -----
#
#   words = ["python", "is", "a", "great", "language"]
#   bigrams (n=2):  [("python","is"), ("is","a"), ("a","great"), ("great","language")]
#
#   Sliding window of size n across the word list:
#     index 0: words[0:2] = ("python", "is")
#     index 1: words[1:3] = ("is", "a")
#     index 2: words[2:4] = ("a", "great")
#     index 3: words[3:5] = ("great", "language")

class PlagiarismNgram:

    def __init__(self, text, document, n=2):
        self.n    = n                                  # phrase length (2=bigram, 3=trigram)
        self.text_ngrams = self._build_ngrams(text.lower().split())
        self.doc_ngrams  = set(self._build_ngrams(document.lower().split()))

    def _build_ngrams(self, words: list) -> list:
        """
        Sliding window: take every consecutive sequence of n words.
        words = [w0, w1, w2, w3],  n=2
          → [(w0,w1), (w1,w2), (w2,w3)]
        """
        return [tuple(words[i:i + self.n]) for i in range(len(words) - self.n + 1)]

    def check(self):
        if not self.text_ngrams:
            print("  Text too short for n-gram analysis.")
            return 0.0
        matched = sum(1 for ng in self.text_ngrams if ng in self.doc_ngrams)
        percentage = (matched / len(self.text_ngrams)) * 100
        verdict = "PLAGIARISED 🚨" if percentage > 50 else "Original ✓"
        label = f"{self.n}-gram"
        print(f"  {label} match: {matched}/{len(self.text_ngrams)} phrases = {percentage:.1f}% — {verdict}")
        matched_phrases = [" ".join(ng) for ng in self.text_ngrams if ng in self.doc_ngrams]
        if matched_phrases:
            print(f"  Matched phrases: {matched_phrases}")
        return percentage

"""

The results highlight an interesting point worth noting:

The same text scored differently across versions:

Version	                Score	  Verdict
Word overlap (V1/V2)	66.7%	Plagiarised
Jaccard (V3)	        36.4%	Original
Bigram phrases (V4)	    40.0%	Original
Trigram phrases (V4)	0.0%	Original

Why the difference? 
Word overlap counts every repeated common word ("is", "Python") — it's the easiest to trigger.
Jaccard only counts unique words so common short words weigh less. 
N-grams are the strictest — "Python is a great" vs "Python is the most" 
breaks the bigram match at word 3, so only 2 out of 5 phrases match.

Real plagiarism detectors (like Turnitin) combine all of these 
plus stop-word filtering and semantic similarity.

"""

# --- Demo ---
text     = "Python is a great programming language"
document = "Python is the most popular programming language in the world"

print(f"\n  Text     : {text!r}")
print(f"  Document : {document!r}\n")

print("  Version 1 — word list (O(n×m)):")
Plagiarism(text, document).check()

print("\n  Version 2 — set lookup (O(n+m)):")
PlagiarismFast(text, document).check()

print("\n  Version 3 — Jaccard similarity:")
PlagiarismJaccard(text, document).check()

print("\n  Version 4 — bigram phrases (n=2):")
PlagiarismNgram(text, document, n=2).check()

print("\n  Version 4 — trigram phrases (n=3):")
PlagiarismNgram(text, document, n=3).check()

# Edge case: text almost identical to document
print("\n  --- Edge case: near-copy ---")
text2     = "Python is the most popular programming language"
document2 = "Python is the most popular programming language in the world"
print(f"  Text     : {text2!r}")
print(f"  Document : {document2!r}")
Plagiarism(text2, document2).check()
PlagiarismNgram(text2, document2, n=3).check()


# =============================================================================
# SECTION 11: Interview Q&A
# =============================================================================

print("\n===== SECTION 11: Interview Q&A =====")

"""
Q1: Why use two stacks to implement a queue instead of just using a list?
A:  The constraint in the problem is that you ONLY have stack operations available.
    It tests whether you understand how to simulate one data structure using another.
    In practice you'd use collections.deque, but the exercise builds deeper
    understanding of both structures.

Q2: What is amortised O(1) and how does it apply to the queue-using-stacks?
A:  Amortised analysis averages the cost over a sequence of operations.
    In our two-stack queue, a single dequeue CAN trigger O(n) work (pouring inbox
    into outbox). But that O(n) work is "paid for" by the n prior enqueues that
    were each O(1). Across any n operations, total work is O(n) → O(1) per op.

Q3: What does it mean when you say a min stack uses O(n) extra space?
A:  We maintain a second stack (min_stack) that is always the same height as
    the main stack. If the main stack has n elements, min_stack also has n elements.
    So we use 2× memory, which is O(n) extra space (constant multiplier on n).

Q4: Why does visiting a new URL clear the forward history in the browser model?
A:  Because forward history is only valid for the path you CAME BACK FROM.
    Once you navigate somewhere new, those "future" pages are no longer reachable
    through the linear history — they've been replaced by the new URL's history.
    This is exactly how Chrome, Firefox etc. behave.

Q5: What is the difference between a linked list and a Python list?
A:  Python list   = dynamic array. Random access O(1), insert/delete in middle O(n).
    Linked list   = chain of nodes. No random access O(n), insert/delete at known
    node O(1) (just pointer update), but you pay O(n) to FIND that node first.
    Linked lists shine when you're always operating at the front (stack/queue).

Q6: When would you use an LRU cache in a real system?
A:  Database layer: cache query results (key = query string, value = result set).
    Web layer: cache rendered HTML or API responses.
    Memory management: OS page replacement policy.
    The key insight: not all data is accessed equally — a small cache of recently
    used items (typically 80/20 rule) eliminates most expensive lookups.

Q7: What Python built-in could replace LRUCache?
A:  functools.lru_cache — a decorator that caches function call results.
    Example:
        from functools import lru_cache
        @lru_cache(maxsize=128)
        def expensive_fn(n):
            ...
    Under the hood it uses the same OrderedDict approach shown here.
"""

print("See docstring above for Interview Q&A.")
print("\nAll sections complete.")
