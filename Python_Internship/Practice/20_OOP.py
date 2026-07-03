###############################################################################
#             OOP Use Cases — Part 2: Real-World System Design                #
###############################################################################

"""
This file is a continuation of 19_OOP_usecases.py.
It covers new OOP-based data structures and system design problems.

Pre-requisites:
    17_OOP.py          — classes, __init__, encapsulation, inheritance, dunder methods
    18_OOP_contd.py    — class methods, static methods, properties, polymorphism
    19_OOP_usecases.py — Stack, Singly Linked List, Queue, MinStack, LRU Cache

Topics in this file:
    Section 0:  Linked List From Scratch — Dict-based → Class-based
    Section 1:  Music Playlist — Doubly Linked List
    Section 2:  Binary Search Tree — Contact Book
    Section 3:  Priority Queue (Min-Heap) — Hospital Emergency Room
    Section 4:  Graph — Social Network
    Section 5:  Shopping Cart — OOP Composition + Inheritance
    Section 6:  Parking Lot System — OOP Design Interview
    Section 7:  Observer Pattern — Stock Price Alerts
    Section 8:  Interview Q&A — Design Questions

Key theme: Most interview system-design questions are just one of these
data structures in disguise. Learn the structure, not just the use case.
"""

import heapq
import math
from collections import deque, defaultdict


# =============================================================================
# ─── QUICK RECAP: Array vs Linked List ───────────────────────────────────────
# =============================================================================
#
# The stub for this file asked: "How is linked list different from array?"
# Here is the complete answer:
#
#  ┌────────────────────────┬──────────────────────────────────────────────────┐
#  │ Property               │ Array (Python list)      │ Linked List           │
#  ├────────────────────────┼──────────────────────────┼───────────────────────┤
#  │ Memory layout          │ Contiguous — all items   │ Non-contiguous — each │
#  │                        │ sit next to each other   │ node can be anywhere  │
#  │                        │ in RAM                   │ in memory             │
#  ├────────────────────────┼──────────────────────────┼───────────────────────┤
#  │ Access by index        │ O(1) — index directly    │ O(n) — must walk from │
#  │ e.g. arr[3]            │ maps to memory address   │ head node to node 3   │
#  ├────────────────────────┼──────────────────────────┼───────────────────────┤
#  │ Insert at beginning    │ O(n) — shift all items   │ O(1) — just rewire    │
#  │                        │ right to make room       │ the head pointer      │
#  ├────────────────────────┼──────────────────────────┼───────────────────────┤
#  │ Insert at end          │ O(1) amortized           │ O(n) singly / O(1)    │
#  │                        │ (append is fast)         │ if tail pointer kept  │
#  ├────────────────────────┼──────────────────────────┼───────────────────────┤
#  │ Delete from middle     │ O(n) — shift items       │ O(n) to find + O(1)   │
#  │                        │ to fill the gap          │ to remove (rewire)    │
#  ├────────────────────────┼──────────────────────────┼───────────────────────┤
#  │ Memory overhead        │ Low — just data values   │ Higher — each node    │
#  │                        │                          │ stores data + pointer │
#  └────────────────────────┴──────────────────────────┴───────────────────────┘
#
# ─── Memory Layout Visual ────────────────────────────────────────────────────
#
#   Array: elements stored sequentially in memory
#   ┌────┬────┬────┬────┬────┐
#   │ 10 │ 20 │ 30 │ 40 │ 50 │   All sit side-by-side in RAM
#   └────┴────┴────┴────┴────┘
#    [0]  [1]  [2]  [3]  [4]     Access arr[3] = 40 instantly (pointer math)
#
#   Singly Linked List: each node points to the next one
#   [10] → [20] → [30] → [40] → [50] → None
#    head                         tail
#   Nodes can be scattered across memory — connected by pointers only.
#
#   Doubly Linked List (used in Music Playlist below): points BOTH ways
#   None ← [10] ⇄ [20] ⇄ [30] ⇄ [40] ⇄ [50] → None
#           head                          tail
#   Can traverse forward AND backward — essential for playlist navigation.
#
# ─── When to use which? ──────────────────────────────────────────────────────
#
#   Use ARRAY when:                     Use LINKED LIST when:
#   - You need index-based access       - You insert/delete at front often
#   - Cache efficiency matters          - You don't know size upfront
#   - Simple iteration                  - Memory for a fixed array is wasteful
#   Example: leaderboard, matrix        Example: playlist, undo history


# =============================================================================
# SECTION 0: Linked List From Scratch — How to Actually Build One
# =============================================================================
#
# Before diving into the Music Playlist, this section shows you HOW a linked
# list is constructed step by step — starting from the instructor's dict-based
# approach, building it up piece by piece, then transitioning to the class-based
# version used in the rest of this file.
#
# ─── The Core Idea ───────────────────────────────────────────────────────────
#
# A linked list is just NODES connected by LINKS.
# In Python, the simplest way to represent a node is a dictionary:
#
#   node = {"data": "Song A", "link": None}
#
#   "data"  → the actual value stored in this node
#   "link"  → a reference (pointer) to the NEXT node, or None if it's the last
#
# The LINKED LIST itself starts as {} (empty dict) and is just the HEAD node
# — the first node. Everything else is reachable by following .link chains.
#
# ─── Visual: what the data looks like in memory ──────────────────────────────
#
#   EMPTY list:
#   LL = {}   ← just an empty dict. No nodes yet.
#
#   After inserting "Song A":
#   LL = {"data": "Song A", "link": None}
#        ──────────────────────────────
#        This IS the first (and only) node. LL points to it directly.
#
#   After inserting "Song B":
#   LL = {"data": "Song A", "link": ──────────────────────────────►{"data": "Song B", "link": None}}
#         head node                                                   second node
#
#   After inserting "Song C":
#   LL = {"data": "Song A",  →  {"data": "Song B",  →  {"data": "Song C", "link": None}
#          "link": ──────►}      "link": ──────►}
#         head (LL)              middle              tail (link = None)
#
# ─── How the chain is traversed ──────────────────────────────────────────────
#
#   To WALK through all nodes:
#   current = LL                    # start at head
#   while current is not None:
#       print(current["data"])      # access the value
#       current = current["link"]   # follow the link to the next node
#
#   The loop ends when current["link"] is None (we've reached the tail).
#
# ─── The Instructor's Starting Code (explained) ──────────────────────────────
#
#   class linked_list_implementation:
#       def __init__(self):
#           self.LL = {}             # empty dict = empty linked list
#
#       def insert_node(self, value):
#           node = {"data": value, "link": None}   # create a new node
#           if self.LL == {}:                       # if list is currently empty
#               self.LL = node                     # THIS node becomes the head
#           return self.LL
#
#   The issue: this only handles the EMPTY case.
#   What if the list already HAS nodes? We need to WALK to the end and
#   attach the new node there. That's what the full implementation below adds.
#
# ─── Step-by-Step: Inserting "Song A", "Song B", "Song C" ───────────────────
#
#   Step 1 — Insert "Song A":
#     node = {"data": "Song A", "link": None}
#     self.LL is {} → assign: self.LL = node
#     State: LL = {"data": "Song A", "link": None}
#
#   Step 2 — Insert "Song B":
#     node = {"data": "Song B", "link": None}
#     self.LL is NOT {} → must find the tail
#     current = self.LL  →  current = {"data": "Song A", "link": None}
#     current["link"] is None → we found the tail!
#     current["link"] = node   →  Song A now points to Song B
#     State: LL = {"data": "Song A", "link": {"data": "Song B", "link": None}}
#
#   Step 3 — Insert "Song C":
#     node = {"data": "Song C", "link": None}
#     current = LL → {"data": "Song A", "link": (Song B node)}
#     current["link"] is NOT None → keep walking
#     current = current["link"] → {"data": "Song B", "link": None}
#     current["link"] is None → found the tail!
#     current["link"] = node
#     State: LL = Song A → Song B → Song C → None
#
#
# =============================================================================
# ─── WHY DO WE NEED A TEMPORARY VARIABLE? (the most confusing part) ──────────
# =============================================================================
#
# Your question: "use a temporary variable, assign the linked list to it,
# this temp variable will point to the first node, because we can't move the
# pointer... then temp["link"] = new node"
#
# You got the RIGHT instinct. Let's make it crystal clear.
#
# ─── THE PROBLEM ─────────────────────────────────────────────────────────────
#
# To insert at the END, we need to WALK through the entire list to find the
# last node (the one whose "link" is None). We walk by doing:
#
#     move to next node → move to next node → move to next node → reached None
#
# But to "move forward" we have to CHANGE what our variable is pointing at.
# And if the only variable we have is self.LL... we'd be moving self.LL forward,
# which means we'd LOSE the start of the list. We can never get back to the
# beginning. The whole list is gone.
#
# So we need a SECOND variable — a temporary one — that can move freely
# while self.LL stays frozen at the head (start) of the list.
#
# ─── PYTHON VARIABLES ARE LABELS, NOT BOXES ──────────────────────────────────
#
# This is the key mental model shift. In Python, a variable is NOT a box that
# holds a value. It is a LABEL (a sticky note) that POINTS to an object.
#
#   x = 5       →  label "x" points to the integer object 5
#   y = x       →  label "y" ALSO points to the same integer 5
#                  (nothing is copied — both labels point to the same thing)
#   y = 10      →  label "y" now points to 10
#                  label "x" is unaffected. x is still 5.
#
# The same principle applies to dict nodes:
#
#   self.LL = {"data": "Song A", "link": None}
#   current  = self.LL
#
#   Now BOTH "self.LL" and "current" are labels pointing to the SAME Song A dict.
#   Moving "current" later does NOT affect "self.LL" at all.
#
# ─── VISUAL: What happens in memory ──────────────────────────────────────────
#
#   State: list has Song A → Song B → None
#
#   Memory (in RAM):
#   ┌─────────────────────────────┐     ┌─────────────────────────────┐
#   │  {"data": "Song A",         │     │  {"data": "Song B",         │
#   │   "link": ─────────────────►│────►│   "link": None}             │
#   └─────────────────────────────┘     └─────────────────────────────┘
#          ▲                                       ▲
#          │                                       │
#       self.LL                                 (no name yet)
#       current  ← after "current = self.LL", current ALSO points here
#
#   Step: current = self.LL
#
#          self.LL ───────────────────────────►  [Song A] ──► [Song B] ──► None
#          current ───────────────────────────►  (same Song A node)
#
#   self.LL and current are two DIFFERENT labels pinned to the SAME node.
#
# ─── VISUAL: Moving current forward ──────────────────────────────────────────
#
#   Step: current = current["link"]
#   (current["link"] IS the Song B node, so current now points to Song B)
#
#          self.LL ───────────────────────────►  [Song A] ──► [Song B] ──► None
#                                                                  ▲
#          current ───────────────────────────────────────────────►
#
#   self.LL has NOT moved. It's still anchored to Song A.
#   current has moved to Song B.
#   The list structure in memory is completely unchanged — all we did was
#   move the "current" label to point at a different node.
#
# ─── VISUAL: Attaching the new node ──────────────────────────────────────────
#
#   current["link"] is None → Song B is the tail. Attach here.
#
#   Step: current["link"] = node   (node = {"data": "Song C", "link": None})
#
#   This changes the Song B dict IN MEMORY:
#   Song B's "link" was None → it's now pointing to the Song C node.
#
#   Result:
#          self.LL ──► [Song A] ──► [Song B] ──► [Song C] ──► None
#
#   self.LL still points to Song A. The whole list is intact and extended.
#
# ─── WHY does current["link"] = node affect the real list? ───────────────────
#
# Because current is not a COPY of Song B. It's a LABEL pointing TO Song B.
# When you write current["link"] = something, you are modifying the actual
# Song B dictionary object in memory. Any other variable pointing to Song B
# (like self.LL["link"] which also reaches Song B by following the chain)
# sees that change too — because it's the SAME object.
#
# Contrast with:
#   current = current["link"]   →  moves the LABEL (current now points elsewhere)
#   current["link"] = node      →  modifies the OBJECT that current is pointing at
#
# One changes WHERE current points. The other changes the CONTENTS of what it points at.
#
# ─── THE TRAIN ANALOGY ───────────────────────────────────────────────────────
#
#   Imagine the linked list is a train:
#
#   [Engine/head] ──► [Carriage 1] ──► [Carriage 2] ──► [End]
#
#   self.LL is a GPS tracker WELDED to the engine.
#   It ALWAYS shows where the engine is. It cannot move.
#
#   current (or "temp") is a PERSON walking through the train.
#   They start at the engine:  current = self.LL  →  person steps onto engine.
#   They walk forward:         current = current["link"]  →  now in Carriage 1.
#   They walk again:           current = current["link"]  →  now in Carriage 2.
#   Carriage 2's "link" is None (no next carriage) → they're at the last one.
#
#   The GPS tracker hasn't moved — it still shows the engine.
#   The person attaches a new carriage: current["link"] = new_node
#   → Carriage 2 now links to the new carriage.
#   → self.LL still points to the engine, which chains all the way to the new one.
#
# ─── THE LOOP IN PLAIN ENGLISH ───────────────────────────────────────────────
#
#   current = self.LL                      # person steps onto head node
#   while current["link"] is not None:     # while there IS a next node...
#       current = current["link"]          # ...walk to that next node
#   current["link"] = node                 # we're at the tail: attach new node
#
#   Translation:
#   "Start at the beginning. Keep moving forward until there's nothing ahead.
#    When you're at the end, hook the new node on."
#
# ─── COMMON MISTAKE: doing it without temp ───────────────────────────────────
#
#   # WRONG — do NOT do this:
#   while self.LL["link"] is not None:
#       self.LL = self.LL["link"]    # ← you just moved self.LL off the head!
#   self.LL["link"] = node           # now self.LL points to the tail, not head
#
#   After this, self.LL no longer points to Song A.
#   You've lost the beginning of the list forever. The list is BROKEN.
#
#   # RIGHT — always use a temp/current:
#   current = self.LL                # temp copy of the starting label
#   while current["link"] is not None:
#       current = current["link"]    # move temp, NOT self.LL
#   current["link"] = node           # attach at tail; self.LL still at head ✓
#
# ─── SUMMARY ─────────────────────────────────────────────────────────────────
#
#   self.LL   = the ANCHOR (head pointer). Never move it. It's how we find
#               the entire list. Lose it → lose the list.
#
#   current   = the WALKER (temp pointer). Starts at self.LL, then walks
#   (or temp)   forward one node at a time until it finds the tail.
#               Moving current does NOT affect self.LL.
#
#   Two types of operations on a reference variable:
#   ┌────────────────────────────────────────────────────────────────────────┐
#   │  current = current["link"]    MOVES the label (now points to next)    │
#   │  current["link"] = new_node   MODIFIES the object the label points to │
#   └────────────────────────────────────────────────────────────────────────┘
#
#   The first line changes WHERE current points.
#   The second line changes the CONTENT of what current is pointing at.
#   This distinction is the key to understanding ALL linked list operations.
#
#
# ─── Deletion: rewiring the "link" pointer ───────────────────────────────────
#
#   To delete "Song B" from:  Song A → Song B → Song C → None
#
#   We need to find the node BEFORE Song B (i.e., Song A),
#   then set Song A's link to point to Song C, skipping Song B entirely.
#
#   Before:  Song A ──► Song B ──► Song C → None
#   After:   Song A ────────────► Song C → None
#                        Song B is now unreachable → garbage collected
#
#   Special case: if we're deleting the HEAD node, just move LL to LL["link"].

print("===== SECTION 0: Linked List From Scratch =====")

# =============================================================================
# ─── ALL 6 FUNDAMENTAL OPERATIONS — Visual Guide ─────────────────────────────
# =============================================================================
#
# Starting list for all examples below:
#
#   self.LL ──► [A] ──► [B] ──► [C] ──► None
#               head           tail
#
# ┌─────┬──────────────────────────┬────────────────────────────────────────────┐
# │  #  │ Operation                │ What changes                               │
# ├─────┼──────────────────────────┼────────────────────────────────────────────┤
# │  1  │ Add at BEGINNING         │ new node's link = old head; head = new     │
# │  2  │ Add at END               │ walk to tail; tail's link = new node       │
# │  3  │ Add IN BETWEEN (after B) │ new.link = B.link; B.link = new            │
# │  4  │ Remove FIRST (head)      │ head = head.link                           │
# │  5  │ Remove LAST (tail)       │ walk to node BEFORE tail; its link = None  │
# │  6  │ Remove IN BETWEEN (B)    │ walk to A; A.link = B.link (skip B)        │
# └─────┴──────────────────────────┴────────────────────────────────────────────┘
#
# ─────────────────────────────────────────────────────────────────────────────
# OPERATION 1: Add at BEGINNING (prepend)         O(1)
# ─────────────────────────────────────────────────────────────────────────────
#
#   Before:  self.LL ──► [A] ──► [B] ──► [C] ──► None
#
#   Step 1:  Create new node Z:     [Z] link=None
#   Step 2:  Point Z's link at old head:   [Z] ──► [A] ──► [B] ──► [C] ──► None
#   Step 3:  Move self.LL to Z:     self.LL ──► [Z] ──► [A] ──► [B] ──► [C] ──► None
#
#   After:   self.LL ──► [Z] ──► [A] ──► [B] ──► [C] ──► None
#
#   Why O(1)? No walking needed — we only touch the head and the new node.
#
#   Code:
#     node["link"] = self.LL    # Z points to the old head (A)
#     self.LL = node            # LL now points to Z (new head)
#
# ─────────────────────────────────────────────────────────────────────────────
# OPERATION 2: Add at END (append)               O(n)
# ─────────────────────────────────────────────────────────────────────────────
#
#   Before:  self.LL ──► [A] ──► [B] ──► [C] ──► None
#
#   Step 1:  Create new node D:  [D] link=None
#   Step 2:  Walk to the tail (C) using current:
#              current = self.LL  →  current at A
#              current["link"] not None → current at B
#              current["link"] not None → current at C
#              current["link"] is None  → STOP. current is at C (the tail).
#   Step 3:  current["link"] = new_node   →  C now points to D
#
#   After:   self.LL ──► [A] ──► [B] ──► [C] ──► [D] ──► None
#
#   Why O(n)? Must walk through all n nodes to reach the tail.
#   (Can make O(1) by keeping a separate tail pointer — used in Section 1)
#
#   Code:
#     current = self.LL
#     while current["link"] is not None:
#         current = current["link"]
#     current["link"] = node
#
# ─────────────────────────────────────────────────────────────────────────────
# OPERATION 3: Add IN BETWEEN — insert after a given node    O(n)
# ─────────────────────────────────────────────────────────────────────────────
#
#   Goal: insert X after B.
#   Before:  [A] ──► [B] ──► [C] ──► None
#
#   Step 1:  Create new node X: [X] link=None
#   Step 2:  Walk to B (current = B after searching for it).
#   Step 3:  Save what B currently points to:  [X]["link"] = B["link"]   →  X ──► C
#   Step 4:  Make B point to X instead:        B["link"] = X             →  B ──► X
#
#   After:   [A] ──► [B] ──► [X] ──► [C] ──► None
#
#   WHY MUST step 3 come BEFORE step 4?
#   If you did step 4 first (B["link"] = X), you would LOSE the pointer to C.
#   B's link now points to X, and C is unreachable — gone forever.
#   Always: save the "what comes next" pointer BEFORE overwriting it.
#
#   Mnemonic: "Save before you sever."
#
#   Code:
#     new_node["link"] = current["link"]   # new node → C  (save first)
#     current["link"] = new_node           # B → new node  (sever after)
#
# ─────────────────────────────────────────────────────────────────────────────
# OPERATION 4: Remove FIRST node (head)          O(1)
# ─────────────────────────────────────────────────────────────────────────────
#
#   Before:  self.LL ──► [A] ──► [B] ──► [C] ──► None
#
#   Step 1:  self.LL = self.LL["link"]   →  self.LL now points to B
#   (A is now unreachable — Python garbage collects it automatically)
#
#   After:   self.LL ──► [B] ──► [C] ──► None
#
#   Edge case: if only ONE node existed, self.LL["link"] is None,
#   so self.LL becomes None (or {} for the dict version) — empty list. ✓
#
#   Why O(1)? No walking. Just move the head pointer one step forward.
#
#   Code:
#     self.LL = self.LL["link"]   # (or {} if that was the only node)
#
# ─────────────────────────────────────────────────────────────────────────────
# OPERATION 5: Remove LAST node (tail)           O(n)
# ─────────────────────────────────────────────────────────────────────────────
#
#   Before:  self.LL ──► [A] ──► [B] ──► [C] ──► None
#
#   We need to reach [B] (the node BEFORE the tail), then cut its link.
#   We can't just jump to the tail directly — we need its PREDECESSOR.
#
#   Step 1:  Walk until current["link"]["link"] is None
#              current = A:  A["link"]["link"] = C["link"] = None? No, B["link"] = C ≠ None
#              current = B:  B["link"]["link"] = C["link"] = None  ← STOP
#   Step 2:  current["link"] = None   →  B's link cut to None (C is detached)
#
#   After:   self.LL ──► [A] ──► [B] ──► None     [C] is garbage collected
#
#   Edge case: if only ONE node, just set self.LL = {} (empty). No loop needed.
#
#   Why O(n)? Must walk to the second-to-last node. No way to get there faster
#   in a singly linked list (that's why doubly linked lists exist — they can
#   go backward from the tail to find its predecessor in O(1)).
#
#   Code:
#     current = self.LL
#     while current["link"]["link"] is not None:
#         current = current["link"]
#     current["link"] = None
#
# ─────────────────────────────────────────────────────────────────────────────
# OPERATION 6: Remove IN BETWEEN — remove a specific middle node    O(n)
# ─────────────────────────────────────────────────────────────────────────────
#
#   Goal: remove B from  [A] ──► [B] ──► [C] ──► None
#
#   We need to find the node BEFORE B (which is A), then rewire A to skip B.
#
#   Step 1:  Walk until current["link"]["data"] == target
#              current = A:  A["link"]["data"] == "B" ← FOUND
#   Step 2:  current["link"] = current["link"]["link"]
#            i.e.  A["link"] = B["link"] = C
#            A now points directly to C, skipping B.
#
#   After:   [A] ──► [C] ──► None      [B] is garbage collected
#
#   Why don't we stop AT B?
#   Because once you're AT B, you've lost the pointer to A.
#   You can't go backward in a singly linked list.
#   We must stop at the node BEFORE the target so we can rewire it.
#
#   Code:
#     current = self.LL
#     while current["link"] is not None:
#         if current["link"]["data"] == target:
#             current["link"] = current["link"]["link"]   # skip the target
#             return
#         current = current["link"]


# ─── Approach 1: Instructor's dict-based linked list (all 6 operations) ──────

class LinkedListDict:
    """
    Linked list using dictionaries as nodes.
    node format: {"data": value, "link": next_node_or_None}

    All 6 fundamental operations implemented and demonstrated.
    """

    def __init__(self):
        self.LL = {}        # {} means "empty list" (no head node yet)

    # ══════════════════════════════════════════════════════════════════════════
    # INSERT OPERATIONS
    # ══════════════════════════════════════════════════════════════════════════

    def insert_at_front(self, value):
        """
        OPERATION 1 — Add at BEGINNING.  O(1)
        New node points to old head, then becomes the new head.
        """
        node = {"data": value, "link": None}
        if self.LL == {}:
            self.LL = node
        else:
            node["link"] = self.LL   # step 2: new node → old head
            self.LL = node           # step 3: LL moves to new node

    def insert_at_end(self, value):
        """
        OPERATION 2 — Add at END.  O(n)
        Walk to the tail node (where link is None), then attach.
        """
        node = {"data": value, "link": None}
        if self.LL == {}:
            self.LL = node
        else:
            current = self.LL
            while current["link"] is not None:   # walk until tail
                current = current["link"]
            current["link"] = node               # attach at tail

    def insert_after(self, target, value):
        """
        OPERATION 3 — Add IN BETWEEN (after a given value).  O(n)
        Walk to target node, then splice new node in.
        CRITICAL: save the "next" pointer BEFORE overwriting it.
        """
        if self.LL == {}:
            print(f"  List is empty.")
            return
        current = self.LL
        while current is not None:
            if current["data"] == target:
                node = {"data": value, "link": None}
                node["link"] = current["link"]   # save: new node → what was next
                current["link"] = node           # sever: target now → new node
                return
            current = current["link"]
        print(f"  '{target}' not found.")

    # ══════════════════════════════════════════════════════════════════════════
    # DELETE OPERATIONS
    # ══════════════════════════════════════════════════════════════════════════

    def delete_first(self):
        """
        OPERATION 4 — Remove FIRST node (head).  O(1)
        Just move the head pointer one step forward.
        """
        if self.LL == {}:
            print("  List is empty.")
            return
        removed = self.LL["data"]
        self.LL = self.LL["link"] if self.LL["link"] is not None else {}
        print(f"  Removed first: '{removed}'")

    def delete_last(self):
        """
        OPERATION 5 — Remove LAST node (tail).  O(n)
        Walk to the node BEFORE the tail, then cut its link.
        Must stop at second-to-last (not the last) because singly linked
        lists can't go backward.
        """
        if self.LL == {}:
            print("  List is empty.")
            return
        # Only one node
        if self.LL["link"] is None:
            removed = self.LL["data"]
            self.LL = {}
            print(f"  Removed last: '{removed}'")
            return
        # Walk to the second-to-last node
        current = self.LL
        while current["link"]["link"] is not None:   # stop when next's next is None
            current = current["link"]
        # current is now the second-to-last; current["link"] is the tail
        removed = current["link"]["data"]
        current["link"] = None                       # cut the tail off
        print(f"  Removed last: '{removed}'")

    def delete_middle(self, value):
        """
        OPERATION 6 — Remove a specific IN-BETWEEN node by value.  O(n)
        Walk to the node BEFORE the target, then rewire to skip it.
        Also handles head and tail — those are just special cases of "any node".
        """
        if self.LL == {}:
            print("  List is empty.")
            return
        # Special case: target is the head
        if self.LL["data"] == value:
            self.LL = self.LL["link"] if self.LL["link"] is not None else {}
            print(f"  Removed '{value}' (was head)")
            return
        # Walk to the node BEFORE the target
        current = self.LL
        while current["link"] is not None:
            if current["link"]["data"] == value:
                removed = current["link"]["data"]
                current["link"] = current["link"]["link"]   # skip over target
                print(f"  Removed '{removed}'")
                return
            current = current["link"]
        print(f"  '{value}' not found.")

    # ══════════════════════════════════════════════════════════════════════════
    # UTILITY
    # ══════════════════════════════════════════════════════════════════════════

    def search(self, value):
        current = self.LL
        pos = 0
        while current != {} and current is not None:
            if current["data"] == value:
                print(f"  Found '{value}' at position {pos}")
                return True
            current = current["link"]
            pos += 1
        print(f"  '{value}' not found")
        return False

    def display(self, label=""):
        prefix = f"  {label}: " if label else "  "
        if self.LL == {}:
            print(prefix + "(empty)")
            return
        parts = []
        current = self.LL
        while current is not None:
            parts.append(str(current["data"]))
            current = current["link"]
        print(prefix + " → ".join(parts) + " → None")

    def display_raw(self):
        import pprint
        print("  Raw dict structure:")
        pprint.pprint(self.LL, indent=4)

    def length(self):
        count = 0
        current = self.LL
        while current != {} and current is not None:
            count += 1
            current = current["link"]
        return count


# ── Demo: all 6 operations, one at a time ────────────────────────────────────

print("\n  ── Dict-based LL: Watching nodes grow ──")
ll = LinkedListDict()
print("  Initial:", ll.LL)

ll.insert_at_end("A")
ll.display_raw()
ll.display("After add 'A' at end")

ll.insert_at_end("B")
ll.display_raw()
ll.display("After add 'B' at end")

ll.insert_at_end("C")
ll.display_raw()
ll.display("After add 'C' at end")

print()
print("  ── OPERATION 1: Add at BEGINNING ──")
ll.insert_at_front("Z")
ll.display("After insert_at_front('Z')")   # Z → A → B → C

print()
print("  ── OPERATION 2: Add at END ──")
ll.insert_at_end("D")
ll.display("After insert_at_end('D')")    # Z → A → B → C → D

print()
print("  ── OPERATION 3: Add IN BETWEEN (after 'B') ──")
ll.insert_after("B", "X")
ll.display("After insert_after('B','X')") # Z → A → B → X → C → D

print()
print("  ── OPERATION 4: Remove FIRST ──")
ll.delete_first()
ll.display("After delete_first()")        # A → B → X → C → D

print()
print("  ── OPERATION 5: Remove LAST ──")
ll.delete_last()
ll.display("After delete_last()")         # A → B → X → C

print()
print("  ── OPERATION 6: Remove IN BETWEEN (remove 'X') ──")
ll.delete_middle("X")
ll.display("After delete_middle('X')")    # A → B → C

print(f"\n  Final length: {ll.length()}")


# ─── Approach 2: Class-based Node (the "proper" way) ─────────────────────────
#
# The dict approach above works, but has two downsides:
#
# 1. String keys ("data", "link") are error-prone: if you typo "lnk" instead
#    of "link", Python silently creates a new key instead of crashing.
#    A class raises AttributeError immediately on a bad attribute name.
#
# 2. No methods on nodes — you have to pass the node around and call external
#    functions on it. A class lets the node carry its own behaviour.
#
# Comparison:
#
#   Dict node:                      Class node:
#   node = {                        class Node:
#     "data": "Song A",                 def __init__(self, data):
#     "link": None                          self.data = data
#   }                                       self.next = None
#   node["link"] = next_node           node.next = next_node
#
# The logic is IDENTICAL — just dot-notation instead of bracket-notation.
# The class version is more readable and safer. That's the only difference.
#
# ─── Side-by-side comparison ─────────────────────────────────────────────────
#
#   Operation          Dict version                 Class version
#   ─────────────────────────────────────────────────────────────
#   Create node        {"data": v, "link": None}    Node(v)
#   Access data        node["data"]                 node.data
#   Access next        node["link"]                 node.next
#   Set next           node["link"] = other         node.next = other
#   Check if tail      node["link"] is None         node.next is None
#
# The traversal loop is exactly the same concept:
#
#   Dict:              current = current["link"]
#   Class:             current = current.next
#
# ─── Full class-based implementation ─────────────────────────────────────────

class Node:
    """One node in a singly linked list. Stores data + a pointer to the next node."""
    def __init__(self, data):
        self.data = data
        self.next = None         # None means "this is the last node"

    def __repr__(self):
        return f"Node({self.data!r})"


class LinkedList:
    """
    Singly linked list — class-based version.
    All 6 operations as dedicated named methods with full explanations.
    """

    def __init__(self):
        self.head = None
        self._size = 0

    # ══════════════════════════════════════════════════════════════════════════
    # INSERT OPERATIONS
    # ══════════════════════════════════════════════════════════════════════════

    def insert_at_front(self, data):
        """
        OPERATION 1 — Add at BEGINNING.  O(1)

        Before:  head ──► [A] ──► [B] ──► [C] ──► None
        After:   head ──► [Z] ──► [A] ──► [B] ──► [C] ──► None

        Steps:
          1. Create new node Z
          2. Z.next = self.head  (Z points to old head A)
          3. self.head = Z       (head now points to Z)
        """
        node = Node(data)
        node.next = self.head    # new node → old head
        self.head = node         # head pointer moves to new node
        self._size += 1

    def insert_at_end(self, data):
        """
        OPERATION 2 — Add at END.  O(n)

        Before:  head ──► [A] ──► [B] ──► [C] ──► None
        After:   head ──► [A] ──► [B] ──► [C] ──► [D] ──► None

        Steps:
          1. Create new node D
          2. Walk current from head until current.next is None (found C)
          3. current.next = D
        """
        node = Node(data)
        if self.head is None:
            self.head = node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = node
        self._size += 1

    def insert_after(self, target_data, new_data):
        """
        OPERATION 3 — Add IN BETWEEN (after a given node).  O(n)

        Goal: insert X after B.
        Before:  [A] ──► [B] ──► [C] ──► None
        After:   [A] ──► [B] ──► [X] ──► [C] ──► None

        Steps:
          1. Walk until current.data == target (find B)
          2. new_node.next = current.next   (X → C)   ← SAVE FIRST
          3. current.next = new_node        (B → X)   ← SEVER SECOND

        Why save first? If you did step 3 before step 2:
          B.next = X  → now X.next = B.next = X (points to itself!)
          You've lost C forever. Always save before severing.
        """
        current = self.head
        while current is not None:
            if current.data == target_data:
                node = Node(new_data)
                node.next = current.next    # save: new → what was next
                current.next = node         # sever: target → new
                self._size += 1
                return
            current = current.next
        print(f"  '{target_data}' not found.")

    def insert_before(self, target_data, new_data):
        """
        OPERATION 3b — Add IN BETWEEN (before a given node).  O(n)

        Goal: insert X before B.
        Before:  [A] ──► [B] ──► [C] ──► None
        After:   [A] ──► [X] ──► [B] ──► [C] ──► None

        This is trickier than insert_after — we must stop at A (before B),
        because we can't go backward once we're at B.

        Steps:
          1. Special case: if target is head, call insert_at_front instead.
          2. Walk until current.next.data == target (stop at A, not B)
          3. new_node.next = current.next   (X → B)
          4. current.next = new_node        (A → X)
        """
        if self.head is None:
            print("  List is empty.")
            return
        if self.head.data == target_data:
            self.insert_at_front(new_data)
            return
        current = self.head
        while current.next is not None:
            if current.next.data == target_data:
                node = Node(new_data)
                node.next = current.next    # X → B
                current.next = node         # A → X
                self._size += 1
                return
            current = current.next
        print(f"  '{target_data}' not found.")

    # ══════════════════════════════════════════════════════════════════════════
    # DELETE OPERATIONS
    # ══════════════════════════════════════════════════════════════════════════

    def delete_first(self):
        """
        OPERATION 4 — Remove FIRST node (head).  O(1)

        Before:  head ──► [A] ──► [B] ──► [C] ──► None
        After:   head ──► [B] ──► [C] ──► None
                 (A is now unreachable → garbage collected)

        Steps:
          1. self.head = self.head.next   (head jumps over A to B)
          That's it. No walking needed. O(1).

        Edge case: if only one node, self.head.next is None → list becomes empty.
        """
        if self.head is None:
            print("  List is empty.")
            return
        removed = self.head.data
        self.head = self.head.next
        self._size -= 1
        print(f"  Removed first: '{removed}'")

    def delete_last(self):
        """
        OPERATION 5 — Remove LAST node (tail).  O(n)

        Before:  head ──► [A] ──► [B] ──► [C] ──► None
        After:   head ──► [A] ──► [B] ──► None
                 (C is now unreachable → garbage collected)

        Steps:
          1. Edge case: if only one node, head = None.
          2. Walk until current.next.next is None  (stop at B, not C)
             Why? We need to cut B's link. Once we're AT C, we can't go back.
          3. current.next = None   (B no longer points to C)

        Stopping condition explained:
          current.next.next is None  means:
          "the node after current has no next" → that node is the tail.
          current is one step BEFORE the tail — exactly where we need to be.
        """
        if self.head is None:
            print("  List is empty.")
            return
        if self.head.next is None:         # only one node
            removed = self.head.data
            self.head = None
            self._size -= 1
            print(f"  Removed last: '{removed}'")
            return
        current = self.head
        while current.next.next is not None:   # stop at second-to-last
            current = current.next
        removed = current.next.data
        current.next = None                    # cut the link to the tail
        self._size -= 1
        print(f"  Removed last: '{removed}'")

    def delete_node(self, data):
        """
        OPERATION 6 — Remove a specific node by value.  O(n)
        Handles head, middle, and tail — all are the same algorithm.

        Goal: remove B from  [A] ──► [B] ──► [C] ──► None

        Before:  [A] ──► [B] ──► [C] ──► None
        After:   [A] ──► [C] ──► None

        Steps:
          1. Special case: if target is head → call delete_first logic.
          2. Walk until current.next.data == target  (stop at A, not B)
          3. current.next = current.next.next        (A skips over B to C)

        Why stop at A and not B?
          Once current IS at B, we can't go backward to update A's pointer.
          We need A's pointer to cut B out — so we must stop BEFORE reaching B.
        """
        if self.head is None:
            print("  List is empty.")
            return
        if self.head.data == data:
            self.head = self.head.next
            self._size -= 1
            print(f"  Removed '{data}' (was head)")
            return
        current = self.head
        while current.next is not None:
            if current.next.data == data:
                print(f"  Removed '{data}'")
                current.next = current.next.next   # skip over target
                self._size -= 1
                return
            current = current.next
        print(f"  '{data}' not found.")

    # ══════════════════════════════════════════════════════════════════════════
    # UTILITY
    # ══════════════════════════════════════════════════════════════════════════

    def find(self, data):
        current = self.head
        while current is not None:
            if current.data == data:
                return current
            current = current.next
        return None

    def display(self, label=""):
        parts = []
        current = self.head
        while current is not None:
            parts.append(str(current.data))
            current = current.next
        chain = " → ".join(parts) + " → None" if parts else "(empty)"
        prefix = f"  {label}: " if label else "  "
        print(prefix + chain)

    def reverse(self):
        """
        Reverse the list IN-PLACE.  O(n) time, O(1) space.

        Before:  [A] ──► [B] ──► [C] ──► None
        After:   [C] ──► [B] ──► [A] ──► None

        Three-pointer technique:
          prev    = None  (what comes "before" current; starts as None = new tail)
          current = head  (the node we're currently flipping)
          next_n  = saved next before we overwrite current.next

        Each iteration:
          1. Save:    next_n  = current.next    (preserve the chain ahead)
          2. Flip:    current.next = prev       (reverse THIS link)
          3. Advance: prev = current            (prev catches up)
          4. Advance: current = next_n          (current moves forward)

        Walkthrough for A → B → C:
          Start:   prev=None, current=A, next_n=?
          Iter 1:  next_n=B,  A.next=None, prev=A, current=B
          Iter 2:  next_n=C,  B.next=A,   prev=B, current=C
          Iter 3:  next_n=None, C.next=B, prev=C, current=None
          End:     self.head = prev = C  → C → B → A → None  ✓
        """
        prev = None
        current = self.head
        while current is not None:
            next_n = current.next
            current.next = prev
            prev = current
            current = next_n
        self.head = prev

    def to_list(self):
        result, current = [], self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    def __len__(self):
        return self._size

    def __repr__(self):
        return f"LinkedList({self.to_list()})"


# ── Demo: all 6 operations clearly labeled ────────────────────────────────────

print("\n\n  ── Class-based LinkedList: All 6 operations ──")

linked = LinkedList()

# Build starting list: A → B → C
linked.insert_at_end("A")
linked.insert_at_end("B")
linked.insert_at_end("C")
linked.display("Starting list")

print()
print("  ── OPERATION 1: Add at BEGINNING ──")
linked.insert_at_front("Z")
linked.display("insert_at_front('Z')")     # Z → A → B → C

print()
print("  ── OPERATION 2: Add at END ──")
linked.insert_at_end("D")
linked.display("insert_at_end('D')")       # Z → A → B → C → D

print()
print("  ── OPERATION 3a: Add IN BETWEEN — after 'B' ──")
linked.insert_after("B", "X")
linked.display("insert_after('B','X')")    # Z → A → B → X → C → D

print()
print("  ── OPERATION 3b: Add IN BETWEEN — before 'X' ──")
linked.insert_before("X", "W")
linked.display("insert_before('X','W')")   # Z → A → B → W → X → C → D

print()
print("  ── OPERATION 4: Remove FIRST ──")
linked.delete_first()
linked.display("delete_first()")           # A → B → W → X → C → D

print()
print("  ── OPERATION 5: Remove LAST ──")
linked.delete_last()
linked.display("delete_last()")            # A → B → W → X → C

print()
print("  ── OPERATION 6: Remove IN BETWEEN (remove 'W') ──")
linked.delete_node("W")
linked.display("delete_node('W')")         # A → B → X → C

print()
print("  ── BONUS: Reverse ──")
linked.reverse()
linked.display("after reverse()")          # C → X → B → A

print(f"\n  Final length: {len(linked)}")
print(f"  As Python list: {linked.to_list()}")


# ─── The key takeaway ─────────────────────────────────────────────────────────
#
#   Dict approach and Class approach ARE THE SAME LOGIC.
#
#   Dict:  node["link"]   →  Class: node.next
#   Dict:  self.LL        →  Class: self.head
#   Dict:  {} (empty)     →  Class: None (empty)
#
#   The class version is used in the rest of this file (Section 1 onwards)
#   because it's cleaner, safer, and lets us add behaviour to nodes.
#   The dict version is useful to UNDERSTAND the concept from scratch —
#   it makes the "node as a container with a pointer" idea very concrete.
#
#   Every linked list operation reduces to one of two things:
#   1. TRAVERSAL: current = current.next  (walk until None)
#   2. REWIRING:  node.next = other_node  (change where a link points)
#   That's it. Everything else is just variations of these two.


# =============================================================================
# SECTION 1: Music Playlist — Doubly Linked List
# =============================================================================
#
# ─── Why Doubly Linked List for a Playlist? ──────────────────────────────────
#
# A music playlist needs:
#   - Play NEXT song  → follow the forward pointer
#   - Play PREVIOUS song → follow the BACKWARD pointer  ← needs doubly linked
#   - Add song at end → update tail's next pointer
#   - Remove song → rewire neighbour pointers (O(1) once found)
#   - Loop / repeat → tail's next can point back to head
#
# A singly linked list (from 19_OOP_usecases.py) can't go BACKWARD.
# That's the key difference here.
#
# ─── Node Structure ──────────────────────────────────────────────────────────
#
#          ┌──────────────────────────────────────────────────┐
#          │  SongNode                                        │
#          │  ┌──────┬──────────────┬──────┐                 │
#          │  │ prev │     data     │ next │                 │
#          │  │  ◄── │  song title │  ──► │                 │
#          │  └──────┴──────────────┴──────┘                 │
#          │  prev → points to the PREVIOUS song             │
#          │  next → points to the NEXT song                 │
#          └──────────────────────────────────────────────────┘
#
# ─── Full Playlist Visual (3 songs) ──────────────────────────────────────────
#
#             head                              tail
#              ↓                                 ↓
#   None ← [Blinding Lights] ⇄ [Bohemian Rhapsody] ⇄ [Lose Yourself] → None
#              ↑
#           current
#           (currently playing)
#
# ─── Operations ──────────────────────────────────────────────────────────────
#
#   add_song(title)       → O(1)  — append to tail, update tail pointer
#   remove_song(title)    → O(n)  — search + O(1) rewire (two pointer rewire)
#   play_next()           → O(1)  — move current to current.next
#   play_prev()           → O(1)  — move current to current.prev
#   display()             → O(n)  — walk from head to tail printing each song
#
# ─── Rewiring on remove (the crucial part) ───────────────────────────────────
#
#   Before removing "Bohemian Rhapsody":
#   [Blinding Lights] ⇄ [Bohemian Rhapsody] ⇄ [Lose Yourself]
#
#   Step 1: Find the node to remove (walk from head)
#   Step 2: node.prev.next = node.next   (Blinding Lights now points forward to Lose Yourself)
#   Step 3: node.next.prev = node.prev   (Lose Yourself now points backward to Blinding Lights)
#
#   After:
#   [Blinding Lights] ⇄ [Lose Yourself]
#   The removed node is now unreachable and gets garbage collected. ✓

print("===== SECTION 1: Music Playlist (Doubly Linked List) =====")


class SongNode:
    """One node in the doubly linked list. Holds a song title + two pointers."""
    def __init__(self, title):
        self.title = title
        self.next = None   # pointer to next song
        self.prev = None   # pointer to previous song


class MusicPlaylist:
    """
    A music playlist backed by a doubly linked list.
    Supports O(1) next/prev navigation.
    """

    def __init__(self, name):
        self.name = name
        self.head = None       # first song in the playlist
        self.tail = None       # last song  (kept so add_song is O(1))
        self.current = None    # the song currently playing
        self._size = 0

    # ── Add / Remove ──────────────────────────────────────────────────────────

    def add_song(self, title):
        """Append a song to the END of the playlist. O(1)."""
        node = SongNode(title)
        if self.tail is None:          # playlist is empty
            self.head = self.tail = node
            self.current = node        # auto-select first song added
        else:
            node.prev = self.tail      # new node points backward to old tail
            self.tail.next = node      # old tail points forward to new node
            self.tail = node           # tail pointer moves to new node
        self._size += 1
        print(f"  Added: '{title}'")

    def remove_song(self, title):
        """Remove a song by title. O(n) to find, O(1) to rewire."""
        node = self._find(title)
        if node is None:
            print(f"  Song '{title}' not found.")
            return

        # If the removed song is playing, move to next (or prev if no next)
        if node is self.current:
            self.current = node.next or node.prev

        # Rewire neighbours
        if node.prev:
            node.prev.next = node.next      # left neighbour skips over node
        else:
            self.head = node.next           # node was the head; update head

        if node.next:
            node.next.prev = node.prev      # right neighbour skips over node
        else:
            self.tail = node.prev           # node was the tail; update tail

        self._size -= 1
        print(f"  Removed: '{title}'")

    # ── Playback ──────────────────────────────────────────────────────────────

    def play_current(self):
        if self.current:
            print(f"  ▶ Now playing: '{self.current.title}'")
        else:
            print("  Playlist is empty.")

    def play_next(self):
        """Advance to the next song. O(1)."""
        if self.current and self.current.next:
            self.current = self.current.next
            self.play_current()
        else:
            print("  Already at the last song.")

    def play_prev(self):
        """Go back to the previous song. O(1)."""
        if self.current and self.current.prev:
            self.current = self.current.prev
            self.play_current()
        else:
            print("  Already at the first song.")

    def play_song(self, title):
        """Jump directly to a song by title. O(n)."""
        node = self._find(title)
        if node:
            self.current = node
            self.play_current()
        else:
            print(f"  Song '{title}' not in playlist.")

    # ── Display / Utility ─────────────────────────────────────────────────────

    def display(self):
        """Print all songs, marking the currently playing one."""
        if self.head is None:
            print("  (empty playlist)")
            return
        print(f"\n  Playlist: {self.name}  [{self._size} songs]")
        node = self.head
        while node:
            marker = " ▶" if node is self.current else "  "
            print(f"  {marker} {node.title}")
            node = node.next
        print()

    def _find(self, title):
        """Walk from head and return the node with this title, or None."""
        node = self.head
        while node:
            if node.title == title:
                return node
            node = node.next
        return None

    def __len__(self):
        return self._size

    def __repr__(self):
        return f"MusicPlaylist(name={self.name!r}, songs={self._size})"


# ── Demo ──────────────────────────────────────────────────────────────────────

playlist = MusicPlaylist("My Favourites")
playlist.add_song("Blinding Lights")
playlist.add_song("Bohemian Rhapsody")
playlist.add_song("Lose Yourself")
playlist.add_song("Levitating")
playlist.add_song("Watermelon Sugar")

playlist.display()
playlist.play_current()       # starts at first song (auto-selected on add)
playlist.play_next()          # → Bohemian Rhapsody
playlist.play_next()          # → Lose Yourself
playlist.play_prev()          # ← Bohemian Rhapsody
playlist.play_song("Levitating")  # jump directly

playlist.remove_song("Levitating")   # remove currently playing song
playlist.play_current()              # should auto-move to Watermelon Sugar
playlist.display()


# =============================================================================
# SECTION 2: Binary Search Tree — Contact Book
# =============================================================================
#
# ─── What is a BST? ──────────────────────────────────────────────────────────
#
# A Binary Search Tree is a tree where:
#   - Each node has at most TWO children (left and right).
#   - LEFT child < current node < RIGHT child (always, at every level).
#   - This ordering is maintained for EVERY node, not just the root.
#
# ─── Why does the ordering matter? ──────────────────────────────────────────
#
# At EACH node, you can instantly eliminate half the remaining tree.
# Searching is like binary search, but on a tree → O(log n) average case.
#
# ─── Visual (inserting names alphabetically) ─────────────────────────────────
#
#   Insert: "Mia", "Alice", "Tom", "David", "Zoe", "Bob"
#
#                     Mia
#                    /   \
#                Alice   Tom
#                   \       \
#                  David    Zoe
#                  /
#                Bob
#
#   Rule check: Alice < Mia ✓  Tom > Mia ✓  David > Alice ✓  Bob < David ✓
#
# ─── Operations ──────────────────────────────────────────────────────────────
#
#   insert(name)     → O(log n) average, O(n) worst (skewed tree)
#   search(name)     → O(log n) average
#   delete(name)     → O(log n) average
#   inorder()        → O(n) — prints ALL contacts in SORTED order
#
# ─── The 3 Traversal Orders ──────────────────────────────────────────────────
#
#   For the tree above (Mia at root):
#
#   In-order   (Left → Root → Right):  Alice Bob David Mia Tom Zoe  ← SORTED
#   Pre-order  (Root → Left → Right):  Mia Alice David Bob Tom Zoe
#   Post-order (Left → Right → Root):  Bob David Alice Zoe Tom Mia
#
#   In-order traversal of a BST ALWAYS gives sorted output. This is used to
#   "print all contacts alphabetically" — no sorting needed!
#
# ─── Delete is the tricky one ────────────────────────────────────────────────
#
#   Three cases when deleting a node:
#
#   Case 1 — No children (leaf):
#     Just remove it. Nothing to rewire.
#     Delete "Bob" → just remove the Bob node. ✓
#
#   Case 2 — One child:
#     Replace the node with its only child.
#     Delete "David" (has only left child Bob) → Alice's right becomes Bob.
#
#   Case 3 — Two children:
#     Find the IN-ORDER SUCCESSOR (smallest node in the right subtree).
#     Replace current node's value with successor's value.
#     Then delete the successor (which has at most 1 child → simpler case).
#     This preserves the BST property.
#
#   Visual — Delete "Alice" (has 1 child: David):
#   Before:                        After:
#        Mia                           Mia
#       /   \                         /   \
#   Alice   Tom          →         David   Tom
#      \       \                   /         \
#      David   Zoe               Bob          Zoe
#      /
#    Bob

print("\n===== SECTION 2: Binary Search Tree — Contact Book =====")


class BSTNode:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
        self.left = None
        self.right = None


class ContactBook:
    """
    Contact book backed by a Binary Search Tree, sorted alphabetically by name.
    Provides O(log n) search and insert (average case).
    """

    def __init__(self):
        self._root = None

    # ── Insert ─────────────────────────────────────────────────────────────────

    def add_contact(self, name, phone):
        """Insert a contact into the BST. Duplicate names are ignored."""
        self._root = self._insert(self._root, name, phone)

    def _insert(self, node, name, phone):
        if node is None:
            print(f"  Added: {name} ({phone})")
            return BSTNode(name, phone)
        if name < node.name:
            node.left = self._insert(node.left, name, phone)
        elif name > node.name:
            node.right = self._insert(node.right, name, phone)
        else:
            print(f"  Contact '{name}' already exists.")
        return node

    # ── Search ─────────────────────────────────────────────────────────────────

    def search(self, name):
        """Find a contact by name. O(log n) average."""
        node = self._search(self._root, name)
        if node:
            print(f"  Found: {node.name} → {node.phone}")
            return node
        print(f"  '{name}' not found in contacts.")
        return None

    def _search(self, node, name):
        if node is None or node.name == name:
            return node
        if name < node.name:
            return self._search(node.left, name)
        return self._search(node.right, name)

    # ── Delete ─────────────────────────────────────────────────────────────────

    def delete_contact(self, name):
        """Remove a contact by name. Handles all 3 deletion cases."""
        existed = self._search(self._root, name) is not None
        self._root = self._delete(self._root, name)
        if existed:
            print(f"  Deleted: '{name}'")

    def _delete(self, node, name):
        if node is None:
            return None
        if name < node.name:
            node.left = self._delete(node.left, name)
        elif name > node.name:
            node.right = self._delete(node.right, name)
        else:                                     # Found the node to delete
            if node.left is None:                # Case 1 & 2: 0 or 1 child
                return node.right
            if node.right is None:
                return node.left
            # Case 3: two children → replace with in-order successor
            successor = self._min_node(node.right)
            node.name = successor.name
            node.phone = successor.phone
            node.right = self._delete(node.right, successor.name)
        return node

    def _min_node(self, node):
        """Find the leftmost (smallest) node in a subtree."""
        while node.left:
            node = node.left
        return node

    # ── Traversals ─────────────────────────────────────────────────────────────

    def show_all(self):
        """Print all contacts in alphabetical order (in-order traversal)."""
        print("\n  All contacts (sorted alphabetically):")
        contacts = []
        self._inorder(self._root, contacts)
        for name, phone in contacts:
            print(f"    {name:<15} {phone}")
        print()

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append((node.name, node.phone))
            self._inorder(node.right, result)


# ── Demo ──────────────────────────────────────────────────────────────────────

contacts = ContactBook()
contacts.add_contact("Mia",   "555-0101")
contacts.add_contact("Alice", "555-0102")
contacts.add_contact("Tom",   "555-0103")
contacts.add_contact("David", "555-0104")
contacts.add_contact("Zoe",   "555-0105")
contacts.add_contact("Bob",   "555-0106")

contacts.show_all()               # prints sorted alphabetically
contacts.search("David")          # O(log n) lookup
contacts.search("Eve")            # not found

contacts.delete_contact("Alice")  # case: 1 child
contacts.show_all()               # Alice is gone; Bob is still there


# =============================================================================
# SECTION 3: Priority Queue — Hospital Emergency Room
# =============================================================================
#
# ─── What is a Priority Queue? ───────────────────────────────────────────────
#
# A queue where elements are served in order of PRIORITY, not arrival time.
# The highest-priority element is always served first regardless of when it arrived.
#
# ─── Real-World Analogy: Hospital Emergency Room ─────────────────────────────
#
# Patients don't get treated in arrival order — they're treated by URGENCY.
# A patient with a heart attack (priority 1 = critical) jumps to the front,
# even if they arrived after a patient with a sprained ankle (priority 5 = minor).
#
# ─── How it's implemented: the MIN-HEAP ──────────────────────────────────────
#
# A min-heap is a binary tree where:
#   - The ROOT always holds the MINIMUM value (highest priority = lowest number)
#   - Every parent is ≤ its children
#   - It's a COMPLETE binary tree (fills level by level, left to right)
#
# ─── Visual: inserting patients ──────────────────────────────────────────────
#
#   After inserting (priority, name) pairs: (3, Bob), (1, Alice), (2, Charlie)
#
#   Heap tree:              Heap stored as array:
#        (1, Alice)             [ (1,Alice), (3,Bob), (2,Charlie) ]
#       /           \             index 0      index 1    index 2
#   (3, Bob)    (2, Charlie)
#
#   Parent of index i → index (i-1)//2
#   Children of index i → 2i+1 (left) and 2i+2 (right)
#
# ─── Heap operations ─────────────────────────────────────────────────────────
#
#   heappush(heap, item)   → insert + bubble UP to restore heap property  O(log n)
#   heappop(heap)          → remove min + bubble DOWN to restore           O(log n)
#   heap[0]                → peek at minimum without removing              O(1)
#
# ─── Python's heapq module ───────────────────────────────────────────────────
#
#   Python only has MIN-heap.
#   For MAX-heap → negate the priority numbers when pushing.
#   For tie-breaking → use tuples: (priority, tie_breaker, value)
#   We add a counter as second element so equal priorities are stable (FIFO).
#
# ─── Walkthrough (n=4 patients) ──────────────────────────────────────────────
#
#   Arrive: Bob(3), Alice(1), Charlie(2), Dave(1)
#
#   push(3, Bob):     heap = [(3, 0, Bob)]
#   push(1, Alice):   heap = [(1, 1, Alice), (3, 0, Bob)]   ← Alice bubbles up
#   push(2, Charlie): heap = [(1, 1, Alice), (3, 0, Bob), (2, 2, Charlie)]
#   push(1, Dave):    heap = [(1, 1, Alice), (1, 3, Dave), (2, 2, Charlie), (3, 0, Bob)]
#
#   pop():  → (1, 1, Alice)   ← lowest priority number = most urgent
#   pop():  → (1, 3, Dave)    ← tie on priority; Alice had lower counter → first
#   pop():  → (2, 2, Charlie)
#   pop():  → (3, 0, Bob)

print("\n===== SECTION 3: Priority Queue — Hospital Emergency Room =====")


class Patient:
    def __init__(self, name, priority, condition):
        self.name = name
        self.priority = priority      # 1=critical, 2=serious, 3=moderate, 4=minor
        self.condition = condition

    def __repr__(self):
        labels = {1: "CRITICAL", 2: "SERIOUS", 3: "MODERATE", 4: "MINOR"}
        return f"Patient({self.name}, {labels.get(self.priority, '?')}, {self.condition})"


class EmergencyRoom:
    """
    Hospital ER triage system using a min-heap priority queue.
    Lower priority number = treated first (1 is most urgent).
    """

    def __init__(self):
        self._heap = []          # stores (priority, counter, Patient)
        self._counter = 0        # tie-breaker: earlier arrivals served first

    def admit_patient(self, name, priority, condition):
        """Admit a new patient into the ER queue."""
        patient = Patient(name, priority, condition)
        heapq.heappush(self._heap, (priority, self._counter, patient))
        self._counter += 1
        labels = {1: "CRITICAL", 2: "SERIOUS", 3: "MODERATE", 4: "MINOR"}
        print(f"  Admitted: {name} [{labels[priority]}] — {condition}")

    def treat_next(self):
        """Call the highest-priority patient. O(log n)."""
        if not self._heap:
            print("  No patients waiting.")
            return None
        priority, _, patient = heapq.heappop(self._heap)
        print(f"  Treating: {patient.name} (priority {priority}) — {patient.condition}")
        return patient

    def peek_next(self):
        """See who will be treated next without calling them."""
        if self._heap:
            _, _, patient = self._heap[0]
            print(f"  Next up: {patient.name} [{patient.condition}]")
        else:
            print("  Queue is empty.")

    def show_queue(self):
        """Display all waiting patients (sorted by priority for display only)."""
        if not self._heap:
            print("  No patients waiting.")
            return
        print(f"\n  Waiting patients ({len(self._heap)} total):")
        labels = {1: "CRITICAL", 2: "SERIOUS", 3: "MODERATE", 4: "MINOR"}
        for p, _, patient in sorted(self._heap):
            print(f"    [{labels[p]}] {patient.name} — {patient.condition}")
        print()

    def __len__(self):
        return len(self._heap)


# ── Demo ──────────────────────────────────────────────────────────────────────

er = EmergencyRoom()
er.admit_patient("Bob",     priority=3, condition="Sprained ankle")
er.admit_patient("Alice",   priority=1, condition="Cardiac arrest")
er.admit_patient("Charlie", priority=2, condition="Broken arm")
er.admit_patient("Dave",    priority=4, condition="Paper cut")
er.admit_patient("Eve",     priority=1, condition="Severe allergic reaction")

er.show_queue()
er.peek_next()

print()
er.treat_next()   # Alice (cardiac arrest, arrived before Eve, same priority)
er.treat_next()   # Eve   (also priority 1, but admitted later → counter wins)
er.treat_next()   # Charlie (priority 2)
er.treat_next()   # Bob


# =============================================================================
# SECTION 4: Graph — Social Network
# =============================================================================
#
# ─── What is a Graph? ────────────────────────────────────────────────────────
#
# A graph is a collection of NODES (also called vertices) connected by EDGES.
# Unlike trees, graphs can have cycles, multiple paths between nodes, and
# edges that go in ONE direction (directed) or BOTH directions (undirected).
#
# ─── Real-World Analogy: Social Network ─────────────────────────────────────
#
# People = nodes.  Friendships = edges (undirected: if A friends B, B friends A).
# "How many degrees of separation between me and Elon Musk?" → shortest path.
# "Who are all the people connected to Alice, directly or indirectly?" → BFS/DFS.
#
# ─── Representation: Adjacency List ──────────────────────────────────────────
#
# We store a dictionary where each key is a node and the value is a list of
# its NEIGHBOURS (nodes it's directly connected to).
#
# Example social network:
#   Alice is friends with Bob and Charlie
#   Bob is friends with Alice and Dave
#   Charlie is friends with Alice and Eve
#   Dave is friends with Bob
#   Eve is friends with Charlie
#
#   Adjacency list:
#   {
#     "Alice":   ["Bob", "Charlie"],
#     "Bob":     ["Alice", "Dave"],
#     "Charlie": ["Alice", "Eve"],
#     "Dave":    ["Bob"],
#     "Eve":     ["Charlie"]
#   }
#
#   Visual:
#   Alice ─── Bob ─── Dave
#     │
#   Charlie ─── Eve
#
# ─── Two Ways to Traverse a Graph ────────────────────────────────────────────
#
#   BFS (Breadth-First Search) — uses a QUEUE:
#     Visit all DIRECT friends first, then friends-of-friends, then further.
#     "Explore level by level."
#     Perfect for finding SHORTEST PATH (fewest hops between two people).
#
#     Queue state while finding friends of Alice:
#     Start:  queue = [Alice]                 visited = {Alice}
#     Step 1: dequeue Alice, enqueue Bob, Charlie
#             queue = [Bob, Charlie]           visited = {Alice, Bob, Charlie}
#     Step 2: dequeue Bob, enqueue Dave
#             queue = [Charlie, Dave]          visited = {Alice, Bob, Charlie, Dave}
#     Step 3: dequeue Charlie, enqueue Eve
#             queue = [Dave, Eve]              visited = {Alice, Bob, Charlie, Dave, Eve}
#     Step 4: dequeue Dave → no new friends
#     Step 5: dequeue Eve → no new friends
#     Result: Alice → Bob → Charlie → Dave → Eve  (in BFS order)
#
#   DFS (Depth-First Search) — uses a STACK (or recursion):
#     Go as DEEP as possible along one path before backtracking.
#     "Dive all the way down one branch, then come back."
#     Used for: detecting cycles, topological sort, maze solving.
#
#     DFS from Alice (recursive):
#     Visit Alice → go to Bob → go to Dave → backtrack to Bob → backtrack to Alice
#              → go to Charlie → go to Eve
#     Result: Alice → Bob → Dave → Charlie → Eve

print("\n===== SECTION 4: Graph — Social Network =====")


class SocialNetwork:
    """
    Undirected graph representing a social network.
    Uses adjacency list (dict of sets) for O(1) add/check.
    """

    def __init__(self):
        self._graph = defaultdict(set)   # {person: {friend1, friend2, ...}}

    # ── Build the network ─────────────────────────────────────────────────────

    def add_person(self, name):
        if name not in self._graph:
            self._graph[name]  # creates empty set via defaultdict
            print(f"  Added person: {name}")

    def add_friendship(self, a, b):
        """Add an undirected edge between a and b."""
        self._graph[a].add(b)
        self._graph[b].add(a)
        print(f"  Friends: {a} ↔ {b}")

    def remove_friendship(self, a, b):
        self._graph[a].discard(b)
        self._graph[b].discard(a)
        print(f"  Unfriended: {a} ↔ {b}")

    # ── Query ─────────────────────────────────────────────────────────────────

    def friends_of(self, person):
        """Return direct friends (O(1))."""
        return sorted(self._graph.get(person, set()))

    def bfs(self, start):
        """
        Breadth-First Search from start.
        Returns people in BFS order (nearest first).
        """
        if start not in self._graph:
            return []
        visited = {start}
        queue = deque([start])
        order = []
        while queue:
            person = queue.popleft()
            order.append(person)
            for friend in sorted(self._graph[person]):  # sorted for determinism
                if friend not in visited:
                    visited.add(friend)
                    queue.append(friend)
        return order

    def dfs(self, start):
        """
        Depth-First Search from start (iterative, using a stack).
        Returns people in DFS order (deepest path first).
        """
        if start not in self._graph:
            return []
        visited = set()
        stack = [start]
        order = []
        while stack:
            person = stack.pop()
            if person not in visited:
                visited.add(person)
                order.append(person)
                for friend in sorted(self._graph[person], reverse=True):
                    if friend not in visited:
                        stack.append(friend)
        return order

    def shortest_path(self, start, end):
        """
        Find the shortest path (fewest hops) between two people using BFS.
        Returns the path as a list, or None if no path exists.
        """
        if start == end:
            return [start]
        visited = {start}
        queue = deque([[start]])        # queue of PATHS (not just nodes)
        while queue:
            path = queue.popleft()
            person = path[-1]
            for friend in self._graph[person]:
                if friend == end:
                    return path + [friend]    # found! return the full path
                if friend not in visited:
                    visited.add(friend)
                    queue.append(path + [friend])
        return None                           # no path exists

    def degrees_of_separation(self, a, b):
        """How many hops between a and b?"""
        path = self.shortest_path(a, b)
        if path is None:
            print(f"  {a} and {b} are not connected.")
            return -1
        hops = len(path) - 1
        print(f"  {a} → {b}: {hops} degree(s) of separation  [{' → '.join(path)}]")
        return hops

    def mutual_friends(self, a, b):
        """Friends that both a and b share."""
        return sorted(self._graph[a] & self._graph[b])

    def show_network(self):
        print("\n  Network connections:")
        for person in sorted(self._graph):
            friends = sorted(self._graph[person])
            print(f"    {person:<12} → {', '.join(friends) if friends else '(none)'}")
        print()


# ── Demo ──────────────────────────────────────────────────────────────────────

net = SocialNetwork()
net.add_friendship("Alice",   "Bob")
net.add_friendship("Alice",   "Charlie")
net.add_friendship("Bob",     "Dave")
net.add_friendship("Charlie", "Eve")
net.add_friendship("Dave",    "Frank")
net.add_friendship("Eve",     "Frank")

net.show_network()

print("  BFS from Alice:", net.bfs("Alice"))
print("  DFS from Alice:", net.dfs("Alice"))
print()

net.degrees_of_separation("Alice", "Frank")   # Alice→Bob→Dave→Frank = 3
net.degrees_of_separation("Alice", "Eve")     # Alice→Charlie→Eve = 2

print("  Mutual friends of Bob and Charlie:",
      net.mutual_friends("Bob", "Charlie"))    # both know Alice


# =============================================================================
# SECTION 5: Shopping Cart — OOP Composition + Inheritance
# =============================================================================
#
# ─── Key OOP Concepts Demonstrated ───────────────────────────────────────────
#
# COMPOSITION:
#   A ShoppingCart HAS products. A product is its own class.
#   "HAS-A" relationship — Cart contains Product objects.
#
# INHERITANCE:
#   DigitalProduct and PhysicalProduct both extend Product.
#   They share common attributes (name, price) but differ in specifics
#   (digital has a download_link; physical has weight and shipping cost).
#
# POLYMORPHISM:
#   Both types have a get_total_cost() method but calculate it differently.
#   Cart calls get_total_cost() on each item without caring which type it is.
#
# ─── Class Hierarchy ─────────────────────────────────────────────────────────
#
#                    Product (base class)
#                   /                   \
#         DigitalProduct           PhysicalProduct
#         - download_link          - weight_kg
#         - no shipping            - shipping_cost()
#
#   ShoppingCart HAS-A list of Products (composition)
#   Discount HAS-A type and value (composition inside Cart)
#
# ─── Visual: Cart with mixed product types ───────────────────────────────────
#
#   Cart:
#   ┌─────────────────────────────────────────────────────────┐
#   │  [1] Python Course (Digital)   $49.99  → no shipping   │
#   │  [2] Laptop Stand (Physical)   $35.00  → +$5.99 ship   │
#   │  [3] DSA eBook (Digital)       $19.99  → no shipping   │
#   │  ─────────────────────────────────────────────────────  │
#   │  Subtotal:  $104.98                                     │
#   │  Shipping:  $5.99                                       │
#   │  Discount:  -$10.00 (coupon)                           │
#   │  TOTAL:     $100.97                                     │
#   └─────────────────────────────────────────────────────────┘

print("\n===== SECTION 5: Shopping Cart — OOP Composition & Inheritance =====")


class Product:
    """Base class for all product types."""

    def __init__(self, name, price):
        self.name = name
        self._price = price        # private via convention

    @property
    def price(self):
        return self._price

    def get_total_cost(self):
        """Override in subclasses to include type-specific costs."""
        return self._price

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, price=${self._price:.2f})"


class DigitalProduct(Product):
    """A product delivered electronically — no shipping cost."""

    def __init__(self, name, price, download_link):
        super().__init__(name, price)
        self.download_link = download_link

    def get_total_cost(self):
        return self._price          # no shipping for digital


class PhysicalProduct(Product):
    """A product that must be shipped — adds shipping cost based on weight."""

    SHIPPING_RATE_PER_KG = 3.00   # $3 per kg

    def __init__(self, name, price, weight_kg):
        super().__init__(name, price)
        self.weight_kg = weight_kg

    def shipping_cost(self):
        return round(self.weight_kg * self.SHIPPING_RATE_PER_KG, 2)

    def get_total_cost(self):
        return self._price + self.shipping_cost()   # item + shipping


class Discount:
    """Represents a discount — either a flat amount or a percentage."""

    def __init__(self, code, discount_type, value):
        self.code = code
        self.discount_type = discount_type   # "flat" or "percent"
        self.value = value

    def apply(self, subtotal):
        if self.discount_type == "flat":
            return min(self.value, subtotal)       # can't discount below $0
        elif self.discount_type == "percent":
            return round(subtotal * self.value / 100, 2)
        return 0


class ShoppingCart:
    """
    A shopping cart that holds Product objects (digital and physical).
    Demonstrates composition: Cart HAS products, not IS a product.
    """

    def __init__(self, owner):
        self.owner = owner
        self._items = []           # list of Product objects
        self._discount = None

    def add_item(self, product):
        self._items.append(product)
        print(f"  Added: {product.name} (${product.price:.2f})")

    def remove_item(self, name):
        before = len(self._items)
        self._items = [p for p in self._items if p.name != name]
        if len(self._items) < before:
            print(f"  Removed: {name}")

    def apply_discount(self, discount):
        self._discount = discount
        print(f"  Discount applied: code '{discount.code}'")

    def subtotal(self):
        return round(sum(p.price for p in self._items), 2)

    def total_shipping(self):
        return round(sum(
            p.shipping_cost() for p in self._items
            if isinstance(p, PhysicalProduct)
        ), 2)

    def total(self):
        sub = self.subtotal()
        shipping = self.total_shipping()
        discount_amount = self._discount.apply(sub) if self._discount else 0
        return round(sub + shipping - discount_amount, 2)

    def checkout(self):
        if not self._items:
            print("  Cart is empty.")
            return
        print(f"\n  ━━ Cart for {self.owner} ━━")
        for i, p in enumerate(self._items, 1):
            if isinstance(p, PhysicalProduct):
                print(f"  [{i}] {p.name:<25} ${p.price:.2f}  +${p.shipping_cost():.2f} shipping")
            else:
                print(f"  [{i}] {p.name:<25} ${p.price:.2f}  (digital, no shipping)")
        print(f"  {'─'*50}")
        sub = self.subtotal()
        ship = self.total_shipping()
        disc = self._discount.apply(sub) if self._discount else 0
        print(f"  Subtotal:  ${sub:.2f}")
        print(f"  Shipping:  ${ship:.2f}")
        if disc > 0:
            print(f"  Discount:  -${disc:.2f}  [{self._discount.code}]")
        print(f"  TOTAL:     ${self.total():.2f}")
        print()

    def __len__(self):
        return len(self._items)


# ── Demo ──────────────────────────────────────────────────────────────────────

cart = ShoppingCart("Rajesh")
cart.add_item(DigitalProduct("Python Masterclass",   49.99, "https://course.example.com"))
cart.add_item(PhysicalProduct("Laptop Stand",        35.00, weight_kg=1.2))
cart.add_item(DigitalProduct("DSA eBook",            19.99, "https://ebook.example.com"))
cart.add_item(PhysicalProduct("Mechanical Keyboard", 89.00, weight_kg=1.5))

cart.apply_discount(Discount("SAVE10", "flat", 10))
cart.checkout()


# =============================================================================
# SECTION 6: Parking Lot System — OOP Design Interview
# =============================================================================
#
# ─── Why this is a classic interview problem ─────────────────────────────────
#
# Parking lot is a favourite OOP design question because it tests whether you
# can identify classes, their relationships, and their responsibilities.
# There's no single "correct" answer — but a good answer shows clear thinking.
#
# ─── Step 1: Identify entities (classes) ─────────────────────────────────────
#
#   Vehicle      — the thing parking (has a license plate and type)
#   ParkingSpot  — one physical space (has a size and occupancy state)
#   ParkingLevel — one floor of the garage (has a collection of spots)
#   ParkingLot   — the whole garage (has levels, entrance/exit logic)
#   Ticket       — given at entry, used to calculate fee at exit
#
# ─── Step 2: Identify relationships ─────────────────────────────────────────
#
#   ParkingLot HAS-A list of ParkingLevel  (composition)
#   ParkingLevel HAS-A list of ParkingSpot (composition)
#   Ticket HAS-A Vehicle and an entry time (composition)
#   Vehicle can be Car, Motorcycle, Truck → Inheritance
#
# ─── Step 3: Define behaviour ─────────────────────────────────────────────────
#
#   park(vehicle)    → find a suitable spot, issue ticket
#   exit(ticket)     → free the spot, calculate fee
#   find_spot(size)  → scan levels for an available spot of the right size
#
# ─── Visual: 2-level lot ─────────────────────────────────────────────────────
#
#   ParkingLot
#   ├── Level 1   [M M M S S S S L L]   ← spots by size: M=Moto, S=Small, L=Large
#   └── Level 2   [S S S S L L L]
#
#   A Motorcycle fits in: Motorcycle, Small, or Large spots (smallest fits anywhere)
#   A Car fits in:        Small or Large spots
#   A Truck fits in:      Large spots only
#
# ─── Ticket lifecycle ────────────────────────────────────────────────────────
#
#   Enter → ParkingLot assigns spot → issues Ticket with timestamp
#   Exit  → Ticket scanned → time delta calculated → fee charged → spot freed
#
#   Fee formula: $2.00 per hour (rounded up)

import time

print("\n===== SECTION 6: Parking Lot System — OOP Design =====")

SPOT_MOTO  = "Motorcycle"
SPOT_SMALL = "Small"
SPOT_LARGE = "Large"


class Vehicle:
    def __init__(self, plate, vehicle_type):
        self.plate = plate
        self.vehicle_type = vehicle_type   # "Motorcycle", "Car", "Truck"

    def spot_sizes_allowed(self):
        """Return the spot sizes this vehicle can park in (smallest to largest)."""
        if self.vehicle_type == "Motorcycle":
            return [SPOT_MOTO, SPOT_SMALL, SPOT_LARGE]
        elif self.vehicle_type == "Car":
            return [SPOT_SMALL, SPOT_LARGE]
        else:                               # Truck
            return [SPOT_LARGE]

    def __repr__(self):
        return f"{self.vehicle_type}({self.plate})"


class ParkingSpot:
    def __init__(self, spot_id, size):
        self.spot_id = spot_id
        self.size = size
        self.vehicle = None        # None = available

    @property
    def is_available(self):
        return self.vehicle is None

    def park(self, vehicle):
        self.vehicle = vehicle

    def vacate(self):
        self.vehicle = None

    def __repr__(self):
        status = "free" if self.is_available else f"occupied by {self.vehicle.plate}"
        return f"Spot({self.spot_id}, {self.size}, {status})"


class ParkingTicket:
    _next_id = 1

    def __init__(self, vehicle, spot):
        self.ticket_id = f"TKT-{ParkingTicket._next_id:04d}"
        ParkingTicket._next_id += 1
        self.vehicle = vehicle
        self.spot = spot
        self.entry_time = time.time()

    def fee(self, rate_per_hour=2.0):
        hours = (time.time() - self.entry_time) / 3600
        return round(math.ceil(hours) * rate_per_hour, 2) if hours > 0 else rate_per_hour * 0.5

    def __repr__(self):
        return f"Ticket({self.ticket_id}, {self.vehicle}, Spot {self.spot.spot_id})"


class ParkingLevel:
    def __init__(self, level_num, spot_config):
        """
        spot_config: list of sizes e.g. ['Motorcycle','Small','Large','Large']
        """
        self.level_num = level_num
        self.spots = [
            ParkingSpot(f"L{level_num}-{i+1}", size)
            for i, size in enumerate(spot_config)
        ]

    def find_spot(self, size):
        """Return the first available spot of the given size, or None."""
        for spot in self.spots:
            if spot.is_available and spot.size == size:
                return spot
        return None

    def available_count(self):
        return sum(1 for s in self.spots if s.is_available)

    def show(self):
        print(f"  Level {self.level_num}: ", end="")
        for s in self.spots:
            symbol = "." if s.is_available else "X"
            print(f"[{symbol}{s.size[0]}]", end=" ")
        print(f"  ({self.available_count()} free)")


class ParkingLot:
    """The top-level controller. Manages multiple levels and issues tickets."""

    HOURLY_RATE = 2.00

    def __init__(self, name):
        self.name = name
        self.levels = []
        self._active_tickets = {}    # plate → ticket

    def add_level(self, spot_config):
        level = ParkingLevel(len(self.levels) + 1, spot_config)
        self.levels.append(level)

    def park_vehicle(self, vehicle):
        """Find best spot for vehicle, park it, return ticket."""
        if vehicle.plate in self._active_tickets:
            print(f"  {vehicle.plate} is already parked.")
            return None

        for size in vehicle.spot_sizes_allowed():
            for level in self.levels:
                spot = level.find_spot(size)
                if spot:
                    spot.park(vehicle)
                    ticket = ParkingTicket(vehicle, spot)
                    self._active_tickets[vehicle.plate] = ticket
                    print(f"  Parked {vehicle} at spot {spot.spot_id}  [{ticket.ticket_id}]")
                    return ticket

        print(f"  No available spot for {vehicle}. Lot may be full.")
        return None

    def exit_vehicle(self, ticket):
        """Release spot and calculate fee."""
        if ticket is None:
            return
        fee = ticket.fee(self.HOURLY_RATE)
        ticket.spot.vacate()
        del self._active_tickets[ticket.vehicle.plate]
        print(f"  Exited: {ticket.vehicle}  spot {ticket.spot.spot_id}  "
              f"Fee: ${fee:.2f}  [{ticket.ticket_id}]")
        return fee

    def status(self):
        print(f"\n  === {self.name} Status ===")
        for level in self.levels:
            level.show()
        total = sum(l.available_count() for l in self.levels)
        total_spots = sum(len(l.spots) for l in self.levels)
        print(f"  Available: {total}/{total_spots} spots\n")


# ── Demo ──────────────────────────────────────────────────────────────────────

lot = ParkingLot("City Centre Garage")
lot.add_level([SPOT_MOTO, SPOT_MOTO, SPOT_SMALL, SPOT_SMALL, SPOT_SMALL, SPOT_LARGE, SPOT_LARGE])
lot.add_level([SPOT_SMALL, SPOT_SMALL, SPOT_LARGE, SPOT_LARGE])

lot.status()

car1  = Vehicle("ABC-123", "Car")
moto1 = Vehicle("MTO-001", "Motorcycle")
truck = Vehicle("TRK-999", "Truck")
car2  = Vehicle("XYZ-456", "Car")

t1 = lot.park_vehicle(car1)
t2 = lot.park_vehicle(moto1)
t3 = lot.park_vehicle(truck)
t4 = lot.park_vehicle(car2)

lot.status()

lot.exit_vehicle(t1)          # car1 leaves
lot.exit_vehicle(t3)          # truck leaves
lot.status()


# =============================================================================
# SECTION 7: Observer Pattern — Stock Price Alerts
# =============================================================================
#
# ─── What is the Observer Pattern? ───────────────────────────────────────────
#
# The Observer Pattern (also called Publish-Subscribe or Pub-Sub) is a design
# pattern where one object (the SUBJECT / PUBLISHER) maintains a list of
# dependents (OBSERVERS / SUBSCRIBERS) and automatically NOTIFIES them when
# its state changes.
#
# ─── Real-World Analogy: Stock Price Tracker ─────────────────────────────────
#
# You "subscribe" to receive alerts when AAPL stock crosses $200.
# You are the OBSERVER. The stock market is the SUBJECT.
# When AAPL price updates, ALL subscribers are notified automatically.
# You don't need to keep checking — the market PUSHES the update to you.
#
# ─── Why use this pattern? ───────────────────────────────────────────────────
#
# Without Observer:
#   Each interested party must constantly POLL the subject ("has it changed?")
#   → wastes CPU, tight coupling, hard to add new listeners.
#
# With Observer:
#   Subject stores a list of listeners. When state changes, loop through and call
#   notify() on each one. Adding a new subscriber = just append to the list.
#   → loose coupling, easy to extend, efficient.
#
# ─── Pattern Structure ───────────────────────────────────────────────────────
#
#                  ┌─────────────────┐
#                  │   StockMarket   │  ← SUBJECT
#                  │  (publisher)    │
#                  │  _subscribers[] │
#                  └───────┬─────────┘
#                          │ notifies all on price change
#                   ┌──────┼──────────────┐
#                   ▼      ▼              ▼
#            PriceAlert  EmailAlert  DashboardAlert  ← OBSERVERS
#            (subscriber)(subscriber) (subscriber)
#
# ─── Walkthrough ─────────────────────────────────────────────────────────────
#
#   market = StockMarket("AAPL", initial_price=195.00)
#   market.subscribe(PriceAlert("Rajesh", threshold=200, above=True))
#   market.subscribe(EmailAlert("rajesh@email.com"))
#
#   market.update_price(199.00)  → PriceAlert: no alert (199 < 200); Email: sends
#   market.update_price(201.00)  → PriceAlert: ALERT! (201 > 200); Email: sends
#   market.update_price(198.00)  → PriceAlert: ALERT! (below 200 again); Email: sends

print("\n===== SECTION 7: Observer Pattern — Stock Price Alerts =====")


# ── Observer interface (base class) ──────────────────────────────────────────

class StockObserver:
    """Base class for all observers. Subclasses must implement update()."""
    def update(self, ticker, old_price, new_price):  # noqa: unused-params — subclasses use them
        raise NotImplementedError


# ── Concrete observers ────────────────────────────────────────────────────────

class PriceAlertObserver(StockObserver):
    """Notifies when the price crosses a threshold in a given direction."""

    def __init__(self, owner, threshold, direction="above"):
        self.owner = owner
        self.threshold = threshold
        self.direction = direction     # "above" or "below"
        self._triggered = False        # avoid repeated alerts for the same crossing

    def update(self, ticker, old_price, new_price):
        if self.direction == "above":
            crossed = old_price <= self.threshold < new_price
            uncrossed = new_price < self.threshold
        else:
            crossed = old_price >= self.threshold > new_price
            uncrossed = new_price > self.threshold

        if crossed:
            dir_str = "above" if self.direction == "above" else "below"
            print(f"  🔔 ALERT [{self.owner}]: {ticker} crossed {dir_str} "
                  f"${self.threshold:.2f}  (now ${new_price:.2f})")
            self._triggered = True
        elif uncrossed and self._triggered:
            print(f"  ℹ️  INFO  [{self.owner}]: {ticker} back {'below' if self.direction == 'above' else 'above'} "
                  f"${self.threshold:.2f}  (now ${new_price:.2f})")
            self._triggered = False


class EmailObserver(StockObserver):
    """Simulates sending an email on every price update."""

    def __init__(self, email):
        self.email = email

    def update(self, ticker, old_price, new_price):
        change = new_price - old_price
        direction = "▲" if change >= 0 else "▼"
        print(f"  📧 EMAIL → {self.email}: {ticker} is now ${new_price:.2f}  "
              f"{direction} ${abs(change):.2f}")


class LogObserver(StockObserver):
    """Records every price update to an in-memory log."""

    def __init__(self):
        self.log = []

    def update(self, ticker, old_price, new_price):
        entry = f"{ticker}: ${old_price:.2f} → ${new_price:.2f}"
        self.log.append(entry)

    def print_log(self):
        print(f"\n  Price history log ({len(self.log)} entries):")
        for entry in self.log:
            print(f"    {entry}")


# ── Subject ───────────────────────────────────────────────────────────────────

class StockMarket:
    """
    The subject (publisher). Maintains a list of observers and notifies
    them all whenever the stock price changes.
    """

    def __init__(self, ticker, initial_price):
        self.ticker = ticker
        self._price = initial_price
        self._observers = []
        print(f"  Stock created: {ticker} at ${initial_price:.2f}")

    def subscribe(self, observer):
        """Add a new observer to the notification list."""
        self._observers.append(observer)
        name = observer.__class__.__name__
        print(f"  Subscribed: {name}")

    def unsubscribe(self, observer):
        """Remove an observer (they stop receiving updates)."""
        self._observers.remove(observer)

    def update_price(self, new_price):
        """Change the price and notify ALL observers automatically."""
        old_price = self._price
        self._price = new_price
        print(f"\n  [{self.ticker}] Price update: ${old_price:.2f} → ${new_price:.2f}")
        for observer in self._observers:
            observer.update(self.ticker, old_price, new_price)

    @property
    def price(self):
        return self._price


# ── Demo ──────────────────────────────────────────────────────────────────────

aapl = StockMarket("AAPL", initial_price=195.00)
print()

logger    = LogObserver()
alert_up  = PriceAlertObserver("Rajesh",  threshold=200.00, direction="above")
alert_dn  = PriceAlertObserver("Rajesh",  threshold=190.00, direction="below")
emailer   = EmailObserver("rajesh@example.com")

aapl.subscribe(alert_up)
aapl.subscribe(alert_dn)
aapl.subscribe(emailer)
aapl.subscribe(logger)

print()
aapl.update_price(199.00)   # no threshold crossed for alert_up; email fires
aapl.update_price(202.50)   # crosses $200 → alert_up fires; email fires
aapl.update_price(198.00)   # drops back below $200 → reset message; email fires
aapl.update_price(188.00)   # crosses $190 from above → alert_dn fires

# Unsubscribe email, then update
aapl.unsubscribe(emailer)
print()
print("  (unsubscribed email observer)")
aapl.update_price(205.00)   # email no longer fires; only alert and logger

logger.print_log()


# =============================================================================
# SECTION 8: Interview Q&A — Design Questions
# =============================================================================

print("\n===== SECTION 8: Interview Q&A =====")

qa = """
Q1: What is the difference between composition and inheritance?
    Inheritance   = IS-A relationship.
                    Dog IS-A Animal → class Dog(Animal)
                    Dog can use and override Animal's methods.
                    Risk: deep hierarchies become brittle ("fragile base class" problem).

    Composition   = HAS-A relationship.
                    Car HAS-A Engine → class Car: def __init__(self): self.engine = Engine()
                    Car delegates engine-specific work to the Engine object.
                    Prefer composition over inheritance when the relationship is "uses" not "is".

    Rule of thumb: "favour composition over inheritance" — it's easier to change
    a component (swap one Engine for another) than to restructure a class hierarchy.

──────────────────────────────────────────────────────────────────────────────

Q2: What is encapsulation and why does it matter?
    Encapsulation = bundling data (attributes) and behaviour (methods) into a
    class, and RESTRICTING direct access to the internals.

    In Python: prefix with _ (convention: "private, don't touch") or __ (name mangling).

    Why it matters:
    - Protects invariants: Cart._items can't be sorted or sliced from outside.
    - Enables refactoring: you can change the internal list to a dict without
      breaking any code that uses the Cart — as long as the PUBLIC API stays the same.
    - Reduces bugs: impossible to accidentally push to the middle of a Stack.

──────────────────────────────────────────────────────────────────────────────

Q3: When would you use a BST over a hash map (Python dict)?
    Hash map:  O(1) average for insert/search/delete. No ordering.
    BST:       O(log n) for insert/search/delete. Maintains SORTED ORDER.

    Use BST when you need:
    - "Get all contacts between 'A' and 'M'" (range query)
    - "Print all contacts alphabetically" (in-order traversal)
    - "Find the largest/smallest key" (O(log n), not O(n) scan)

    Use hash map when you need:
    - Fast exact-key lookups with no need for ordering.

──────────────────────────────────────────────────────────────────────────────

Q4: What is the Observer Pattern and when would you use it?
    Observer = a pattern where a SUBJECT automatically notifies a list of
    OBSERVERS when its state changes.

    Use it when:
    - Multiple parts of an app care about the same state change (price, login, etc.)
    - You want to decouple the PRODUCER of events from the CONSUMERS.
    - You need to dynamically add/remove listeners at runtime.

    Real examples: Django signals, React state → component re-render, stock alerts,
    notification systems, event-driven architectures.

──────────────────────────────────────────────────────────────────────────────

Q5: Design a simple notification system for a social media app.
    Entities:
        User         — has a name, follows other users
        Post         — belongs to a User, has content
        Notification — generated when someone you follow posts

    Pattern: User IS-A Subject. Followers ARE-A Observer.
    When User.post(content) is called:
        → notify all followers with "X posted: content"

    This is exactly the Observer Pattern (Section 7), applied to social media.
    Follow = subscribe.   Unfollow = unsubscribe.   Post = update_price().

──────────────────────────────────────────────────────────────────────────────

Q6: What is a min-heap and how is it different from a sorted list?
    Both keep elements orderable.

    Sorted list:
        Insertion: O(n)     — must find the right position
        Access min: O(1)    — it's always at index 0
        Pop min: O(n)       — must shift all elements left

    Min-heap:
        Insertion: O(log n) — bubble up to restore heap property
        Access min: O(1)    — root is always minimum
        Pop min: O(log n)   — sift down after removing root

    Use heap when you need repeated insert + pop-min (Priority Queue use case).
    Use sorted list when you mostly read and rarely insert.

──────────────────────────────────────────────────────────────────────────────

Q7: What is the difference between BFS and DFS? When to use each?
    BFS (Breadth-First Search):
        Uses QUEUE. Explores level by level (all neighbours first).
        Guarantees SHORTEST PATH in unweighted graphs.
        Use for: friend suggestions, navigation, shortest path.

    DFS (Depth-First Search):
        Uses STACK (or recursion). Dives deep before backtracking.
        Does NOT guarantee shortest path.
        Use for: cycle detection, topological sort, maze solving, connected components.

    Memory:
        BFS holds the entire "frontier" (all nodes at current depth) in the queue.
            → More memory for wide, shallow graphs.
        DFS holds only the current path in the stack.
            → More memory-efficient for deep, narrow graphs.

──────────────────────────────────────────────────────────────────────────────

Q8: "Design a music streaming service" — how would you start?
    Step 1: Identify core entities.
        Song, Album, Artist, User, Playlist, PlaybackQueue

    Step 2: Identify key data structures.
        Playlist → Doubly Linked List (next/prev song in O(1))
        PlaybackQueue → Queue (songs queued up to play after current)
        Search index → BST or hash map (find songs by name)
        Recommendations → Graph (users who liked X also liked Y)

    Step 3: Identify relationships.
        Playlist HAS-A list of Songs (composition)
        Artist HAS-A list of Albums (composition)
        User HAS-A list of Playlists (composition)
        Playlist IS-A... no, Playlist is not a Song.

    Step 4: Define key operations and their complexity.
        Add to playlist: O(1) — append to doubly linked list
        Skip to next:    O(1) — follow next pointer
        Search song:     O(log n) — BST lookup or O(1) hash map
        Get recommendations: O(V+E) — graph traversal

    This is how you approach OOP design in an interview:
    Entities → Structures → Relationships → Operations → Complexity.
"""

print(qa)
