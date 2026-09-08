import csv
import json
import os
import secrets
import string
from datetime import datetime

HISTORY_FILE = "password_history.json"
CSV_FILE = "password_history.csv"

# Characters that can be easily confused
CONFUSING_CHARACTERS = "0Ool1I"


def ask_yes_no(question):
    """Keep asking until the user enters Y or N."""
    while True:
        answer = input(f"{question} (Y/N): ").strip().upper()

        if answer in ("Y", "N"):
            return answer == "Y"

        print("Please enter Y or N.")


def get_number(question, minimum, maximum):
    """Get a valid whole number within a chosen range."""
    while True:
        try:
            number = int(input(question))

            if minimum <= number <= maximum:
                return number

            print(f"Please enter a number between {minimum} and {maximum}.")

        except ValueError:
            print("Please enter a whole number.")


def load_history():
    """Load previously saved password history."""
    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, list):
                return data

    except (json.JSONDecodeError, OSError):
        print("Warning: Password history could not be loaded.")

    return []


def save_history(history):
    """Save password history to a JSON file."""
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump(history, file, indent=4)

    except OSError as error:
        print(f"Could not save password history: {error}")


def remove_confusing_characters(characters):
    """Remove characters such as 0, O, o, l, 1 and I."""
    return "".join(
        character
        for character in characters
        if character not in CONFUSING_CHARACTERS
    )


def build_character_groups(use_uppercase, use_numbers, use_symbols,
                           exclude_confusing):
    """Build the character groups selected by the user."""
    groups = [string.ascii_lowercase]

    if use_uppercase:
        groups.append(string.ascii_uppercase)

    if use_numbers:
        groups.append(string.digits)

    if use_symbols:
        groups.append(string.punctuation)

    if exclude_confusing:
        groups = [
            remove_confusing_characters(group)
            for group in groups
        ]

    return [group for group in groups if group]


def secure_shuffle(items):
    """Shuffle a list using the secrets module."""
    for position in range(len(items) - 1, 0, -1):
        new_position = secrets.randbelow(position + 1)
        items[position], items[new_position] = (
            items[new_position],
            items[position]
        )


def create_password(length, groups):
    """Create a password containing every selected character type."""
    password_characters = []

    # Guarantee one character from each selected group
    for group in groups:
        password_characters.append(secrets.choice(group))

    all_characters = "".join(groups)

    while len(password_characters) < length:
        password_characters.append(secrets.choice(all_characters))

    secure_shuffle(password_characters)

    return "".join(password_characters)


def check_strength(password):
    """Give the generated password a simple strength rating."""
    score = 0

    if len(password) >= 12:
        score += 1

    if len(password) >= 16:
        score += 1

    if any(character.isupper() for character in password):
        score += 1

    if any(character.isdigit() for character in password):
        score += 1

    if any(character in string.punctuation for character in password):
        score += 1

    if score <= 2:
        return "Weak"

    if score <= 4:
        return "Medium"

    return "Strong"


def copy_to_clipboard(password):
    """Copy a password using the optional pyperclip package."""
    try:
        import pyperclip
        pyperclip.copy(password)
        print("Password copied to clipboard.")

    except ImportError:
        print("\nClipboard support is not installed.")
        print("Run this command in the VS Code terminal:")
        print("python -m pip install pyperclip")

    except Exception as error:
        print(f"Password could not be copied: {error}")


def add_to_history(password):
    """Save one generated password to history."""
    history = load_history()

    history.append({
        "password": password,
        "strength": check_strength(password),
        "created": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    })

    save_history(history)


def generate_passwords():
    """Collect settings and generate one or more passwords."""
    print("\n--- Password Settings ---")

    length = get_number("Password length (8-64): ", 8, 64)
    amount = get_number("How many passwords (1-20): ", 1, 20)

    use_uppercase = ask_yes_no("Include uppercase letters?")
    use_numbers = ask_yes_no("Include numbers?")
    use_symbols = ask_yes_no("Include symbols?")
    exclude_confusing = ask_yes_no(
        "Exclude confusing characters (0, O, o, l, 1, I)?"
    )

    groups = build_character_groups(
        use_uppercase,
        use_numbers,
        use_symbols,
        exclude_confusing
    )

    if length < len(groups):
        print("The password is too short for the selected options.")
        return []

    passwords = []

    print("\n==============================")
    print("     GENERATED PASSWORDS")
    print("==============================")

    for number in range(1, amount + 1):
        password = create_password(length, groups)
        strength = check_strength(password)

        passwords.append(password)
        print(f"{number}. {password} [{strength}]")

    if ask_yes_no("\nSave these passwords to history?"):
        for password in passwords:
            add_to_history(password)

        print(f"History saved to {HISTORY_FILE}.")

    if len(passwords) == 1:
        if ask_yes_no("Copy the password to clipboard?"):
            copy_to_clipboard(passwords[0])

    else:
        if ask_yes_no("Copy one password to clipboard?"):
            selection = get_number(
                f"Choose password number (1-{len(passwords)}): ",
                1,
                len(passwords)
            )

            copy_to_clipboard(passwords[selection - 1])

    return passwords


def view_history():
    """Display saved password history."""
    history = load_history()

    print("\n--- Password History ---")

    if not history:
        print("No saved password history.")
        return

    for number, entry in enumerate(history, start=1):
        print(f"""
Entry    : {number}
Password : {entry.get("password", "Unknown")}
Strength : {entry.get("strength", "Unknown")}
Created  : {entry.get("created", "Unknown")}
------------------------------
""")


def export_history_to_csv():
    """Export saved JSON history to a CSV spreadsheet."""
    history = load_history()

    if not history:
        print("No password history to export.")
        return

    try:
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
            column_names = ["password", "strength", "created"]

            writer = csv.DictWriter(
                file,
                fieldnames=column_names,
                extrasaction="ignore"
            )

            writer.writeheader()
            writer.writerows(history)

        print(f"Password history exported to {CSV_FILE}.")

    except OSError as error:
        print(f"Could not export the CSV file: {error}")


def clear_history():
    """Delete all saved password history."""
    history = load_history()

    if not history:
        print("Password history is already empty.")
        return

    if ask_yes_no("Delete all saved password history?"):
        save_history([])
        print("Password history cleared.")
    else:
        print("History was not changed.")


def password_generator():
    """Display the password generator menu."""
    while True:
        print("""
================================
      PASSWORD GENERATOR
================================
1. Generate Passwords
2. View Password History
3. Export History to CSV
4. Clear Password History
5. Return to IT Toolkit
""")

        choice = input("Select option: ").strip()

        if choice == "1":
            generate_passwords()

        elif choice == "2":
            view_history()

        elif choice == "3":
            export_history_to_csv()

        elif choice == "4":
            clear_history()

        elif choice == "5":
            print("Returning to IT Toolkit...")
            break

        else:
            print("Invalid option. Choose 1 to 5.")


if __name__ == "__main__":
    password_generator()
