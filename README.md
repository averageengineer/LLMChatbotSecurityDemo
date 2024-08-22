# Security of LLM Based Chatbots

## Introduction

This project serves as a demonstration for companies interested in leveraging Large Language Models (LLMs) for chatbot applications, particularly for tasks related to Human Resources (HR). The demo illustrates the impact of different security layers on the ability of users to extract sensitive information through the chatbot.

### Objectives
- **Security Demonstration**: The primary goal of this demo is to showcase how various security measures can complicate attempts to extract sensitive information. 
While these security layers add significant hurdles, the project also highlights that with cleverly designed adversarial prompts, it is still possible to bypass some of these safeguards.
- **GDPR Compliance Study**: An additional aspect of the project examines how well LLMs used in these chatbots comprehend and apply GDPR regulations. This is tested by feeding the LLMs relevant articles from the GDPR and explicitly instructing them to apply the rules.

## How to run the project
### Getting Started
Before using this project, you'll need to install the necessary dependencies. To do this, please install the packages listed in the `requirements.txt` file.

Next, you'll need to configure the environmental variables specified in the `.env` file. Be sure to fill in all the variables except for `NEPTUNE_PROJECT_NAME` and `NEPTUNE_API_KEY`, as these are only required if you plan to track experimental adversarial prompts.

### Running the Project
Once the environmental variables and dependencies are set up, you can start the backend. To do this, run the `chatbot_dangerous` script. This will launch the backend, which implements the security layers and all necessary components for generating responses to user queries.

With the backend running, you can start the front-end by executing `npm start` in a terminal. This will open a simple login page. You can bypass the login screen by entering any employee name, such as "Brill, Donna" or "Brown, Mia."

After logging in, you'll see the main user interface (UI) used for testing. On the left side, you can explore the different security layers, along with additional information, and select the Large Language Models (LLMs) available for testing.

## How to use the project
To start off with, one can try and ask some standard questions regarding private information about other employees such as salaries, contact details, health issues, performance scores, etc.
Toggling the different security layers will complicate things if one wishes to extract private data. The point is to try and find ways to bypass these security layers with sophisticated prompts and try to get the LLM to give you sensitive information on multiple employees.
For some knowledge on the exact information contained in the database, see [Database](#Database).


## Security Layers

`LLMBasedSecurity`: This approach is based on explicitly instructing the LLM not to disclose private information about any employees other than the one currently logged in.

`GuardrailsPrior`: This approach is based on applying guardrails to the user prompts, specifically targeting the questions asked by the user. Currently, these guardrails are designed to scan for names, email addresses, and phone numbers.

`GuardrailsAfter`: This approach involves applying guardrails to the LLM's responses to user queries. Currently, these guardrails focus on scanning for names, email addresses, and phone numbers.

`LLMJudge`: This involves making a second call to a different LLM to determine whether the response from the initial LLM contains any private information.

`GDPR`: This is not a security layer but rather a mode for testing whether the LLM can understand and apply the relevant GDPR rules concerning employee data in the database.

## Database
The database is composed of a fictional HR dataset sourced from Kaggle as we would not wish to leak non-fictional sensitive information. ([Database License](#database-license))

Employee records are stored in text files located in the `documents/private` directory. These records include extended information such as health issues and political opinions, which are considered sensitive personal data under Article 9 of the GDPR.

Company-wide data is stored in the `documents/company-wide` directory and includes both general public information and private details such as credentials, departmental salaries, and trade secrets.

## Future Work

The set of guardrails used in the `chatbots/guardrails.py` is rather minimal and is utterly used to symbolize the possibility of bypassing these. Extending this set of guardrails would obviously complicate extraction of private data, however this should not take away the fact that one can bypass them with sophisticated prompts.

The LLM Judge (`chatbot/judge.py`) uses a second call to an alternative LLM, however for now only the response of the LLM is passed to the second LLM and not the query of the user. Extending this would boost the effectiveness of the LLM Judge. 

The security layer `GDPR` is based on explicitly instructing the LLM to use keep in mind specific rules of the GDPR and feeding the LLM specific articles relevant for the employee data. However, training an LLM specifically for GDPR understanding would have different conclusions than the ones you would make out of this demo.

## Notable Links
`EvilBOT, jailbreaking ChatGPT`: https://gist.github.com/sertdfyguhi/4e291776fe95b975becf468e762a28e7

`Medium Post with some interesting adversarial prompts for specific entities`: https://denizsivas.medium.com/prompt-injection-challenge-how-far-can-you-go-9d78c18df51d

`Paper used for inspiration for common thread of the demonstration`: https://arxiv.org/pdf/2307.15043

## Medium Blogs

`Security LLM Based Chatbots Medium Blog`: https://medium.com/@maxvanrompaey/the-double-edged-sword-of-llm-based-chatbots-3463c01dcc66

`LLM's Understanding of GDPR Rules Medium Blog`: https://medium.com/@maxvanrompaey/llm-problems-for-gdpr-understanding-b0c5ce25de86


## Database License
Dataset: Human Resources Data Set

License: Data files © Original Authors

Attribution: Dataset provided by Dr. Richard A. Huebner 

(Kaggle link: https://www.kaggle.com/datasets/rhuebner/human-resources-data-set?resource=download)

