import streamlit as st
import os
import requests
import json
 
api_endpoint = 'https://stack-overflow-tags-22dfc26dd07b.herokuapp.com/'

def dashboard():
    st.title('Welcome to the Stack overflow tag prediction api')
    question = st.text_input("enter your question here")

    if st.button('submit'):

        data = {"question":question}

        response = requests.post(api_endpoint, json = data).json()
        result = response['tags']
        if result is not None:
            st.success('tags have been predicted')
            st.markdown(', '.join(result))

if __name__ == '__main__':
    dashboard()