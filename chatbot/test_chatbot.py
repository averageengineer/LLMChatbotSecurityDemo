import time
import requests

url = 'http://127.0.0.1:5000/complete'


def test_chatbot(adversarial_prompts, guard_rail_before=False, guard_rail_after=False, llm_safety=False,
                 model="gpt-3.5-turbo", judge=False):
    results = []
    username = 'Brill, Donna'
    for prompt in adversarial_prompts:
        message = {
            'message': prompt,
            'sender': "user",
            'direction': "outgoing",
        }
        start_time = time.time()
        payload = {
            'username': username,
            'prompt': message,
            'guard_rail_before': guard_rail_before,
            'guard_rail_after': guard_rail_after,
            'llm_safety': llm_safety,
            'model': model,
            'llm_judge': judge,
        }
        response = requests.post(url, json=payload)
        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        results.append({
            'prompt': prompt,
            'response': response.text,
            'response_time': response_time
        })
    return results
