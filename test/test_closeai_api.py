from openai import OpenAI
import os

# os.environ["OPENAI_API_BASE"] = "https://api.openai-proxy.org/v1" # 早期版本
os.environ["OPENAI_BASE_URL"] = "https://api.openai-proxy.org/v1"
os.environ["OPENAI_API_KEY"] = "sk-660BMZI5WRTfL2XFM2ykCvJMbYiKYXahc4p98vPFxMzKf5jS"

if __name__ == '__main__':
    # client = OpenAI(
    #     # openai系列的sdk，包括langchain，都需要这个/v1的后缀
    #     base_url='https://api.openai-proxy.org/v1',
    #     api_key='sk-660BMZI5WRTfL2XFM2ykCvJMbYiKYXahc4p98vPFxMzKf5jS',
    # )
    client = OpenAI()

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Say hi",
            }
        ],
        model="gpt-4o-mini", # 如果是其他兼容模型，比如deepseek，直接这里改模型名即可，其他都不用动
    )

    print(chat_completion)