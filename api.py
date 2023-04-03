from flask import Flask, request, jsonify, make_response
import lib.readFileExcel as readFileExcel
import lib.createStudentCard as createStudentCard
import service.StudentCardService as studentCardService
import json
from flask_cors import CORS
import base64
from io import BytesIO
from PIL import Image

url = 'D:\\Study\\DHPhuXuan\\Nam3\\HK-Spring\\Python\\TheSinhVien\\assets\\input\\danhsachsinhvien.xlsx'


app = Flask(__name__)
CORS(app)

# API endpoint to get list of all students
@app.route('/hello', methods=['GET'])
def hello():
    response = make_response(jsonify({"Success": "Thành công"}), 200)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/chooseForm', methods=['POST'])
def create_student_card():
    # Get param
    backgroundBase64 = request.json.get('backgroundBase64')
    fileBase64 = request.json.get('fileBase64')
    outputPath = request.json.get('outputPath')
    idForm = request.json.get('idForm')

    # Validate param
    if not backgroundBase64:
        return make_response(jsonify({"error": "Thiếu thông tin tham số backgroundPath"}), 400) # trả về mã lỗi 400 Bad Request
    if not fileBase64:
        return make_response(jsonify({"error": "Thiếu thông tin tham số fileBase64"}), 400) # trả về mã lỗi 400 Bad Request
    if not outputPath:
        return make_response(jsonify({"error": "Thiếu thông tin tham số outputPath"}), 400) # trả về mã lỗi 400 Bad Request

    try:
        # xử lý logic và trả về kết quả
        listStudent, totalRecordSuccess, totalRecordError = studentCardService.handleCreateStudentCard(fileBase64, outputPath, backgroundBase64, idForm)

        return make_response(jsonify({"success": {"totalRecord": len(listStudent), "totalRecordSuccess": totalRecordSuccess, "totalRecordError": totalRecordError}}), 200, {'Access-Control-Allow-Origin': '*'})
    except FileNotFoundError:
        return make_response(jsonify({"error": "File không tồn tại"}), 404) # trả về mã lỗi 404 Not Found
    except Exception as e:
        return make_response(jsonify({"error": "Lỗi: " + str(e)}), 500) # trả về mã lỗi 500 Internal Server Error
    
@app.route('/selectForm', methods=['GET'])
def selectForm():
    # Get param
    idForm = request.args.get('idForm')

    # Validate param
    if not idForm:
        return make_response(jsonify({"error": "Thiếu thông tin tham số idForm"}), 400) # trả về mã lỗi 400 Bad Request
    try:
       # xử lý logic và trả về kết quả
        img_str = studentCardService.handleSelectForm(idForm)
        
        # Trả về chuỗi base64
        return make_response(jsonify({"image": img_str}), 200)
    except Exception as e:
        return make_response(jsonify({"error": "Lỗi: " + str(e)}), 500) # trả về mã lỗi 500 Internal Server Error

if __name__ == '__main__':
    app.run(host="127.0.0.1", port="6868")
    app.run(debug=True)



# Viết API return ra image khi có sự thay đổi về chọn mẫu thẻ sinh viên