from openai import OpenAI
from ..config import CHAT_MODEL, OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def generate(system, user):
    r = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[{"role":"system","content":system},
                  {"role":"user","content":user}]
    )
    return r.choices[0].message.content
