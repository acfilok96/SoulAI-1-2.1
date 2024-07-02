## OCR Details & Summarization Load on Database

-  **About:** This application has been designed to facilitate information extraction from images, leveraging advanced retrieval augmented generation capabilities, supported by the large language model Llama3-70.

-  **Generator Model:** Llama3, `llama3-70b-8192` model with 70b parameter.
-  **Embedding Model:**  `BAAI/bge-base-en-v1.5` from `FastEmbedEmbeddings`

## Folder Set up

`Folder`

  `├──── .streamlit`
  
  `|       ├──── config.toml`
  
  `├── Image_Record_SQLDB.db`
  
  `├── app.py`

  `├──functions.py`

  `├──functions_2.py`
  
  `├── requirements.txt`

Download the `Folder` file & open `Visual Studio Code` into `Folder`. Open  `terminal` and run there

-  **Run on terminal:**
  
\> `streamlit run app.py`

## Application Link

- **Proof Of Concept:** [OCRLLM.app](https://task-dp-a8fyzuu3g7venkwbge7ac7.streamlit.app/)

## Set up API Keys 🔗
Change the Groq API Key `GROQ_API_KEY`, LlamaPaser API Key `LLAMA_PARSE_API_KEY` & HuggingFace API Token `HF_TOKEN` inside the function of the python files  `function.py` & `function_2.py`. 

- **Generate Groq API Key:** [Groq Playground](https://console.groq.com/keys)
- **HuggingFace API Key:** [HuggingFace Access Token](https://huggingface.co/settings/tokens)
- **LlamaCloud API Key:** [LLamaCloud](https://cloud.llamaindex.ai/api-key)
 
