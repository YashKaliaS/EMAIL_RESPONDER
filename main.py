from src.graph import WorkFlow

# Provide an initial state with the required keys.
initial_state = {
    "checked_emails_ids": [],  # Start with an empty list of checked email IDs.
    "emails": []               # Optionally, add an empty emails list.
}

app = WorkFlow().app
app.invoke(initial_state)
