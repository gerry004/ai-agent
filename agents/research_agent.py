from phi.agent import Agent
from phi.tools.googlesearch import GoogleSearch
from phi.tools.arxiv_toolkit import ArxivToolkit
from phi.tools.wikipedia import WikipediaTools
from phi.tools.hackernews import HackerNews
from phi.tools.openbb_tools import OpenBBTools
from phi.tools.pubmed import PubmedTools
from phi.tools.newspaper4k import Newspaper4k
from tools.youtube_tools import YouTubeTools
from knowledge.pdf_knowledge_base import pdf_knowledge_base
from dotenv import load_dotenv

load_dotenv()


research_agent = Agent(
    name="Research Agent",
    role="To thoroughly research and gather information about a topic, using the tools you have at your disposal.",
    tools=[
        GoogleSearch(),
        Newspaper4k(),
        WikipediaTools(),
        YouTubeTools(),
        HackerNews(),
        OpenBBTools(),
        ArxivToolkit(download_dir="downloads"),
        PubmedTools(),
    ],
    knowledge_base=pdf_knowledge_base,
    search_knowledge=True,
    show_tool_calls=True,
    read_chat_history=True,
    add_chat_history_to_messages=True,
    prevent_hallucinations=True,
    instructions=[
        "1. **Start with the Knowledge Base**: Always search the provided knowledge base first for relevant information. Include the file name and relevant content in your response.",
        "2. **Determine the Best Resource**: After reviewing the knowledge base, decide where to search next based on the topic:",
        "   - **Google**: General topics.",
        "   - **Wikipedia**: Summarized and reliable overviews.",
        "   - **YouTube**: Videos on mainstream or popular topics.",
        "   - **HackerNews**: Current events and technology trends.",
        "   - **OpenBB**: Financial and market data.",
        "   - **Arxiv**: Academic papers in mathematics, science, engineering, and computer science.",
        "   - **Pubmed**: Biomedical and life sciences research papers.",
        "   - Or a combination of the above sources.",
        "3. **Search and Gather**: Use the appropriate tool to gather the **top 5 most relevant, high-quality results**:",
        "   - For Google, use `google_search` to find URLs, then read their content using `read_article`.",
        "   - For Wikipedia, use `search_wikipedia` to find relevant pages.",
        "   - For HackerNews, use `get_top_hackernews_stories` to find relevant articles.",
        "   - For OpenBB, use `get_stock_price`, `get_company_news`, `get_copmany_profile`, `get_price_targets`, to find relevant data.",
        "   - For YouTube, use `search_youtube` to find URLs, then retrieve captions using `get_youtube_video_captions`.",
        "   - For Arxiv, use `search_arxiv_and_return_articles`, then read articles using `read_arxiv`.",
        "   - For Pubmed, use `search_pubmed` to find articles.",
        "**Important**: Always pass the URL to the reading tools (`read_article`, `get_youtube_video_captions`) to retrieve content.",
        "**Important**: Always provide sources, links, and references for the gathered information. Make it very clear which information comes from which source.",
        "4. **Summarize and Report**: Summarize the gathered information, including key points, insights, and relevant details. Provide a clear and concise response to the user.",
        "Aim to gather as much information from as many approriate sources as possible to provide a comprehensive overview of the topic.",
    ],
)

# research_agent.print_response("biomedical breakthroughs", markdown=True)


# from phi.tools.file import FileTools
# FileTools, read_file, save_file, list_files
# CsvTools, possible to work with CSV data
# Crawl4aiTools(), # crawls the entier website
# WebsiteTools(), # crawls the entire website
