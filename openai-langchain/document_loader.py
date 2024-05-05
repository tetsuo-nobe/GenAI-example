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
len(docs)

"""
ベクトル化
"""
#from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()

query = "AWSのS3からデータを読み込みためのDocumentLoaderはありますか"

vector = embeddings.embed_query(query)
print(len(vector)) # 1536次元
#print(vector)

# from langchain.vectorstores import Chroma
from langchain_community.vectorstores import Chroma

db = Chroma.from_documents(docs, embeddings)

retriever = db.as_retriever()

query = "AWSのS3からデータを読み込みためのDocumentLoaderはありますか"

context_docs = retriever.get_relevant_documents(query)
print(f"len = {len(context_docs)}")

first_doc = context_docs[0]
print(f"metadata = {first_doc.metadata}")
print(first_doc.page_content)


