from openai import OpenAI
import streamlit as st

st.title("GPTeacher")
st.write("Welcome! This is an English teaching assistant chatbot.")
st.write("Feel free to ask questions about English grammar, vocabulary, writing tips, or any English-related topic.")

client = OpenAI(api_key="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")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

initial_prompt = "Act like an English teacher."
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": initial_prompt}]

# st.session_state.messages = [{"role": "assistant", "content": initial_prompt}]

for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What would you like to learn about English today"):
#if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            # full_response += (response.choices[0].delta.content or "")
            # message_placeholder.markdown(full_response + "▌")
            assistant_message = response.choices[0].delta.content or ""
            full_response += assistant_message
            message_placeholder.markdown(full_response + "▌")
            
            # Check if the user's query contains specific keywords
            user_input = st.session_state.messages[-1]["content"].lower()
            if "grammar" in user_input or "rules" in user_input:
                explanation = "Sure, let's talk about grammar rules. Grammar refers to the structure of language, including syntax, punctuation, and more. Are you looking for information about a specific grammar rule?"
                full_response += explanation
                message_placeholder.markdown(full_response + "▌")
                break 
            if "vocabulary" in user_input or "word" in user_input:
                explanation = "Certainly! Vocabulary refers to the words used in a language. Building a strong vocabulary is essential for effective communication. Are you looking for help with learning new words or understanding specific vocabulary terms?"
                full_response += explanation
                message_placeholder.markdown(full_response + "▌")
                break
            if "writing" in user_input or "tips" in user_input:
                explanation = "Sure! Writing effectively involves clear communication, organization, and expression of ideas. Are you seeking guidance on structuring essays, improving sentence structure, or enhancing overall writing skills?"
                full_response += explanation
                message_placeholder.markdown(full_response + "▌")
                break 
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})