import os
import sys
sys.path.insert(0, 'C:\\Users\\USER\\Documents\\python projects\\docbot')
from src.logger import logging
from src.exception import CustomException
import pandas as pd
from langchain import document_loaders as dl
import streamlit as st

class DataRead:
    def __init__(self):
        # self.datapath = "data/tatasample.pdf"
        self.datapath = None
        self.output_dir = "data/"
    
    def getdata(self):

        if self.datapath is None:
            st.error("Please upload a PDF file.")
            return

        logging.info("Data reading initiated")
        try:
            data = dl.PyPDFLoader(self.datapath)
            self.document = data.load()
            logging.info("Data read completed.")
            return self.document
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

    st.title("PDF Data Reader")
    st.write("Upload a PDF file to read its content.")

    obj = DataRead()

    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        # Save the uploaded file to a temporary location
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())
        obj.datapath = "temp.pdf"
        document = obj.getdata()
        if document:
            st.success("Data read successfully.")
            st.write("PDF Content:")
            st.write(document)
            # obj.save_document(document,'temp.pdf')
            
    
    # Remove the temporary file
    if obj.datapath:
        os.remove(obj.datapath)



