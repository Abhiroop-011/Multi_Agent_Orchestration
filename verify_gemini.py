from google import genai
import inspect
import os
from dotenv import load_dotenv

load_dotenv()  # 👈 THIS was missing

print("genai loaded from:")
print(inspect.getfile(genai))

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

resp = client.models.generate_content(
    model="models/gemini-flash-latest",
    contents="Say OK"
)
print(resp.text)

