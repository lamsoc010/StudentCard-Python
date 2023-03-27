from flask import Flask, request, jsonify, make_response
import lib.readFileExcel as readFileExcel
import lib.createStudentCard as createStudentCard
import json

url = 'D:\\Study\\DHPhuXuan\\Nam3\\HK-Spring\\Python\\TheSinhVien\\assets\\input\\danhsachsinhvien.xlsx'


app = Flask(__name__)

# API endpoint to get list of all students
@app.route('/', methods=['GET'])
def hello():
    return jsonify("Hello World")

@app.route('/chooseForm', methods=['POST'])
def create_student_card():
    # Get param
    backgroundPath = request.json.get('backgroundPath')
    filePath = request.json.get('filePath')
    outputPath = request.json.get('outputPath')

    # Validate param
    if not backgroundPath:
        return make_response(jsonify({"error": "Thiếu thông tin tham số backgroundPath"}), 400) # trả về mã lỗi 400 Bad Request
    if not filePath:
        return make_response(jsonify({"error": "Thiếu thông tin tham số filePath"}), 400) # trả về mã lỗi 400 Bad Request
    if not outputPath:
        return make_response(jsonify({"error": "Thiếu thông tin tham số outputPath"}), 400) # trả về mã lỗi 400 Bad Request

    try:
        # xử lý logic và trả về kết quả
        listStudent = readFileExcel.readExcel2(filePath)
        totalRecordError = 0
        totalRecordSuccess = 0
        for i, student in enumerate(listStudent, start=0):
            if student is None: 
                totalRecordError += 1
            if(student.trangThai == 0):
                createStudentCard.renderStudentCard(student, i, outputPath, backgroundPath)
                totalRecordSuccess += 1
        readFileExcel.writeExcel(filePath, listStudent)
        # return make_response(jsonify({"success": f"Đã tạo {totalRecordSuccess} thẻ trên {len(listStudent)} tổng số sinh viên"}), 200) # Thành công
        return make_response(jsonify({"success": {"totalRecord": len(listStudent), "totalRecordSuccess": totalRecordSuccess, "totalRecordError": totalRecordError}}), 200)
    except FileNotFoundError:
        return make_response(jsonify({"error": "File không tồn tại"}), 404) # trả về mã lỗi 404 Not Found
    except Exception as e:
        return make_response(jsonify({"error": "Lỗi: " + str(e)}), 500) # trả về mã lỗi 500 Internal Server Error
    

if __name__ == '__main__':
    app.run(host="127.0.0.1", port="6868")
    app.run(debug=True)



# Viết API return ra image khi có sự thay đổi về chọn mẫu thẻ sinh viên