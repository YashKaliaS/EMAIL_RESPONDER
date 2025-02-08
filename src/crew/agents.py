from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools.gmail.get_thread import GmailGetThread
from langchain_community.tools.tavily_search import TavilySearchResults
from crewai import LLM
from textwrap import dedent
from crewai import Agent
from langchain_core.tools import Tool
from .tools import CreateDraftTool

llm = LLM(
    model="groq/gemma2-9b-it",
    temperature=0.7
)

class EmailFilterAgents():
    def __init__(self):
        print("Entered constructor of EmailFilterAgents")
        self.gmail = GmailToolkit()

    def email_filter_agent(self):
        return Agent(
            role='Senior Email Analyst',
            goal='Filter out non-essential emails like newsletters and promotional content',
            backstory=dedent("""\
                As a Senior Email Analyst, you have extensive experience in email content analysis.
                You are adept at distinguishing important emails from spam, newsletters, and other
                irrelevant content. Your expertise lies in identifying key patterns and markers that
                signify the importance of an email.
            """),
            verbose=True,
            llm=llm,
            allow_delegation=False
        )

    def email_action_agent(self):
        return Agent(
            role='Email Action Specialist',
            goal='Identify action-required emails and compile a list of their IDs',
            backstory=dedent("""\
                With a keen eye for detail and a knack for understanding context, you specialize
                in identifying emails that require immediate action. Your skill set includes interpreting
                the urgency and importance of an email based on its content and context.
            """),
            tools=[
                Tool(
                    name="get_gmail_thread",
                    func=lambda thread_id: (
    				print(f"Debug: get_gmail_thread called with thread_id={thread_id}") or
    				GmailGetThread(api_resource=self.gmail.api_resource).run(thread_id)
					),	
                    description="Fetches Gmail thread details."
                ),
                
                Tool(
                    name="tavily_search",
                    func=lambda query: TavilySearchResults().run(query),
                    description="Performs a web search."
                )
            ],
            llm=llm,
            verbose=True,
            allow_delegation=False,
        )

    def email_response_writer(self):
        return Agent(
            role='Email Response Writer',
            goal='Draft responses to action-required emails',
            backstory=dedent("""\
                You are a skilled writer, adept at crafting clear, concise, and effective email responses.
                Your strength lies in your ability to communicate effectively, ensuring that each response is
                tailored to address the specific needs and context of the email.
            """),
            tools=[
                Tool(
                    name="tavily_search",
                    func=lambda query: TavilySearchResults().run(query),
                    description="Performs a web search."
                ),
                Tool(
                    name="get_gmail_thread",
                    func=lambda thread_id: GmailGetThread(api_resource=self.gmail.api_resource).run(thread_id),
                    description="Fetches Gmail thread details."
                ),
                # Assuming CreateDraftTool.create_draft is a valid callable tool or already wrapped appropriately.
                CreateDraftTool.create_draft  
            ],
            llm=llm,
            verbose=True,
            allow_delegation=False,
        )
