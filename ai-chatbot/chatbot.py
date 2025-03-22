import openai
from fastapi import FastAPI, HTTPException
from typing import List
import uvicorn

# Initialize FastAPI app
app = FastAPI()

# OpenAI API Key (Replace with your own)
openai.api_key = "your-api-key-here"

# Store chat history
chat_history = []

@app.post("/chat/")
async def chat_with_ai(user_message: str):
    global chat_history

    # Maintain chat history (only last 5 messages)
    chat_history.append({"role": "user", "content": user_message})
    chat_history = chat_history[-5:]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=chat_history
        )

        ai_reply = response["choices"][0]["message"]["content"]
        chat_history.append({"role": "assistant", "content": ai_reply})

        return {"response": ai_reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the API
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
