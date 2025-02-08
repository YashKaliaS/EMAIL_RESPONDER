from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools.gmail.create_draft import GmailCreateDraft
from langchain.tools import tool

class CreateDraftTool:
    @tool("Create Draft")
    def create_draft(data):
        """Create an email draft.

        Useful to create an email draft. The input to this tool should be a pipe (|) separated string
        of length 3, representing:
          - who to send the email to,
          - the subject of the email, and
          - the actual message.
        
        For example: 
            lorem@ipsum.com|Nice To Meet You|Hey it was great to meet you.
        """
        print("DEBUG: Entered CreateDraftTool.create_draft")
        email, subject, message = data.split('|')
        print(f"DEBUG: Parsed email: {email}, subject: {subject}, message: {message}")
        gmail = GmailToolkit()
        draft = GmailCreateDraft(api_resource=gmail.api_resource)
        print("DEBUG: GmailCreateDraft instantiated:", draft)
        result = draft({
            'to': [email],
            'subject': subject,
            'message': message
        })
        print("DEBUG: Draft creation result:", result)
        return f"\nDraft created: {result}\n"
