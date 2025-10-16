from src.data_loader import load_data
from src.llm_chain import get_llm
from src.bge_embedder import BGEM3Embeddings
from src.data_splitter import data_split
from langchain.llms import OpenAI
from langchain import PromptTemplate, LLMChain
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as pltfrom
from langchain.document_loaders import CSVLoader, DataFrameLoader
from langchain.text_splitter import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
)
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

course_api_key = 'sk-h7YcuRfbDw_2fPiuZzz06w'


def build_rag_pipeline():
    df = load_data()
    llm = get_llm()
    # Определяем сплиттер
    split_texts = data_split(df)

    embeddings = BGEM3Embeddings(api_key=course_api_key)

    # Векторное хранилище
    db = FAISS.from_documents(split_texts, embeddings)

    # Задаём ретривер
    retriever = db.as_retriever()
    bm25 = BM25Retriever.from_documents(split_texts)  # Эмбеддинги ему не нужны
    bm25.k = 3  # Так можно задать количество возвращаемых документов

    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25, retriever],  # список ретриверов
        weights=[
            0.4,
            0.6,
        ],  # веса, на которые домножается скор документа от каждого ретривера
    )

    print(db.similarity_search_with_score('Я не помню пароль'))


    return "RAG pipeline готова (добавь retrieval)"
