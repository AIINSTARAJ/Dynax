import json
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
    
    # Prompt for PDF version (kept simple and focused on content)
    pdf_prompt = PromptTemplate(
        input_variables=["title", "authors", "full_text"],
        template="""
        You are an expert academic research analyst and summarizer. Create a comprehensive summary of the following research paper.
        
        INPUT:
        PAPER_TITLE: {title}
        AUTHORS: {authors}
        FULL_TEXT: {full_text}
        
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

        -- Each Sections shouldn't be less than 2500 words
        
        Focus on clarity and accuracy in your summary. Use academic language but avoid unnecessary jargon. Not less than 10000 words.
        """
    )
    
    html_prompt = PromptTemplate(
        input_variables=["title", "authors", "pdf_content"],
        template="""
      You are an expert HTML formatter for academic content. Convert the following research summary into a well-styled HTML document that's fully compatible with an existing application styling system. The HTML must use a special namespace suffix for all classes and IDs to prevent styling conflicts.
      
      PAPER_TITLE: {title}
      AUTHORS: {authors}
      SUMMARY_CONTENT: {pdf_content}
      
      OUTPUT INSTRUCTIONS:
      Create an HTML document with the following specifications:
      
      1. MOST IMPORTANT: Every single class name and ID must end with "-dynax" suffix to prevent styling conflicts
      2. Structure:
        - Everything must be contained within a single parent div with class="paper-container-dynax"
        - Proper HTML structure with proper nesting
        - No styling in the head section - all styling must be within style tags in the body
      
      3. Styling:
        - All CSS class and ID selectors must include the "-dynax" suffix (e.g., .highlight-dynax, #title-dynax)
        - Font: Arial or sans-serif for body text, size 16px, line height 1.6
        - Title: 28px, centered, bold, with gradient from purple to cyan
        - Authors: 16px, centered, italic, indigo color
        - Section headers: 21px, bold, with gradient from purple to cyan
        - Text: Justified paragraphs with 18px bottom margin and appropriate color
        - Highlights: Dark background with padding for key findings
        - Links: Blue with hover underline effect
      
      4. Content Organization:
        - Structured sections with numbered headers
        - Lists for multiple points within sections
        - Highlight boxes for key findings
      
      Here's the CSS structure you MUST follow (note all selectors have -dynax suffix):
      
      <style>
        .paper-container-dynax {{
          font-family: Arial, sans-serif;
          line-height: 1.6;
          margin: 20px;
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
              color: #333;
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
              color: #303F9F;
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
      """
    )

      
    
    # Initialize LLM
    llm = GoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2, google_api_key=google_api_key)
    
    # Generate PDF content
    pdf_chain = pdf_prompt | llm
    pdf_content = pdf_chain.invoke({
        "title": title,
        "authors": authors,
        "full_text": full_text  
    })
    
    # Generate HTML content based on PDF content
    html_chain = html_prompt | llm
    html_content = html_chain.invoke({
        "title": title,
        "authors": authors,
        "pdf_content": pdf_content
    })

    # Clean any potential code markers from the output
    content = html_content.replace("```html","").replace("```","")
    
    return content

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
    
    set_pdf(analysis,'arXiv:2504.07109')
    
    with open('html_output.html', 'w', encoding='utf-8') as f:
        f.write(analysis)