from mistralai import Mistral
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")
print(api_key)

client = Mistral(api_key=api_key)


def llm_trouve_similaires(musiques, prompt):
    chat_response = client.chat.complete(
        model="mistral-medium-latest",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    return chat_response.choices[0].message.content
