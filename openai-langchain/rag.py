# from langchain.document_loaders import GitLoader
from langchain_community.document_loaders import GitLoader

def file_filter(file_path):
  return file_path.endswith(".mdx")

loader = GitLoader(
    clone_url ="https://github.com/langchain-ai/langchain",
    repo_path="./langchain",
    branch="master",
    file_filter=file_filter

)

raw_docs = loader.load()
# 時間かかる
print(len(raw_docs))

from langchain.text_splitter import CharacterTextSplitter

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(raw_docs)

"""
ベクトル化
"""
#from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()

query = "AWSのS3からデータを読み込みためのDocumentLoaderはありますか"

#vector = embeddings.embed_query(query)
#print(len(vector)) # 1536次元
#print(vector)

# from langchain.vectorstores import Chroma
from langchain_community.vectorstores import Chroma

db = Chroma.from_documents(docs, embeddings)

retriever = db.as_retriever()

"""
RAG
"""
from langchain.chains import RetrievalQA
#from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI

chat = ChatOpenAI(model_name = "gpt-3.5-turbo", temperature=0)
qa_chain = RetrievalQA.from_chain_type(llm = chat, chain_type="stuff", retriever=retriever)
result = qa_chain.invoke(query)
print(result)