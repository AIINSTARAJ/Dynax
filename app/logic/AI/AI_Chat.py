from langchain_google_genai import *
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentType, initialize_agent, Tool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools.arxiv.tool import ArxivQueryRun
from langchain_community.utilities.arxiv import ArxivAPIWrapper
from dotenv import load_dotenv
import os


load_dotenv()

google_api_key = os.environ.get("GOOGLE_API_KEY")


llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.7, google_api_key=google_api_key)

wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

arxiv = ArxivQueryRun(api_wrapper=ArxivAPIWrapper())

tools = [
    Tool(
        name="Wikipedia",
        func=wikipedia_tool.run,
        description="Searches Wikipedia for academic-related articles and general knowledge. Input should be a search query."
    ),
    Tool(
        name="Arxiv",
        func=arxiv.run,
        description="Searches Arxiv for research papers. Input should be a search query."
    )
]


user_memories = {}


html_prompt = PromptTemplate(
    input_variables=["content"],
    template="""
    You are an AI Research Assistant. Your task is to provide a detailed, organized, and well-structured academic response to the user's query. Your response should include any relevant citations, references, or key findings in bold or as hyperlinks.
    
    --- Provide Intellectual Content and Response too..

    CONTENT: {content}

    Please format the content in a structured way, with the following formatting guidelines:
    - Important terms or phrases should be **bolded**.
    - Include any relevant academic paper links as [hyperlinks](link).
    - If the content refers to multiple sections or points, organize them in bullet points or numbered lists.
    - Include any necessary citations in parentheses (Author, Year) or as links.
    - Keep the language professional and academic in tone.
    - Output everything in a basic html that can be rendered in a chatbot
    """
)

# Function to generate HTML content
def generate_html_content(content):
    html_chain = html_prompt | llm
    html_content = html_chain.invoke({
        "content": content
    })
    return html_content


def get_agent(user_token):
    if user_token not in user_memories:
        user_memories[user_token] = ConversationBufferMemory(memory_key="chat_history")
    
    agent = initialize_agent(
        tools=tools, 
        llm=llm, 
        agent_type=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        memory=user_memories[user_token],
        verbose=True
    )
    return agent

def research(user_token, message):
    """
    Process a research query and return the formatted response.
    
    Args:
        user_token (str): Unique identifier for the user
        message (str): The research query/question
        
    Returns:
        dict: Dictionary containing status, content (formatted HTML) or error message
    """
    try:
        
        agent = get_agent(user_token)
        research_content = agent.run(input=f"Research the following topic and provide detailed academic information: {message}")
        
        html_content = generate_html_content(research_content)
        
        return {
            "status": "success",
            "messsage": html_content
        }
    except Exception as e:

        return {
            "status": "error",
            "message": """ 
                <div style="
                background-color: rgba(255, 0, 0, 0.05);
                border: 1px solid rgba(255, 0, 0, 0.2);
                color: #d32f2f;
                padding: 12px 16px;
                border-radius: 6px;
                font-family: 'Segoe UI', Tahoma, sans-serif;
                font-size: 14px;
                font-weight: 500;
                max-width: 500px;
                margin: 20px auto;
            ">
                <strong>⚠️ Oops! Something went wrong.</strong>
            </div>
        """
        }

def clear_user_memory(user_token):
    """
    Clear a user's conversation memory
    
    Args:
        user_token (str): Unique identifier for the user
        
    Returns:
        bool: True if memory was cleared, False if no memory found
    """
    if user_token in user_memories:
        del user_memories[user_token]
        return True
    return False
