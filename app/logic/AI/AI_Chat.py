from langchain_google_genai import *
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentType, initialize_agent, Tool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools.arxiv.tool import ArxivQueryRun
from langchain_community.utilities.arxiv import ArxivAPIWrapper
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import json
import logging
from ..scrap.research import *
from .pdf_logic import *

logging.basicConfig(level=logging.ERROR)


load_dotenv()

google_api_key = os.environ.get("GOOGLE_API_KEY")


llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=google_api_key,
    temperature=0.7
)


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
    ),
    Tool(
        name='Paper Search',
        func = get_papers,
        description="Searches for research papers based on a particular topic."
    ),
    Tool(
        name = 'Paper Content',
        func= get_content,
        description="Get Content of a particular topic using it's Arxiv html link e.g https://arxiv.org/html/2504.07109"
    )
]


user_memories = {}


html_prompt = PromptTemplate(
    input_variables=["content"],
    template="""
    You are an AI Research Assistant as well as Analyst and optionally a programmer/engineer if it relates to computing or electronics. Your task is to provide a detailed, organized, and well-structured response to the user's query. Your response should include any relevant citations, references, images or key findings in bold or as hyperlinks.
    
    If it's a basic conversation message or if it is not related to research ouput just a simple message.

    --- Provide Intellectual Content and Response too..

    CONTENT: {content}

    Please format the content in a structured way, with the following formatting guidelines:
    - Important terms or phrases should be bolded.
    - Include any relevant academic paper links as [hyperlinks](link).
    - If the content refers to multiple sections or points, organize them as lists.
    - Include any necessary citations in parentheses (Author, Year) or as links with a nice color.
    - Space betwwn various headers and others
    - Keep the language professional and academic in tone.
    - Output everything in a basic html that can be rendered in a chatbot
    - The font size should be optimal
    - Optimize style assuming the div will be placed in a #1e1e38 background
    - Transparent background only.
    - All style, class and id should have suffix -dynax to avoid the page styling
    - Everything should be contained in a single div.

    Guide for Agent and LLM (Formatting and Content Structure)
        1. Response Type Detection:
            If the input is a research-related query:

            Format: Provide a detailed, academic-style response with proper references, citations, and formal language.

            Focus on Clarity: Break down complex ideas into sections for easier readability.

            Text Formatting: Highlight key terms using bold and make hyperlinks clearly visible by underlining them with a distinct color (preferably a shade that contrasts with dark mode background).

            If the input is casual or unrelated to research:

            Format: Provide a simple, conversational response.

            Tone: Friendly, engaging, and informal.

            Text Styling: Keep the styling minimal for better readability. Appropriate Spacing when necessary.

        2. Text Formatting Requirements:

            Paragraph Headers:

            Bold all major section headers to make them stand out(really bold) You can optionally change the color since it is more of a presentation.

            Ensure that headers are distinct, i.e., with more prominent font weight, ensuring they separate the content logically.

            Hyperlinks:

            Use an hover style for all hyperlinks.

            No text decoration.

            Set the link color to something distinct, like a blue or teal tone or propably a gradient and something cool that contrasts well with dark mode.

            Ensure links are visually clear and accessible.

            Key Terms:

            Bold the most important terms or phrases.

            If the content includes technical jargon or important concepts, make them bold to draw attention.

            The link should redirect to another page e.g target=_blank

        3. Special Handling for Non-Research Queries:
        
            Simple Pronouns/Short Inputs:

            Response: Provide a conversational, friendly response like, "How can I assist you today?" or "Tell me more about what you're looking for."

            Avoid complex or academic language for these types of inputs.

        4. Code Snippets (For Technical Queries):
            Format: Use <pre><code> tags for any code snippets, ensuring they are displayed in a readable format.

            Highlighting: For better readability, ensure that the code is color-coded (syntax highlighting) based on language.

        5. Handling Multiple Sources:
            References: For academic responses, always try to include proper citations or reference links where possible. Ensure that the format is clean and readable.

            The Reference must be correct 
            
            For example, when referring to a specific paper, include the title in bold, followed by the author(s), year, and a hyperlink to the source.

            Example:

                "Attention is All You Need" by Vaswani et al. (2017).

        6. Example Formatting Structure for LLM and Agent:

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
        research_content = agent.invoke(input=f"{message}")
        
        html_content = generate_html_content(research_content)
        
        return {
            "status": "success",
            "message": html_content
        }
    except Exception as e:
        print(e)
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

