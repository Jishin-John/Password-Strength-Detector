import math

def estimate_crack_time(pwd):
    length = len(pwd)
    has_lower = any(c.islower() for c in pwd)
    has_upper = any(c.isupper() for c in pwd)
    has_digit = any(c.isdigit() for c in pwd)
    has_special = any(not c.isalnum() for c in pwd)

    # Estimate character set size
    charset_size = 0
    if has_lower: charset_size += 26
    if has_upper: charset_size += 26
    if has_digit: charset_size += 10
    if has_special: charset_size += 32  # approx special characters

    # Total combinations = charset_size ^ password_length
    total_combinations = charset_size ** length

    # Assume attacker can try 1 billion passwords per second
    guesses_per_second = 1_000_000_000
    seconds = total_combinations / guesses_per_second

    return convert_seconds(seconds)
