import json
import os

TICKETS_FILE = "tickets.json"


# Load tickets from file
def load_tickets():
    if os.path.exists(TICKETS_FILE):
        with open(TICKETS_FILE, "r") as file:
            return json.load(file)
    return []


# Save tickets to file
def save_tickets(tickets):
    with open(TICKETS_FILE, "w") as file:
        json.dump(tickets, file, indent=4)


# Create a new ticket
def create_ticket(tickets):
    print("\n--- Create Ticket ---")

    user = input("Your Name: ")
    issue = input("Issue Description: ")
    priority = input("Priority (Low / Medium / High): ")

    ticket = {
        "id": len(tickets) + 1,
        "user": user,
        "issue": issue,
        "priority": priority.title(),
        "status": "Open"
    }

    tickets.append(ticket)
    save_tickets(tickets)

    print(f"\n✅ Ticket #{ticket['id']} created successfully!")


# View all tickets
def view_tickets(tickets):
    print("\n--- All Tickets ---")

    if not tickets:
        print("No tickets found.")
        return

    for ticket in tickets:
        print(f"""
Ticket ID : {ticket['id']}
User      : {ticket['user']}
Issue     : {ticket['issue']}
Priority  : {ticket['priority']}
Status    : {ticket['status']}
-----------------------------
""")


# Close a ticket
def close_ticket(tickets):
    ticket_id = input("\nEnter Ticket ID to close: ")

    for ticket in tickets:
        if str(ticket["id"]) == ticket_id:
            ticket["status"] = "Closed"
            save_tickets(tickets)
            print("✅ Ticket closed.")
            return

    print("❌ Ticket not found.")


# Dashboard
def dashboard(tickets):
    open_tickets = sum(1 for t in tickets if t["status"] == "Open")
    closed_tickets = sum(1 for t in tickets if t["status"] == "Closed")

    print("\n--- Dashboard ---")
    print(f"Open Tickets   : {open_tickets}")
    print(f"Closed Tickets : {closed_tickets}")
    print(f"Total Tickets  : {len(tickets)}")


# Main Help Desk Menu
def helpdesk():

    tickets = load_tickets()

    while True:

        print("""
=========================
      HELP DESK
=========================
1. Create Ticket
2. View Tickets
3. Close Ticket
4. Dashboard
5. Return to Toolkit
""")

        choice = input("Select option: ")

        if choice == "1":
            create_ticket(tickets)

        elif choice == "2":
            view_tickets(tickets)

        elif choice == "3":
            close_ticket(tickets)

        elif choice == "4":
            dashboard(tickets)

        elif choice == "5":
            break

        else:
            print("Invalid option.")


# Run directly
if __name__ == "__main__":
    helpdesk()
