import os
from langchain_community.llms import Tongyi
from langchain.prompts import PromptTemplate

# DashScope API Key
os.environ["DASHSCOPE_API_KEY"] = "sk-0738f7176f0a44e8ae8bc1569c2b6032"

# 初始化模型
llm = Tongyi(
    model_name="qwen-coder-plus",
    dashscope_api_key=os.environ["DASHSCOPE_API_KEY"]
)

# 创建一个提示模板
prompt = PromptTemplate(
    input_variables=["question"],
    template="你是一个编程助手，请回答以下问题：{question}"
)

# 构建 Chain
chain = prompt | llm

if __name__ == "__main__":
    question = "用 Python 写一个快速排序算法。"
    result = chain.invoke({"question": question})  # 使用 invoke 替代 run
    print(f"\033[1;32mQwen3 回答\033[0m")
    print(result)