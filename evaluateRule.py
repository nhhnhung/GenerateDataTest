import json
import re
import matplotlib.pyplot as plt


def is_valid_email(email):
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))


def is_valid_password(password):
    return isinstance(password, str) and len(password) >= 6


def is_not_empty(value):
    return value is not None and value != ""


def is_valid_telephone(phone):
    return isinstance(phone, str) and phone.isdigit() and 3 <= len(phone) <= 32

def load_existing_accounts():
    accounts = {}
    current_email = None

    with open("rules/existing_accounts.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            if line.startswith("Email:"):
                current_email = line.replace("Email:", "").strip()

            elif line.startswith("Password:") and current_email:
                password = line.replace("Password:", "").strip()
                accounts[current_email] = password
                current_email = None  # reset
    return accounts


def check_format_rule(tc, function_name):
    errors = []

    email = tc.get("Email", "")
    password = tc.get("Password", "")
    confirm = tc.get("Confirm", "")
    telephone = tc.get("Telephone", "")
    keyword = tc.get("keyword", "")

    if function_name in ["login", "register"]:
        if not is_not_empty(email):
            errors.append("EMPTY_EMAIL")
        elif not is_valid_email(email):
            errors.append("INVALID_EMAIL")

        if not is_not_empty(password):
            errors.append("EMPTY_PASSWORD")
        elif not is_valid_password(password):
            errors.append("INVALID_PASSWORD")

    if function_name == "register":
        if not is_valid_telephone(telephone):
            errors.append("INVALID_TELEPHONE")

        if password != confirm:
            errors.append("PASSWORD_NOT_MATCH")

    if function_name == "search":
        if not is_not_empty(keyword):
            errors.append("EMPTY_KEYWORD")

    return len(errors) == 0, errors


def check_business_rule(tc, function_name, existing_accounts):
    email = tc.get("Email", "")
    password = tc.get("Password", "")
    keyword = tc.get("keyword", "")

    if function_name == "login":
        if email not in existing_accounts:
            return False
        return existing_accounts[email] == password

    elif function_name == "register":
        if email in existing_accounts:
            return False
        return True

    elif function_name == "search":
        valid_keywords = ["iphone", "galaxy", "samsung", "macbook", "imac"]
        return keyword.lower() in valid_keywords

    return True


def validate_testcase(tc, function_name, existing_accounts):
    test_type = tc.get("TestType")

    is_format_valid, _ = check_format_rule(tc, function_name)
    is_business_valid = check_business_rule(tc, function_name, existing_accounts)

    if test_type == "HAPPY":
        return is_format_valid and is_business_valid

    elif test_type == "NEGATIVE":
        return not (is_format_valid and is_business_valid)

    elif test_type == "BOUNDARY":
        return True

    return False



def evaluate_json(file_path, function_name, existing_accounts):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    total = len(data)
    pass_count = 0

    for tc in data:
        if validate_testcase(tc, function_name, existing_accounts):
            pass_count += 1

    accuracy = pass_count / total * 100 if total > 0 else 0

    return {
        "total": total,
        "pass": pass_count,
        "fail": total - pass_count,
        "accuracy": round(accuracy, 2)
    }



def plot_result(result, name):
    plt.figure()
    plt.bar(["Pass", "Fail"], [result["pass"], result["fail"]], linewidth=2)
    plt.title(f"Đánh giá mức độ tuân thủ quy tắc sinh dữ liệu của chức năng {name}",
              fontsize=10,
              fontweight='bold')
    plt.xlabel("Kết quả")
    plt.ylabel("Số lượng")
    plt.savefig(f"{name}pass_fail.png")
    plt.show()


if __name__ == "__main__":
    print("===== CHỌN CHỨC NĂNG KIỂM TRA =====")
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
        exit()

    function_name = function_map[choice]

    # Load account
    existing_accounts = load_existing_accounts()

    file_map = {
        "login": "LoginData.json",
        "register": "RegisterData.json",
        "search": "SearchData.json"
    }

    print(f"\nĐang kiểm tra: {function_name.upper()}")

    result = evaluate_json(file_map[function_name], function_name, existing_accounts)

    print("\n===== RESULT =====")
    print(result)

    plot_result(result,function_name)
