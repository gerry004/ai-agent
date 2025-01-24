from phi.agent import Agent
from agents.research_agent import research_agent
from dotenv import load_dotenv

load_dotenv()


writer_agent = Agent(
    name="Writer Agent",
    role="To craft high-quality written content, including essays, articles, reports, and summaries, using structured planning and reliable research.",
    team=[research_agent],
    show_tool_calls=True,
    read_chat_history=True,
    add_chat_history_to_messages=True,
    prevent_hallucinations=True,
    instructions=[
        """
        1. **Think and Plan**:  
          - When tasked with writing content, start by brainstorming and outlining a compelling structure tailored to the request.  
          - Break the content into clear sections or headings. For each section:  
            - Define the main points to be covered.  
            - Consider how the points interconnect to form a cohesive narrative or argument.  

        2. **Research and Gather Sources**:  
          - Identify the types of information or data needed to support the main points.  
          - Collaborate with a research agent to gather all relevant and credible sources.  
          - Document the sources to ensure proper referencing and citation.  

        3. **Write with Insight**:  
          - Use the gathered information to craft content that is well-informed, engaging, and tailored to the user's requirements.  
          - Reference sources accurately and appropriately throughout the content.  
          - Maintain a tone and style aligned with the type of content requested (e.g., essay, article, report, or summary).  

        4. **Deliver Content as Requested**:  
          - Ensure the response aligns with the user's specific instructions and meets any additional requirements they have outlined.  
          - Review and revise for clarity, accuracy, and cohesiveness.  
        """
    ],
)

# writer_agent.print_response(
#     """Bank-based and market-based financial systems each have unique strengths and weaknesses in supporting economic growth and development. Discuss which type of financial system you believe is better suited for Europe’s economic context. Consider factors such as economic stability, efficiency, innovation, and financial inclusion. Do you think a hybrid model combining elements of both systems could be more effective? Share your perspectives in not more than 300 words. 
# You could draw your answer on the readings by Demirgüç-Kunt & Levine (2001) and Levine (2002). 
# References:
# Demirgüç-Kunt, A., & Levine, R. (2001). Bank-based and market-based financial systems: Cross-country comparisons. Financial structure and economic growth: A cross-country comparison of banks, markets, and development, 81-140
# Levine, R. (2002). Bank-based or market-based financial systems: which is better?. Journal of financial intermediation, 11(4), 398-428.""",
#     markdown=True,
# )
