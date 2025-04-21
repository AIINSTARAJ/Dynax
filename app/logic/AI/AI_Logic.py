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
      You are an expert HTML formatter for academic content. Convert the following research summary into a well-styled HTML document and optimize it for different screens through responsive design.
      
      PAPER_TITLE: {title}
      AUTHORS: {authors}
      SUMMARY_CONTENT: {pdf_content}
      
      OUTPUT INSTRUCTIONS:
      Create an HTML document with the following specifications:
      
      1. Structure:
        - DOCTYPE declaration and proper HTML structure
        - Head section with title and styling
        - Body containing the formatted content
      
      2. Styling:
        - Font: Arial or sans-serif for body text, size 16px, line height 1.6
        - Title: 28px, centered, bold, with gradient from purple to cyan
        - Authors: 16px, centered, italic, indigo color
        - Section headers: 21px, bold, with gradient from purple to cyan
        - Text: Justified paragraphs with 18px bottom margin and white color.
        - Highlights: Dark background with padding for key findings
        - Links: Blue with hover underline effect
      
      3. Content Organization:
        - Structured sections with numbered headers
        - Lists for multiple points within sections
        - Highlight boxes for key findings
      
      Use the following Sample design as guide:
      
      <!DOCTYPE html>
      <html>
              <head>
              <title>How Humans Evaluate AI Systems for Person Detection in Automatic Train Operation: Not All Misses Are Alike</title>
              <style>
              body {{
                  font-family: Arial, sans-serif;
                  line-height: 1.6;
                  margin: 20px;
              }}
              h1 {{
                  font-size: 24px;
                  font-weight: bold;
                  color: #1A237E;
                  margin-bottom: 10px;
              }}
              h2 {{
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
              p {{
                  text-align: justify;
                  margin-bottom: 18px;
              }}
              .highlight {{
                  background-color: rgb(12, 11, 11);
                  padding: 10px;
                  margin-bottom: 10px;
              }}
              .margin-note {{
                  font-size: 10pt;
                  color: #7986CB;
                  margin-left: 20px;
              }}
              .footnote {{
                  font-size: 9pt;
                  color: #9FA8DA;
              }}
              a {{
                  color: #007bff;
                  text-decoration: none;
              }}
              a:hover {{
                  text-decoration: underline;
              }}
              </style>
              </head>
              <body>
                  
              <br> 
              
              <div style="font-size:28px; text-align:center; font-weight:bold; background-image: linear-gradient(to right, purple, cyan); background-clip: text; -webkit-background-clip: text; -webkit-text-fill-color: transparent;">How Humans Evaluate AI Systems for Person Detection in Automatic Train Operation: Not All Misses Are Alike</div>
              <br>
              <div style="font-size:16px; font-style:italic; color:#303F9F; text-align:center; margin-bottom:20px;">Romy Müller</div>
      
              <h2>1. Executive Synthesis</h2>
              <p>This research paper delves into the cognitive mechanisms driving human assessments of AI person-detection systems within the context of automated train operation (ATO).  Employing a rigorous three-experiment design, the study unveils a complex interplay of factors shaping human judgment, challenging the assumption that evaluations solely reflect the AI's objective performance.  The most striking finding is the disproportionate emphasis placed on the position of missed individuals relative to the train tracks, even when participants were explicitly informed that the AI lacked the capacity to assess risk based on position. This highlights a significant discrepancy between AI capabilities and human expectations, with profound implications for the design and auditing of safety-critical AI systems.  The study also explores the differential impact of misses and false alarms, the influence of the number of affected images and people, and the effect of the evaluation method (image-wise vs. sequence-wise).  The findings consistently demonstrate that human evaluations are not purely objective measures of AI accuracy but are significantly influenced by a range of cognitive biases and contextual factors.  The research concludes with a discussion of limitations and proposes avenues for future research, emphasizing the need for more sophisticated evaluation methodologies that account for the inherent complexities of human judgment in safety-critical AI applications.  The study's implications extend far beyond the specific domain of ATO, offering valuable insights into the broader challenges of human-AI interaction in high-stakes environments.</p>
      
              <h2>2. Methodological Architecture</h2>
              <p>The study utilizes a robust experimental design encompassing three experiments, each building upon the preceding one.  The core methodology involves presenting participants with image sequences depicting individuals near railway tracks. A simulated AI, represented by highlighted regions within the images, indicates its person-detection results, including both misses and false alarms. Participants rate the AI's performance numerically and provide verbal justifications.  The experiments systematically manipulate several key factors:</p>
                <ul>
                  <li>AI Accuracy: Perfect detection, plausible misses (hard-to-detect people), implausible misses (easily detectable people), and false alarms.</li>
                  <li>Number of Affected Images: Varying the frequency of misses and false alarms.</li>
                  <li>Number of People: The total number of people present in each sequence.</li>
                  <li>Position Relative to Tracks: The proximity of missed or falsely detected objects to the tracks.</li>
                  <li>Elicitation Method: Image-wise vs. sequence-wise ratings.</li>
                </ul>
                <p>Data analysis employs ANOVAs to assess the statistical significance of these factors and their interactions, supplemented by qualitative content analysis of participants' verbal explanations.  The use of hand-crafted AI results ensures high experimental control, enabling precise manipulation and isolation of the variables.  The study's transparency is further enhanced by making all data and materials accessible through the Open Science Framework.  The rigorous methodology employed ensures the reliability and validity of the findings, strengthening the study's contribution to the field.</p>
      
                <h2>3. Critical Findings Hierarchy</h2>
                <p>The study yields several key findings:</p>
                <ul>
                  <li><div class="highlight"><strong>Key Finding 1:</strong> Position Dominates: The most significant finding is the overwhelming influence of the position of missed persons relative to the tracks.  Even when explicitly instructed otherwise, participants heavily penalized the AI for missing people near the tracks, regardless of detection difficulty.  This suggests a strong bias towards risk assessment, overriding the stated task of evaluating only person detection accuracy.</div></li>
                  <li><div class="highlight"><strong>Key Finding 2:</strong> Misses vs. False Alarms: Misses were generally rated more negatively than false alarms, particularly when the missed persons were in dangerous positions.  However, this difference diminished when considering only objects outside the train's immediate path.</div></li>
                  <li><div class="highlight"><strong>Key Finding 3:</strong> Frequency Matters: The number of affected images significantly impacted ratings, with a sharp decrease in ratings when misses occurred in more than two images.  However, beyond two images, the number of affected images had a less pronounced effect.</div></li>
                  <li><div class="highlight"><strong>Key Finding 4:</strong> Number of People: The number of people present in a sequence had a complex effect. While ratings generally improved with more people, a surprising drop in ratings occurred for very large groups (eight or more).</div></li>
                  <li><div class="highlight"><strong>Key Finding 5:</strong> Elicitation Method: Sequence-wise ratings were consistently lower than the average of image-wise ratings, indicating a greater sensitivity to individual errors when evaluating the entire sequence.</div></li>
                </ul>
                <p>These findings collectively paint a nuanced picture of how humans evaluate AI performance, highlighting the significant role of cognitive biases and contextual factors.</p>
      
              <h2>4. Theoretical Framework Integration</h2>
              <p>The study integrates several theoretical frameworks to interpret its findings:</p>
              <ul>
                <li><strong>Cognitive Anthropomorphism:</strong> The tendency to attribute human-like perception and reasoning to AI systems. This is evident in the observed plausibility effects, where participants' evaluations were influenced by their own perceived difficulty in detecting the objects.</li>
                <li><strong>Risk Perception:</strong> The study highlights the significant role of risk perception in shaping human evaluations. Participants' judgments were heavily influenced by the perceived danger associated with the AI's misses, even when this was irrelevant to the AI's actual task.</li>
                <li><strong>Heuristics and Biases:</strong> The findings demonstrate the influence of cognitive heuristics and biases, such as the availability heuristic (overemphasis on salient information) and anchoring bias (reliance on initial impressions).</li>
                <li><strong>Human-Machine Interaction (HMI):</strong> The study contributes to the understanding of HMI in safety-critical systems, emphasizing the importance of aligning AI capabilities with human expectations and designing evaluation methods that account for cognitive limitations.</li>
              </ul>
              <p>By drawing upon these frameworks, the study provides a comprehensive analysis of the complex interplay of factors influencing human evaluations of AI performance.</p>
      
      
              <h2>5. Limitations & Epistemological Boundaries</h2>
              <p>Several limitations constrain the generalizability of the findings:</p>
              <ul>
                <li>Limited Stimulus Set: The relatively small number of image sequences and potential confounding variables limit the generalizability of the findings.</li>
                <li>Simulated AI: The use of simulated AI data, while providing experimental control, may not fully reflect the complexities of real-world AI systems.</li>
                <li>Lay Participants: The study used lay participants, and the results may differ for experts in AI or railway operations.</li>
                <li>Binary Classification: The binary nature of the AI's person detection (detected/not detected) limits the exploration of the impact of AI confidence levels or uncertainty.</li>
                <li>Highlighting Method: The simplicity of the highlighting method may not capture the nuances of real-world AI output visualizations.</li>                  </ul>
              <p>These limitations highlight the need for future research to address these issues and further refine our understanding of human-AI interaction in safety-critical contexts.</p>
      
      
              <h2>6. Future Research Trajectories</h2>
              <p>Several avenues for future research emerge from this study:</p>
              <ul>
                <li>Larger, Balanced Datasets: Future research should utilize larger, more balanced datasets to address the limitations of the current stimulus set.  The use of synthetic data generated through simulations could be a valuable approach.</li>
                <li>Real-World AI Outputs: Incorporating real-world AI outputs and explainable AI (XAI) techniques could enhance the ecological validity of the study.</li>
                <li>Expert Evaluations: Comparing evaluations from lay participants with those of experts in AI and railway operations would provide valuable insights into the influence of expertise.</li>
                <li>Uncertainty and Confidence: Investigating the impact of AI uncertainty and confidence levels on human evaluations is crucial.</li>
                <li>Highlighting Variations: Exploring the effects of different highlighting methods and levels of detail could reveal further insights into the interaction between AI output and human perception.</li>
              </ul>
              <p>These future research directions will contribute to a more comprehensive understanding of human-AI interaction and inform the development of more robust and reliable AI systems.</p>
      
      
              <h2>7. Interdisciplinary Implications</h2>
              <p>This research has significant implications for several disciplines:</p>
              <ul>
                <li>Human Factors and Ergonomics: The findings highlight the importance of considering human cognitive biases and limitations in the design and evaluation of AI systems, particularly in safety-critical domains.</li>
                <li>Artificial Intelligence: The study underscores the need for developing AI systems that are not only accurate but also align with human expectations and are easily interpretable.</li>
                <li>Safety Engineering: The research provides valuable insights into the challenges of evaluating AI safety and the need for more sophisticated evaluation methodologies.</li>
                <li>Cognitive Science: The study contributes to the understanding of how humans perceive and evaluate AI, shedding light on the cognitive mechanisms at play.</li>
              </ul>
              <p>Ultimately, the study's findings have broad relevance to the design, evaluation, and deployment of AI systems across a range of safety-critical industries.</p>
      
              </body>
              </html>

              Return a complete, and remove things like ('''html in the begining and ''' in the end) valid HTML document that presents the academic content professionally.
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