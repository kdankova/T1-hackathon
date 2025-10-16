from langchain_text_splitters import RecursiveCharacterTextSplitter


def data_split(data):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    split_texts = splitter.split_documents(data)
    return split_texts