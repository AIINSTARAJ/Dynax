document.addEventListener("DOMContentLoaded", function () {
    const searchButton = document.getElementById("btn-ls");
    const AnalysisContainer = document.querySelector(".analysis_");
    const IntroContainer = document.querySelector(".res-txt");
    const DOI = document.getElementById("res-doi").innerText.trim()
    const Title = document.getElementById("title").innerText
    const loadingSpinner = document.querySelector(".dyn-loading");
    const auth = document.getElementById("auth-token").innerText.trim();

    function showLoading() {
        loadingSpinner.style.display = "block"; 
        AnalysisContainer.style.display = "none"; 
        IntroContainer.style.display = "none"; 
    }

    function hideLoading() {
        loadingSpinner.style.display = "none"; 
        AnalysisContainer.style.display = "grid";
        IntroContainer.style.display = "grid";
    }

    async function getAnalysis(doi) {

        showLoading(), 10000;
        
        try {

            /*const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(
                    {'doi': doi,
                     'user': auth}
                ),
            });
    
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const msg = await response.text();

            AnalysisContainer.innerHTML = msg;*/

            IntroContainer.innerHTML = `<br> Dynax! AI Analysis -- ${Title}`
   
            AnalysisContainer.innerHTML = `
                  <!DOCTYPE html>
                  <html>
                  <head>
                  <title>How Humans Evaluate AI Systems for Person Detection in Automatic Train Operation: Not All Misses Are Alike</title>
                  <style>
                  body {
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    margin: 20px;
                  }
                  h1 {
                    font-size: 24px;
                    font-weight: bold;
                    color: #1A237E;
                    margin-bottom: 10px;
                  }
                  h2 {
                    font-size: 21px;
                    font-weight: bold;
                    color: #512DA8;
                    margin-top: 20px;
                    margin-bottom: 10px;
                    background-image: linear-gradient(to right, purple, cyan);
                    -webkit-background-clip: text;
                    background-clip: text;
                    -webkit-text-fill-color: transparent;
                  }
                  p {
                    text-align: justify;
                    margin-bottom: 18px;
                  }
                  .highlight {
                    background-color: rgb(12, 11, 11);
                    padding: 10px;
                    margin-bottom: 10px;
                  }
                  .margin-note {
                    font-size: 10pt;
                    color: #7986CB;
                    margin-left: 20px;
                  }
                  .footnote {
                    font-size: 9pt;
                    color: #9FA8DA;
                  }
                  a {
                    color: #007bff;
                    text-decoration: none;
                  }
                  a:hover {
                    text-decoration: underline;
                  }
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


                  </body>
                  </html>`
                        
        } catch (error) {

            console.error('Error Analyzing Paper',error);

            alert('Error Analyzing Paper. Please Try Again Later.');

        } finally {

            hideLoading(),5000
        }
    }
    
        
    searchButton.addEventListener("click", function () {
        if (DOI) {
            getAnalysis(DOI);
        } else {
            alert("Error!");
        }
    });
    
});

