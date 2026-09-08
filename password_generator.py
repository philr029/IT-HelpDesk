import random
import string


def generate_password():

    length = int(input("Password Length: "))

    characters = ""

    uppercase = input("Include Uppercase? (Y/N): ").upper()
    numbers = input("Include Numbers? (Y/N): ").upper()
    symbols = input("Include Symbols? (Y/N): ").upper()

    # Always include lowercase
    characters += string.ascii_lowercase

    if uppercase == "Y":
        characters += string.ascii_uppercase

    if numbers == "Y":
        characters += string.digits

    if symbols == "Y":
        characters += string.punctuation

    password = ""

    for _ in range(length):
        password += random.choice(characters)

    print("\nGenerated Password:")
    print(password)
