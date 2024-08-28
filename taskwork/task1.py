import math

def is_palindrome(s):
    s = s.lower().replace(" ", "")  # Normalize string by converting to lowercase and removing spaces
    is_pal = s == s[::-1]  # Check if string is equal to its reverse
    char_freq = {}  # Dictionary to store character frequency
    
    for char in s:
        if char in char_freq:
            char_freq[char] += 1
        else:
            char_freq[char] = 1
    
    return is_pal, char_freq

def is_prime(n):
    if n <= 1:
        return [(False, i) for i in range(2, int(math.sqrt(abs(n))) + 1)]
    
    result = []
    for i in range(2, int(math.sqrt(n)) + 1):
        result.append((n % i == 0, i))
    return result

def main():
    attempts = 3
    error_log = []
    results = []
    
    # Handle string input for palindrome check
    while True:
        user_string = input("Enter a string to check if it's a palindrome: ")
        if user_string.strip():###########################
            palindrome_result = is_palindrome(user_string)
            break
        else:
            print("Invalid input. Please enter a non-empty string.")
    
    # Handle integer input for prime number check
    for attempt in range(attempts):
        try:
            user_number = int(input("Enter a number to check if it's prime: "))
            prime_result = is_prime(user_number)
            break
        except ValueError as e:
            error_log.append((input("What did you enter? "), str(e)))
            print(f"Invalid input. Please enter a valid integer. {attempts - attempt - 1} attempts remaining.")
    else:
        print("Too many invalid attempts. Exiting the program.")
        print("Error log:", error_log)
        return
    
    # Store results
    result = {
        "input_string": user_string,
        "palindrome_result": palindrome_result,
        "input_number": user_number,
        "prime_result": prime_result
    }
    
    results.append(result)
    
    # Print results
    print("\nResults:")
    for res in results:
        print(res)
    
    if error_log:
        print("\nError Log:")
        for error in error_log:
            print(error)

if __name__ == "__main__":
    main()
