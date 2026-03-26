import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")
model_name = os.getenv("MODEL_NAME")

if not api_key:
    raise ValueError("没有读取到 API_KEY，请检查 .env 文件")

client = OpenAI(
    api_key=api_key,
    base_url=base_url if base_url else None
)

def chat_with_model(user_input: str) -> str:
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": "你是一个帮助大学生分析 AI 岗位要求的助手，请输出清晰、结构化、简洁的内容。"
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    print("请输入一句话，输入 quit 退出。")
    while True:
        user_text = input("你：").strip()
        if user_text.lower() == "quit":
            print("已退出。")
            break

        try:
            answer = chat_with_model(user_text)
            print("\n模型：")
            print(answer)
            print("\n" + "-" * 40)
        except Exception as e:
            print(f"调用失败：{e}")
