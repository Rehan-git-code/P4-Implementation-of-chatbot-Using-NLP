import datetime
from sklearn.linear_model import LogisticRegression
import streamlit as st
import os
import csv
from cryptography.fernet import Fernet
import json
import random
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from nltk.corpus import stopwords
import nltk
from nltk.stem import PorterStemmer
from sklearn.preprocessing import LabelEncoder

vectorizer = TfidfVectorizer()
lr_model = LogisticRegression()
nltk.download('stopwords')
with open("data.json", "r") as file:
        data = json.load(file)
intents = data['intents']
encoder = LabelEncoder()
def clean_text(text):
        stop_words=stopwords.words('english')
        stemmer=PorterStemmer()
        text = text.lower()
        text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
        words=[word for word in text.split() if word not in stop_words]
        stemmed_word=[stemmer.stem(word) for word in words]
        
        return "".join(stemmed_word)
def train_model():
    
    patterns = []
    tags = []
    responses = {}

    for intent in intents:
        for pattern in intent['patterns']:
            patterns.append(pattern)
            tags.append(intent['tag'])
        responses[intent['tag']] = intent['responses']

    patterns = [clean_text(pattern) for pattern in patterns]
    
    
    train_vectorized = vectorizer.fit_transform(patterns)
    lr_model.fit(train_vectorized, tags)
    
def generate_key():
    key = Fernet.generate_key()
    with open("key.txt", "wb") as key_file:
        key_file.write(key)
    return key

def load_key():
    if os.path.exists("key.txt"):
        with open("key.txt", "rb") as key_file:
            return key_file.read()
    else:
        return generate_key()  
def encrypt_password(password, key):
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password

def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password).decode()
    return decrypted_password

def register_user(name,username, password,phone, key):
    if not os.path.exists('users.csv'):
        
        with open('users.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name','username', 'password','Phone'])  

    with open('users.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader) 
        for row in reader:
            if row[0] == name and row[1] == username:
                return False  

   
    encrypted_password = encrypt_password(password, key)
    with open('users.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name,username, encrypted_password.decode(),phone])  
    return True

def validate_user(username, password, key):
    if not os.path.exists('users.csv'):
        return False

    with open('users.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader) 
        for row in reader:
            if row[1] == username:
                decrypted_password = decrypt_password(row[2].encode(), key)
                if decrypted_password == password:
                    
                    return row[0]
    return False
def chatbot(input_text):
    input_text = vectorizer.transform([clean_text(input_text)])
    predicted_tag = lr_model.predict(input_text)[0] 
    
    for intent in intents:
        if intent['tag'] == predicted_tag:
            response = random.choice(intent['responses'])
            return response

def chat_interface():
    global counter
    counter=0
    st.title("Pandora-Therapeutic AI Assitant ")
    st.sidebar.title(f"Welcome {st.session_state.name}")
    menu = ["Home", "Conversation History", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.write("Welcome to the chatbot. Please type a message and press Enter to start the conversation.")

        if not os.path.exists('chat_log.csv'):
            with open('chat_log.csv', 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['User Input', 'Chatbot Response', 'Timestamp'])

        counter += 1
        user_input = st.text_input("You:", key=f"user_input_{counter}")

        if user_input:

            
            user_input_str = str(user_input)

            response = chatbot(user_input)
            st.text_area("Chatbot:", value=response, height=120, max_chars=None, key=f"chatbot_response_{counter}")

            timestamp = datetime.datetime.now().strftime(f"%Y-%m-%d %H:%M:%S")

            with open('chat_log.csv', 'a', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([user_input_str, response, timestamp])

            if response and response.lower() in ['goodbye', 'bye']:
                st.write("Thank you for chatting with me. Have a great day!")
                st.stop()

    elif choice == "Conversation History":
        
        st.header("Conversation History")
        
        with open('chat_log.csv', 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  
            for row in csv_reader:
                st.text(f"User: {row[0]}")
                st.text(f"Chatbot: {row[1]}")
                st.text(f"Timestamp: {row[2]}")
                st.markdown("---")

    elif choice == "About":
        st.write("The goal of this project is to create a Pandora, a Therapeutic AI Assitant designed to assist you. The chatbot is built using Natural Language Processing (NLP) library and Logistic Regression, to extract the intents and entities from user input. The chatbot is built using Streamlit, a Python library for building interactive web applications.Authentication using the cryptography library in web applications.")

        st.subheader("Project Overview:")

        st.write("""
        The project is divided into two parts:
        1. NLP techniques and Logistic Regression algorithm is used to train the chatbot on labeled intents and entities.
        2. For building the Chatbot interface, Streamlit web framework is used to build a web-based chatbot interface. The interface allows users to input text and receive responses from the chatbot.
        3. Implement a password verification system using encryption for enhanced security.
        """)

        st.subheader("Dataset:")

        st.write("""
        The dataset used in this project is a collection of labelled intents and entities. The data is stored in a list.
        - Intents: The intent of the user input (e.g. "greeting", "about",etc)
        - Entities: The entities extracted from user input (e.g. "Hi", "What is your purpose?",etc)
        - Text: The user input text.
        """)

        st.subheader("Streamlit Chatbot Interface:")

        st.write("The chatbot interface is built using Streamlit. The interface includes a text input box for users to input their text and a chat window to display the chatbot's responses. The interface uses the trained model to generate responses to user input.")

        st.subheader("Conclusion:")

        st.write("In this project,conversational agent designed to mimic a therapist. The chatbot was trained using NLP and Logistic Regression, and the interface was built using Streamlit. This project can be extended by adding more data, using more sophisticated NLP techniques, deep learning algorithms.")

        

def authenticate():
    key = load_key()
    st.title("Pandora-Therapeutic AI Assitant ")
    

    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Select Action", menu)

    if choice == "Register":
        st.subheader("Register New Account")
        name = st.text_input("Name")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        phone = st.text_input("Phone")

        if st.button("Register"):
            if register_user(name,username, password, phone,key):
                st.success("Registration successful! Please login.")
            else:
                st.warning("Username already exists. Please try a different one.")

    elif choice == "Login":
        st.subheader("Login")
        st.write("Default Credential-Guest,Guest")
        with st.form(key='login_form'):
            username = st.text_input("Username")
            password = st.text_input("Password", type='password')

            submit=st.form_submit_button("Login")
            if submit:
                name=validate_user(username, password, key)
                if name:
                    st.success(f"Welcome {username}!")
                    st.session_state.logged_in = True
                    st.session_state.name = name
                    
                else:
                    st.warning("Invalid username or password.")

def main():
    train_model()
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.name = ""
    if st.session_state.logged_in:
        chat_interface()
    else:
        authenticate()
        

if __name__ == '__main__':
    main()
