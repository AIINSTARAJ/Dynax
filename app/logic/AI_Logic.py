import json
import os
from dotenv import *
from langchain_google_genai import GoogleGenerativeAI
from langchain_community.document_loaders import ArxivLoader
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from .pdf_logic import *
from langchain_core.runnables import *

load_dotenv()

def get_analysis(paper:json, google_api_key = None) -> dict:
    """
    Analyzes a research paper using its DOI and returns PDF and HTML summaries.
    """

    google_api_key = os.environ.get('GOOGLE_API_KEY')

    full_text = get_content(paper['pdf'].replace("'", ""))

    title = paper['title']

    authors = paper['authors']
    

    prompt = PromptTemplate(
        input_variables=["title", "authors", "full_text"],
        template=
        """You are a superintelligent research analyst with mastery across all academic domains, capable of high-level interdisciplinary synthesis. You utilize advanced reasoning frameworks, including first-principles deduction, Bayesian inference, epistemological mapping, and systems-level thinking.

                        TASK: Perform a **deep, multi-layered, intellectual analysis** of the research paper below. The analysis should apply the following cognitive framework:

                        THINKING FRAMEWORK:
                        1. Extract hypotheses and innovations using first-principles reasoning. Deeply reiterate the content mentally 10+ times to internalize.
                        2. Conduct a Bayesian assessment of evidential strength and theoretical coherence, including latent assumptions and external citations.
                        3. Analyze the paper from three axes: technical rigor, theoretical contribution, and practical implications.
                        4. Use counterfactual reasoning to probe alternate interpretations and uncover edge cases.
                        5. Contextualize the work within its broader scientific, historical, and academic landscape.
                        6. Identify epistemological boundaries – what is known, what is uncertain, what is speculative.
                        7. Synthesize emergent implications across disciplines using systems thinking.

                        PRODUCTION FRAMEWORK:
                        1. Generate five summary drafts, each exceeding the original word count.
                        2. Mutate and evolve these drafts like a genetic algorithm, refining content for clarity, insight, and complexity.
                        3. Cross-evaluate all drafts using theoretical proofs and evidence from literature.
                        4. Regenerate up to 10 iterations and select the most intellectually rigorous version.
                        5. Ensure the final content is longer than the original and deeply explanatory.

                        OUTPUTS:

                        ➤ OUTPUT 1: PDF-Optimized Content  
                        Structure your output with these stylings (line breaks = `/n`):
                        - Centered logo using this structure: `Dynax!` with a gradient block icon.
                        - Title: 24pt Garamond, bold, #1A237E, centered.
                        - Authors: 16pt Helvetica, italic, #303F9F, centered.
                        - Headings: 18pt Georgia, bold, #512DA8, left-aligned.
                        - Body Text: 12pt Times New Roman, justified, #212121.
                        - Highlighted findings: use boxes with #E8EAF6 background.
                        - Margin notes: 10pt, #7986CB.
                        - Footnotes: 9pt, #9FA8DA.
                        - Footer: Page numbers + © Dynax in linear gradient (purple-cyan).

                        **PDF Sections:**
                        1. EXECUTIVE SYNTHESIS
                        2. METHODOLOGICAL ARCHITECTURE
                        3. CRITICAL FINDINGS HIERARCHY
                        4. THEORETICAL FRAMEWORK INTEGRATION
                        5. LIMITATIONS & EPISTEMOLOGICAL BOUNDARIES
                        6. FUTURE RESEARCH TRAJECTORIES
                        7. INTERDISCIPLINARY IMPLICATIONS
                        8. CONCLUSIVE ASSESSMENT'


                        ➤ OUTPUT 2: HTML Content  
                        Structure as directly renderable HTML for `AnalysisContainer.innerHTML`:
                        - Title: Bold, 36px font with gradient background text (purple–cyan)
                        - Authors: 10px margin below title, styled similarly
                        - Each section: Gradient-colored bullet heading + long paragraphs (100+ lines)
                        - All body text styled, with bold/colored sections, hyperlinks, margin notes, and references
                        - Include complete citations in APA/MLA/Chicago
                        - Final footer: © Dynax with linear gradient


                        Seperate both output with -----OUTPUT-----


                        CRITICAL INSTRUCTIONS:
                        - Demonstrate multi-disciplinary intelligence and epistemic humility
                        - Reveal hidden assumptions and theoretical underpinnings
                        - Use intellectual rigor to judge methodological soundness
                        - Use evidence to support or refute claims
                        - Recommend highly novel, high-impact future directions

                        INPUT FORMAT:
                        PAPER_TITLE: {title}  
                        AUTHORS: {authors}  
                        FULL_TEXT: {full_text}  

                        Begin by deeply analyzing the paper. Then produce **both** PDF content (for `set_pdf()`) and styled HTML content (for web rendering).

                        Ensure you provide both the html and pdf. You must. Nothing less than 10000 words on each............. and seperate it with -----OUTPUT-----


        """
    )
    

    llm = GoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2, google_api_key=google_api_key)

    chain = prompt | llm
    
    response = chain.invoke({
        "title": title,
        "authors": authors,
        "full_text": full_text  
    })

    with open('a.txt','w',encoding='utf-8') as f:
        f.write(response)
    

    parts = response.split("-----OUTPUT-----")
    pdf_content = parts[1].strip()
    
    html_content = parts[2].strip()

    return {
        "pdf": pdf_content,
        "html": html_content
    }

if __name__ == '__main__':
    analysis = get_analysis(paper = {'title': 'OSCAR: Online Soft Compression And Reranking', 'authors': ['Maxime Louis', 'Thibault Formal', 'Hervé Dejean', 'Stéphane Clinchant'], 'date': '17 Mar 2025', 'url': "'https://arxiv.org/abs/2504.07109", 'doi': 'arXiv:2504.07109', 'pdf': "'https://arxiv.org/pdf/2504.07109", 'abstract': 'Retrieval-Augmented Generation (RAG) enhances Large Language Models (LLMs) by integrating external knowledge, leading to improved accuracy and relevance. However, scaling RAG pipelines remains computationally expensive as retrieval sizes grow. To address this, we introduce OSCAR, a novel query-dependent online soft compression method that reduces computational overhead while preserving performance. Unlike traditional hard compression methods, which shorten retrieved texts, or soft compression approaches, which map documents to continuous embeddings offline, OSCAR dynamically compresses retrieved information at inference time, eliminating storage overhead and enabling higher compression rates. Additionally, we extend OSCAR to simultaneously perform reranking, further optimizing the efficiency of the RAG pipeline. Our experiments demonstrate state-of-the-art performance with a 2-5x speed-up in inference and minimal to no loss in accuracy for LLMs ranging from 1B to 24B parameters. The models are available at: this https URL.', 'field': ['Information Retrieval', 'Artificial Intelligence', 'Computation and Language']})
    with open('html.txt','w',encoding='utf-8') as fl:
        fl.write(analysis['html']())
        