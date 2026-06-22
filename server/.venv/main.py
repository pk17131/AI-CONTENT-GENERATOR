import os
from fastapi import FastAPI, HTTPException # pyright: ignore[reportMissingImports]
from pydantic import BaseModel # pyright: ignore[reportMissingImports]
from openai import OpenAI # type: ignore

# 1. Initialize FastAPI and OpenAI
app = FastAPI(title="My Custom AI Gateway API")

# Securely load your key from the environment variables
# Run 'export OPENAI_API_KEY="your_actual_key"' in your terminal before running
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 2. Define the structure of data your API expects to receive
class ContentRequest(BaseModel):
    topic: str
    tone: str = "Professional"

# 3. Create your custom POST endpoint
@app.post("/generate-content")
async def create_content(request: ContentRequest):
    if not request.topic:
        raise HTTPException(status_code=400, detail="Topic cannot be empty")
        
    try:
        # Internal AI Logic hidden from the public
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"Write a marketing post in a {request.tone} tone."},
                {"role": "user", "content": request.topic}
            ]
        )
        # Return a custom clean JSON object
        return {
            "status": "success",
            "ai_response": response.choices[0].message.content
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
