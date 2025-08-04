import os
from langchain_community.llms import Tongyi
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import Chroma

# 设置API密钥
os.environ["DASHSCOPE_API_KEY"] = "sk-0738f7176f0a44e8ae8bc1569c2b6032"

# 初始化LLM
llm = Tongyi(model_name="qwen-coder-plus", temperature=0.7)

print("\n3. RAG (检索增强生成) 链")

# 创建示例文档
os.makedirs("output", exist_ok=True)  # 如果目录不存在则创建
with open("output/rag_sample.txt", "w", encoding="utf-8") as f:
    f.write("""
    机器学习是人工智能的一个重要分支。
    深度学习是机器学习的一个子领域，使用神经网络。
    自然语言处理让计算机能够理解和生成人类语言。
    计算机视觉使机器能够识别和理解图像内容。
    """)

# 加载和处理文档
loader = TextLoader("output/rag_sample.txt", encoding="utf-8")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
texts = text_splitter.split_documents(documents)

# 创建向量存储
embeddings = DashScopeEmbeddings(
    model="text-embedding-v1",
    dashscope_api_key=os.environ["DASHSCOPE_API_KEY"]
)
vectorstore = Chroma.from_documents(texts, embeddings)

# 创建检索器
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# RAG 链
rag_prompt = ChatPromptTemplate.from_template(
    "基于以下上下文回答问题：\n\n{context}\n\n问题：{question}\n\n回答："
)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# 完整的 RAG 链
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)

# 执行 RAG 查询
rag_question = "机器学习包括哪些领域？"
rag_result = rag_chain.invoke(rag_question)
print(f"RAG 问题: {rag_question}")
print(f"RAG 回答: {rag_result}")