from langchain import text_splitter as ts
from langchain import embeddings
from langchain import vectorstores as vs
from langchain.chains.question_answering import load_qa_chain
from langchain import HuggingFaceHub
from langchain import PromptTemplate
import sys
from src.logger import logging
from src.exception import CustomException
import os
from dotenv import load_dotenv
load_dotenv()
HFapi_key = os.getenv('HF_API')




class LLMmodel(object):
    def __init__(self,data):
        self.document = data

        self.repo_id = 'declare-lab/flan-alpaca-large'
        self.HF_API_TOKEN = HFapi_key
        
        self.llm = None
        self.chain = None
        
    def split(self, split_type="character", chunk_size=200, chunk_overlap=10):
        try:

            if self.document:
                if split_type == "character":
                    text_splitter = ts.RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
                elif split_type == "token":
                    text_splitter  = ts.TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

                self.document_splited = text_splitter.split_text(self.document)
                logging.info("Data Split Done")      
            return self.document_splited
    
        except Exception as error:
                logging.info("Data split failed")
                raise CustomException(error, sys)
    
    def embedding(self, embedding_type="HF"):
        try:
            self.embedding_model = embeddings.HuggingFaceEmbeddings()
            self.embedding_type = embedding_type
            logging.info("Embedding Finished.")
        except Exception as error:
            logging.info("Embedding failed ,e:",error)
            raise CustomException(error, sys)
        
        return self.embedding_model
    
    def storage(self, vectorstore_type = "FAISS", embedding_type="HF"):

        self.embedding_type = "HF"
        vectorstore_type = "FAISS"

        self.embedding(embedding_type=self.embedding_type)

        if vectorstore_type == "FAISS":
            model_vectorstore = vs.FAISS

        if self.document:
            try:
                self.db = model_vectorstore.from_texts(self.document_splited, self.embedding_model)
                logging.info("Storage in FAISS Finished.")
            except Exception as error:
                self.db = None
                logging.info("Storage failed ,e:",error)
                raise CustomException(error, sys)
                

        return self.db

    def search(self, question, with_score=False):
        relevant_docs = None
        try:
            if self.db and "SVM" not in str(type(self.db)):
                relevant_docs = self.db.similarity_search(question)
            elif self.db:
                relevant_docs = self.db.get_relevant_documents(question)
                logging.info("search done")
        except Exception as error:
            logging.info("search failed ,e:",error)
            raise CustomException(error, sys)

        return relevant_docs
    

    def question(self,question,repo_id="declare-lab/flan-alpaca-large", chain_type="stuff", 
                 relevant_docs=None,with_score=False, temperature=0,max_length=300,language="English"):
        try:
            relevant_docs = self.search(question, with_score=with_score)
            if relevant_docs:

                self.repo_id = self.repo_id if self.repo_id is not None else repo_id
                chain_type = "stuff"
                if (self.repo_id != repo_id ) or (self.llm is None):
                    self.repo_id = repo_id 
                    self.llm = HuggingFaceHub(repo_id=self.repo_id,huggingfacehub_api_token=self.HF_API_TOKEN,
                                                model_kwargs=
                                                {"temperature":temperature,
                                                "max_length": max_length})
                    
                prompt_template = """Use the following pieces of context to answer the question at the end. 
                If you don't know the answer, just say that you don't know, don't try to make up an answer.
                If the question is similar to [Talk me about the document], 
                the response should be a summary commenting on the most important points about the document
                {context}
                Question: {question}
                """
                PROMPT = PromptTemplate(
                    template=prompt_template, input_variables=["context", "question"]
                )
                PROMPT = PROMPT  + f" The Answer have to be in  {language} language:"
                self.chain = self.chain if self.chain is not None else load_qa_chain(self.llm, chain_type=chain_type, prompt = PROMPT)
                response = self.chain({"input_documents": relevant_docs, "question": question}, return_only_outputs=True)
                logging.info("response generation success")  
                return response
                 
            else:
                logging.info("response generation failed")
                return {"output_text": "ERROR: Something went wrong and the query could not be performed. Check the data source and its access"}
            
        except Exception as error:
            logging.info("Question response creatiion failed ,e:",error)
            raise CustomException(error,sys)
    
    def create_db_document(self, 
                            split_type="token",
                            chunk_size=200,
                            embedding_type="HF",
                            chunk_overlap=10,
                            vectorstore_type = "FAISS"):
            
            self.split(split_type=split_type, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            db = self.storage(vectorstore_type=vectorstore_type, embedding_type=embedding_type)
            return db

        