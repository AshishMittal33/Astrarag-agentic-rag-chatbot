from pprint import pprint

from src.agents_src.crew import qa_crew

input_data={
    "user_query": "what is human reproduction",
    "chat_history":"{}"
}

result = qa_crew.kickoff(input_data)

result_dict = result.to_dict()

pprint(result_dict)