import os
import sys
sys.path.insert(0, 'C:\\Users\\USER\\Documents\\python projects\\docbot')
from src.logger import logging
from src.exception import CustomException
import pandas as pd
from langchain import document_loaders as dl

class DataRead:
    def __init__(self):
        self.datapath = "./data/tatasample.pdf"
    
    def getdata(self):
        logging.info("data reading initiated")
        try:
            data = dl.PyPDFLoader(self.datapath)
            self.document = data.load()
            logging.info("data read completed.")
            return self.document
        except Exception as e:
            logging.info("Data read failed.")
            raise CustomException(e,sys)

if __name__=="__main__":
    obj=DataRead()
    obj.getdata()



