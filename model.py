import os
import re
import requests
import pickle
from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
temp_val = 0.3


# function to validate urls
def validate_urls(url1, url2, url3):
    # Regular expression to validate URL
    regex = (
        r'^(?:http|ftp)s?://'  # http:// or https://
        # domain...
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$'
    )
    urls = []
    for url in [url1, url2, url3]:
        if url and re.match(regex, url, re.IGNORECASE):
            try:
                response = requests.head(url)
                if response.status_code == 200:
                    urls.append(url)
            except:
                return "Invalid URL: Check your URLs"
    if urls:
        return urls
    else:
        return "No valid URLs provided"


# function to process pdf and urls data
def process_data(urls, slider_value):
    global temp_val
    urls_embeddings_and_index(urls)
    temp_val = slider_value


# function to create embeddings for urls
def urls_embeddings_and_index(urls):
    # load data from urls
    loader = UnstructuredURLLoader(urls=urls)
    urls_data = loader.load()

    # Split data into documents
    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', '.', ','],
        chunk_size=1000
    )

    urls_docs = text_splitter.split_documents(urls_data)
    # Create embeddings and save it to FAISS index
    vector_store = FAISS.from_documents(urls_docs, embeddings)
    vector_store.save_local("faiss_index")

    # Save the FAISS index to a pickle file
    with open("faiss_index.pickle", "wb") as f:
        pickle.dump(vector_store, f)


# function to create conversational chain
def get_conversational_chain():

    prompt_template = """
    Conversational Chain Prompt
    Context:
    {context}
    Question:
    {question}
    Please provide a detailed and accurate response to the question based on the provided context.
    If the answer requires steps or a list, format it accordingly with each step or list item in its own <p> tag.
    Avoid providing incorrect information.
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro",
                                   temperature=temp_val)

    prompt = PromptTemplate(template=prompt_template,
                            input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain


# process user input and get response
def user_input_response(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    faiss_file = FAISS.load_local(
        "faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = faiss_file.similarity_search(user_question)

    chain = get_conversational_chain()

    response = chain(
        {"input_documents": docs, "question": user_question}, return_only_outputs=True)

    return response
