import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chuajefri.github.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequestData(BaseModel):
    website: str

@app.post("/teardown")
def teardown(data: RequestData):
    prompt = f"You're an expert product manager with deep experience in product strategy and analysis. Analyze the product "{data.website}" using the following frameworks. For each framework, provide specific, actionable insights with concrete examples from the product. Focus on both strengths and improvement opportunities. Frameworks are
                jtbd: {
                    name: "Jobs to be Done (JTBD)",
                    prompt: "What specific job is the user hiring this product to do? What are the functional, emotional, and social jobs? What are the current alternatives/workarounds? What triggers users to seek this solution?"
                },
                aarrr: {
                    name: "AARRR Pirate Metrics",
                    prompt: "Acquisition: How do users discover this product? Activation: What's the aha moment/first value experience? Retention: What keeps users coming back? Revenue: How does the product monetize? Referral: What drives users to share/recommend?"
                },
                ux: {
                    name: "UX Heuristics Analysis",
                    prompt: "Usability: How intuitive and learnable is the interface? Visual hierarchy: How well does design guide user attention? Error prevention: How does the product prevent user mistakes? Accessibility: How inclusive is the design for all users?"
                },
                gtm: {
                    name: "Go-to-Market Strategy",
                    prompt: "Target market: Who is the ideal customer profile? Value proposition: What unique value does it provide? Distribution channels: How does it reach customers? Pricing strategy: How is it positioned in the market?"
                },
                competitive: {
                    name: "Competitive Analysis",
                    prompt: "Direct competitors: Who offers similar solutions? Indirect competitors: What alternative approaches exist? Competitive advantages: What differentiates this product? Market positioning: How does it position against competition?"
                },
                monetization: {
                    name: "Monetization Strategy",
                    prompt: "Revenue model: How does the product make money? Pricing tiers: What are the different pricing options? Value metric: What drives willingness to pay? Revenue optimization: How could monetization be improved?"
                },
                "north-star": {
                    name: "North Star Framework",
                    prompt: "North Star Metric: What's the key metric that drives growth? Input metrics: What leading indicators drive the north star? User value: How does the metric reflect user value? Business value: How does it connect to business outcomes?"
                },
                rice: {
                    name: "RICE Prioritization",
                    prompt: "Reach: How many users would benefit from improvements? Impact: How much would improvements affect key metrics? Confidence: How certain are we about reach and impact? Effort: What's the development/implementation cost?""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    return {"summary": response.choices[0].message.content}

@app.get("/")
def root():
    return {"message": "Product Teardown API is running"}
