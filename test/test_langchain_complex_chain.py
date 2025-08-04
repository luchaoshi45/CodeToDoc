import os
from langchain_community.llms import Tongyi
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnableLambda

os.environ["DASHSCOPE_API_KEY"] = "sk-0738f7176f0a44e8ae8bc1569c2b6032"
llm = Tongyi(model_name="qwen-coder-plus", temperature=0.7)
prompt1 = ChatPromptTemplate.from_template("请回答以下问题：{question1}")
prompt2 = ChatPromptTemplate.from_template("请回答以下问题：{question2}")

def get_res(res):
    return f"""
    问题1：{res["question1"]}
    问题2：{res["question2"]}
    """

parallel_chain = RunnableParallel({
    "question1": prompt1 | llm | StrOutputParser(),
    "question2": prompt2 | llm | StrOutputParser()
}) | RunnableLambda(get_res)


res = parallel_chain.invoke({"question1": "什么是时间", "question2": "什么是空间"})
print(res)


# 虚假并行
# prompt = ChatPromptTemplate.from_template("请回答以下问题：1.{topic} 2.{question}")
# parallel_chain = RunnableParallel({
#     "topic": lambda x: f"{x['topic']}什么时候有的",
#     "question": lambda x: f"请介绍{x['topic']}"
# })

# complex_chain = (
#     parallel_chain | prompt | llm | StrOutputParser()
# )

# res = complex_chain.invoke({"topic": "机器学习"})
# print(res)
