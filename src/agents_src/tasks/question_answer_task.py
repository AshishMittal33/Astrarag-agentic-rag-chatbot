from crewai import Task
from pydantic import BaseModel

from src.agents_src.agents.question_answer_agent import qa_agent

class AnswerStructure(BaseModel):
    answer: str
    sources: list[str]
    tool_used:str
    rationale:str


qa_task = Task(
    agent=qa_agent,
    name="Questing Answering Task",
    description="""

    Answer the user query "{user_query}" using a Retrieval-Augmented Genaration(RAG) pipeline.
    chat_history: "{chat_History}"

    Instructions:
    - Retrieve relevant context from the document store
    - Prioritize evidence that directly addresses the query
    - Synthesis a clear, accurate answer grounded in the retrived sources or chat history
    - If the query cananot be answered from knowledge source or chat history, do not generate your response.
    Instead, state clearly that the knowledge source does not contain the required information.
     - provide transparency by including references, tool usage, and reasoning steps
    """,

    expected_output="""
    A structured JSON object with the following fields:
    {
       "answer": "Direct response to the query (1-3 paragraphs, clear and accurate).
       if no answer is found, return : 'The knowledge source does not contain the required information.'",
       "sources": ["List of document titles, sections, or citations used (empty list if none)"],
       "tool_used": "Name of the retrieval/analysis tool invovked (e.g., RAG Retriever, VectorDB, ChatHistory,etc.)",
       "rationale": "Brief explanation of why this answer was choosen, or why no relevent information was found"
    }
""",
  output_pydantic=AnswerStructure,
)