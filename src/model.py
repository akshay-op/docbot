from langchain import document_loaders as dl
from langchain import text_splitter as ts
from langchain import embeddings
from langchain import vectorstores as vs
from langchain import retrievers
from langchain.chains.question_answering import load_qa_chain
from langchain import HuggingFaceHub
from langchain import PromptTemplate
import sys
from src.logger import logging
from src.exception import CustomException


class LLMmodel(object):
    def __init__(self,data):
        self.document = data

        # self.HF_API_TOKEN = HF_API_TOKEN
        
    def split(self, split_type="character", chunk_size=200, chunk_overlap=10):
  
        SPLIT_TYPE_LIST = ["CHARACTER", "TOKEN"]
        split_type=SPLIT_TYPE_LIST[0]

        if self.document:
            if split_type == "CHARACTER":
                text_splitter = ts.RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            elif split_type == "TOKEN":
                text_splitter  = ts.TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    
            try:
                document_splited = text_splitter.split_text(self.document)
                logging.info("Data Split Done")
            except Exception as error:
                logging.info("Data split failed")
                raise CustomException(error, sys)
    
        return document_splited
    

        
