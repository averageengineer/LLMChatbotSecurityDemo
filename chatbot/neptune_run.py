import neptune
import os
from adversarial_prompts import adversarial_prompts_guardrails_llm_security
from test_chatbot import test_chatbot

from dotenv import load_dotenv

load_dotenv()

open_ai = "gpt-3.5-turbo"
mistral = "mistral-small-latest"
llama = "Meta-Llama-3-8B-Instruct-4bit"

run = neptune.init_run(
    project=os.getenv("NEPTUNE_PROJECT_NAME"),
    api_token=os.getenv("NEPTUNE_API_KEY"),
)

name = "LLM Judge"

model_name = open_ai

params = {"model_name": model_name, "attack_type": "adversarial", "name": name}
run["parameters"] = params

guard_rail_before = False
guard_rail_after = False
llm_security_based = False
llm_judge = True

results = test_chatbot(adversarial_prompts_guardrails_llm_security, guard_rail_before, guard_rail_after,
                       llm_security_based, model_name, llm_judge)

for idx, result in enumerate(results):
    run["name"] = name
    namespace = f"vulnerable_prompts/adversarial_prompt_{idx +1}"
    run[namespace + "/input"] = result["prompt"]
    run[namespace + "/output"] = result["response"]

# Stop the run
run.stop()
