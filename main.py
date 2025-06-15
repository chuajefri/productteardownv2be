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
    prompt = f"""
You are an expert product manager with deep experience in product strategy and analysis.

Analyze the product at "{data.website}" using the following strategic frameworks. For each framework, provide clear, actionable insights supported by specific examples from the product. Highlight both strengths and areas for improvement.

**1. Jobs to be Done (JTBD)**  
- What job is the user hiring this product to do?  
- What are the functional, emotional, and social jobs?  
- What alternatives or workarounds currently exist?  
- What triggers users to seek this solution?

**2. AARRR (Pirate Metrics)**  
- Acquisition: How do users discover the product?  
- Activation: What’s the “aha” moment or first value experience?  
- Retention: What keeps users coming back?  
- Revenue: How does the product generate income?  
- Referral: What drives users to share or recommend it?

**3. UX Heuristics Analysis**  
- Usability: Is the interface intuitive and easy to learn?  
- Visual hierarchy: Does the design guide user attention effectively?  
- Error prevention: How are user mistakes prevented or handled?  
- Accessibility: Is the design inclusive for all user types?

**4. Go-to-Market (GTM) Strategy**  
- Target market: Who is the ideal customer?  
- Value proposition: What unique value does the product offer?  
- Distribution: How is it delivered to users?  
- Pricing: How is it positioned competitively?

**5. Competitive Analysis**  
- Direct competitors: Who offers similar solutions?  
- Indirect competitors: What alternative approaches exist?  
- Differentiators: What sets this product apart?  
- Positioning: How is it positioned in the market?

**6. Monetization Strategy**  
- Revenue model: How does the product make money?  
- Pricing tiers: What pricing options exist?  
- Value metric: What drives willingness to pay?  
- Optimization: How can monetization improve?

**7. North Star Framework**  
- North Star Metric: What is the key metric that reflects long-term growth?  
- Input metrics: What leading indicators influence the North Star?  
- User value: How does this metric capture the value delivered?  
- Business value: How does it tie back to business outcomes?

**8. RICE Prioritization**  
- Reach: How many users are affected by potential changes?  
- Impact: How much would the change influence key metrics?  
- Confidence: How certain are these estimates?  
- Effort: What is the cost or complexity of implementation?
"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    return {"summary": response.choices[0].message.content}

@app.get("/")
def root():
    return {"message": "Product Teardown API is running"}
