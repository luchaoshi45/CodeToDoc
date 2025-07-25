import os
from langchain_community.llms import Tongyi
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_community.embeddings import DashScopeEmbeddings
from langchain.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# DashScope API Key
os.environ["DASHSCOPE_API_KEY"] = "sk-0738f7176f0a44e8ae8bc1569c2b6032"

print("=== LangChain LCEL 语法演示 ===\n")

# 1. 基础 LCEL 链式调用
print("1. 基础 LCEL 链式调用")
llm = Tongyi(model_name="qwen-coder-plus", temperature=0.7)

# 创建提示模板
prompt = ChatPromptTemplate.from_template("请回答以下问题：{question}")

# 构建 Chain (使用管道语法)
chain = prompt | llm | StrOutputParser()

# 执行 (使用 invoke 替代 run)
question = "什么是人工智能？"
result = chain.invoke({"question": question})
print(f"问题: {question}")
print(f"回答: {result}")

# 2. 更复杂的 LCEL 链
print("\n2. 复杂 LCEL 链")
# 并行处理
parallel_chain = RunnableParallel({
    "topic": lambda x: x["topic"],
    "question": lambda x: f"请介绍{x['topic']}"
})

# 顺序处理链
complex_chain = (
    parallel_chain
    | prompt
    | llm
    | StrOutputParser()
)

result = complex_chain.invoke({"topic": "机器学习"})
print(f"复杂链结果: {result}")

# 3. 带有文档检索的 RAG 链
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

# 4. 条件链
print("\n4. 条件链")
from langchain_core.runnables import RunnableLambda

def route_question(info):
    if "技术" in info["question"]:
        return tech_chain
    else:
        return general_chain

# 技术问题链
tech_prompt = ChatPromptTemplate.from_template("作为技术专家，请回答：{question}")
tech_chain = tech_prompt | llm | StrOutputParser()

# 一般问题链
general_prompt = ChatPromptTemplate.from_template("请简单回答：{question}")
general_chain = general_prompt | llm | StrOutputParser()

# 条件路由链
conditional_chain = (
    RunnablePassthrough()
    | RunnableLambda(route_question)
)

tech_result = conditional_chain.invoke({"question": "Python 技术问题"})
general_result = conditional_chain.invoke({"question": "今天天气如何？"})

print(f"技术问题回答: {tech_result}")
print(f"一般问题回答: {general_result}")

# 5. 批量处理
print("\n5. 批量处理")
questions = [
    {"question": "什么是深度学习？"},
    {"question": "人工智能的历史"},
    {"question": "机器学习算法"}
]

# 批量执行
batch_results = chain.batch(questions)
for i, result in enumerate(batch_results):
    print(f"问题 {i+1}: {questions[i]['question']}")
    print(f"回答: {result[:100]}...")

# 清理文件
os.remove("output/rag_sample.txt")

print("\n=== LCEL 语法演示完成 ===")