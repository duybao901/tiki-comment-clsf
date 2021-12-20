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
            predict = {"msg":"hài lòng", "result": True }
        else:
            predict = {"msg":"không hài lòng"}
    except:
        result = 'Đã xảy ra lỗi...'
    return render_template('home.html', comment=comment, predict=predict)


# Trang chủ dẩn đến home
@app.route('/')
def home():
    comment=''
    predict={}
    return render_template('home.html',comment=comment, predict=predict) # Render home.html

# Start server
if __name__ == '__main__':
    app.run(debug=True)