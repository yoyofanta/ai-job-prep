import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")
model_name = os.getenv("MODEL_NAME")

if not api_key:
    raise ValueError("没有读取到 API_KEY，请检查 .env 文件")

if not model_name:
    raise ValueError("没有读取到 MODEL_NAME，请检查 .env 文件")

client = OpenAI(
    api_key=api_key,
    base_url=base_url if base_url else None
)

SYSTEM_PROMPT = """
你是一个帮助大学生分析 AI 岗位 JD 的助手。
请基于用户输入的岗位描述，输出清晰、结构化、简洁的分析，严格按照以下格式：

1. 岗位定位
2. 核心技能要求
3. 加分项
4. 适合什么背景的人投递
5. 我现在该怎么准备
6. 可以做什么项目来匹配这个岗位

要求：
- 用中文输出
- 每一部分都要有标题
- 表达具体，不要空泛
- 默认用户是第一次准备 AI 实习的学生
"""

def analyze_jd(jd_text: str) -> str:
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"请分析这段岗位 JD：\n\n{jd_text}"}
        ],
        temperature=0.5
    )
    return response.choices[0].message.content

def read_multiline_input() -> str:
    print("请粘贴岗位 JD 内容，输入 END 结束：")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    return "\n".join(lines).strip()

if __name__ == "__main__":
    try:
        jd_text = read_multiline_input()
        if not jd_text:
            print("你没有输入任何 JD 内容。")
        else:
            result = analyze_jd(jd_text)
            print("\n====== 分析结果 ======\n")
            print(result)
    except Exception as e:
        print(f"运行失败：{e}")