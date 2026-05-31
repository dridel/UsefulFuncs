from ollama import chat
from pydantic import BaseModel, conlist, Field


class PlushToyNameSuggestion(BaseModel):
    plush_toy_name_suggestions: conlist(str, min_length=3, max_length=3) = Field(
        ...,
        description="List of plush toy names suggestions. Please only return MIN 3 and MAX 3 items"
    )
prompt_text = """
I got a new plush toy, it's a green frog, with a formal shirt and a bow tie.
I want to find a creative name for him, could you help me by providing 3 to 3 name options?
Thank you!
"""

prompt = {'role':'user', 'content': prompt_text}

response = chat(
    model='llama3.2:latest',
    messages=[prompt],
    format=PlushToyNameSuggestion.model_json_schema(),
    options={'temperature': 0.0}
)
output = PlushToyNameSuggestion.model_validate_json(response.message.content)

for i, name_suggestion in enumerate(output.plush_toy_name_suggestions):
    print(f" Suggestion ({i}): {name_suggestion}")
