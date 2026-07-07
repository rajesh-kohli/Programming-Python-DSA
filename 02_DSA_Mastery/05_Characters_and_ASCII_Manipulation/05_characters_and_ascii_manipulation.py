###############################################################################
#                 05 - Characters and ASCII Manipulation                      #
###############################################################################

# =============================================================================
# SECTION 1: ASCII Basics (ord and chr)
# =============================================================================

def ascii_basics():
    char = 'A'
    ascii_val = ord(char)
    print(f"ord('{char}') = {ascii_val}")
    
    num = 97
    char_from_num = chr(num)
    print(f"chr({num}) = '{char_from_num}'")

# =============================================================================
# SECTION 2: Character Math & Case Conversion
# =============================================================================

def manual_to_lowercase(char: str) -> str:
    """ Convert a single uppercase character to lowercase using ASCII math. """
    # 'A' is 65, 'a' is 97. Difference is 32.
    if 'A' <= char <= 'Z': # Same as ord('A') <= ord(char) <= ord('Z')
        return chr(ord(char) + 32)
    return char

def manual_to_uppercase(char: str) -> str:
    """ Convert a single lowercase character to uppercase using ASCII math. """
    if 'a' <= char <= 'z':
        return chr(ord(char) - 32)
    return char

def toggle_case_string(s: str) -> str:
    """ Toggle case for an entire string without using .swapcase() """
    # Strings are immutable in Python, so we build a list
    result = []
    for char in s:
        if 'A' <= char <= 'Z':
            result.append(chr(ord(char) + 32))
        elif 'a' <= char <= 'z':
            result.append(chr(ord(char) - 32))
        else:
            result.append(char)
            
    # Join list back to a string
    return "".join(result)


# =============================================================================
# SECTION 3: Custom Integer Conversion
# =============================================================================

def string_to_integer(s: str) -> int:
    """ 
    Convert a string of digits to an integer without using int(). 
    Assumes positive numbers only.
    """
    result = 0
    for char in s:
        # Get numerical value of character
        digit_value = ord(char) - ord('0')
        # Shift current result left by 1 decimal place and add new digit
        result = result * 10 + digit_value
        
    return result


# --- Practice Skeletons ---

def practice_is_alphanumeric(char: str) -> bool:
    """
    Return True if the character is a letter (a-z, A-Z) or a digit (0-9)
    using ONLY ASCII boundaries (no .isalnum()).
    """
    pass

def practice_caesar_cipher(s: str, shift: int) -> str:
    """
    Shift every lowercase character in the string `s` by `shift` positions.
    Wrap around 'z' back to 'a'. Leave non-lowercase characters unchanged.
    """
    pass


# =============================================================================
# DRIVER CODE
# =============================================================================
if __name__ == "__main__":
    print("--- ASCII Basics ---")
    ascii_basics()
    
    print("\n--- Case Conversion ---")
    print("Lower of 'G':", manual_to_lowercase('G'))
    print("Upper of 'm':", manual_to_uppercase('m'))
    print("Toggle 'HeLLo 123!':", toggle_case_string('HeLLo 123!'))
    
    print("\n--- String to Integer ---")
    print("str_to_int('4096'):", string_to_integer('4096'), type(string_to_integer('4096')))
    
    print("\n--- Practice Skeletons ---")
    print("Is 'x' alphanumeric?", practice_is_alphanumeric('x'))
    print("Caesar cipher 'abc' shift 2:", practice_caesar_cipher('abc', 2))
