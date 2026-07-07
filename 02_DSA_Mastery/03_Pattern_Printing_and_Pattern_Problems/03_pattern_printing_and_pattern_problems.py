###############################################################################
#                 03 - Pattern Printing and Pattern Problems                  #
###############################################################################

# =============================================================================
# SECTION 1: Standard Grids & Triangles
# =============================================================================

def print_square(n: int):
    """
    ***
    ***
    ***
    """
    for i in range(n):
        for j in range(n):
            print("*", end="")
        print()

def print_increasing_triangle(n: int):
    """
    *
    **
    ***
    """
    for i in range(n):
        for j in range(i + 1):
            print("*", end="")
        print()

def print_decreasing_triangle(n: int):
    """
    ***
    **
    *
    """
    for i in range(n):
        for j in range(n - i):
            print("*", end="")
        print()


# =============================================================================
# SECTION 2: Pyramids and Spaces
# =============================================================================

def print_right_aligned_triangle(n: int):
    """
      *
     **
    ***
    """
    for i in range(n):
        # 1. Print spaces
        for s in range(n - i - 1):
            print(" ", end="")
        # 2. Print stars
        for j in range(i + 1):
            print("*", end="")
        # 3. Newline
        print()

def print_pyramid(n: int):
    """
      *
     ***
    *****
    """
    for i in range(n):
        # Spaces: n - i - 1
        for s in range(n - i - 1):
            print(" ", end="")
            
        # Stars: 2*i + 1
        for j in range(2 * i + 1):
            print("*", end="")
            
        print()


# =============================================================================
# SECTION 3: Number Patterns
# =============================================================================

def print_number_triangle(n: int):
    """
    1
    12
    123
    """
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            print(j, end="")
        print()

def print_floyds_triangle(n: int):
    """
    1
    2 3
    4 5 6
    """
    count = 1
    for i in range(n):
        for j in range(i + 1):
            print(count, end=" ")
            count += 1
        print()


# --- Practice Skeletons ---

def practice_diamond_pattern(n: int):
    """
    Print a full diamond (Top pyramid + inverted bottom pyramid).
    """
    pass

def practice_hollow_square(n: int):
    """
    Print a square of size n x n, but only the border is '*' and inside is ' '.
    """
    pass


# =============================================================================
# DRIVER CODE
# =============================================================================
if __name__ == "__main__":
    print("--- Increasing Triangle ---")
    print_increasing_triangle(4)
    
    print("\n--- Right Aligned Triangle ---")
    print_right_aligned_triangle(4)
    
    print("\n--- Pyramid ---")
    print_pyramid(4)
    
    print("\n--- Number Triangle ---")
    print_number_triangle(4)
    
    print("\n--- Floyd's Triangle ---")
    print_floyds_triangle(4)
    
    print("\n--- Practice Skeletons ---")
    practice_diamond_pattern(3)
    practice_hollow_square(4)
