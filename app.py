import streamlit as st


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
    query = st.chat_input("Ask a question about the resume:")

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
        st.write("Please enter a question.")

def send_query_to_backend(query):
    # Send a POST request with a JSON payload
    response = requests.post(f"{BACKEND_URL}/ask", json={"query": query})
    return response


if __name__ == "__main__":
    main()