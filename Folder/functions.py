import streamlit as st 
 
import nest_asyncio
nest_asyncio.apply()

import os, tempfile, base64

from langchain.schema import Document 
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from llama_parse import LlamaParse

from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import img2pdf
# from PIL import Image
import os
from groq import Groq


def GroqSummary(user_prompt):
  
  GROQ_API_KEY = str("Enter Groq API Key")

  system_promot = f"""Your task is to generate a summary of the information in the document. \
  Try to specific about your response. Do not share any additional information. \
  Share only exact response, nothing extra, nothing else."""
  
  groq_model = Groq(api_key = str(GROQ_API_KEY))
  
  response = groq_model.chat.completions.create(
        model = "llama3-70b-8192",
        messages=[
            {"role": "system","content": str(system_promot)},
            {"role": "user","content": str(user_prompt)}],
        temperature = 0.2,
        max_tokens = 3024,
        top_p = 1,
        stream = False,
        stop = None
      )
  return response.choices[0].message.content



def DocSpliting(image_file):
    # try:
        
    instruction = f"""The provided document is a resume or letter. This document provides detailed \
                    tabular information about the profile. It may include unaudited financial \
                    statements, management discussion and analysis, and other relevant disclosures. \
                    It may contains tables. Try to be precise while answering the questions. \
                    Share only exact response, nothing extra, nothing else."""
    
    LLAMA_PARSE_API_KEY = str("Enter LlamaParse API Key")

    parser = LlamaParse(
                        api_key = LLAMA_PARSE_API_KEY,
                        result_type = "markdown",
                        parsing_instruction = instruction,
                        max_timeout = 5000,
                    )
    ############################################
    # st.write("In doc splitting image")
    # Check
    # image_s = Image.open(image_file)
    pdf_bytes = img2pdf.convert(image_file.getvalue())

    # file_1 = open(str("temp")+str(".pdf"), "wb")
    # file_1.write(pdf_bytes)
    
    temp_dir = tempfile.mkdtemp()
    path = os.path.join(temp_dir, str("tempjpg.pdf"))
    with open(path, "wb") as f:
        f.write(pdf_bytes)
    # Check
    ##############################################
        
    llama_parse_documents = parser.load_data(path)
    parsed_doc = llama_parse_documents[0]

    loaded_documents = Document(page_content = parsed_doc.text,
                                metadata = {"source" : "A delivery chalan or invoice."})
    loaded_documents = [loaded_documents]

    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 2000, chunk_overlap = 400)
    docs = text_splitter.split_documents(loaded_documents)
    return docs
            
    # except Exception as e:
    #     st.warning("Corrupted Data or Load Data Again @ DocSpliting!")
    #     return None
        
        
def DocDatabase(docs):
    # try:
    HF_TOKEN = str("Enter HuggingFace API Key")
    embeddings = FastEmbedEmbeddings(model_name = "BAAI/bge-base-en-v1.5")

    database = FAISS.from_documents(docs, embeddings)
    return database
    
    # except Exception as e:
    #     st.warning("Corrupted Data or Load Data Again @ DocDatabase!")
    #     return None

def DocRetriever(database):
    # try:
    retriever = database.as_retriever(search_kwargs = {"k" : 5})
    return retriever 
    
    # except Exception as e:
    #     st.warning("Corrupted Data or Load Data Again @ DocRetriever!")
    #     return None
    
def DocModel():
    # try:
    GROQ_API_KEY = str("Enter Groq API Key")
    llm = ChatGroq(temperature = 0,
                    model_name = "llama3-70b-8192",
                    groq_api_key = GROQ_API_KEY,
                    max_tokens = 3024)

    prompt_template = """
    Use the following pieces of information to answer the user's question.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    Context: {context}
    Question: {question}

    Answer the question and provide additional helpful information,
    based on the pieces of information, if applicable. Be succinct.

    Responses should be properly formatted to be easily read.
    """

    prompt = PromptTemplate(template = prompt_template,
                            input_variables = ["context", "question"])
    return [llm, prompt]
    
    # except Exception as e:
    #     st.warning("Corrupted Data or Load Data Again @ DocModel!")
    #     return None
    
def DocRetrievalQA(llm, prompt, compression_retriever):
    # try:
    qa = RetrievalQA.from_chain_type(
                llm = llm,
                chain_type = "stuff",
                retriever = compression_retriever,
                return_source_documents = True,
                chain_type_kwargs = {"prompt" : prompt, "verbose" : False},
            )
    return qa
    
    # except Exception as e:
    #     st.warning("Corrupted Data or Load Data Again @ DocRetrievalQA!")
    #     return None
    
    
def DocResponseGeneration(qa):
    # with st.spinner(":green[Typing . . . ]"):
    user_prompt = f"""Share the information of the document. \
                    Try to specific about your response. Do not share any additional information. \
                    Share only exact response, nothing extra, nothing else."""
    # try:
    response = qa.invoke(str(user_prompt))
    return response["result"]
    
    # except Exception as e:
    #     st.warning("Corrupted Data or Load Data Again @ DocResponseGeneration!")
    #     return None
    
def mainFunc(images):
    # try:
    qa = None
    with st.spinner(":green[Loading document . . . ]"):
        docs = DocSpliting(images)
        database = DocDatabase(docs)
        compression_retriever = DocRetriever(database)
        [llm, prompt] = DocModel()
        qa = DocRetrievalQA(llm, prompt, compression_retriever)
        details_response = DocResponseGeneration(qa)
        summary_response = GroqSummary(details_response)
    return details_response, summary_response
    # except Exception as e:
    #     st.warning("Corrupted Data or Load Data Again @ mainFunc!")
    #     return None
