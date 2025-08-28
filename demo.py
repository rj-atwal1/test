# Function to determine if a number is prime
# A prime number is a natural number greater than 1 that has no positive divisors other than 1 and itself.
# This function returns True if the input number is prime, and False otherwise.
def is_prime(num):
    # Step 1: Exclude numbers less than or equal to 1
    # By definition, 0 and 1 are not prime numbers, and negative numbers are not considered prime.
    # So, immediately return False for these cases.
    if num <= 1:
        return False

    # Step 2: Check divisibility for all numbers from 2 up to the square root of num (inclusive)
    # If num is divisible by any of these, it is not prime.
    # We use int(num**0.5) + 1 because any factor larger than the square root would have a corresponding factor smaller than the square root.
    for i in range(2, int(num**0.5) + 1):
        # If num divided by i leaves no remainder, then i is a divisor of num, so num is not prime.
        # For example, if num is 9 and i is 3, 9 % 3 == 0, so 9 is not prime.
        if num % i == 0:
            return False

    # Step 3: If the loop completes without finding any divisors, num is prime.
    # This means num is only divisible by 1 and itself.
    return True

# Test cases for the is_prime function
# The following lines demonstrate how the function works with example inputs.
# The expected output is shown in the comments for clarity.
print(is_prime(11))  # Should print True, since 11 is a prime number (only divisible by 1 and 11)
print(is_prime(4))   # Should print False, since 4 is not a prime number (divisible by 1, 2, and 4)

