# 引入依赖包，这里的 pydantic 版本为 v2
from pydantic import BaseModel, Field, model_validator
from langchain_deepseek import ChatDeepSeek
from langchain.tools import tool
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.output_parsers import PydanticOutputParser, JsonOutputParser, StrOutputParser
from langchain.output_parsers import RetryOutputParser, OutputFixingParser
from typing import Dict
from pydantic import BaseModel, Field
import asyncio

# 使用 deepseek
llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    api_key="sk-6b2a3015b6094e68aa2956124ad1e870",
    api_base="https://api.deepseek.com",
)

prompt = ChatPromptTemplate.from_template("讲一个关于{topic}的笑话,不要有任何解释")
chain = prompt | llm | StrOutputParser()

# print(chain.invoke({"topic":"狗"}))

# for chunk in chain.stream("小狗"): # 生成器
#     print(chunk, end="", flush=True)

async def stream_response():
    async for chunk in chain.astream("小狗"):
        print(chunk, end="", flush=True)
# 运行异步函数
asyncio.run(stream_response())
print("最后执行我")