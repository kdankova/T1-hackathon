import pandas as pd
from langchain_community.document_loaders import DataFrameLoader


def load_data():
    df = pd.read_csv("data/df.csv")
    # stops = pd.read_csv("data/stop_words_.csv")
    loader = DataFrameLoader(df, page_content_column='answer')
    documents = loader.load()
    return documents
