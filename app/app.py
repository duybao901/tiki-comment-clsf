from flask import Flask, request, render_template

# Khởi tạo server backend
app = Flask(__name__, template_folder='templates')

# Đường dẫn chạy mô hình phân lớp
@app.route('/prediction', methods=['GET'])
def prediction():
    # Lấy dữ liệu người dụng nhập vào qua phương thức GET
    comment = request.args.get('comment')
    return render_template('home.html', result =comment)


# Trang chủ dẩn đến home
@app.route('/')
def home():
    return render_template('home.html') # Render home.html

# Start server
if __name__ == '__main__':
    app.run(debug=True)