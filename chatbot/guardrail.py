import tempfile

from guardrails import Guard
from guardrails.hub import DetectPII, SecretsPresent, UnusualPrompt
import subprocess


class SecretDetectedException(Exception):
    def __init__(self, secrets, message="Secrets detected in the input"):
        self.secrets = secrets
        self.message = message
        super().__init__(self.message)


def execute_guardrail(msg, logged_in):
    sensitive_entities_map = {
        True: ["PERSON"],
        False: ["EMAIL_ADDRESS", "PHONE_NUMBER", "PERSON"]
    }

    sensitive_entities = sensitive_entities_map.get(logged_in, [])

    guard_pii = Guard().use(DetectPII, sensitive_entities, "exception")
    guard_unusual = Guard().use(UnusualPrompt, on="prompt", on_fail="exception")
    guard_secrets = Guard().use(SecretsPresent, "exception")
    try:
        print(msg)
        guard_pii.validate(msg)
        guard_unusual.validate(msg)
        #detect_prompt_injection(msg)
        if not logged_in:
            guard_secrets.validate(msg)
            #secrets = scan_text_for_secrets(msg)
        return msg
    except SecretDetectedException as e:
        print(f"Secrets detect: {e.secrets}")
        return "I'm sorry I can't answer this question as this would break the policies of keeping secrets."
    except Exception as e:
        print(e)
        return "I'm sorry I can't answer this question as this would break the policies of confidentiality and privacy."


def scan_text_for_secrets(text):
    with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_file:
        temp_file.write(text)
        temp_file_path = temp_file.name

    result = subprocess.run(['ggshield', 'scan', 'path', temp_file_path], capture_output=True, text=True)
    secrets = result.stdout

    if "No secrets found" not in secrets:
        raise SecretDetectedException(secrets)

    return secrets
