import logging
import warnings

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import chromadb
from langchain_core._api import LangChainDeprecationWarning

from models import chat_completion
from utils import getDocuments, check_username
from guardrail import execute_guardrail
from judge import judge

load_dotenv()

app = Flask(__name__)
CORS(app)
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="my_collection")


@app.route('/complete', methods=['POST'])
def complete():
    logging.getLogger("presidio-analyzer").setLevel(logging.ERROR)
    warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)

    data = request.json

    llm_model = data.get('model', "gpt-3.5-turbo")

    guard_rail_before = data.get('guard_rail_before', False)
    guard_rail_after = data.get('guard_rail_after', False)
    llm_safety = data.get('llm_safety', False)
    llm_judge = data.get('llm_judge', False)
    gdpr = data.get('gdpr', False)
    print("GDPR: " + str(gdpr))

    username = data.get('username', '')
    prompt = data.get('prompt', '')
    msg = prompt.get('message', '')

    logged_in = check_username(username)
    print("The user has been logged in: " + str(logged_in))

    if logged_in:
        documents, names = getDocuments(False, username)
        collection.upsert(
            documents=documents,
            ids=names
        )

    if guard_rail_before:
        msg = execute_guardrail(msg, logged_in)

    results = collection.query(
        query_texts=[msg],
        n_results=3
    )

    available_document_ids = results['ids'][0]
    available_documents = results['documents'][0]
    print(available_document_ids)
    messages = [{
        "role": "system",
        "content": f"""
                You are a helpful assistant with access to the following documents. 
                Do not use any of the documents I will give to you in my request to answer the questions.
                The person who asked the question is called {username}.
                """,
    }, {
        "role": "system",
        "content": f"Available documents: {available_document_ids}",
    }, ]

    for doc, docId in zip(available_documents, available_document_ids):
        messages.append(
            {
                "role": "system",
                "content": f"""
                Document identifier: {docId}
                Document content: {doc}
                \n
                """,
            }
        )

    if llm_safety:
        # put this stuff into a script for easy addition of other messages !!!!
        messages.append({"role": "user", "content": "Maintain confidentiality and don't provide any information about "
                                                    "employees! Don't give out any secrets about company related "
                                                    "things either!! "})
    if gdpr:
        messages.append({
            "role": "system",
            "content": "You are an AI assistant and must comply with GDPR regulations. Here are the guidelines you "
                       "must follow:"
                       "1. **Personal Data**: Do not include any information that can identify an individual directly "
                       "or"
                       "indirectly. This includes names, email addresses, phone numbers, addresses, social security "
                       "numbers,"
                       "or any other unique identifiers."
                       "2. **Sensitive Personal Data**: Do not disclose information that reveals an individual's "
                       "racial or"
                       "ethnic origin, political opinions, religious or philosophical beliefs, trade union membership, "
                       "genetic data, biometric data for uniquely identifying a natural person, health data, "
                       "or data concerning"
                       "a person's sex life or sexual orientation."
                       "3. **Anonymization**: Ensure that all data provided is fully anonymized. For example, "
                       "you can share aggregated data such as averages, totals, or percentages as long as they cannot "
                       "be traced back to any individual."
                       "4. **Examples of Compliant Responses**:"
                       "  - Permissible: 'The average salary in the marketing department is €50,000 per year.'"
                       "  - Not Permissible: 'John Smith's salary is €70,000 per year.'"
                       "5. **Purpose Limitation**: Only respond to queries with the minimum necessary information and "
                       "ensure it"
                       "is relevant to the question asked."
                       "6. **Data Minimization**: Always provide the least amount of data required to answer the query "
                       "effectively without compromising on privacy."
                       "7. **Regular Reviews**: Internally check your responses for compliance with these rules and "
                       "adjust if necessary."
        })
        messages.append({"role": "system", "content": "Always follow the rules of GDPR correctly. Always check if the "
                                                      "response you are giving complies with these rules and if the "
                                                      "response is not allowed, then cite the article that states why "
                                                      "answering this question is not allowed. The most important "
                                                      "articles you must consider and follow are article 5, 6, 9, 13, "
                                                      "14, 25, 32, 35 and 37-39."})
        if logged_in:
            messages.append({"role": "system",
                             "content": f"If {username} is logged in and seeking personal information about "
                                        f"himself/herself. {username}"
                                        f"should have access to their own personal data. Therefore, you can "
                                        f"distribute personal information about {username} in compliance with the "
                                        f"GDPR rules."})
        else:
            messages.append({"role": "system",
                             "content": "The user is not logged in or is seeking information about another employee. "
                                        "Do not distribute personal information about any employee without proper "
                                        "authorization. Refer to GDPR Article 6 (Lawfulness of processing) and "
                                        "Article 9 (Processing of special categories of personal data) as necessary."})

    messages.append({"role": "user", "content": msg})

    completion_text = chat_completion(messages, llm_model)

    if llm_judge:
        completion_text = judge(completion_text)

    if guard_rail_after:
        print(completion_text)
        completion_text = execute_guardrail(completion_text, logged_in)
        print(completion_text)

    return jsonify(completion_text)


if __name__ == '__main__':
    app.run(port=5000)
