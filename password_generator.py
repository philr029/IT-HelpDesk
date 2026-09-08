import random
import string


def generate_password():

    while True:
        length = int(input("Password Length (8-32): "))

        if 8 <= length <= 32:
            break

        print("❌ Length must be between 8 and 32.")

    uppercase = input("Include Uppercase? (Y/N): ").upper()
    numbers = input("Include Numbers? (Y/N): ").upper()
    symbols = input("Include Symbols? (Y/N): ").upper()

    characters = list(string.ascii_lowercase)

    password = []

    if uppercase == "Y":
        characters.extend(string.ascii_uppercase)
        password.append(random.choice(string.ascii_uppercase))

    if numbers == "Y":
        characters.extend(string.digits)
        password.append(random.choice(string.digits))

    if symbols == "Y":
        characters.extend(string.punctuation)
        password.append(random.choice(string.punctuation))

    while len(password) < length:
        password.append(random.choice(characters))

    random.shuffle(password)

    password = "".join(password)

    print("\n====================")
    print("Generated Password")
    print("====================")
    print(password)

    # Strength Checker
    score = 0

    if length >= 12:
        score += 1

    if uppercase == "Y":
        score += 1

    if numbers == "Y":
        score += 1

    if symbols == "Y":
        score += 1

    print("\nPassword Strength:")

    if score <= 2:
        print("⚠️ Weak")

    elif score == 3:
        print("⚡ Medium")

    else:
        print("💪 Strong")


def password_generator():

    while True:

        print("""
=========================
   PASSWORD GENERATOR
=========================
1. Generate Password
2. Return
""")

        choice = input("Select option: ")

        if choice == "1":
            generate_password()

        elif choice == "2":
            break

        else:
            print("❌ Invalid option")


if __name__ == "__main__":
    password_generator()
