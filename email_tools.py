
import json
import re

from prompts import (
    GENERATE_EMAIL_PROMPT,
    REPLY_EMAIL_PROMPT,
    CATEGORIZE_EMAIL_PROMPT,
    SUPPORTED_CATEGORIES,
)


def invoke_model(llm, prompt):
    """Send a prompt to the local Ollama model."""

    try:
        response = llm.invoke(prompt)
        content = response.content

        if not isinstance(content, str):
            raise ValueError("The AI returned an unsupported response.")

        if not content.strip():
            raise ValueError("The AI returned an empty response.")

        return content.strip()

    except Exception as error:
        raise RuntimeError(
            f"Unable to communicate with the local AI model: {error}"
        ) from error


def parse_json_response(response_text):
    """Extract a JSON object from the model response."""

    if not isinstance(response_text, str) or not response_text.strip():
        raise ValueError("The AI returned an empty response.")

    cleaned = response_text.strip()

    cleaned = re.sub(
        r"^```(?:json)?\s*",
        "",
        cleaned,
        flags=re.IGNORECASE
    )

    cleaned = re.sub(r"\s*```$", "", cleaned)

    decoder = json.JSONDecoder()

    for index, character in enumerate(cleaned):
        if character == "{":
            try:
                data, _ = decoder.raw_decode(cleaned[index:])

                if isinstance(data, dict):
                    return data

            except json.JSONDecodeError:
                continue

    raise ValueError(
        "Invalid JSON response received from the AI model. Please try again."
    )


def generate_email(llm, user_input):
    """Generate a new email draft."""

    prompt = GENERATE_EMAIL_PROMPT.format(
        user_input=user_input
    )

    response = invoke_model(llm, prompt)
    data = parse_json_response(response)

    subject = data.get("subject")
    body = data.get("body")

    if not isinstance(subject, str) or not subject.strip():
        raise ValueError("The AI did not generate a valid email subject.")

    if not isinstance(body, str) or not body.strip():
        raise ValueError("The AI did not generate a valid email body.")

    return {
        "subject": subject.strip(),
        "body": body.strip(),
    }


def suggest_reply(llm, incoming_email):
    """Prepare a reply draft for an incoming email."""

    prompt = REPLY_EMAIL_PROMPT.format(
        user_input=incoming_email
    )

    response = invoke_model(llm, prompt)
    data = parse_json_response(response)

    subject = data.get("subject")
    body = data.get("body")

    if not isinstance(subject, str) or not subject.strip():
        raise ValueError("The AI did not generate a valid reply subject.")

    if not isinstance(body, str) or not body.strip():
        raise ValueError("The AI did not generate a valid reply body.")

    return {
        "subject": subject.strip(),
        "body": body.strip(),
    }


def categorize_email(llm, email_content):
    """Classify an email into Work, Personal, or Urgent."""

    prompt = CATEGORIZE_EMAIL_PROMPT.format(
        user_input=email_content
    )

    response = invoke_model(llm, prompt)
    data = parse_json_response(response)

    category = data.get("category")
    reason = data.get("reason")

    if not isinstance(category, str):
        raise ValueError("The AI returned an invalid category.")

    category = category.strip().title()

    if category not in SUPPORTED_CATEGORIES:
        raise ValueError(
            f"The AI returned an unsupported category: {category}"
        )

    if not isinstance(reason, str) or not reason.strip():
        raise ValueError("The AI did not provide a classification reason.")

    return {
        "category": category,
        "reason": reason.strip(),
    }
