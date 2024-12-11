
# Chatbot using NLP

## Overview
The goal of this project is to create a Pandora, a Therapeutic AI Assitant designed to assist you. The chatbot is designed to understand user intents and provide appropriate responses based on predefined patterns and responses. It utilizes the `nltk` library for natural language processing, `scikit-learn` for machine learning, and `streamlit` for creating an interactive web interface.Authentication using the cryptography library in web applications.

---

## Features
- Understands various user intents such as greetings, about, medical fact, and more.
- Provides relevant responses based on user input.
- Maintains a conversation history that can be viewed by the user.
- Built using Python and leverages popular libraries for NLP and machine learning.

---

## Technologies Used
- **Python**
- **NLTK**
- **Scikit-learn**
- **Streamlit**
- **cryptography**
- **JSON** for intents data

---

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Required Packages
```bash
pip install -r requirements.txt
```

### 4. Download NLTK Data
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')

```

---

## Usage
To run the chatbot application, execute the following command:
```bash
streamlit run app.py
```

Once the application is running, you can interact with the chatbot through the web interface. Type your message in the input box and press Enter to see the chatbot's response.

---

## Intents Data
The chatbot's behavior is defined by the `data.json` file, which contains various tags, patterns, and responses. You can modify this file to add new intents or change existing ones.

---

## Conversation History
The chatbot saves the conversation history in a CSV file (`chat_log.csv`). You can view past interactions by selecting the "Conversation History" option in the sidebar.

---
## User Data
The chatbot saves the user data in a CSV file (`users.csv`).Login key is stored in TXT file(`key.txt`)

---
## Contributing
Contributions to this project are welcome! If you have suggestions for improvements or features, feel free to open an issue or submit a pull request.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments
- **NLTK** for natural language processing.
- **Scikit-learn** for machine learning algorithms.
- **Streamlit** for building the web interface.
- **cryptography** for authenticate users in the web interface.
---

Replace `<repository-url>` and `<repository-directory>` with the actual URL of your repository and the name of the directory where the project is located. Adjust any sections as necessary to better fit your project's specifics.
