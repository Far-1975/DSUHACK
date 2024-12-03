import streamlit as st
import pandas as pd
from utils import load_issue_tickets, save_issue_ticket, send_email_to_citizen

def authority_interface():
    st.title("Authority Page")
    st.header("Manage Issue Tickets")

    # Load tickets
    issue_tickets = load_issue_tickets()

    if issue_tickets:
        df_tickets = pd.DataFrame(issue_tickets)

        # Display open tickets
        open_tickets = [ticket for ticket in issue_tickets if ticket["status"] == "Open"]
        st.subheader("Open Tickets")

        if open_tickets:
            st.dataframe(pd.DataFrame(open_tickets))

            # Manage a selected ticket
            ticket_index = st.selectbox("Select a Ticket to Manage", range(len(open_tickets)))

            if ticket_index is not None:
                selected_ticket = open_tickets[ticket_index]

                st.subheader("Ticket Details")
                st.json(selected_ticket)

                # Resolve or take action
                if st.button("Mark as Resolved"):
                    # Mark ticket as resolved
                    selected_ticket["status"] = "Resolved"
                    save_issue_ticket(issue_tickets)  # Save updated ticket list to CSV

                    # Notify the citizen
                    st.success("Ticket marked as resolved!")

                    # Compose the email content
                    citizen_name = selected_ticket["name"]
                    citizen_email = selected_ticket["email"]
                    subject = f"Your reported issue '{selected_ticket['description']}' has been resolved"
                    body = f"Dear {citizen_name},\n\nYour reported issue '{selected_ticket['description']}' has been resolved. Thank you for bringing it to our attention.\n\nBest regards,\nBBMP Authority"
                    
                    # Send the email
                    send_email_to_citizen(citizen_email, subject, body)

                    # Simulate notifying the citizen in the app
                    st.write(f"Message sent to citizen: {citizen_name}")

                    # Refresh the page after resolving
                    st.rerun()  # Use st.rerun() to refresh the page and display the updated ticket status.
        else:
            st.info("No open tickets available.")
    else:
        st.info("No tickets to display.")
