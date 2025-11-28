import getpass
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_demo.config import EMBEDDINGS_MODEL_NAME, MODEL_NAME

load_dotenv()

if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")


model = init_chat_model(MODEL_NAME)

embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDINGS_MODEL_NAME)

vector_store = InMemoryVectorStore(embeddings)

import bs4
from langchain_community.document_loaders import WebBaseLoader

# Only keep post title, headers, and content from the full HTML.
# bs4_strainer = bs4.SoupStrainer(id=("main-heading"), **{"data-testid":"recipe-ingredients"})
bs4_strainer = bs4.SoupStrainer(
    **{"id": "main-heading", "data-testid": "recipe-ingredients"}
)
bs4_strainer = bs4.SoupStrainer(
    **{"data-testid": ["recipe-ingredients", "recipe-method"]}
)
loader = WebBaseLoader(
    web_paths=("https://www.bbc.co.uk/food/recipes/indonesian_biryani_17351",),
    bs_kwargs={"parse_only": bs4_strainer},
)
docs = loader.load()

# assert len(docs) == 1
# print(f"RECIPE: {docs[0].page_content}")
# print(f"Total characters: {len(docs[0].page_content)}")


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # chunk size (characters)
    chunk_overlap=200,  # chunk overlap (characters)
    add_start_index=True,  # track index in original document
)
all_splits = text_splitter.split_documents(docs)

print(f"Split blog post into {len(all_splits)} sub-documents.")


@tool(response_format="content_and_artifact")
def retrieve_context(query: str):
    """Retrieve information to help answer a query."""
    retrieved_docs = vector_store.similarity_search(query, k=2)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs


tools = [retrieve_context]
# If desired, specify custom instructions
prompt = (
    "You have access to a tool that retrieves context from a blog post. "
    "Use the tool to help answer user queries."
)
agent = create_agent(model, tools, system_prompt=prompt)
