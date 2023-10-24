import os
import sys
sys.path.insert(0, 'C:\\Users\\USER\\Documents\\python projects\\docbot')
from src.logger import logging
from src.exception import CustomException
from src.model import LLMmodel
import pandas as pd
from PyPDF2 import PdfReader

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
