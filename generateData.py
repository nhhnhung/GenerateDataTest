import os
import re
import json
import time

import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
from rag_engine import RAGEngine


load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

rag = RAGEngine()

#Phần Load tài khoản và từ khóa

def load_existing_accounts():
    try:
        with open("rules/existing_accounts.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return []


#Phần lưu excel
def save_to_excel_with_type(data, name):
    df = pd.DataFrame(data)

    # đưa TestType lên đầu
    cols = ["TestType"] + [c for c in df.columns if c != "TestType"]
    df = df[cols]

    df.to_excel(f"{name}Data.xlsx", index=False)

    print(f"Đã lưu {name}Data.xlsx")

#Phần làm sạch Json
def clean_json(text):
    if not text:
        raise ValueError("Empty response")

    text = re.sub(r"```.*?```", "", text, flags=re.S)
    match = re.search(r"\[\s*{.*}\s*\]", text, re.S)

    if not match:
        raise ValueError("Không tìm thấy JSON hợp lệ")

    return match.group(0)

#Phần xây dựng prompt
def build_prompt(function_name):

    rule_context = rag.retrieve(f"{function_name} validation rules")[0]

    base_prompt = f"""
Bạn là chuyên gia kiểm thử phần mềm.

FUNCTION: {function_name.upper()}

================ RULE =================
{rule_context}
=======================================

YÊU CẦU:
- Sinh CHÍNH XÁC test data theo yêu cầu bên dưới
- 1 HAPPY
- 3 NEGATIVE
- 1 BOUNDARY
- TestType phải là field đầu tiên
- TestType phải viết IN HOA hoàn toàn (HAPPY, NEGATIVE, BOUNDARY)
- Không trùng dữ liệu
- Dữ liệu realistic
- Chỉ trả JSON
- Không markdown
- Không giải thích
QUAN TRỌNG:
- Return STRICT valid JSON array
- Không dùng .repeat() hoặc expression
- Mọi giá trị phải là literal string đầy đủ
- Không text ngoài JSON
"""

    # Phần đăng ký
    if function_name.lower() == "register":
        existing_accounts = load_existing_accounts()
        existing_context = "\n".join(existing_accounts)

        base_prompt += f"""

EMAIL ĐÃ TỒN TẠI:
{existing_context}

Phải có:
- 1 test Email đã tồn tại (dùng email từ danh sách trên)
- 1 test số điện thoại bằng chữ
- Các test phải khác password nhau
BOUNDARY (CỰC KỲ QUAN TRỌNG):
- CHỈ sinh boundary FAIL (KHÔNG được sinh boundary hợp lệ)
- BẮT BUỘC dùng:
    + min - 1 (dưới min)
    + max + 1 (vượt max)

CHI TIẾT:
- FirstName:
    + "" (0 ký tự) → FAIL
    + 33 ký tự → FAIL

- LastName:
    + "" (0 ký tự) → FAIL
    + 33 ký tự → FAIL

- Telephone:
    + "12" (2 ký tự) → FAIL
    + 33 số → FAIL

LUẬT CỨNG:
- Không được dùng giá trị đúng biên (1 hoặc 32)
- Nếu sinh giá trị hợp lệ → SAI YÊU CẦU
- Expected phải là lỗi tương ứng validation

"""

    # Phần đăng nhập
    elif function_name.lower() == "login":
        existing_accounts = load_existing_accounts()
        existing_context = "\n".join(existing_accounts)

        base_prompt += f"""

TÀI KHOẢN ĐANG TỒN TẠI:
{existing_context}

HAPPY:
- Phải dùng email từ danh sách trên
NEGATIVE:
- Email không tồn tại phải KHÔNG nằm trong danh sách
- Bỏ trống trường 
- SQL injection
BOUNDARY:
- Giá trị vượt biên min-1, max+1
"""

    # Phần tìm kiếm
    elif function_name.lower() == "search":
        base_prompt += f"""

HAPPY:
- Keyword phải trùng sản phẩm trong danh sách
- Keyword có thể viết hoa hoặc chữ thường

NEGATIVE:
- Keyword không được trùng sản phẩm nào
- Keyword bỏ trống

BOUNDARY:
- Keyword 1 ký tự
- Keyword rất dài (>=100 ký tự)
"""

    return base_prompt

#Phần sinh dữ liệu
def generate_data(function_name):
    start_time = time.time()
    full_prompt = build_prompt(function_name)
    if not full_prompt:
        raise ValueError(f"Prompt builder failed for function: {function_name}")
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": full_prompt}],
        temperature=0.3
    )

    raw = response.choices[0].message.content

    if not raw:
        raise ValueError("LLM trả kết quả rỗng")

    print("RAW OUTPUT:\n", raw)
    end_time = time.time()
    clean = clean_json(raw)
    print(f"Thời gian sinh data: {end_time - start_time: .2f} giây")
    return json.loads(clean)

def main():
    print("===== CHỌN CHỨC NĂNG SINH DATA =====")
    print("1. Login")
    print("2. Register")
    print("3. Search")

    choice = input("Nhập lựa chọn (1/2/3): ").strip()

    function_map = {
        "1": "login",
        "2": "register",
        "3": "search"
    }

    if choice not in function_map:
        print("Lựa chọn không hợp lệ!")
        return

    function_name = function_map[choice]

    print(f"Đang sinh data cho: {function_name.upper()}")

    data = generate_data(function_name)

    # Lưu JSON
    file_name = function_name.capitalize()
    with open(f"{file_name}Data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Lưu Excel
    save_to_excel_with_type(data, file_name)

    print(f"Đã lưu {file_name}Data.json và {file_name}Data.xlsx")


if __name__ == "__main__":
    main()