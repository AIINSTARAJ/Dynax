'''import json
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from .pdf_logic import *


load_dotenv()

def get_analysis(paper: json, google_api_key = None) -> dict:
    """
    Analyzes a research paper using its DOI and returns PDF and HTML summaries.
    """
    google_api_key = google_api_key or os.environ.get('GOOGLE_API_KEY')
    
    full_text = get_content(paper['pdf'].replace("'", ""))
    title = paper['title']
    authors = paper['authors']
    
    #Prompt for PDF version
    pdf_prompt = PromptTemplate(
        input_variables=["title", "authors", "full_text"],
        template="""
        You are an expert academic research analyst and summarizer. Create a comprehensive summary of the following research paper.
        
        INPUT:
        PAPER_TITLE: {{title}}
        AUTHORS: {{authors}}
        FULL_TEXT: {{full_text}}
        
        OUTPUT INSTRUCTIONS:
        Create a detailed academic and highly intellectual summary of this paper with the following sections:

        1. Executive Synthesis (overview of key contributions)
        2. Methodological Architecture (approach and design)
        3. Critical Findings Hierarchy (main results)
        4. Theoretical Framework Integration (how findings connect to theory)
        5. Limitations & Epistemological Boundaries
        6. Future Research Trajectories
        7. Interdisciplinary Implications
        8. Conclusive Assessment

        -- It's not compulsory to use the exact section above but make it as  structured as that.

        -- Each Sections shouldn't be less than 5000 words
        
        Focus on clarity and accuracy in your summary. Use academic language but avoid unnecessary jargon. Not less than 32000 words.
        """
    )
    
    html_prompt = PromptTemplate(
        input_variables=["title", "authors", "pdf_content"],
        template="""
      You are an expert HTML formatter for academic content. Convert the following research summary into a well-styled HTML document that's fully compatible with an existing application styling system. The HTML must use a special namespace suffix for all classes and IDs to prevent styling conflicts.
      
      PAPER_TITLE: {{title}}
      AUTHORS: {{authors}}
      SUMMARY_CONTENT: {{pdf_content}}
      
      OUTPUT INSTRUCTIONS:
      Create an HTML document with the following specifications:
      
      1. MOST IMPORTANT: Every single class name and ID must end with "-dynax" suffix to prevent styling conflicts

      2. Structure:
        - Everything must be contained within a single parent div with class="paper-container-dynax"
        - Proper HTML structure with proper nesting
        - No styling in the head section - all styling must be within style tags in the body
      
      3. Styling:

        - All CSS class and ID selectors must include the "-dynax" suffix (e.g., .highlight-dynax, #title-dynax)
        - Font: Arial or sans-serif/Poppins for body text, size 16px, line height 1.6
        - Title: 28px, centered, bold, with gradient from purple to cyan
        - Authors: 16px, centered, italic, indigo color
        - Section headers: 21px, bold, with gradient from purple to cyan
        - Text: Justified paragraphs with 18px bottom margin and appropriate color
        - Highlights: Dark background with padding for key findings
        - Links: Blue with hover effect
      
      4. Content Organization:

        - Structured sections with numbered headers
        - Lists for multiple points within sections
        - Highlight boxes for key findings
      
      Here's the CSS structure you can follow (note all selectors have -dynax suffix):

      -- It's not necessary it must have the same css styling but something similar.
      
      <style>
        .paper-container-dynax {{
          font-family: Arial, sans-serif;
          line-height: 1.6;
          margin: 20px;
          color:transparent;
        }}
        .paper-title-dynax {{
          font-size: 28px;
          font-weight: bold;
          text-align: center;
          margin-bottom: 10px;
          background-image: linear-gradient(to right, purple, cyan);
          -webkit-background-clip: text;
          background-clip: text;
          -webkit-text-fill-color: transparent;
        }}
        .paper-authors-dynax {{
          font-size: 16px;
          font-style: italic;
          color: white;
          text-align: center;
          margin-bottom: 20px;
        }}
        .section-header-dynax {{
          font-size: 21px;
          font-weight: bold;
          color: #512DA8;
          margin-top: 20px;
          margin-bottom: 10px;
          background-image: linear-gradient(to right, purple, cyan);
          -webkit-background-clip: text;
          background-clip: text;
          -webkit-text-fill-color: transparent;
        }}
        .paragraph-dynax {{
          text-align: justify;
          margin-bottom: 18px;
          color: white;
        }}
        .highlight-dynax {{
          background-color: rgb(12, 11, 11);
          padding: 10px;
          margin-bottom: 10px;
          color: white;
        }}
        .list-item-dynax {{
          margin-bottom: 10px;
        }}
        .margin-note-dynax {{
          font-size: 10pt;
          color: #7986CB;
          margin-left: 20px;
        }}
        .footnote-dynax {{
          font-size: 9pt;
          color: #9FA8DA;
        }}
        a-dynax {{
          color: #007bff;
          text-decoration: none;
        }}
        a-dynax:hover {{
          text-decoration: underline;
        }}
        .list-container-dynax {{
          margin-left: 20px;
          margin-bottom: 15px;
        }}
      </style>
      
      Sample structure you should follow:
      
      <div class="paper-container-dynax">
          <div class="paper-title-dynax">TITLE HERE</div>
          <div class="paper-authors-dynax">AUTHORS HERE</div>
          
          <div class="section-header-dynax">1. Executive Synthesis</div>
          <div class="paragraph-dynax">Content here...</div>
          
          <div class="section-header-dynax">2. Methodological Architecture</div>
          <div class="paragraph-dynax">Content here...</div>
          <div class="list-container-dynax">
            <div class="list-item-dynax">• Item one</div>
            <div class="list-item-dynax">• Item two with <span class="highlight-dynax">highlighted text</span></div>
          </div>
          
          <!-- And so on for all sections -->
      </div>

      Example == '
      <div class="paper-container-dynax">
          <style>
            .paper-container-dynax {{
              font-family: Arial, sans-serif;
              line-height: 1.6;
              margin: 20px;
              color: white;
            }}
            .paper-title-dynax {{
              font-size: 28px;
              font-weight: bold;
              text-align: center;
              margin-bottom: 10px;
              background-image: linear-gradient(to right, purple, cyan);
              -webkit-background-clip: text;
              background-clip: text;
              -webkit-text-fill-color: transparent;
            }}
            .paper-authors-dynax {{
              font-size: 16px;
              font-style: italic;
              color: white;
              text-align: center;
              margin-bottom: 20px;
            }}
            .section-header-dynax {{
              font-size: 21px;
              font-weight: bold;
              color: #512DA8;
              margin-top: 20px;
              margin-bottom: 10px;
              background-image: linear-gradient(to right, purple, cyan);
              -webkit-background-clip: text;
              background-clip: text;
              -webkit-text-fill-color: transparent;
            }}
            .paragraph-dynax {{
              text-align: justify;
              margin-bottom: 18px;
            }}
            .highlight-dynax {{
              background-color: rgb(12, 11, 11);
              padding: 10px;
              margin-bottom: 10px;
              color: white;
            }}
            .list-container-dynax {{
              margin-left: 20px;
              margin-bottom: 15px;
            }}
            .list-item-dynax {{
              margin-bottom: 10px;
            }}
            .margin-note-dynax {{
              font-size: 10pt;
              color: #7986CB;
              margin-left: 20px;
            }}
            .footnote-dynax {{
              font-size: 9pt;
              color: #9FA8DA;
            }}
            a-dynax {{
              color: #007bff;
              text-decoration: none;
            }}
            a-dynax:hover {{
              text-decoration: underline;
            }}
          </style>
        
        -- Sample HTML FORMAT.
        -- Not necessary it is exact but follow the structure.

          <div class="paper-title-dynax">Scalable Neural Architectures for Distributed Edge Intelligence</div>
          <div class="paper-authors-dynax">Alice Morgan, David Turing, Elias Kim, Fatima Rahman</div>

          <div class="section-header-dynax">1. Executive Summary</div>
          <div class="paragraph-dynax">
            In this research, we propose a scalable framework for the deployment and training of neural networks across
            distributed edge devices with limited computational resources. The motivation stems from the increasing demand for
            intelligent inference directly on devices such as smart cameras, drones, and embedded sensors, where latency, privacy,
            and energy constraints render cloud-based approaches suboptimal. Our system introduces a new paradigm called *Hierarchical
            Layered Distribution (HLD)* that allows different layers of a neural network to be assigned dynamically to different
            devices based on available compute power and real-time connectivity status. This model not only improves efficiency
            but also significantly reduces data movement and preserves privacy by localizing sensitive computations. We benchmarked
            our method on multiple datasets including ImageNet subsets and edge-specific benchmarks. The results demonstrate
            state-of-the-art trade-offs in speed, accuracy, and power consumption. Our findings have strong implications for the
            future of real-time AI inference at the network edge, especially in smart city and industrial IoT settings.
          </div>

          <div class="section-header-dynax">2. Methodological Architecture</div>
          <div class="paragraph-dynax">
            The architecture proposed in this paper combines three core methodologies: (1) Network disaggregation, (2) Edge resource profiling,
            and (3) Adaptive synchronization. Firstly, the neural models are disaggregated into atomic operations (such as conv, pool, dense)
            and profiled using a custom-developed latency estimator. This estimation considers not only FLOPs but also hardware-specific
            execution overheads derived from runtime measurements on real devices. Secondly, we built a lightweight profiler in Rust that
            runs on the edge device to capture GPU and CPU load, temperature, thermal throttling metrics, and memory usage. Based on this,
            a priority score is computed per device to influence task distribution. Finally, adaptive synchronization mechanisms were employed
            to ensure consistency of feature maps and gradients across a distributed device mesh. The system utilizes a gossip-based
            protocol for fault-tolerance and real-time topology adjustments. Together, these components create a resilient framework that
            handles intermittent connectivity and still achieves convergence comparable to centralized training. Experiments included
            a simulated smart street camera network and a fleet of autonomous quadcopters performing collaborative object detection.
          </div>
          <div class="list-container-dynax">
            <div class="list-item-dynax">• Network disaggregation enables intelligent placement of model layers</div>
            <div class="list-item-dynax">• On-device profilers adapt to compute constraints in real-time</div>
            <div class="list-item-dynax">• <span class="highlight-dynax">Dynamic edge distribution achieves 40% latency reduction</span></div>
            <div class="list-item-dynax">• Robust to connectivity loss via gossip-based synchronization</div>
          </div>

          <div class="section-header-dynax">3. Key Findings</div>
          <div class="highlight-dynax">
            Through rigorous testing across five edge clusters and synthetic topologies, our HLD framework reduced inference time
            by 40% on average compared to full-cloud inference. Additionally, training time was decreased by up to 27% in multi-device
            configurations without compromising on final model accuracy. One of the most surprising findings was that models trained
            in this hybrid-distributed way actually generalized better to new datasets, likely due to regularization effects
            introduced by the heterogeneous compute environments. The system maintained full operational integrity even when
            30% of nodes were randomly disconnected, showcasing its fault tolerance. Across all experiments, the HLD-enabled
            network outperformed standard federated learning pipelines in convergence speed, accuracy, and resilience.
          </div>

          <div class="section-header-dynax">4. Conclusions</div>
          <div class="paragraph-dynax">
            The implementation of scalable, distributed deep learning systems for edge intelligence represents a pivotal direction
            for the future of AI. Our research demonstrates the feasibility of real-time model partitioning and execution across
            heterogeneous nodes in a network, delivering efficient and private computation with minimal infrastructure. Future work
            includes deeper exploration into attention-based layer assignment, automated layer compression strategies, and integration
            with neural architecture search to produce models optimized for HLD distribution. Furthermore, we are exploring
            integration with blockchain-based consensus mechanisms to ensure integrity and trustworthiness in highly decentralized
            edge networks. Ultimately, we envision a future where every smart device becomes a contributor to a planetary-scale,
            intelligent mesh — a shift that will redefine AI infrastructure.
          </div>

          <div class="section-header-dynax">5. References</div>
          <div class="paragraph-dynax">
            For full source code and implementation details, visit our <a class="dynax" href="https://github.com/edge-ai/hld">GitHub repository</a>.
            Detailed logs and profiling scripts are also available for reproducibility. Some core techniques were inspired by
            recent work in multi-agent reinforcement learning and large-scale decentralized inference. Further reading includes
            [Smith et al., 2023], [Rahman & Liu, 2022], and edge computing frameworks outlined by the OpenFog Consortium.
          </div>
          <div class="footnote-dynax">Funding was provided by the Global Edge AI Alliance under grant number GEAA-2025-042.</div>
        </div>
        '
      
      CRITICAL REQUIREMENTS:
      1. DO NOT use HTML lists (ul/li) - instead use div with appropriate classes as shown above
      2. EVERY class and ID must end with -dynax suffix
      3. All content must be inside the single parent div
      4. Do not include any DOCTYPE declarations or HTML/HEAD tags
      5. Make sure all styling is contained within the style tags
      6. Use divs instead of paragraphs, headings, etc.
      7. Return complete, valid HTML that presents the academic content professionally
      8. Do not include code tags, backticks or HTML comments in your output
      9. Make sure the output is presentable and highly intuitive as it is to be read by researchers.
      """
    )
    
    # Initialize LLM
    llm = GoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2, google_api_key=google_api_key)
    
    # Generate PDF content
    pdf_chain = pdf_prompt | llm
    pdf_content = pdf_chain.invoke({{
        "title": title,
        "authors": authors,
        "full_text": full_text  
    }})
    
    # Generate HTML content based on PDF content
    html_chain = html_prompt | llm
    html_content = html_chain.invoke({{
        "title": title,
        "authors": authors,
        "pdf_content": pdf_content
    }})

    # Clean any potential code markers from the output
    content = html_content.replace("```html","").replace("```","")
    
    return content

if __name__ == '__main__':
    analysis = get_analysis(paper = {{
        'title': 'OSCAR: Online Soft Compression And Reranking', 
        'authors': ['Maxime Louis', 'Thibault Formal', 'Hervé Dejean', 'Stéphane Clinchant'], 
        'date': '17 Mar 2025', 
        'url': "https://arxiv.org/abs/2504.07109", 
        'doi': 'arXiv:2504.07109', 
        'pdf': "https://arxiv.org/pdf/2504.07109", 
        'abstract': 'Retrieval-Augmented Generation (RAG) enhances Large Language Models (LLMs)...',
        'field': ['Information Retrieval', 'Artificial Intelligence', 'Computation and Language']
    }})
    
    set_pdf(analysis,'arXiv:2504.07109')
    
    with open('output.html', 'w', encoding='utf-8') as f:
        f.write(analysis)
'''


"""
Advanced Research Paper Analysis System
- Creates detailed academic summaries with responsive design
- Integrates multiple AI models for depth and precision
- Generates book-like HTML with rich formatting and content connections
"""

import json
import os
from typing import Dict, List, Optional, Tuple, Any
import re
from datetime import datetime
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from .pdf_logic import get_content, set_pdf

# Load environment variables
load_dotenv()

class ResearchSection(BaseModel):
    """Schema for structured research paper sections"""
    title: str = Field(description="Section title")
    content: str = Field(description="Section content")
    key_points: List[str] = Field(description="Key points from this section")
    
class PaperAnalysis(BaseModel):
    """Schema for complete paper analysis output"""
    title: str = Field(description="Paper title")
    authors: str = Field(description="Paper authors")
    executive_summary: str = Field(description="High-level overview of key contributions")
    methodology: ResearchSection = Field(description="Research methodology")
    findings: ResearchSection = Field(description="Critical research findings")
    theoretical_framework: ResearchSection = Field(description="Theoretical connections")
    limitations: ResearchSection = Field(description="Research limitations")
    future_work: ResearchSection = Field(description="Future research directions")
    interdisciplinary_impact: ResearchSection = Field(description="Broader impact across fields")
    conclusion: ResearchSection = Field(description="Final assessment")
    related_papers: List[Dict[str, str]] = Field(description="Related research papers")
    key_concepts: List[str] = Field(description="Key concepts from the paper")

class ResearchAnalyzer:
    """Advanced system for analyzing research papers with multi-model approach"""
    
    def __init__(
        self, 
        google_api_key: Optional[str] = None,
        anthropic_api_key: Optional[str] = None,
        understanding_model: str = "gemini-2.0-flash",
        formatting_model: str = "claude-3-opus-20240229",
        temperature: float = 0.2
    ):
        """Initialize with API keys and model configuration"""
        self.google_api_key = google_api_key or os.environ.get('GOOGLE_API_KEY')
        self.anthropic_api_key = anthropic_api_key or os.environ.get('ANTHROPIC_API_KEY')
        
        # Initialize understanding model (for deep comprehension)
        self.understanding_llm = GoogleGenerativeAI(
            model=understanding_model, 
            temperature=temperature,
            google_api_key=self.google_api_key
        )
        
        # Initialize formatting model (for beautiful output)
        if self.anthropic_api_key:
            self.formatting_llm = GoogleGenerativeAI(
                model=formatting_model,
                temperature=temperature,
                anthropic_api_key=self.google_api_key
            )
        else:
            # Fallback to Google model if Anthropic not available
            self.formatting_llm = self.understanding_llm
            
        # Define output parser for structured analysis
        self.parser = PydanticOutputParser(pydantic_object=PaperAnalysis)
        
        # Setup prompts
        self._setup_prompts()
    
    def _setup_prompts(self):
        """Configure advanced prompts for paper analysis"""
        
        # Deep understanding prompt
        self.understanding_prompt = PromptTemplate(
            input_variables=["title", "authors", "full_text", "format_instructions"],
            template="""
            You are an expert academic research analyst specialized in creating detailed paper summaries.
            Analyze the following research paper thoroughly and extract structured information.
            
            PAPER METADATA:
            TITLE: {title}
            AUTHORS: {authors}
            
            FULL TEXT:
            {full_text}
            
            YOUR TASK:
            Create a comprehensive, scholarly analysis with depth and precision. Your analysis should:
            1. Identify the paper's core contributions, methodologies, and findings
            2. Analyze theoretical frameworks and connections to existing literature
            3. Evaluate limitations and methodological constraints
            4. Suggest future research directions and interdisciplinary applications
            5. Provide a scholarly assessment of the paper's significance
            6. Identify 5-10 related papers that would complement understanding of this research
            7. Extract 10-15 key concepts that define this research
            
            Your analysis should be highly detailed and academically rigorous.
            
            {format_instructions}
            """
        )
        
        # Add parser instructions to prompt
        self.understanding_chain = LLMChain(
            llm=self.understanding_llm,
            prompt=self.understanding_prompt.partial(format_instructions=self.parser.get_format_instructions())
        )
        
        # HTML formatting prompt
        self.html_prompt = PromptTemplate(
            input_variables=["title", "authors", "analysis", "date"],
            template="""
            You are an expert HTML designer for academic publishing platforms. Create a responsive, 
            visually compelling HTML document for the following research paper analysis.
            
            PAPER METADATA:
            TITLE: {title}
            AUTHORS: {authors}
            DATE: {date}
            
            ANALYSIS CONTENT:
            {analysis}
            
            OUTPUT INSTRUCTIONS:
            Create a responsive HTML document with these specifications:
            
            1. NAMESPACE REQUIREMENT: Every class and ID must end with "-dynax" suffix
            
            2. STRUCTURE:
               - Everything contained in a parent div with class="research-container-dynax"
               - Responsive design with media queries for mobile, tablet, and desktop
               - Proper heading hierarchy with semantic HTML5 elements
            
            3. STYLING FEATURES:
               - Modern, academic visual design with responsive typography
               - Color-coded sections with appropriate visual hierarchy
               - Gradient backgrounds for headers (purple to cyan)
               - Drop shadows and subtle animations for interactive elements
               - Card-based layout for sections with proper spacing
               - Responsive navigation menu that shows section headers
               - Highlight boxes for key findings with distinct styling
               - Citation styling for references
               - SVG icons for different section types
               - Interactive footnotes
            
            4. ADVANCED ELEMENTS:
               - Table of contents with smooth scroll to sections
               - Key concept tags with hover effects
               - Responsive image placeholders with captions where appropriate
               - Code snippet styling for technical papers
               - Block quotes for important quotations
               - Interactive reference section with hover details
               - Progress indicator showing reading position
               - Font size adjustment controls
            
            5. RESPONSIVENESS:
               - Mobile-first approach with progressive enhancement
               - Fluid typography scaling based on viewport
               - Collapsible sections for mobile viewing
               - Grid layout that adapts to screen size
               - Touch-friendly controls for mobile devices
            
            IMPORTANT STYLING REQUIREMENTS:
            - Use CSS variables for consistent theming
            - Include print stylesheet optimization
            - Avoid fixed pixel widths for responsive elements
            - Ensure high contrast for accessibility
            - Include dark mode toggle functionality
            - ALL class and ID names must end with "-dynax" suffix
            - Include appropriate ARIA attributes for accessibility
            
            SAMPLE STRUCTURE:
            ```html
            <div class="research-container-dynax">
                <style>
                    /* CSS variables for theming */
                    
                    
                    /* Dark mode theme */
                    .dark-mode-dynax {{
                        --text-color-dynax: #e0e0e0;
                        --background-color-dynax: #121212;
                        --highlight-color-dynax: #1f1f1f;
                    }}
                    
                    /* Base styles */
                    .research-container-dynax {{
                        font-family: var(--font-primary-dynax);
                        line-height: 1.6;
                        max-width: 1200px;
                        margin: 0 auto;
                        padding: 1rem;
                        color: var(--text-color-dynax);
                        background-color: var(--background-color-dynax);
                        transition: all 0.3s ease;
                    }}
                    
                    .paper-title-dynax {{
                        font-size: clamp(1.8rem, 5vw, 2.5rem);
                        font-weight: 800;
                        text-align: center;
                        margin-bottom: 1rem;
                        background-image: var(--gradient-dynax);
                        -webkit-background-clip: text;
                        background-clip: text;
                        -webkit-text-fill-color: transparent;
                        line-height: 1.2;
                    }}
                    
                    .paper-authors-dynax {{
                        font-size: clamp(1rem, 3vw, 1.2rem);
                        font-weight: 400;
                        text-align: center;
                        margin-bottom: 2rem;
                        color: var(--text-color-dynax);
                        opacity: 0.8;
                    }}
                    
                    .paper-date-dynax {{
                        font-size: 0.9rem;
                        text-align: center;
                        margin-bottom: 2rem;
                    }}
                    
                    .toc-container-dynax {{
                        background-color: var(--highlight-color-dynax);
                        border-radius: 8px;
                        padding: 1.5rem;
                        margin-bottom: 2rem;
                        box-shadow: var(--shadow-dynax);
                    }}
                    
                    .toc-title-dynax {{
                        font-size: 1.3rem;
                        font-weight: 700;
                        margin-bottom: 1rem;
                        color: var(--primary-color-dynax);
                    }}
                    
                    .toc-link-dynax {{
                        display: block;
                        padding: 0.5rem 0;
                        color: var(--text-color-dynax);
                        text-decoration: none;
                        transition: transform 0.2s;
                        border-left: 3px solid transparent;
                        padding-left: 1rem;
                    }}
                    
                    .toc-link-dynax:hover {{
                        transform: translateX(5px);
                        border-left: 3px solid var(--secondary-color-dynax);
                    }}
                    
                    .section-card-dynax {{
                        background-color: var(--background-color-dynax);
                        border-radius: 8px;
                        box-shadow: var(--shadow-dynax);
                        padding: 2rem;
                        margin-bottom: 2rem;
                        transition: transform 0.3s ease;
                    }}
                    
                  .section-card-dynax:hover {{
                        transform: translateY(-5px);
                    }}
                    
                    .section-header-dynax {{
                        font-size: clamp(1.3rem, 4vw, 1.8rem);
                        font-weight: 700;
                        margin-bottom: 1.5rem;
                        background-image: var(--gradient-dynax);
                        -webkit-background-clip: text;
                        background-clip: text;
                        -webkit-text-fill-color: transparent;
                        display: flex;
                        align-items: center;
                        gap: 0.5rem;
                    }}
                    
                    .section-icon-dynax {{
                        width: 1.5rem;
                        height: 1.5rem;
                        fill: var(--primary-color-dynax);
                    }}
                    
                    .paragraph-dynax {{
                        font-family: var(--font-secondary-dynax);
                        text-align: justify;
                        margin-bottom: 1.5rem;
                        font-size: clamp(1rem, 2vw, 1.1rem);
                    }}
                    
                    .highlight-box-dynax {{
                        background-color: var(--highlight-color-dynax);
                        border-left: 4px solid var(--secondary-color-dynax);
                        padding: 1.5rem;
                        margin: 1.5rem 0;
                        border-radius: 0 8px 8px 0;
                    }}
                    
                    .key-points-container-dynax {{
                        display: grid;
                        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
                        gap: 1rem;
                        margin: 1.5rem 0;
                    }}
                    
                    .key-point-dynax {{
                        background-color: var(--highlight-color-dynax);
                        padding: 1rem;
                        border-radius: 8px;
                        border-left: 3px solid var(--primary-color-dynax);
                    }}
                    
                    .concepts-container-dynax {{
                        display: flex;
                        flex-wrap: wrap;
                        gap: 0.5rem;
                        margin: 1.5rem 0;
                    }}
                    
                    .concept-tag-dynax {{
                        background-image: var(--gradient-dynax);
                        color: white;
                        padding: 0.5rem 1rem;
                        border-radius: 20px;
                        font-size: 0.9rem;
                        transition: transform 0.2s;
                    }}
                    
                    .concept-tag-dynax:hover {{
                        transform: scale(1.05);
                    }}
                    
                    .reference-dynax {{
                        font-size: 0.9rem;
                        margin-bottom: 0.5rem;
                        padding-left: 1.5rem;
                        text-indent: -1.5rem;
                    }}
                    
                    .code-block-dynax {{
                        background-color: #1e1e1e;
                        color: #d4d4d4;
                        padding: 1rem;
                        border-radius: 8px;
                        overflow-x: auto;
                        font-family: 'Consolas', monospace;
                        margin: 1.5rem 0;
                    }}
                    
                    .blockquote-dynax {{
                        border-left: 4px solid var(--primary-color-dynax);
                        padding-left: 1.5rem;
                        font-style: italic;
                        margin: 1.5rem 0;
                        color: var(--text-color-dynax);
                        opacity: 0.8;
                    }}
                    
                    .figure-dynax {{
                        margin: 2rem 0;
                        text-align: center;
                    }}
                    
                    .figure-img-dynax {{
                        max-width: 100%;
                        height: auto;
                        border-radius: 8px;
                        box-shadow: var(--shadow-dynax);
                    }}
                    
                    .figure-caption-dynax {{
                        font-size: 0.9rem;
                        opacity: 0.8;
                        margin-top: 0.5rem;
                        text-align: center;
                    }}
                    
                    .controls-dynax {{
                        position: fixed;
                        bottom: 2rem;
                        right: 2rem;
                        display: flex;
                        flex-direction: column;
                        gap: 0.5rem;
                        z-index: 100;
                    }}
                    
                    .theme-toggle-dynax, .font-size-dynax {{
                        width: 2.5rem;
                        height: 2.5rem;
                        border-radius: 50%;
                        background: var(--gradient-dynax);
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        color: white;
                        border: none;
                        cursor: pointer;
                        box-shadow: var(--shadow-dynax);
                    }}
                    
                    /* Responsive styles */
                    @media (max-width: 768px) {{
                        .section-card-dynax {{
                            padding: 1.5rem;
                        }}
                        
                        .key-points-container-dynax {{
                            grid-template-columns: 1fr;
                        }}
                        
                        .controls-dynax {{
                            bottom: 1rem;
                            right: 1rem;
                        }}
                    }}
                    
                    /* Print styles */
                    @media print {{
                        .research-container-dynax {{
                            max-width: 100%;
                            padding: 0;
                            box-shadow: none;
                        }}
                        
                        .section-card-dynax {{
                            box-shadow: none;
                            break-inside: avoid;
                        }}
                        
                        .controls-dynax {{
                            display: none;
                        }}
                    }}
                </style>
                
                <!-- Dark mode & font size control script -->
                <script>
                    document.addEventListener('DOMContentLoaded', () => {{
                        const container = document.querySelector('.research-container-dynax');
                        const themeBtn = document.querySelector('.theme-toggle-dynax');
                        const fontSizeBtn = document.querySelector('.font-size-dynax');
                        let fontSize = 100;
                        
                        // Theme toggle
                        themeBtn.addEventListener('click', () => {{
                            container.classList.toggle('dark-mode-dynax');
                        }});
                        
                        // Font size toggle
                        fontSizeBtn.addEventListener('click', () => {{
                            fontSize = fontSize === 100 ? 120 : fontSize === 120 ? 80 : 100;
                            container.style.fontSize = `${{fontSize}}%`;
                        }});
                        
                        // Smooth scroll for TOC links
                        document.querySelectorAll('.toc-link-dynax').forEach(link => {{
                            link.addEventListener('click', e => {{
                                e.preventDefault();
                                const targetId = link.getAttribute('href').substring(1);
                                const targetElement = document.getElementById(targetId);
                                window.scrollTo({{
                                    top: targetElement.offsetTop,
                                    behavior: 'smooth'
                                }});
                            }});
                        }});
                    }});
                </script>
                
                <div class="paper-title-dynax">TITLE HERE</div>
                <div class="paper-authors-dynax">AUTHORS HERE</div>
                <div class="paper-date-dynax">DATE HERE</div>
                
                <!-- Table of Contents -->
                <div class="toc-container-dynax">
                    <div class="toc-title-dynax">Table of Contents</div>
                    <a href="#section1" class="toc-link-dynax">1. Executive Summary</a>
                    <a href="#section2" class="toc-link-dynax">2. Methodology</a>
                    <!-- Additional TOC links -->
                </div>
                
                <!-- Example section card -->
                <div id="section1" class="section-card-dynax">
                    <div class="section-header-dynax">
                        <svg class="section-icon-dynax" viewBox="0 0 24 24">
                            <path d="M12 2L2 7v10l10 5 10-5V7z"></path>
                        </svg>
                        1. Executive Summary
                    </div>
                    <div class="paragraph-dynax">Content here...</div>
                    
                    <div class="highlight-box-dynax">
                        Key finding highlighted here...
                    </div>
                    
                    <div class="key-points-container-dynax">
                        <div class="key-point-dynax">Key point one</div>
                        <div class="key-point-dynax">Key point two</div>
                    </div>
                </div>
                
                <!-- Additional sections... -->
                
                <!-- Controls -->
                <div class="controls-dynax">
                    <button class="theme-toggle-dynax" aria-label="Toggle dark mode">🌓</button>
                    <button class="font-size-dynax" aria-label="Change font size">Aa</button>
                </div>
            </div>
            ```
            
            IMPORTANT FINAL REQUIREMENTS:
            1. Return complete, valid HTML with all script functionality inline
            2. Every class name and ID must end with "-dynax" suffix
            3. Output must be responsive from mobile to large desktop screens
            4. Include proper semantic HTML structure
            5. Include all interactive elements mentioned above
            6. Generate appropriate SVG icons for each section
            7. Include appropriate ARIA attributes for accessibility
            """
        )
        
        # Create HTML chain
        self.html_chain = LLMChain(
            llm=self.formatting_llm,
            prompt=self.html_prompt
        )
    
    def _clean_text(self, text: str) -> str:
        """Clean text removing code markers and other artifacts"""
        return text.replace("```html", "").replace("```", "").strip()
    
    def _extract_related_resources(self, text: str, paper_title: str) -> Dict[str, List[Dict[str, str]]]:
        """Extract related papers and resources from text"""
        # This would ideally use the LLM to parse related papers
        # For now using a simple pattern-based extraction
        resources = {
            "papers": [],
            "repositories": [],
            "datasets": []
        }
        
        # Simple extraction logic (could be enhanced with LLM)
        paper_pattern = re.compile(r'\[([^\]]+)\s*,\s*(\d{{4}})\]')
        matches = paper_pattern.findall(text)
        
        for authors, year in matches:
            resources["papers"].append({
                "title": f"Research by {authors}",
                "authors": authors,
                "year": year,
                "relation": f"Related to {paper_title}"
            })
            
        return resources
    
    def analyze_paper(self, paper: Dict[str, str]) -> str:
        """
        Perform comprehensive analysis of research paper
        
        Args:
            paper: Dictionary with keys:
                - title: Paper title
                - authors: Paper authors
                - date: Publication date
                - url: Paper URL
                - doi: Paper DOI
                - pdf: PDF URL
                - abstract: Paper abstract
                - field: List of research fields
                
        Returns:
            HTML content as string
        """
        title = paper.get('title', '')
        authors = paper.get('authors', [])
        authors_str = ', '.join(authors) if isinstance(authors, list) else authors
        date = paper.get('date', datetime.now().strftime('%d %b %Y'))
        
        # Get full text from PDF
        try:
            full_text = full_text = get_content(paper['pdf'].replace("'", ""))
            print(f"Successfully extracted {len(full_text)} characters from PDF")
        except Exception as e:
            print(f"Error extracting PDF content: {{e}}")
            full_text = paper.get('abstract', '')
            if isinstance(paper.get('field', []), list):
                full_text += "\n\nFields: " + ", ".join(paper['field'])
        
        # Step 1: Generate structured paper analysis
        try:
            understanding_result = self.understanding_chain.run(
                title=title,
                authors=authors_str,
                full_text=full_text
            )
            
            # Parse structured output
            analysis_data = self.parser.parse(understanding_result)
            print(f"Successfully parsed structured analysis with {len(analysis_data.key_concepts)} key concepts")
            
        except Exception as e:
            print(f"Error in paper understanding: {e}")
            # Fallback to simple text format if parsing fails
            analysis_data = {
                "title": title,
                "authors": authors_str,
                "executive_summary": paper.get('abstract', ''),
                "key_concepts": paper.get('field', []) if isinstance(paper.get('field', []), list) else []
            }
        
        # Step 2: Generate HTML format
        try:
            # Convert analysis to formatted HTML
            html_result = self.html_chain.run(
                title=title,
                authors=authors_str,
                analysis=str(analysis_data),
                date=date
            )
            
            # Clean HTML output
            html_content = self._clean_text(html_result)
            print(f"Successfully generated HTML with {len(html_content)} characters")
            
        except Exception as e:
            print(f"Error in HTML formatting: {{e}}")
            # Fallback to basic HTML
            html_content = f"""
            <div class="research-container-dynax">
                <div class="paper-title-dynax">{{title}}</div>
                <div class="paper-authors-dynax">{{authors_str}}</div>
                <div class="section-header-dynax">Abstract</div>
                <div class="paragraph-dynax">{{paper.get('abstract', '')}}</div>
            </div>
            """
        
        return html_content

def get_analysis(paper: Dict[str, str], google_api_key: Optional[str] = None) -> str:
    """
    Enhanced interface function for analyzing research papers.
    
    Args:
        paper: Dictionary with paper metadata
        google_api_key: Optional Google API key
        
    Returns:
        HTML content as string
    """
    # Initialize analyzer with provided or environment API keys
    analyzer = ResearchAnalyzer(google_api_key=google_api_key)
    
    # Generate analysis
    try:
        html_content = analyzer.analyze_paper(paper)
        return html_content
    except Exception as e:
        print(f"Error during analysis: {{e}}")
        # Fallback minimal HTML
        return f"""
        <div class="research-container-dynax">
            <style>
                .research-container-dynax {{
                    font-family: 'Arial', sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .paper-title-dynax {{
                    font-size: 24px;
                    font-weight: bold;
                    color: #6200ea;
                    margin-bottom: 10px;
                }}
                .paper-authors-dynax {{
                    font-size: 16px;
                    margin-bottom: 20px;
                }}
                .paper-abstract-dynax {{
                    line-height: 1.6;
                }}
                .error-message-dynax {{
                    color: #d32f2f;
                    font-style: italic;
                }}
            </style>
            <div class="paper-title-dynax">{{paper.get('title', 'Untitled Paper')}}</div>
            <div class="paper-authors-dynax">{{', '.join(paper.get('authors', [])) if isinstance(paper.get('authors', []), list) else paper.get('authors', 'Unknown')}}</div>
            <div class="paper-abstract-dynax">{{paper.get('abstract', '')}}</div>
            <p class="error-message-dynax">Note: An error occurred during advanced analysis. Displaying basic information only.</p>
        </div>
        """

if __name__ == '__main__':
    analysis = get_analysis(paper = {
        'title': 'OSCAR: Online Soft Compression And Reranking', 
        'authors': ['Maxime Louis', 'Thibault Formal', 'Hervé Dejean', 'Stéphane Clinchant'], 
        'date': '17 Mar 2025', 
        'url': "https://arxiv.org/abs/2504.07109", 
        'doi': 'arXiv:2504.07109', 
        'pdf': "https://arxiv.org/pdf/2504.07109", 
        'abstract': 'Retrieval-Augmented Generation (RAG) enhances Large Language Models (LLMs)...',
        'field': ['Information Retrieval', 'Artificial Intelligence', 'Computation and Language']
    })
    
    set_pdf(analysis, 'arXiv:2504.07109')
    
    with open('output.html', 'w', encoding='utf-8') as f:
        f.write(analysis)