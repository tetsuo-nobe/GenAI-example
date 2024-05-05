# from langchain.document_loaders import GitLoader
from langchain_community.document_loaders import GitLoader

def file_filter(file_path):
  return file_path.endswith(".md")

loader = GitLoader(
    clone_url ="https://github.com/tetsuo-nobe/advdev_on_aws",
    repo_path="./tree",
    branch="main",
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
#from langchain_aws import BedrockEmbeddings
from langchain_community.embeddings import BedrockEmbeddings

embeddings = BedrockEmbeddings()
#embeddings = BedrockEmbeddings(
#    credentials_profile_name="bedrock-admin", region_name="us-east-1"
#)

#query = "AWS Lambda レイヤーの my-boto3-layer とは何ですか"
query = "AWS CodePipeline のワークはありますか"


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
from langchain_aws import ChatBedrock

chat = ChatBedrock(model_id = "anthropic.claude-3-sonnet-20240229-v1:0", model_kwargs={"temperature":0})
qa_chain = RetrievalQA.from_chain_type(llm = chat, chain_type="stuff", retriever=retriever)
result = qa_chain.invoke(query)
print(result)