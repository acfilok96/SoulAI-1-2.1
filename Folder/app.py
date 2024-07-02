import streamlit as st
from functions import *
from functions_2 import *

st.set_page_config(page_title="Load Data", layout="wide", initial_sidebar_state = 'auto')

# filename = st.text_input(":blue[**File Name**]", placeholder = "Enter here") 
# summary = st.text_input(":blue[**Summary**]", placeholder = "Enter here")

st.markdown("""
<style>
.big-font-1 {
    font-size:30px !important;
    text-align: center; 
    color: yellow
}
</style>
""", unsafe_allow_html = True)

st.markdown('<p class = "big-font-1">OCR Details & Summarization Load on Database</p>', unsafe_allow_html = True)


images = st.file_uploader(":blue[Upload Photo]", type = ["png","jpg","jpeg"], accept_multiple_files = False)
if images:
    st.success("Image Uploded!")
    



col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Load Database"):
        try:
            if images:
                store_image_summary(images)
                st.success("Loaded!")
        except Exception as e:
            st.warning("Corrupted Data or Load Data Again @ Load Database!")
        
with col2:
    if st.button("Show Database"):
        try:
            with st.container(height = 350, border = False):
                database = "Image_Record_SQLDB.db"
                sql_query = "SELECT * FROM Image_Record_SQLDB_TABLE"
                data = read_sql_databse(database, sql_query)
                data = [i for i in data]
                st.info(data)
        except Exception as e:
            st.warning("Corrupted Data or Load Data Again @ Load Database!")

with col3:
    # database = "Image_Record_SQLDB.db"
    # sql_query = "SELECT * FROM Image_Record_SQLDB_TABLE"
    # data = read_sql_databse(database, sql_query)
    # if data:
    downloadData()


with col4:
    if st.button("View Data Summary"):
        try:
            with st.container(height = 350, border = False):
                with st.spinner(":green[Loading . . .]"):
                    result = watchSummary()
                    st.info(result)
        except Exception as e:
            st.warning("Corrupted Data or Load Data Again @ main!")
        
