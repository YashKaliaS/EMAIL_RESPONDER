from crewai import Crew, LLM
from .agents import EmailFilterAgents
from .tasks import EmailFilterTasks

llm = LLM(
    model="groq/gemma2-9b-it",
    temperature=0.7
)

class EmailFilterCrew:
    def __init__(self):
        print("DEBUG: Entered EmailFilterCrew constructor")
        agents = EmailFilterAgents()
        self.filter_agent = agents.email_filter_agent()
        self.action_agent = agents.email_action_agent()
        self.writer_agent = agents.email_response_writer()
        print("DEBUG: Exiting EmailFilterCrew constructor")

    def kickoff(self, state):
        print("DEBUG: kickoff() started with state:", state)
        tasks = EmailFilterTasks()
        
        # Format emails and print the result
        formatted_emails = self._format_emails(state.get('emails', []))
        print("DEBUG: Formatted emails:")
        print(formatted_emails)
        
        # Create Crew with tasks and agents
        crew = Crew(
            agents=[self.filter_agent, self.action_agent, self.writer_agent],
            tasks=[
                tasks.filter_emails_task(self.filter_agent, formatted_emails),
                tasks.action_required_emails_task(self.action_agent),
                tasks.draft_responses_task(self.writer_agent)
            ],
            verbose=True
        )
        
        print("DEBUG: Running Crew.kickoff()")
        result = crew.kickoff()
        print("DEBUG: Crew.kickoff() returned:", result)
        
        # Check if the result contains any required update keys
        required_keys = ['checked_emails_ids', 'emails', 'action_required_emails']
        if not (isinstance(result, dict) and any(key in result for key in required_keys)):
            print("DEBUG: Warning: Crew result does not contain any of the required keys:", required_keys)
            # Fallback: wrap a default update so that the state is valid
            result = {"action_required_emails": "Default update: no actionable emails were produced by the tasks."}
        else:
            print("DEBUG: Crew result contains at least one required key.")

        updated_state = {**state, "action_required_emails": result}
        print("DEBUG: Final updated state:")
        print(updated_state)
        return updated_state

    def _format_emails(self, emails):
        emails_string = []
        for email in emails:
            print("DEBUG: Processing email:", email)
            arr = [
                f"ID: {email['id']}",
                f"- Thread ID: {email['threadId']}",
                f"- Snippet: {email['snippet']}",
                f"- From: {email['sender']}",
                "--------"
            ]
            emails_string.append("\n".join(arr))
        formatted = "\n".join(emails_string)
        return formatted
