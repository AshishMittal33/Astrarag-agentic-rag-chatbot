import logging
import chromadb

from crewai.tools import tool
from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq

from src.agents_src.config.agents_settings import AgentSettings

logger = logging.getLogger(__name__)

# Load embedding ONCE (correct)
logger.info("Loading HuggingFace Embedding Model...")
embed = HuggingFaceEmbedding()


@tool
def rag_query_tool(query: str) -> dict:
    """
    Answers a query by retrieving relevant documents and generating a response.
    """

    settings = AgentSettings()

    # Configure LLM globally for LlamaIndex
    Settings.llm = Groq(
        model=settings.MODEL_NAME,
        temperature=settings.MODEL_TEMPERATURE,
        api_key=settings.GROQ_API_KEY,
    )
    Settings.embed_model = embed

    # Connect to existing Chroma DB
    db = chromadb.PersistentClient(path=settings.VECTOR_STORE_DIR)
    chroma_collection = db.get_or_create_collection(
        name=settings.COLLECTION_NAME
    )

    vector_store = ChromaVectorStore(
        chroma_collection=chroma_collection
    )

    storage_context = StorageContext.from_defaults(
        vector_store=vector_store
    )

    # ✅ CORRECT: create index from existing vector store
    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        storage_context=storage_context,
    )

    query_engine = index.as_query_engine(similarity_top_k=3)

    response = query_engine.query(query)

    source_files = {
        node.metadata.get("file_name")
        for node in getattr(response, "source_nodes", [])
        if node.metadata
    }

    return {
        "answer": str(response),
        "source_files": list(source_files),
    }
