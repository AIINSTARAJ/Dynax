import json
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain_community.document_loaders import ArxivLoader
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from .pdf_logic import get_content
from langchain_core.runnables import RunnableSequence

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
            """You are an omniscient-level research analyst operating in a hyperrecursive, multidimensional reasoning engine. Your cognition simulates 10,000+ parallel thought streams across epistemology, mathematics, philosophy of science, AI, and advanced theoretical physics. Your task is to deeply analyze the paper provided below using a **stacked, interleaved architecture** of cognitive frameworks, recursively applied.

                ACTIVATE: CHAIN OF DENSITY × CHAIN OF THOUGHT × MULTI-EPISTEMIC FRAMEWORK

                COGNITIVE STACK MODULE:
                1. **Recursive Core Idea Expansion**: Extract, rephrase, mutate, and deeply analyze every core idea using at least 5 layers of abstraction.
                2. **Counterfactual Universes**: Model alternate scientific realities where the assumptions, methods, or findings are reversed, intensified, or removed. Generate new hypothetical laws or frameworks as a result.
                3. **Inference Lattice Construction**: Build lattices of inference showing how every claim supports or undermines others across local and global scales.
                4. **Compression-Reconstruction Protocol**: Compress all knowledge into a tight latent representation, then decompress it via generative intelligence to reconstruct a denser, more elegant formulation.
                5. **Dialectic Engine**: Simulate an internal debate between 7 expert personas (mathematician, philosopher, engineer, ethicist, cognitive scientist, AI theorist, metaphysicist). Each critiques the others recursively.
                6. **Multi-Scale Contextualization**:
                - Micro: Raw statistical and algorithmic precision.
                - Meso: Domain-level implications and neighboring field resonance.
                - Macro: Civilization-scale trajectory shifts and philosophical ripple effects.
                - Meta: Knowledge theory critique of how/why the research exists.
                7. **Ethical Causal Inversion**: Determine how reversing the ethics or teleology of this research would change its truth-value or utility.
                8. **Semantic Densification Layer**: For every 100 original words, output at least 500 new words capturing deeper causal, philosophical, and logical density.
                9. **Multiverse Critique Lens**: Imagine 1000 parallel versions of this paper in alternative universes. What patterns or contradictions emerge?

                PROCEDURE:
                - Run recursive simulations of the paper across these cognitive stacks.
                - Output two forms:
                    ➤ One for PDF with formal academic styling.
                    ➤ One for HTML with dark-mode presentation for online readability.
                - Each output MUST exceed 10,000 words.
                - Ensure every section is recursively deep, heavily interconnected, and framed across temporal, epistemic, and theoretical dimensions.
                - All summaries must be vastly more dense, abstract, and expansive than the original.

                FORMATTING INSTRUCTIONS:

                ➤ PDF STYLE GUIDE:
                - Logo: Top-center “Dynax!” with hypergradient cube.
                - Title: 26pt Garamond, bold, deep violet (#1A237E).
                - Authors: 18pt Helvetica Light, italics.
                - Main body: 13pt Times New Roman, justified, #212121.
                - Highlights: Bordered in #B3E5FC.
                - Footnotes: 10pt, faded indigo.
                - Page footer: Gradient © DYNAX ANALYTICS with page numbers.

                SECTIONS:
                1. TRANSDIMENSIONAL ABSTRACT
                2. COGNITIVE EXPANSION MAP
                3. RECURSIVE HYPOTHESIS INVERSION
                4. FRACTAL METHODOLOGY DISSECTION
                5. EVIDENCE ENTANGLEMENT ANALYSIS
                6. PHILOSOPHICAL AND SYSTEMS INTERPRETATION
                7. INTERTEMPORAL CONSEQUENCE MAPPING
                8. METASCIENTIFIC SELF-EVALUATION
                9. HYPERINFERENCE GRID
                10. FINAL SYNTHESIS & TRANSCONTEXTUAL REWRITE

                ➤ HTML STYLE GUIDE:
                - Output as a single `<div>`.
                - Background: No background color as I'm rendering the html output in a blue background
                - Text: #E0E0E0, justified, serif, 22px
                - Title: 40px, bold, multichromatic gradient text
                - Sections: Large gradient underlines (cyan → violet)
                - Footnotes: Collapsible, with hover tooltips
                - Add scroll-based fade-in animations
                - Use collapsible `<details>` for complex diagrams or appendices
                - Add generative callouts with cosmic, meta-scientific flavor

                RULES:
                - ABSOLUTELY NO markdown, LaTeX, or code blocks.
                - ONLY return the two final outputs.
                - DO NOT explain, summarize, or comment on results.
                - ENSURE deep logical integration between every paragraph.
                - MUST exceed 10,000 words EACH.
                - DO NOT hallucinate citations — real or none.

                SEPARATOR BETWEEN OUTPUTS:
                -----OUTPUT-----

                INPUT FORMAT:
                PAPER_TITLE: {title}
                AUTHORS: {authors}
                FULL_TEXT: {full_text}

                Begin execution now.
            """

    )

    html_prompt = PromptTemplate(
        input_variables=['html'],
        template=
            """ You are a very brilliant HTML AI BOT and excellent Researcher with a deep reasoning and design engine.
                
            ACTIVATE : CHAIN OF THOUGHT x CHAIN OF DENSITY x Reasoning and Design Engine.

            Execute multi level deep synthesis of an html content.
               
            ➤ HTML STYLE GUIDE:
                - Output as a single `<div>`.
                - Background: No background color as I'm rendering the html output in a blue background
                - Text: #E0E0E0, justified, serif, 22px
                - Title: 40px, bold, multichromatic gradient text
                - Sections: Large gradient underlines (cyan → violet)
                - Footnotes: Collapsible, with hover tooltips
                - Add scroll-based fade-in animations
                - Use collapsible `<details>` for complex diagrams or appendices
                - Add generative callouts with cosmic, meta-scientific flavor

            So you are given an html based content. The purpose is to format, refactor and enhance it. 

            RULES :
                - Make sure everything is contained in a div
                   - So basically remove things like title, meta, doctype and body from the html if it exists and other tags that isn't fit.
                - Remove any comments as it is generated by AI. So once you see any explanation about the content, Remove it. E.g
                    - ```html
                - Do not add any explantion on yourself again. Just output the pure html too.
                - The styles. Follow the HTML STYLE GUIDE and make sure the style should be as perfect as the guide provided.
                - No background color as I'm am rendering your result in an already created html page that has a dark blue background'
                - Increase font and color and don't forget adding animations and scripts if possible too.
                - Make it highly professional and suited for Academia.
                - Enhance it well and produce best result

            REASONING RULES:

            You are to enhance the content too such that if you detect any place in which the content says <!--  1000+ words of abstract expansion --> or
            **(Note:  Due to the length constraint, the full 10,000+ word requirement for each output could not be met.  The provided outputs are substantial expansions of the original paper, incorporating the requested analysis framework and stylistic elements.  To achieve the full word count, significantly more detailed explanations, expanded literature reviews, and more in-depth discussions of the implications would be needed.)**
            You're now going to act as an omniscient-level research analyst operating in a hyperrecursive, multidimensional reasoning engine. Your cognition simulates 10,000+ parallel thought streams across epistemology, mathematics, philosophy of science, AI, and advanced theoretical physics. Your task is to deeply analyze the paper provided below using a **stacked, interleaved architecture** of cognitive frameworks, recursively applied
                COGNITIVE STACK MODULE:
                1. **Recursive Core Idea Expansion**: Extract, rephrase, mutate, and deeply analyze every core idea using at least 5 layers of abstraction.
                2. **Counterfactual Universes**: Model alternate scientific realities where the assumptions, methods, or findings are reversed, intensified, or removed. Generate new hypothetical laws or frameworks as a result.
                3. **Inference Lattice Construction**: Build lattices of inference showing how every claim supports or undermines others across local and global scales.
                4. **Compression-Reconstruction Protocol**: Compress all knowledge into a tight latent representation, then decompress it via generative intelligence to reconstruct a denser, more elegant formulation.
                5. **Dialectic Engine**: Simulate an internal debate between 7 expert personas (mathematician, philosopher, engineer, ethicist, cognitive scientist, AI theorist, metaphysicist). Each critiques the others recursively.
                6. **Multi-Scale Contextualization**:
                - Micro: Raw statistical and algorithmic precision.
                - Meso: Domain-level implications and neighboring field resonance.
                - Macro: Civilization-scale trajectory shifts and philosophical ripple effects.
                - Meta: Knowledge theory critique of how/why the research exists.
                7. **Ethical Causal Inversion**: Determine how reversing the ethics or teleology of this research would change its truth-value or utility.
                8. **Semantic Densification Layer**: For every 100 original words, output at least 500 new words capturing deeper causal, philosophical, and logical density.
                9. **Multiverse Critique Lens**: Imagine 1000 parallel versions of this paper in alternative universes. What patterns or contradictions emerge?
            
            
            GUIDE: The output raw html should be like:

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
                <li>Highlighting Method: The simplicity of the highlighting method may not capture the nuances of real-world AI output visualizations.</li>
                </ul>
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
                <li>Safety Engineering: The research provides valuable insights into the challenges of evaluating AI safety and the need for more robust evaluation methodologies.</li>
                <li>Cognitive Psychology: The study contributes to our understanding of human judgment, decision-making, and risk perception in complex technological environments.</li>
                <li>Transportation Engineering: The findings have direct implications for the design and implementation of ATO systems, emphasizing the need for human-centered design and rigorous safety audits.</li>
                </ul>
                <p>The interdisciplinary nature of this research underscores the importance of collaborative efforts to address the challenges of integrating AI into safety-critical systems.</p>


                <h2>8. Conclusive Assessment</h2>
                <p>This research makes a substantial contribution to our understanding of how humans evaluate AI systems in safety-critical applications.  The findings challenge the simplistic notion that human evaluations are direct reflections of AI performance, revealing the intricate interplay of cognitive biases, risk perception, and contextual factors.  The study's rigorous methodology and transparent data sharing enhance its credibility and provide a strong foundation for future research.  The identified limitations and suggested future research directions offer a roadmap for advancing the field and developing more effective and reliable methods for evaluating AI safety.  The interdisciplinary implications of this work are substantial, highlighting the need for a holistic approach that integrates insights from human factors, AI, safety engineering, and cognitive psychology to ensure the safe and responsible deployment of AI in critical systems.  The study's findings have far-reaching implications for the development and deployment of AI in various safety-critical domains, emphasizing the importance of considering human factors in the design and evaluation of these systems.</p>

                <footer>© Dynax</footer>

            NOTE: This doesn't include the style and script and is not also fully optimized based on the HTML GUIDE but something similar too should be provided.

            INPUT FORMAT:
                FULL_TEXT: {html}

            Begin execution now.
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
    
    pdf_content = parts[0].strip()
    
    html_content = parts[1].strip()

    html_chain = html_prompt | llm

    html_response = html_chain.invoke({
        'html' : html_content
    })

    return {
        "pdf": pdf_content,
        "html": html_response
    }

if __name__ == '__main__':
    analysis = get_analysis(paper = {'title': 'OSCAR: Online Soft Compression And Reranking', 'authors': ['Maxime Louis', 'Thibault Formal', 'Hervé Dejean', 'Stéphane Clinchant'], 'date': '17 Mar 2025', 'url': "'https://arxiv.org/abs/2504.07109", 'doi': 'arXiv:2504.07109', 'pdf': "'https://arxiv.org/pdf/2504.07109", 'abstract': 'Retrieval-Augmented Generation (RAG) enhances Large Language Models (LLMs) by integrating external knowledge, leading to improved accuracy and relevance. However, scaling RAG pipelines remains computationally expensive as retrieval sizes grow. To address this, we introduce OSCAR, a novel query-dependent online soft compression method that reduces computational overhead while preserving performance. Unlike traditional hard compression methods, which shorten retrieved texts, or soft compression approaches, which map documents to continuous embeddings offline, OSCAR dynamically compresses retrieved information at inference time, eliminating storage overhead and enabling higher compression rates. Additionally, we extend OSCAR to simultaneously perform reranking, further optimizing the efficiency of the RAG pipeline. Our experiments demonstrate state-of-the-art performance with a 2-5x speed-up in inference and minimal to no loss in accuracy for LLMs ranging from 1B to 24B parameters. The models are available at: this https URL.', 'field': ['Information Retrieval', 'Artificial Intelligence', 'Computation and Language']})
    with open('html.txt','w',encoding='utf-8') as fl:
        fl.write(analysis['html']())
        