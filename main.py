from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)


# Đọc dữ liệu từ CSV
def read_csv(file_name):
    return pd.read_csv(file_name)


csv_data = read_csv('C:\\Users\\ASUS\\Desktop\\DATAA\\DAP\\lab4_labdataset_chapter3.csv')


# Tìm kiếm dữ liệu trong CSV dựa trên truy vấn của người dùng
def search_data(query, csv_data):
    # Tìm kiếm theo tên khóa học hoặc mô tả
    result = csv_data[csv_data['name'].str.contains(query, case=False, na=False) |
                      csv_data['description'].str.contains(query, case=False, na=False)]

    if not result.empty:
        # Trả về tên khóa học và mô tả của kết quả đầu tiên tìm được
        return {
            "course_name": result.iloc[0]['name'],
            "description": result.iloc[0]['description']
        }
    else:
        return {"message": "Không tìm thấy khóa học phù hợp."}


# API Webhook để Watson Assistant gọi tới
@app.route('/webhook', methods=['POST'])
def webhook():
    query = request.json.get('input')  # Nhận câu hỏi từ Watson Assistant
    response = search_data(query, csv_data)  # Tìm kiếm trong CSV
    return jsonify(response)  # Trả về câu trả lời dưới dạng JSON


if __name__ == '__main__':
    app.run(debug=True)
