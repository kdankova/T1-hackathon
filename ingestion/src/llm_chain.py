from langchain_openai import ChatOpenAI
from getpass import getpass

def get_llm():
    course_api_key = getpass(prompt="Введите ваш ключ, полученный в Scibox")

    # инициализируем языковую модель
    llm = ChatOpenAI(api_key=course_api_key, model='Qwen2.5-72B-Instruct-AWQ',
                     base_url="https://llm.t1v.scibox.tech/v1")
    return llm
