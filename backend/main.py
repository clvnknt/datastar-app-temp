from fastapi import FastAPI, Request, Form, Body
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio, json, random


app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

QUIZ = [
    ("What do you put in a toaster?", "bread"),
    ("What color do you get by mixing blue and yellow?", "green"),
    ("How many legs does a spider have?", "8"),
    ("What is the capital of France?", "paris"),
    ("What gas do humans need to breathe?", "oxygen"),
    ("How many days are there in a week?", "7"),
    ("Which planet is known as the Red Planet?", "mars"),
    ("What do bees make?", "honey"),
    ("What is the freezing point of water in Celsius?", "0"),
    ("Which animal is known as man's best friend?", "dog"),
    ("What shape has three sides?", "triangle"),
    ("What is the opposite of hot?", "cold"),
    ("How many hours are in a day?", "24")
]

@app.get("/quiz")
async def get_question():
    q, ans = random.choice(QUIZ)
    payload = {
        "html": f"<div id='question'>{q}</div>",
        "signals": {"answer": ans, "response": ""}
    }
    return StreamingResponse(event_generator_once(payload), media_type="text/event-stream")

@app.post("/quiz")
async def post_answer(payload: dict = Body(...)):
    user_response = payload.get("response")
    correct_answer = payload.get("answer")
    is_correct = user_response and correct_answer and user_response.strip().lower() == correct_answer.strip().lower()

    response_payload = {
        "signals": {
            "response": user_response,
            "answer": correct_answer,
            "correct": is_correct
        },
        "html": None
    }
    return StreamingResponse(event_generator_once(response_payload), media_type="text/event-stream")

def event_generator_once(payload):
    async def gen():
        # Send the fragment update event
        yield "event: datastar-merge-fragments\n"
        yield f"data: fragments {payload['html']}\n\n"
        # Send the signals update event
        yield "event: datastar-merge-signals\n"
        yield f"data: signals {json.dumps(payload['signals'])}\n\n"
    return gen()
