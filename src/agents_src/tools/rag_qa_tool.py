import logging

from crewai.tools import tool
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq
from llama_index.core import Settings
import chromadb

from src.agents_src.config.agents_settings import AgentSettings

logger=logging.getLogger(__name__)

logger.info("Loading Hugginface Embedding Model...")

embed=HuggingFaceEmbedding()

@tool
def rag_query_tool(query:str)-> dict:
    """
    Answers a query by retrieving relevant documents and generating a response.
    Returns both the generated answer and the source file names from which the information was retrived.

    Args:
        query(str): The  input query string to be processed.

    Returns:
        dict: A dictionary with the following keys:
            - 'answer' : The generated answer string.
            - 'source_files': List of source file names used for retrieval.

    Notes:
        - Requires properly configured AgentSettings and access to the vector store.
        - the function loads the embedding model and llm each time it is called.
    """

    settings = AgentSettings()
    vector_store_path = settings.VECTOR_STORE_DIR
    collection_name = settings.COLLECTION_NAME

    Settings.llm = Groq(
        model=settings.MODEL_NAME,
        temperature=settings.MODEL_TEMPREATURE,
        api_key=settings.GROQ_API_URL
    )


    db = chromadb.PersistentClient(path=vector_store_path)
    chroma_collection = db.get_or_create_collection(name=collection_name)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.load_from_disk(
        vector_store=vector_store,
        storage_context=storage_context,
        embed_model=embed
    )

    query_engine = index.as_query_engine(similarity_top_k=3)

    response = query_engine.query(query)
    source_files_names = {m.get("file_name") for m in getattr(response, "metadata",{}).values()}

    return {"answer":response.response,
            "source_files":list(source_files_names)}


