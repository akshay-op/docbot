import os
import sys
sys.path.insert(0, 'C:\\Users\\USER\\Documents\\python projects\\docbot')
from src.logger import logging
from src.exception import CustomException
from src.model import LLMmodel
import pandas as pd
import streamlit as st
from PyPDF2 import PdfReader
from src.components.data_read import DataRead

st.set_page_config(initial_sidebar_state="collapsed")
from streamlit_extras.stylable_container import *
from streamlit_extras.switch_page_button import switch_page
import streamlit_scrollable_textbox as stx

if __name__=="__main__":

    st.title("PDF Data bot")
    st.write("Upload a PDF file to read its content.")

    obj = DataRead()
    

    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        # Save the uploaded file to a temporary location
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())
        obj.datapath = "temp.pdf"
        document = obj.getdata()
        

        llm_model_instance = LLMmodel(document)
        st.session_state['LLMmodel'] = llm_model_instance
        db = llm_model_instance.create_db_document(split_type="character",
                                                    embedding_type='HF',
                                                    vectorstore_type='FAISS',
                                                                   )
        st.session_state["db"] = db
        st.session_state['repoid'] = "declare-lab/flan-alpaca-large"


        # splited_data = llm_model_instance.split(split_type="CHARACTER", chunk_size=200, chunk_overlap=10)

        if document:
            st.success("Data read successfully.")
            st.write("PDF Content:")
            stx.scrollableTextbox(document,height = 300)

            if st.button("Go to chat page"):
                switch_page("data_ask")
            
    
    # Remove the temporary file
    if obj.datapath:
        os.remove(obj.datapath)