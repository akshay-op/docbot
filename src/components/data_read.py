import os
import sys
sys.path.insert(0, 'C:\\Users\\USER\\Documents\\python projects\\docbot')
from src.logger import logging
from src.exception import CustomException
from src.model import LLMmodel
import pandas as pd
from langchain import document_loaders as dl
import streamlit as st
from PyPDF2 import PdfReader

st.set_page_config(initial_sidebar_state="collapsed")
from streamlit_extras.stylable_container import *
from streamlit_extras.switch_page_button import switch_page
import streamlit_scrollable_textbox as stx

class DataRead:
    def __init__(self):
        # self.datapath = "./data/tatasample.pdf"
        self.datapath = None
        self.output_dir = "data/"
    
    def getdata(self):

        if self.datapath is None:
            st.error("Please upload a PDF file.")
            return

        logging.info("Data reading initiated")
        try:
            pdf_readed = PdfReader(self.datapath)
            document_text = ""
            
            for page in pdf_readed.pages:
                document_text+= page.extract_text()
                type_doc = "TXT"
                
            logging.info("Data read completed.")
            return document_text
        except Exception as e:
            logging.info("Data read failed.")
            raise CustomException(e, sys)
        
    def save_document(self, document, filename):
        save_path = os.path.join(self.output_dir, filename)
        with open(save_path, "w", encoding="utf-8") as file:
            # file.write(document)
            file.write('\n'.join(document))


if __name__=="__main__":
    # obj=DataRead()
    # obj.getdata()

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



