# WebChat

WebChat is a powerful tool that extracts data from provided website links and enables question-answering based on the extracted information. Utilizing advanced AI and natural language processing techniques, WebChat delivers accurate and contextually relevant responses.

<img width="919" alt="image" src="https://github.com/usman-29/WebChat/assets/96678300/c1b0caba-29e3-4650-8261-58f60fd6308e">
<img width="931" alt="image" src="https://github.com/usman-29/WebChat/assets/96678300/107099ee-d440-46c3-97e2-4c7dc91fbdb9">
<img width="949" alt="image" src="https://github.com/usman-29/WebChat/assets/96678300/5f5dbf99-c3d7-4b64-8692-b6362093d4cf">




## Features

- **URL Validation**: Ensure the provided URLs are valid and accessible.
- **Data Extraction**: Load and process data from specified URLs.
- **Document Splitting**: Split the extracted data into manageable chunks for efficient processing.
- **Embeddings and Indexing**: Create embeddings from the data and store them in a FAISS index for quick retrieval.
- **Conversational Chain**: Generate responses to user queries based on the indexed data using Google Generative AI.

## Technologies Used

- **Python**: The core programming language for the project.
- **Flask**: A lightweight WSGI web application framework used for creating the API endpoints.
- **HTML**: Markup language for creating the web interface.
- **CSS**: Style sheet language used for describing the presentation of the web interface.
- **JavaScript**: Programming language for creating dynamic and interactive web content.


## Installation

1. To get started with WebChat, clone the repository:

    ```bash
    git clone https://github.com/usman-29/WebChat.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Dependencies

WebChat relies on the following Python libraries:

python-dotenv==1.0.1
unstructured==0.11.8
faiss-cpu==1.8.0
flask==3.0.3
langchain==0.1.20
langchain_community==0.0.38
langchain_google_genai==1.0.3
google-generativeai==0.5.2
flask-sqlalchemy==2.0.30
flask-login==0.6.3

## Contributing

Contributions are welcome! Fork the repository, make your changes, and submit a pull request.
