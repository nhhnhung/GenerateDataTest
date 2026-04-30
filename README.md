# 🧠 Generate Test Data using RAG + LLM

## 📌 Giới thiệu

Dự án này tập trung vào việc **tự động sinh dữ liệu kiểm thử (test data)** bằng cách kết hợp giữa:

* 🔎 Retrieval-Augmented Generation (RAG)
* 🤖 Large Language Model (LLM)

Mục tiêu chính là tạo ra dữ liệu kiểm thử **đa dạng, có ngữ cảnh và sát thực tế**, thay thế cho việc tạo dữ liệu thủ công.

---

## 🎯 Mục tiêu

* Tự động sinh dữ liệu đầu vào cho các test case
* Tăng độ bao phủ kiểm thử (test coverage)
* Giảm thời gian và công sức viết dữ liệu thủ công
* Sinh dữ liệu theo rule (validation, format, business logic)

---

## ⚙️ Công nghệ sử dụng

* Python
* LLM (Groq / OpenAI API)
* RAG (Retrieval-Augmented Generation)
* JSON / Excel để lưu dữ liệu
* Rule-based validation

---

## 🧠 Ý tưởng chính (RAG + LLM)

Luồng hoạt động:

1. 📥 Input:

   * Rule kiểm thử (vd: email phải đúng format)
   * Ngữ cảnh từ hệ thống (file rules/)

2. 🔎 Retrieval:

   * Trích xuất thông tin liên quan từ rule

3. 🤖 Generation:

   * LLM sinh dữ liệu phù hợp với rule

4. ✅ Validation:

   * Kiểm tra dữ liệu bằng rule (regex, logic)

5. 📤 Output:

   * Lưu vào file JSON / Excel

---

## 📂 Cấu trúc project

```
GenerateDataTest/
│
├── generateData.py      # Sinh dữ liệu
├── rag_engine.py        # Xử lý RAG
├── evaluateRule.py      # Đánh giá dữ liệu
├── rules/               # Rule kiểm thử
├── LoginData.json       # Output dữ liệu
├── LoginData.xlsx       # Output Excel
└── README.md
```
## requirements
1. LLM + API
groq
openai

2. Environment
python-dotenv

3. Data processing
pandas
openpyxl

4. RAG
faiss-cpu
sentence-transformers

5. Utils
tqdm
---

## 🚀 Cách chạy project

### 1. Cài thư viện

```bash
Cài các thư viện cần thiết
```

### 2. Thiết lập API Key

Tạo file `.env`:

```env
GROQ_API_KEY=your_api_key_here
```

---

### 3. Chạy sinh dữ liệu

```bash
python generateData.py
```

---

## 📊 Kết quả

* Sinh dữ liệu tự động với độ chính xác cao
* Bao phủ nhiều trường hợp (valid + invalid)
* Giảm thời gian tạo dữ liệu kiểm thử hỗ trợ tốt cho tester

---

## 📌 Ưu điểm

* Tự động hóa quá trình sinh dữ liệu
* Dữ liệu có ngữ cảnh (context-aware)
* Dễ mở rộng thêm rule mới
* Kết hợp AI + Testing

---

## ⚠️ Hạn chế

* Phụ thuộc vào chất lượng prompt
* LLM có thể sinh dữ liệu chưa chính xác 100%
* Cần bước validate bổ sung

---

## 🔮 Hướng phát triển

* Tích hợp trực tiếp với Selenium/TestNG
* Sinh test case tự động từ UI
* Kết hợp CI/CD (GitHub Actions)
* Tối ưu prompt và embedding cho RAG

---

## 👨‍💻 Tác giả

* Sinh viên ngành Hệ thống thông tin
* Hướng nghiên cứu: Ứng dụng AI trong kiểm thử phần mềm

---

## ⭐ Ghi chú

Dự án phục vụ mục đích học tập và nghiên cứu, minh họa việc ứng dụng AI (RAG + LLM) trong sinh dữ liệu kiểm thử.
