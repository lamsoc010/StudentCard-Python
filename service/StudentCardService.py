from flask import Flask, request, jsonify, make_response
import lib.readFileExcel as readFileExcel
import lib.createStudentCard as createStudentCard
from flask_cors import CORS
from io import BytesIO
from PIL import Image
import base64

def handleCreateStudentCard(fileBase64, outputPath, backgroundBase64):
    listStudent = readFileExcel.readExcel2(fileBase64)
    totalRecordError = 0
    totalRecordSuccess = 0
    for i, student in enumerate(listStudent, start=0):
        if student is None: 
            totalRecordError += 1
        if(student.trangThai == 0):
            createStudentCard.renderStudentCard(student, i, outputPath, backgroundBase64)
            totalRecordSuccess += 1
    readFileExcel.writeExcel(fileBase64, listStudent)
    return listStudent, totalRecordSuccess, totalRecordError

def handleSelectForm(idForm):
    # Đọc ảnh từ tệp tin
    with open(f'assets/form/form{idForm}.png', 'rb') as f:
        img = Image.open(BytesIO(f.read()))

    # Chuyển đổi ảnh thành chuỗi base64
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str