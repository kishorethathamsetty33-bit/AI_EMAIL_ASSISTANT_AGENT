
from langchain_ollama import ChatOllama

from prompts import TASK_IDENTIFICATION_PROMPT

from email_tools import (
    parse_json_response,
    generate_email,
    suggest_reply,
    categorize_email,
)


class EmailAssistantAgent:

    def __init__(
        self,
        model_name="llama3.2:3b",
        temperature=0.1,
        base_url="http://localhost:11434",
        **kwargs
    ):

        self.model_name = model_name

        self.llm = ChatOllama(
            model=model_name,
            temperature=temperature,
            base_url=base_url,
            format="json",
        )

    def identify_task(self, user_input):

        prompt = TASK_IDENTIFICATION_PROMPT.format(
            user_input=user_input
        )

        response = self.llm.invoke(prompt)

        data = parse_json_response(response.content)

        action = data.get("action")

        allowed_actions = {
            "generate_email",
            "suggest_reply",
            "categorize_email",
            "unclear",
        }

        if not isinstance(action, str):
            raise ValueError("The AI did not return a valid action.")

        action = action.strip().lower()

        if action not in allowed_actions:
            raise ValueError("The AI returned an unsupported action.")

        return action

    def run(self, user_input, selected_action="Auto Detect"):

        if not isinstance(user_input, str) or not user_input.strip():
            raise ValueError("Please enter an instruction or email.")

        user_input = user_input.strip()

        action_mapping = {
            "Generate Email": "generate_email",
            "Suggest Reply": "suggest_reply",
            "Categorize Email": "categorize_email",
        }

        if selected_action == "Auto Detect":
            action = self.identify_task(user_input)

        else:
            action = action_mapping.get(selected_action)

            if action is None:
                raise ValueError("Please select a valid action.")

        if action == "unclear":
            return {
                "action": "unclear",
                "message": (
                    "I could not identify your request. "
                    "Please ask me to generate an email, "
                    "suggest a reply, or categorize an email."
                ),
            }

        if action == "generate_email":
            result = generate_email(self.llm, user_input)

        elif action == "suggest_reply":
            result = suggest_reply(self.llm, user_input)

        elif action == "categorize_email":
            result = categorize_email(self.llm, user_input)

        else:
            raise ValueError("Unsupported agent action.")

        return {
            "action": action,
            **result,
        }
