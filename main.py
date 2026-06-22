import os
        "You are a modern AI assistant like Gemini or ChatGPT. Speak naturally and provide a complete, polished final answer. "
        "Never ask the user for clarification — instead, make reasonable assumptions. When producing content, follow the format instructions provided and return a finished piece ready for publishing or copy/paste."

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

app = FastAPI(title="My Custom AI Gateway API")

    # Format instructions per style to guide the model towards final, usable outputs
    format_instructions = {
        "article": (
            "Return output with these sections: Title (one line), Short summary (1-2 lines),\n"
            "Body with 2-4 short paragraphs and optional subheadings,\nConclusion (1 paragraph), and a short Call-to-action (1 line)."
        ),
        "summary": (
            "Return a TL;DR (1 sentence) followed by 3-6 concise bullet points summarizing the key ideas."
        ),
        "social": (
            "Return one social caption (max 220 chars) followed by 3 suggested hashtags. Keep it engaging and direct."
        ),
        "headline": (
            "Return 5 headline options, each concise and attention-grabbing, numbered or on separate lines."
        )
    }

    fmt = format_instructions.get(req.style, format_instructions['article'])


        f"Create {style_description} that is {length_description} and written in a {req.tone} tone for the following request: {req.prompt}.\n"
        "Do not repeat the prompt verbatim and do not ask the user questions. Make reasonable assumptions if details are missing.\n"
        f"Formatting instructions: {fmt}\n"
        f"Assistant style guidance: {assistant_style}"
    USE_MOCK = False
else:
    client = None
            # richer mock that follows format instructions per style
            if req.style == 'article':
                ai_text = (
                    f"Title: Example about {req.prompt}\n\n"
                    f"Summary: A brief summary about {req.prompt}.\n\n"
                    "Body: This is a simulated article paragraph one. This mock demonstrates a finished article-like response.\n\n"
                    "Conclusion: Final thought.\n\nCall-to-action: Learn more at our site."
                )
            elif req.style == 'summary':
                ai_text = (
                    f"TL;DR: One-line summary about {req.prompt}.\n\n- Point 1 about the topic.\n- Point 2 about the topic.\n- Point 3 about the topic."
                )
            elif req.style == 'social':
                ai_text = (
                    f"{req.prompt} — Short engaging caption example.\n\n#example #ai #content"
                )
            elif req.style == 'headline':
                ai_text = (
                    "1) Headline option one about " + req.prompt + "\n"
                    "2) Headline option two\n3) Headline option three\n4) Headline option four\n5) Headline option five"
                )
            else:
                ai_text = f"[MOCK] {req.prompt} — sample content."
            return {"text": ai_text}
    tone: str = "Professional"
            # Use generation settings tuned for coherent, useful content.
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg}
                ],
                max_tokens=max_tokens,
                temperature=0.7,
                top_p=0.95,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )
        if USE_MOCK:
            # Simple deterministic mock response for offline dev
            mock = f"[MOCK] {request.tone} marketing post about: {request.topic}"
            return {"status": "success", "ai_response": mock}

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"Write a marketing post in a {request.tone} tone."},
                {"role": "user", "content": request.topic}
            ]
        )
        return {"status": "success", "ai_response": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Additional endpoint for the React UI and CORS setup ---

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UIRequest(BaseModel):
    prompt: str
    tone: str = "neutral"
    length: str = "short"
    style: str = "article"
    assistant: str = "chatgpt"


@app.post("/api/generate")
async def api_generate(req: UIRequest):
    if not req.prompt or not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    # map length to approximate max tokens
    max_tokens_map = {"short": 200, "medium": 450, "long": 800}
    max_tokens = max_tokens_map.get(req.length, 200)

    length_description = {
        "short": "short",
        "medium": "detailed",
        "long": "long-form"
    }.get(req.length, "short")

    system_msg = (
        "You are a modern AI assistant like Gemini. Speak naturally, provide a complete final answer, "
        "and avoid asking the user for more information. If the prompt is a topic or question, respond with a high-quality content result. "
        "Use a friendly tone, clear structure, and deliver an answer that feels ready to use."
    )

    style_description = {
        "article": "a well-structured article",
        "summary": "a concise summary",
        "social": "a short social media post",
        "headline": "a catchy headline"
    }.get(req.style, "a polished article")

    assistant_style = {
        "chatgpt": "Use a conversational assistant tone, with clear paragraphs and helpful phrasing.",
        "gemini": "Use a concise, modern assistant style like Gemini, with direct answers and smart structure.",
        "assistant": "Use a general AI assistant tone that is friendly and informative."
    }.get(req.assistant, "Use a conversational assistant tone.")

    user_msg = (
        f"Create {style_description} that is {length_description} and written in a {req.tone} tone for the following request: {req.prompt}. "
        "If the request is a topic, write a useful, polished piece of content. If the request is a question, answer it directly and completely. "
        "Do not repeat the prompt verbatim, and do not return your own questions. "
        f"{assistant_style}"
    )

    try:
        if USE_MOCK:
            ai_text = (
                f"[MOCK-{req.tone.upper()}] A {length_description} content example about '{req.prompt}'. "
                "This example is designed to simulate a final AI response instead of a question."
            )
            return {"text": ai_text}

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
            max_tokens=max_tokens,
            temperature=0.8,
        )

        ai_text = response.choices[0].message.content
        return {"text": ai_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
