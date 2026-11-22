
# AI Email Assistant Agent

## Project Information

- Organization: Xpert Champs
- Project Category: Agentic AI / Email Productivity
- Project Name: AI Email Assistant Agent
- Language: Python

## 1. Project Overview

The AI Email Assistant Agent is a web application that helps users
generate professional email drafts, suggest replies to incoming
emails and categorize email messages.

The application uses a locally running Large Language Model through
Ollama. It does not require a paid API subscription.

## 2. Technologies Used

- Python
- Streamlit
- Ollama
- Llama 3.2
- LangChain
- SQLite
- Git
- GitHub

## 3. Main Features

1. Automatic task identification.
2. Professional email generation.
3. Incoming email reply suggestions.
4. Email categorization.
5. Editable email drafts.
6. SQLite draft storage.
7. Saved draft history.
8. Input validation.
9. AI response validation.
10. Local LLM error handling.

## 4. Project Architecture

User Input
    |
    v
Streamlit Interface
    |
    v
Agent Controller
    |
    v
Task Identification
    |
    v
Action Selection
    |
    v
LangChain + Ollama
    |
    v
Local LLM
    |
    v
Generated Result
    |
    v
Draft Editing
    |
    v
SQLite Database

## 5. Installation

Install Python 3.11 and Ollama.

Download the model:

    ollama pull llama3.2:3b

Create a virtual environment:

    py -3.11 -m venv .venv

Activate it:

    .venv\Scripts\activate

Install dependencies:

    python -m pip install -r requirements.txt

## 6. Run the Application

    streamlit run app.py

Open:

    http://localhost:8501

## 7. Database

SQLite is used to store:

- Draft ID
- Action
- Original user input
- Email subject
- Email body
- Category
- Classification reason
- Creation timestamp

## 8. Limitations

- The application requires Ollama and a locally downloaded model.
- Generation speed depends on system hardware.
- AI responses should be reviewed before use.
- Emails are saved as drafts and are not automatically sent.

## 9. Conclusion

The project demonstrates a basic agentic AI workflow through
task identification, action routing, local LLM interaction,
response validation, editable drafts and persistent SQLite storage.
