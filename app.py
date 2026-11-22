
import streamlit as st

from agent import EmailAssistantAgent

from database import (
    initialize_database,
    save_draft,
    get_all_drafts,
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Email Assistant",
    page_icon="📧",
    layout="wide",
)


# --------------------------------------------------
# DATABASE INITIALIZATION
# --------------------------------------------------

initialize_database()


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "result" not in st.session_state:
    st.session_state.result = None

if "original_input" not in st.session_state:
    st.session_state.original_input = ""

if "current_action" not in st.session_state:
    st.session_state.current_action = ""

if "saved_message" not in st.session_state:
    st.session_state.saved_message = ""


# --------------------------------------------------
# LOAD AI AGENT
# --------------------------------------------------

@st.cache_resource
def load_agent():

    return EmailAssistantAgent(
        model_name="llama3.2:3b",
        temperature=0.1,
        base_url="http://localhost:11434",
    )


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title("📧 Email Assistant")

    st.caption("Agentic AI | Local LLM | SQLite")

    st.divider()

    st.subheader("Saved Draft History")

    try:

        saved_records = get_all_drafts()

        if not saved_records:

            st.info("No saved records available yet.")

        else:

            for record in saved_records:

                title = (
                    record["subject"]
                    or record["category"]
                    or record["action"].replace("_", " ").title()
                )

                with st.expander(
                    f"#{record['id']} - {title}"
                ):

                    st.write(
                        "**Action:**",
                        record["action"].replace("_", " ").title()
                    )

                    if record["subject"]:
                        st.write("**Subject:**")
                        st.write(record["subject"])

                    if record["body"]:
                        st.write("**Body:**")
                        st.write(record["body"])

                    if record["category"]:
                        st.write("**Category:**")
                        st.write(record["category"])

                    if record["reason"]:
                        st.write("**Reason:**")
                        st.write(record["reason"])

                    st.caption(
                        f"Created: {record['created_at']}"
                    )

    except Exception as error:

        st.error(f"Database error: {error}")

    st.divider()

    st.caption("Local AI Model: llama3.2:3b")

    st.caption("Database: SQLite")


# --------------------------------------------------
# MAIN PAGE
# --------------------------------------------------

st.title("📧 AI Email Assistant Agent")

st.write(
    "Create professional email drafts, suggest replies, "
    "and categorize messages using a locally running AI model."
)

st.caption(
    "Powered by Python, Streamlit, LangChain, Ollama and SQLite."
)

st.divider()


# --------------------------------------------------
# USER INPUT
# --------------------------------------------------

st.subheader("Enter Your Email Request")

selected_action = st.selectbox(
    "Choose an action",
    [
        "Auto Detect",
        "Generate Email",
        "Suggest Reply",
        "Categorize Email",
    ],
)

user_input = st.text_area(
    "Enter your instruction or paste an incoming email",
    height=180,
    placeholder=(
        "Example: Write a professional email to my manager "
        "requesting one day leave due to personal work."
    ),
)


# --------------------------------------------------
# GENERATE BUTTON
# --------------------------------------------------

if st.button(
    "✨ Generate",
    type="primary",
    use_container_width=True,
):

    if not user_input.strip():

        st.warning("Please enter an instruction or email.")

    else:

        try:

            with st.spinner(
                "AI assistant is processing your request..."
            ):

                assistant = load_agent()

                result = assistant.run(
                    user_input=user_input,
                    selected_action=selected_action,
                )

            st.session_state.result = result

            st.session_state.original_input = user_input.strip()

            st.session_state.current_action = result.get(
                "action",
                ""
            )

            st.session_state.saved_message = ""

            if result.get("action") in [
                "generate_email",
                "suggest_reply",
            ]:

                st.session_state.draft_subject = result["subject"]

                st.session_state.draft_body = result["body"]

            st.rerun()

        except Exception as error:

            st.error(
                f"Unable to process your request: {error}"
            )

            st.info(
                "Check that Ollama is running and that "
                "llama3.2:3b is installed."
            )


# --------------------------------------------------
# DISPLAY RESULT
# --------------------------------------------------

result = st.session_state.result

if result:

    st.divider()

    st.subheader("AI Assistant Result")

    action = result.get("action", "")

    if action == "unclear":

        st.warning(result.get("message", "Please clarify your request."))

    elif action in [
        "generate_email",
        "suggest_reply",
    ]:

        if action == "generate_email":

            st.success("Email draft generated successfully.")

        else:

            st.success("Email reply generated successfully.")

        st.text_input(
            "Email Subject",
            key="draft_subject",
        )

        st.text_area(
            "Email Body",
            key="draft_body",
            height=280,
        )

        if st.button(
            "💾 Save Draft",
            type="primary",
            use_container_width=True,
        ):

            subject = st.session_state.draft_subject.strip()

            body = st.session_state.draft_body.strip()

            if not subject or not body:

                st.warning(
                    "Subject and email body cannot be empty."
                )

            else:

                try:

                    save_draft(
                        action=action,
                        original_input=st.session_state.original_input,
                        subject=subject,
                        body=body,
                    )

                    st.session_state.saved_message = (
                        "Draft saved successfully in SQLite."
                    )

                    st.rerun()

                except Exception as error:

                    st.error(
                        f"Unable to save draft: {error}"
                    )

        if st.session_state.saved_message:

            st.success(st.session_state.saved_message)

    elif action == "categorize_email":

        category = result.get("category", "")

        reason = result.get("reason", "")

        st.subheader("Email Classification")

        st.metric(
            label="Predicted Category",
            value=category,
        )

        st.write("**Reason:**")

        st.write(reason)

        if st.button(
            "💾 Save Classification",
            type="primary",
            use_container_width=True,
        ):

            try:

                save_draft(
                    action=action,
                    original_input=st.session_state.original_input,
                    category=category,
                    reason=reason,
                )

                st.session_state.saved_message = (
                    "Classification saved successfully in SQLite."
                )

                st.rerun()

            except Exception as error:

                st.error(
                    f"Unable to save classification: {error}"
                )

        if st.session_state.saved_message:

            st.success(st.session_state.saved_message)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "AI Email Assistant Agent | Xpert Champs AI Engineering Internship Project"
)

st.caption(
    "All generated emails are drafts. This application does not send emails."
)
