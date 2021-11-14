from flask import Flask, request, render_template
import model

# Khởi tạo server backend
app = Flask(__name__, template_folder='templates')

# Đường dẫn chạy mô hình phân lớp
@app.route('/prediction', methods=['GET'])
def prediction():
    # Lấy dữ liệu người dụng nhập vào qua phương thức GET
    comment = request.args.get('comment')
    result = model.predict(comment)
    try:
        if result == 1:
            result = 'I guess you are satisfied with the product'
        else:
            result = 'I guess you are unsatisfied with the product'
    except:
        result = 'Đã xảy ra lỗi...'
    return render_template('home.html', comment=comment, result=result)


# Trang chủ dẩn đến home
@app.route('/')
def home():
    return render_template('home.html') # Render home.html

# Start server
if __name__ == '__main__':
    app.run(debug=True)