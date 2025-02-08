from crewai import Task
from textwrap import dedent

class EmailFilterTasks:
    def filter_emails_task(self, agent, emails):
        print("DEBUG: Entered filter_emails_task with emails:")
        print(emails)
        description = dedent(f"""\
            Analyze a batch of emails and filter out non-essential ones such as newsletters, promotional content, and notifications.

            Use your expertise in email content analysis to distinguish important emails from the rest. Pay attention to the sender and avoid invalid emails.

            Make sure to filter for messages actually directed at the user and avoid notifications.

            EMAILS:
            -------
            {emails}

            Your final answer MUST include the relevant thread IDs and the sender information (use bullet points).
            """)
        return Task(
            description=description,
            agent=agent,
            expected_output="" 
        )

    def action_required_emails_task(self, agent):
        print("DEBUG: Entered action_required_emails_task")
        description = dedent("""\
            For each email thread, pull and analyze the complete thread using only the actual Thread ID.
            Understand the context, key points, and the overall sentiment of the conversation.

            Identify the main query or concerns that need to be addressed in the response for each thread.

            Your final answer MUST be a list for all emails with:
            - the thread ID,
            - a summary of the email thread,
            - a highlighting of the main points,
            - identification of the user and who they will be answering to,
            - the communication style in the thread, and
            - the sender's email address.
            """)
        return Task(
            description=description,
            agent=agent,
            expected_output="" 
        )

    def draft_responses_task(self, agent):
        print("DEBUG: Entered draft_responses_task")
        description = dedent("""\
            Based on the action-required emails identified, draft responses for each.
            Ensure that each response is tailored to address the specific needs and context outlined in the email.

            - Assume the persona of the user and mimic the communication style in the thread.
            - Feel free to research the topic to provide a more detailed response, IF NECESSARY.
            - IF research is necessary, do it BEFORE drafting the response.
            - If you need to pull the thread again, do it using only the actual Thread ID.

            Use the provided tool to draft each of the responses.
            When using the tool, pass the following input:
            - To (recipient email)
            - Subject
            - Message

            You MUST create all drafts before sending your final answer.
            Your final answer MUST be a confirmation that all responses have been drafted.
            """)
        return Task(
            description=description,
            agent=agent,
            expected_output="" 
        )
