import logging

import chromadb
from llama_index.core import VectorStoreIndex , SimpleDirectoryReader , StorageContext
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

from src.rag_doc_ingestion.config.doc_ingestion_setting import DocIngestionSettings

logging.basicConfig(
    level = logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


setting = DocIngestionSettings()

logger.info("Loading Hugginface Embedding Model...")
embed_model = HuggingFaceEmbedding()


def build_vector_store_from_documents():
    logger.info("Starting vector store ingestion process...")
    try:
        docs_dir_path = setting.DOCUMENTS_DIR
        vector_store_path = setting.VECTOR_STORE_DIR
        collection_name = setting.COLLECTION_NAME
        logger.info(f"Loading Documents Directory: {docs_dir_path}")
        loader = SimpleDirectoryReader(input_dir=docs_dir_path)
        documents = loader.load_data()

        parser = SimpleNodeParser().from_defaults(chunk_size=1024, chunk_overlap=50)
        logger.info("Parsing Documents into Nodes...")
        nodes= parser.get_nodes_from_documents(documents)
        logger.info(f"Parsed {len(nodes)} nodes from documents.")
        logger.info(f"Setting up Chroma Vector Store at: {vector_store_path}")
        db = chromadb.PersistentClient(path=vector_store_path)
        chroma_collection = db.get_or_create_collection(name=collection_name)
        logger.info(f"Creating Chroma Vector Store with collection: {collection_name}")
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        logger.info("Building Vector Store Index from Nodes...")
        index = VectorStoreIndex(
            nodes,
            storage_context =storage_context,
            vector_store=vector_store,
            embed_model=embed_model
        )

        logger.info("Vector Store Ingestion Completed Successfully.")
        return 0
    except Exception as e:
        logger.error(f"Error during vector store ingestion: {e}")
        return 1
    

if __name__ == "__main__":
    build_vector_store_from_documents()