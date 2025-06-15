from fastapi import FastAPI
from pydantic import BaseModel
import openai
from fastapi.middleware.cors import CORSMiddleware
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chuajefri.github.io/productteardownv2/"],  # Replace with your frontend GitHub Pages URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequestData(BaseModel):
    website: str

@app.post("/teardown")
def teardown(data: RequestData):
    prompt = f"Analyze the website: {data.website} from a product strategy perspective."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    return {"summary": response.choices[0].message["content"]}

# Optional: Friendly root message
@app.get("/")
def root():
    return {"message": "Product Teardown API is running"}
