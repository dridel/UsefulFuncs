from pydantic import BaseModel, Field, conlist
from utils import OpenAIClient, read_prompt # src.utils
from typing import Type

class Suggestion(BaseModel):
    item_ids: conlist(str, min_length=2, max_length=5) = Field(
        ...,description= "List of item_ids that form a cohesive sugegstion. Please only return MIN 2 and MAX 5 items.")
    title: str= Field(description="make a bold title to reflect the choice")
    reasoning: str = Field(description="Take into consideration the provided info" 
                                              " and provide a reasoning why the choice was made")
    location: str


def create_model(max_items: int) -> Type[BaseModel]:
    class ListOfSuggestions(BaseModel):
        suggested_items: conlist(Suggestion, min_length=max_items, max_length=max_items) = Field(
            ..., description=f"Create a list with {max_items} Suggestion items"
        )
    return ListOfSuggestions




obj_list_suggestions = create_model(max_items=3)



response = llm_connection.client.responses.parse(
                model="gpt-4.1-mini",
                input=[
                    {"role": "system", "content": prompt},
                    {"role": "user","content": system_prompt,},
                ],
                text_format=obj_list_suggestions
                max_output_tokens=1500
            )

suggestions = []
for suggestion in response.output_parsed.suggested_items:
    final = filter_out_hallucinations(suggestion)
    suggestions.append(final)