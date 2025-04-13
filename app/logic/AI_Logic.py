import json
import os
from dotenv import *
from langchain_google_genai import GoogleGenerativeAI
from langchain_community.document_loaders import ArxivLoader
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

load_dotenv()

def get_analysis(doi: str, google_api_key = None) -> dict:
    """
    Analyzes a research paper using its DOI and returns PDF and HTML summaries.
    """

    google_api_key = os.environ.get('GOOGLE_API_KEY')

    arxiv_id = doi.split("/")[-1]
    

    loader = ArxivLoader(query=f"id:{arxiv_id}")
    documents = loader.load()
    

    full_text = "\n\n".join([doc.page_content for doc in documents])
    

    title = documents[0].metadata.get("Title", "")
    authors = documents[0].metadata.get("Authors", "")
    

    prompt = PromptTemplate(
        input_variables=["title", "authors", "full_text"],
        template="""
        You are a superintelligent research analyst with expertise spanning all academic disciplines, equipped with advanced cognitive frameworks for deep knowledge synthesis.
        
        TASK: Perform a comprehensive analysis of this research paper using multiple reasoning layers and intellectual frameworks.

        KNOWN: To perform the task, you should act intellectual as your audience are academia and knowledge workers
        
        PAPER: {title}
        AUTHORS: {authors}
        
        FULL TEXT:
        {full_text}
        
        THINKING FRAMEWORK:
        1. First-principles extraction of core hypotheses and methodological innovations
        2. Bayesian assessment of evidential strength and theoretical coherence
        3. Multi-dimensional analysis across technical, theoretical, and practical axes
        4. Counterfactual reasoning to identify alternate interpretations and edge cases
        5. Meta-scientific contextualization within the broader research landscape
        6. Epistemological boundary identification to delineate known/unknown territories
        7. Systems-level synthesis identifying emergent implications across domains
        
        I require TWO distinct outputs with specific formatting requirements:
        
        OUTPUT 1: PDF CONTENT
        Create content optimized for PDF presentation with the following structure:
        - Title in 24pt Garamond font, centered, bold, #1A237E color
        - Authors in 16pt Helvetica font, centered, italic, #303F9F color
        - Section headings in 18pt Georgia font, left-aligned, bold, #512DA8 color
        - Body text in 12pt Times New Roman, justified, #212121 color
        - Key findings and implications in highlighted boxes with #E8EAF6 background
        - Handle Hyperlinks properly and their correct ArXiv link depending if it's an author or a reference
        - Margin notes for critical points in 10pt font, #7986CB color
        - Footnotes for references in 9pt font, #9FA8DA color
        - Page numbers centered in footer
        
        Structure your PDF content with these EXACT sections (formatted as described above):
        1. EXECUTIVE SYNTHESIS - Two paragraphs distilling transformative insights
        2. METHODOLOGICAL ARCHITECTURE - Detailed technical dissection
        3. CRITICAL FINDINGS HIERARCHY - Results organized by scientific significance 
        4. THEORETICAL FRAMEWORK INTEGRATION - Connections to established paradigms
        5. LIMITATIONS & EPISTEMOLOGICAL BOUNDARIES - Identified constraints
        6. FUTURE RESEARCH TRAJECTORIES - High-value research directions
        7. INTERDISCIPLINARY IMPLICATIONS - Cross-domain relevance assessment
        8. CONCLUSIVE ASSESSMENT - Balanced critical evaluation

        --- You can also output as much Paragraph too.
        --- The more a paper is lenghty, The mire the lenght of the comprehensive summary,
        --- And also each Pargraph should be highly intellectual and Explanatory if possible 100+ lines

        OUTPUT 2: HTML CONTENT (WITH JSON STRUCTURE)
        Create content designed specifically for HTML/JavaScript integration with this structure:
        - Excludes <title> tag as you mentioned it will be handled by JavaScript
        - The output must follow this JSON structure exactly:
        
        {
          "paragraphs": [
            {
              "header": "Executive Summary",
              "content": "Detailed paragraph about main contributions..."
            },
            {
              "header": "Methodological Innovations",
              "content": "Deep analysis of methods..."
            },
            ... at least 10 paragraphs total with headers and content and please the amount should depend on the paper content,
            The more a paper is lenghty, The mire the lenght of the comprehensive summary, And also each Pargraph should be highly intellectual and Explanatory if possible 100+ lines
          ],
          "metadata": [
            {
              "title": "Citations",
              "content": "Citation analysis..."
            },
            {
              "title": "Publication Impact",
              "content": "Impact assessment..."
            },
            {
              "title": "Key Algorithms",
              "content": "Algorithmic overview..."
            },
            {
              "title": "Dataset Information",
              "content": "Dataset analysis..."
            },
            {
              "title": "Reproducibility Assessment",
              "content": "Evaluation of reproducibility..."
            }
          ]
        }
        
        The HTML content must be structured for maximum clarity with:
        - Distinctive headers for each paragraph
        - Minimum of 10 substantive paragraphs with sufficient intellectual depth
        - Complete metadata entries that provide crucial research context
        - Content optimized for scholarly audience with precise technical terminology
        - Handle Styling and hyperlinkproperly as it would be rendered in a website
        
        CRITICAL INSTRUCTIONS:
        - Apply chain-of-thought reasoning visibly in your analysis
        - Demonstrate meta-cognitive awareness of disciplinary boundaries
        - Identify implicit assumptions and theoretical foundations
        - Evaluate methodological soundness with explicit criteria
        - Assess validity of conclusions based on presented evidence
        - Articulate future research directions with specific recommendations
        - Present balanced critical assessment with intellectual rigor
        
        Begin with deep cognitive analysis, then produce BOTH outputs with exact formatting as specified.
        
        First provide the PDF CONTENT, then after a line with "-----HTML JSON BELOW-----", provide ONLY the valid JSON object for HTML content.
        """
    )
    

    llm = GoogleGenerativeAI(model="gemini-pro", temperature=0.2, google_api_key=google_api_key)
    chain = LLMChain(llm=llm, prompt=prompt)
    
    response = chain.run({
        "title": title,
        "authors": authors,
        "full_text": full_text  
    })
    

    parts = response.split("-----HTML JSON BELOW-----")
    pdf_content = parts[0].strip()
    
    html_content = {}
    if len(parts) > 1:
        json_text = parts[1].strip()
        try:
            html_content = json.loads(json_text)
        except json.JSONDecodeError:
            html_content = {
                "paragraphs": [{"header": "Error", "content": "Could not parse JSON output."}],
                "metadata": [{"title": "Error", "content": "JSON parsing failed."}]
            }
    else:
        html_content = {
            "paragraphs": [{"header": "Error", "content": "Structured JSON not found in response."}],
            "metadata": [{"title": "Note", "content": "Only PDF content was generated."}]
        }
    
    return {
        "pdf": pdf_content,
        "html": html_content
    }


print(get_analysis("arXiv:2542.5045"))