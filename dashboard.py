import streamlit as st
import os
import requests
import json

# URL de l'API locale
api_endpoint = 'https://git.heroku.com/sof-test.git/tag_prediction'

# Fonction principale de l'application Streamlit
def dashboard():
    # Titre de l'application
    st.title('Welcome to the Stack Overflow Tag Prediction API')
    
    # Champ de saisie pour la question
    question = st.text_input("Enter your question here")

    # Bouton pour soumettre la question
    if st.button('Submit'):
        # Préparation des données à envoyer à l'API
        data = {"question": question}

        # Appel de l'API en utilisant la bibliothèque requests
        response = requests.post(api_endpoint, json=data)

        # Vérification de la réponse de l'API
        if response.status_code == 200:
            # Récupération des tags prédits depuis la réponse JSON
            result = response.json().get('tags')

            # Vérification si des tags ont été prédits
            if result:
                st.success('Tags have been predicted:')
                # Affichage des tags prédits sous forme de liste
                st.markdown(', '.join(result))
            else:
                st.warning('No tags were predicted for this question.')
        else:
            st.error('Error: Unable to connect to the prediction API.')

if __name__ == '__main__':
    # Appel de la fonction principale pour lancer l'application Streamlit
    dashboard()

#         response = requests.post(api_endpoint, json = data).json()
#         result = response['tags']
#         if result is not None:
#             st.success('tags have been predicted')
#             st.markdown(', '.join(result))

# if __name__ == '__main__':
#     dashboard()



