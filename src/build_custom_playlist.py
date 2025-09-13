from dotenv import load_dotenv
import os 
import json
from pydantic import BaseModel

from mistralai import Mistral

load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")

class Musique(BaseModel):
    titre: str
    artiste: str
    date: str
    genre: str

class ListMusique(BaseModel):
    morceaux: list[Musique]


def extract_answer(response):
    outputs = response.outputs
    for output in outputs:
        if output.type == "message.output":
            return output.content
    return "No text found"


def get_structured_output(response):
    chat_response = client.chat.parse(
        model="mistral-medium-latest",
        messages=[
            {
                "role": "system", 
                "content": "Extract the music info."
            },
            {
                "role": "user", 
                "content": response
            },
        ],
        response_format=ListMusique,
        max_tokens=512,
        temperature=0
    )
    return chat_response.choices[0].message.parsed

client =  Mistral(api_key=api_key)

web_search_tool = {"type": "web_search"}

agent = client.beta.agents.create(
    model="mistral-medium-latest",
    name = "Custom Playlist Generator",
    description = "Generates a Spotify playlist based on user mood or activity",
    instructions = None,
    tools = [web_search_tool],
    completion_args={"temperature": 0.2, "max_tokens": 1000}
)

def get_musics_from_query(query: str, k:int = 10) -> ListMusique:
    response  = client.beta.conversations.start(
        agent_id=agent.id,
        inputs=f"Generate a list of {k} songs for the following query: {query}",
    )
    print(response)
    return get_structured_output(extract_answer(response))


if __name__ == "__main__":
    query = "Top musique de rap allemand entre 2003 et 2007"
    musics = get_musics_from_query(query, 5)
    for music in musics.morceaux:
        print(music)