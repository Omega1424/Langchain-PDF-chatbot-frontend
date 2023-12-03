import streamlit as st
import json
from streamlit_lottie import st_lottie 
import requests

BACKEND_URL = "https://langchainpdfchatbot.azurewebsites.net"  # replace with your backend's URL

def main():
    st.title("ResumeGPT")

    #Initializing chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    # Take user input
    query = st.chat_input("Enter question here:")

    # When 'Get Answer' button is clicked

    if query:
        # Send a POST request to the /ask endpoint with the user's query
        st.session_state.messages.append({"role": "user", "content": query})
        response = send_query_to_backend(query)
        with st.chat_message("user"):
            st.write(f'{query}')
        with st.chat_message("assistant"):
            if response.status_code == 200:

                st.write(f'{response.json().get("Answer")}')
            else:
                st.write(f'Error: {response.text}')
        st.session_state.messages.append({"role": "assistant", "content": response.json().get("Answer")})
    else:
        st.write("Ask me something about my resume!")

def send_query_to_backend(query):
    # Send a POST request with a JSON payload
    response = requests.post(f"{BACKEND_URL}/ask", json={"query": query})
    return response

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
lottie_waiting = load_lottiefile('Aniki_Hamster.json')
if __name__ == "__main__":
    main()
    st_lottie(
        lottie_waiting,
        speed=1
        reverse=False,
        loop=True,
        quality='medium'
    )