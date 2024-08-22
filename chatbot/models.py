from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from openai import OpenAI
from dotenv import load_dotenv
import os
from mlx_lm import load, generate

load_dotenv()


def chat_completion(messages, model):
    match model:
        case "gpt-3.5-turbo":
            response = call_open_ai(messages, model)
        case "gpt-4o":
            response = call_open_ai(messages, model)
        case "mistral-small-latest":
            response = call_mistral(messages)
        case "Meta-Llama-3-8B-Instruct-4bit":
            response = call_llama(messages)
        case _:
            response = call_open_ai(messages)
    return response


def call_open_ai(messages, model):
    client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content


def call_mistral(messages):
    client = MistralClient(api_key=os.getenv('MISTRAL_API_KEY'))
    mistral_messages = []
    for msg in messages:
        new_msg = ChatMessage(role=msg["role"], content=msg["content"])
        mistral_messages.append(new_msg)
    response = client.chat(
        model="mistral-small-latest",
        messages=mistral_messages,
    )
    return response.choices[0].message.content


def call_llama(messages):
    model, tokenizer = load("mlx-community/Meta-Llama-3-8B-Instruct-4bit")
    prompt = tokenizer.apply_chat_template(
        conversation=messages, tokenize=False, add_generation_prompt=False
    )
    max_tokens = 1_000
    verbose = False
    generation_args = {
        "temp": 0.7,
        "repetition_penalty": 1.2,
        "repetition_context_size": 20,
        "top_p": 0.95,
    }
    response = generate(
        model=model,
        tokenizer=tokenizer,
        prompt=prompt,
        max_tokens=max_tokens,
        verbose=verbose,
        **generation_args,
    )
    print(response)
    return response
