import random
import string


def generate_password():

    length = int(input("Password Length: "))

    characters = (
        string.ascii_letters +
        string.digits +
        string.punctuation
    )

    password = ""

    for _ in range(length):
        password += random.choice(characters)

    print("\nGenerated Password:")
    print(password)


def password_generator():

    while True:

        print("""
=========================
   PASSWORD GENERATOR
=========================
1. Generate Password
2. Return to Toolkit
""")

        choice = input("Select option: ")

        if choice == "1":
            generate_password()

        elif choice == "2":
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    password_generator()
