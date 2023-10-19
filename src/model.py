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
    
    def embedding(self, embedding_type="HF", OPENAI_KEY=None):

        try:
            if not self.embedding_model:
                embedding_type = "HF"
                if embedding_type == "HF":
                    self.embedding_model = embeddings.HuggingFaceEmbeddings()
                self.embedding_type = embedding_type
                logging.info("Embedding Finished.")
        except Exception as error:
            logging.info("Embedding failed ,e:",error)
            raise CustomException(error, sys)
        
        return self.embedding_model
    
    def get_storage(self, vectorstore_type = "FAISS", embedding_type="HF", OPENAI_KEY=None):

        self.embedding_type = "HF"
        vectorstore_type = "FAISS"

        self.embedding(embedding_type=self.embedding_type, OPENAI_KEY=OPENAI_KEY)

        if vectorstore_type == "FAISS":
            model_vectorstore = vs.FAISS

        if self.data_text:
            try:
                self.db = model_vectorstore.from_texts(self.document_splited, self.embedding_model)
            except Exception as error:
                print(f"Error in storage data text step: {error}")
                self.db = None

        return self.db

    def search(self, question, with_score=False):
        relevant_docs = None

        if self.db and "SVM" not in str(type(self.db)):
            relevant_docs = self.db.similarity_search(question)
        elif self.db:
            relevant_docs = self.db.get_relevant_documents(question)
        
        return relevant_docs


    