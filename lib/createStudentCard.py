from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import qrcode
from unidecode import unidecode
import os
import base64


# Độ phân giải xuất ảnh
DPI = 300
# Kích thước thẻ theo cm
widthCard = 8.6
hightCard = 5.4
# Kích thước thẻ theo pixel
width =int(widthCard * DPI)
hight = int(hightCard * DPI)

# Đường dẫn tới file ảnh
# backgroundImagePath = "TheSinhVien/assets/image/background.jpg"


def renderStudentCard(student, i, outputPath, backgroundBase64):
    imageStudentPath = student.anhThe
    # Tạo ảnh nền cho thẻ sinh viên
    # img = Image.new('RGB', (width, hight), (255, 255, 255))
    # img = Image.open(backgroundImagePath)
    # Xử lý ảnh background từ base64
    backgroundBytes = base64.b64decode(backgroundBase64)
    img = Image.open(BytesIO(backgroundBytes))
    img = img.resize((width, hight))

    # Vẽ khung trên 
    draw = ImageDraw.Draw(img)
    hightHeader = int(hight/4)
    draw.rectangle((0, 0, width, hightHeader), fill =(0, 0, 102))

    
    # Tạo đối tượng QRCode
    qr = qrcode.QRCode(version=1, box_size=15, border=1)
    # Lưu dữ liệu vào QRCode
    data = student.hoTen
    qr.add_data(data)
    # Tạo QRCode
    qr.make(fit=True)
    # Lấy hình ảnh của QRCode
    imgQr = qr.make_image(fill_color="black", back_color="white")
    widthQr, heightQr = imgQr.size
    qr_pos = ((width - widthQr), (hight - heightQr))
    

    # Vẽ logo
    student_image = Image.open(student.anhThe)
    widthLogo = int(width/6)
    paddingLogo = 50
    hightLogo = int(hightHeader) - paddingLogo*2
    student_image = student_image.resize((widthLogo, hightLogo))
    img.paste(student_image, (paddingLogo, paddingLogo))

    # Tiêu đề trường phía trên
    fontHeader = ImageFont.truetype('arialbd.ttf', 100)
    headerTitle = "BỘ GIÁO DỤC VÀ ĐÀO TẠO"
    headerTitle2 = "TRƯỜNG ĐẠI HỌC PHÚ XUÂN"
    textWidthHeader, textHeightHeader = fontHeader.getsize(headerTitle)
    textWidthHeader2, textHeightHeader2 = fontHeader.getsize(headerTitle2)
    paddingLeft = ((width - widthLogo - paddingLogo * 2) - textWidthHeader) / 2 + (widthLogo + paddingLogo * 2)
    paddingLeft2 = ((width - widthLogo - paddingLogo * 2) - textWidthHeader2) / 2 + (widthLogo + paddingLogo * 2)
   
    paddingTop = (hightHeader - textHeightHeader) / 4
    paddingTop2 = (hightHeader - textHeightHeader2) / 1.5
  
    draw.text((paddingLeft, paddingTop), headerTitle, font=fontHeader, fill=(255, 204, 0))
    draw.text((paddingLeft2, paddingTop2), headerTitle2, font=fontHeader, fill=(255, 204, 0))

    # Ảnh sinh viên
    hightImage = int(hight / 2 )
    withImage = int(width / 4)
    # draw.rectangle((paddingLogo, hightHeader + 100, withImage, hightImage), fill ='black')
    imgLogo = Image.open(imageStudentPath)
    imgLogo = imgLogo.resize((withImage, hightImage))
    imageStudentPos = ((paddingLogo, hightHeader + 100))
    img.paste(imgLogo, imageStudentPos)

    # Thêm text Thẻ sinh viên
    fontStudentCard = ImageFont.truetype('arialbd.ttf', 120)
    titleStudentCard = "Thẻ Sinh Viên"
    textWidthStudentCard, textHeightStudentCard = fontStudentCard.getsize(titleStudentCard)
    paddingLeftStudentCard = ((width - withImage - paddingLogo * 2) - textWidthStudentCard) / 2 + (withImage + paddingLogo * 2)
    paddingTopStudentCard = (hightHeader  + 100) 
    draw.text((paddingLeftStudentCard, paddingTopStudentCard), titleStudentCard, font=fontStudentCard, fill=(180, 37, 50))

    # Thêm text Họ và tên
    fillText = (0, 0, 0)
    fontInfo= ImageFont.truetype('arial.ttf', 80)
    fontInfoDetail= ImageFont.truetype('arialbd.ttf', 80)
    paddingLeftInfo= paddingLogo * 2 + withImage
    paddingTopText = 130
    paddingTopName = paddingTopStudentCard + paddingTopText
    textWidthName, textHeightName = fontInfo.getsize("Họ và Tên")
    draw.text((paddingLeftInfo, paddingTopName), "Họ và Tên:", font=fontInfo, fill=fillText)
    draw.text((paddingLeftInfo + textWidthName + 50, paddingTopName), student.hoTen, font=fontInfoDetail, fill=fillText)


    paddingTopName = paddingTopStudentCard + paddingTopText * 2
    textWidthBirthday, textHeightBirthday = fontInfo.getsize("Ngày Sinh:")
    draw.text((paddingLeftInfo, paddingTopName), "Ngày Sinh:", font=fontInfo, fill=fillText)
    draw.text((paddingLeftInfo + textWidthBirthday + 50, paddingTopName), student.ngaySinh, font=fontInfoDetail, fill=fillText)


    paddingTopName = paddingTopStudentCard + paddingTopText * 3
    textWidthKhoa, textHeightKhoa = fontInfo.getsize("Khoa:")
    draw.text((paddingLeftInfo, paddingTopName), "Khoa:", font=fontInfo, fill=fillText)
    draw.text((paddingLeftInfo + textWidthKhoa + 50, paddingTopName), student.khoa, font=fontInfoDetail, fill=fillText)

    paddingTopName = paddingTopStudentCard + paddingTopText * 4
    textWidthKhoa, textHeightKhoa = fontInfo.getsize("Ngành:")
    draw.text((paddingLeftInfo, paddingTopName), "Ngành:", font=fontInfo, fill=fillText)
    draw.text((paddingLeftInfo + textWidthKhoa + 50, paddingTopName), student.nganh, font=fontInfoDetail, fill=fillText)

    paddingTopName = paddingTopStudentCard + paddingTopText * 5
    textWidthKhoa, textHeightKhoa = fontInfo.getsize("Niên khoá:")
    draw.text((paddingLeftInfo, paddingTopName), "Niên khoá:", font=fontInfo, fill=fillText)
    draw.text((paddingLeftInfo + textWidthKhoa + 50, paddingTopName), student.nienKhoa, font=fontInfoDetail, fill=fillText)

    paddingTopName = paddingTopStudentCard + paddingTopText * 6
    textWidthKhoa, textHeightKhoa = fontInfo.getsize("Mã sinh viên:")
    draw.text((paddingLeftInfo, paddingTopName), "Mã sinh viên:", font=fontInfo, fill=fillText)
    draw.text((paddingLeftInfo + textWidthKhoa + 50, paddingTopName), student.maSV, font=fontInfoDetail, fill=fillText)

    paddingTopName = paddingTopStudentCard + paddingTopText * 7
    textWidthKhoa, textHeightKhoa = fontInfo.getsize("Đại học 3 năm, tốt nghiệp sớm, việc làm ngay!")
    # draw.text((paddingLeftInfo, paddingTopName), "Mã sinh viên:", font=fontInfo, fill=fillText)
    draw.text(((width - textWidthKhoa - widthQr) / 2, paddingTopName), "Đại học 3 năm, tốt nghiệp sớm, việc làm ngay!", font=fontInfoDetail, fill=fillText)

    img.paste(imgQr, qr_pos)


    # draw.text((170, 100), student_name, font=font, fill=(0, 0, 0))
    nameStudentCard = f"{unidecode(student.hoTen).replace(' ', '')}"
    # Tạo thư mục mới
    folder_path = f"{outputPath}/{unidecode(student.khoa).replace(' ', '')}/{unidecode(student.nganh).replace(' ', '')}/{student.lop}"
    os.makedirs(folder_path, exist_ok=True)

    # Lưu file ảnh
    # file_name = 'image1.jpg'
    file_path = os.path.join(folder_path, f"{nameStudentCard}.png")

    # Image.save cai la no bi reload
    img.save(file_path)
    
    # img.save(f'TheSinhVien/output/{nameStudentCard}.png')

def renderStudentCard2(student, i, outputPath, backgroundBase64):
    imageStudentPath = student.anhThe
    # Tạo ảnh nền cho thẻ sinh viên
    # img = Image.new('RGB', (width, hight), (255, 255, 255))
    # img = Image.open(backgroundImagePath)
    # Xử lý ảnh background từ base64
    backgroundBytes = base64.b64decode(backgroundBase64)
    img = Image.open(BytesIO(backgroundBytes))
    img = img.resize((width, hight))

    # Vẽ khung trên 
    draw = ImageDraw.Draw(img)
    hightHeader = int(hight/4)
    draw.rectangle((0, 0, width, hightHeader), fill =(0, 0, 102))

    
    # Tạo đối tượng QRCode
    qr = qrcode.QRCode(version=1, box_size=15, border=1)
    # Lưu dữ liệu vào QRCode
    data = student.hoTen
    qr.add_data(data)
    # Tạo QRCode
    qr.make(fit=True)
    # Lấy hình ảnh của QRCode
    imgQr = qr.make_image(fill_color="black", back_color="white")
    widthQr, heightQr = imgQr.size
    qr_pos = ((width - widthQr), (hight - heightQr))
    

    # Vẽ logo
    student_image = Image.open(student.anhThe)
    widthLogo = int(width/6)
    paddingLogo = 50
    hightLogo = int(hightHeader) - paddingLogo*2
    student_image = student_image.resize((widthLogo, hightLogo))
    img.paste(student_image, (paddingLogo, paddingLogo))

    # Tiêu đề trường phía trên
    fontHeader = ImageFont.truetype('arialbd.ttf', 100)
    headerTitle = "BỘ GIÁO DỤC VÀ ĐÀO TẠO"
    headerTitle2 = "TRƯỜNG ĐẠI HỌC PHÚ XUÂN"
    textWidthHeader, textHeightHeader = fontHeader.getsize(headerTitle)
    textWidthHeader2, textHeightHeader2 = fontHeader.getsize(headerTitle2)
    paddingLeft = ((width - widthLogo - paddingLogo * 2) - textWidthHeader) / 2 + (widthLogo + paddingLogo * 2)
    paddingLeft2 = ((width - widthLogo - paddingLogo * 2) - textWidthHeader2) / 2 + (widthLogo + paddingLogo * 2)
   
    paddingTop = (hightHeader - textHeightHeader) / 4
    paddingTop2 = (hightHeader - textHeightHeader2) / 1.5
  
    draw.text((paddingLeft, paddingTop), headerTitle, font=fontHeader, fill=(255, 204, 0))
    draw.text((paddingLeft2, paddingTop2), headerTitle2, font=fontHeader, fill=(255, 204, 0))

    # Ảnh sinh viên
    hightImage = int(hight / 2 )
    withImage = int(width / 4)
    # draw.rectangle((paddingLogo, hightHeader + 100, withImage, hightImage), fill ='black')
    imgLogo = Image.open(imageStudentPath)
    imgLogo = imgLogo.resize((withImage, hightImage))
    imageStudentPos = ((paddingLogo, hightHeader + 100))
    img.paste(imgLogo, imageStudentPos)

    # Thêm text Thẻ sinh viên
    fontStudentCard = ImageFont.truetype('arialbd.ttf', 120)
    titleStudentCard = "Thẻ Sinh Viên"
    textWidthStudentCard, textHeightStudentCard = fontStudentCard.getsize(titleStudentCard)
    paddingLeftStudentCard = ((width - withImage - paddingLogo * 2) - textWidthStudentCard) / 2 + (withImage + paddingLogo * 2)
    paddingTopStudentCard = (hightHeader  + 100) 
    draw.text((paddingLeftStudentCard, paddingTopStudentCard), titleStudentCard, font=fontStudentCard, fill=(180, 37, 50))

    # Thêm text Họ và tên
    fillText = (0, 0, 0)
    fontInfo= ImageFont.truetype('arial.ttf', 80)
    fontInfoDetail= ImageFont.truetype('arialbd.ttf', 80)
    paddingLeftInfo= paddingLogo * 2 + withImage
    paddingTopText = 130
    paddingTopName = paddingTopStudentCard + paddingTopText
    textWidthName, textHeightName = fontInfo.getsize("Họ và Tên")
    draw.text((paddingLeftInfo, paddingTopName), "Họ và Tên:", font=fontInfo, fill=fillText)
    draw.text((paddingLeftInfo + textWidthName + 50, paddingTopName), student.hoTen, font=fontInfoDetail, fill=fillText)


    paddingTopName = paddingTopStudentCard + paddingTopText * 2
    textWidthBirthday, textHeightBirthday = fontInfo.getsize("Ngày Sinh:")
    draw.text((paddingLeftInfo, paddingTopName), "Ngày Sinh:", font=fontInfo, fill=fillText)
    draw.text((paddingLeftInfo + textWidthBirthday + 50, paddingTopName), student.ngaySinh, font=fontInfoDetail, fill=fillText)


    paddingTopName = paddingTopStudentCard + paddingTopText * 3
    textWidthKhoa, textHeightKhoa = fontInfo.getsize("Khoa:")
    draw.text((paddingLeftInfo, paddingTopName), "Khoa:", font=fontInfo, fill=fillText)
    draw.text((paddingLeftInfo + textWidthKhoa + 50, paddingTopName), student.khoa, font=fontInfoDetail, fill=fillText)

    paddingTopName = paddingTopStudentCard + paddingTopText * 4
    textWidthKhoa, textHeightKhoa = fontInfo.getsize("Ngành:")
    draw.text((paddingLeftInfo, paddingTopName), "Ngành:", font=fontInfo, fill=fillText)
    draw.text((paddingLeftInfo + textWidthKhoa + 50, paddingTopName), student.nganh, font=fontInfoDetail, fill=fillText)

    paddingTopName = paddingTopStudentCard + paddingTopText * 5
    textWidthKhoa, textHeightKhoa = fontInfo.getsize("Niên khoá:")
    draw.text((paddingLeftInfo, paddingTopName), "Niên khoá:", font=fontInfo, fill=fillText)
    draw.text((paddingLeftInfo + textWidthKhoa + 50, paddingTopName), student.nienKhoa, font=fontInfoDetail, fill=fillText)

    paddingTopName = paddingTopStudentCard + paddingTopText * 6
    textWidthKhoa, textHeightKhoa = fontInfo.getsize("Mã sinh viên:")
    draw.text((paddingLeftInfo, paddingTopName), "Mã sinh viên:", font=fontInfo, fill=fillText)
    draw.text((paddingLeftInfo + textWidthKhoa + 50, paddingTopName), student.maSV, font=fontInfoDetail, fill=fillText)

    paddingTopName = paddingTopStudentCard + paddingTopText * 7
    textWidthKhoa, textHeightKhoa = fontInfo.getsize("Đại học 3 năm, tốt nghiệp sớm, việc làm ngay!")
    # draw.text((paddingLeftInfo, paddingTopName), "Mã sinh viên:", font=fontInfo, fill=fillText)
    draw.text(((width - textWidthKhoa - widthQr) / 2, paddingTopName), "Đại học 3 năm, tốt nghiệp sớm, việc làm ngay!", font=fontInfoDetail, fill=fillText)

    img.paste(imgQr, qr_pos)


    # draw.text((170, 100), student_name, font=font, fill=(0, 0, 0))
    nameStudentCard = f"{unidecode(student.hoTen).replace(' ', '')}"
    # Tạo thư mục mới
    folder_path = f"{outputPath}/{unidecode(student.khoa).replace(' ', '')}/{unidecode(student.nganh).replace(' ', '')}/{student.lop}"
    os.makedirs(folder_path, exist_ok=True)

    # Lưu file ảnh
    # file_name = 'image1.jpg'
    file_path = os.path.join(folder_path, f"{nameStudentCard}.png")

    # Image.save cai la no bi reload
    img.save(file_path)
    
    # img.save(f'TheSinhVien/output/{nameStudentCard}.png')


def renderStudentCard3(student, i, outputPath, backgroundBase64):
    imageStudentPath = student.anhThe
    # Tạo ảnh nền cho thẻ sinh viên
    # img = Image.new('RGB', (width, hight), (255, 255, 255))
    # img = Image.open(backgroundImagePath)
    # Xử lý ảnh background từ base64
    backgroundBytes = base64.b64decode(backgroundBase64)
    img = Image.open(BytesIO(backgroundBytes))
    img = img.resize((width, hight))

    # Vẽ khung trên 
    draw = ImageDraw.Draw(img)
    hightHeader = int(hight/4)
    draw.rectangle((0, 0, width, hightHeader), fill =(0, 0, 102))

    
    # Tạo đối tượng QRCode
    qr = qrcode.QRCode(version=1, box_size=15, border=1)
    # Lưu dữ liệu vào QRCode
    data = student.hoTen
    qr.add_data(data)
    # Tạo QRCode
    qr.make(fit=True)
    # Lấy hình ảnh của QRCode
    imgQr = qr.make_image(fill_color="black", back_color="white")
    widthQr, heightQr = imgQr.size
    qr_pos = ((width - widthQr), (hight - heightQr))
    

    # Vẽ logo
    student_image = Image.open(student.anhThe)
    widthLogo = int(width/6)
    paddingLogo = 50
    hightLogo = int(hightHeader) - paddingLogo*2
    student_image = student_image.resize((widthLogo, hightLogo))
    img.paste(student_image, (paddingLogo, paddingLogo))

    # Tiêu đề trường phía trên
    fontHeader = ImageFont.truetype('arialbd.ttf', 100)
    headerTitle = "BỘ GIÁO DỤC VÀ ĐÀO TẠO"
    headerTitle2 = "TRƯỜNG ĐẠI HỌC PHÚ XUÂN"
    textWidthHeader, textHeightHeader = fontHeader.getsize(headerTitle)
    textWidthHeader2, textHeightHeader2 = fontHeader.getsize(headerTitle2)
    paddingLeft = ((width - widthLogo - paddingLogo * 2) - textWidthHeader) / 2 + (widthLogo + paddingLogo * 2)
    paddingLeft2 = ((width - widthLogo - paddingLogo * 2) - textWidthHeader2) / 2 + (widthLogo + paddingLogo * 2)
   
    paddingTop = (hightHeader - textHeightHeader) / 4
    paddingTop2 = (hightHeader - textHeightHeader2) / 1.5
  
    draw.text((paddingLeft, paddingTop), headerTitle, font=fontHeader, fill=(255, 204, 0))
    draw.text((paddingLeft2, paddingTop2), headerTitle2, font=fontHeader, fill=(255, 204, 0))

    # Ảnh sinh viên
    hightImage = int(hight / 2 )
    withImage = int(width / 4)
    # draw.rectangle((paddingLogo, hightHeader + 100, withImage, hightImage), fill ='black')
    imgLogo = Image.open(imageStudentPath)
    imgLogo = imgLogo.resize((withImage, hightImage))
    imageStudentPos = ((paddingLogo, hightHeader + 100))
    img.paste(imgLogo, imageStudentPos)

    # Thêm text Thẻ sinh viên
    fontStudentCard = ImageFont.truetype('arialbd.ttf', 120)
    titleStudentCard = "Thẻ Sinh Viên"
    textWidthStudentCard, textHeightStudentCard = fontStudentCard.getsize(titleStudentCard)
    paddingLeftStudentCard = ((width - withImage - paddingLogo * 2) - textWidthStudentCard) / 2 + (withImage + paddingLogo * 2)
    paddingTopStudentCard = (hightHeader  + 100) 
    draw.text((paddingLeftStudentCard, paddingTopStudentCard), titleStudentCard, font=fontStudentCard, fill=(180, 37, 50))

    # Thêm text Họ và tên
    fillText = (0, 0, 0)
    fontInfo= ImageFont.truetype('arial.ttf', 80)
    fontInfoDetail= ImageFont.truetype('arialbd.ttf', 80)
    paddingLeftInfo= paddingLogo * 2 + withImage
    paddingTopText = 130
    paddingTopName = paddingTopStudentCard + paddingTopText
    textWidthName, textHeightName = fontInfo.getsize("Họ và Tên")
    draw.text((paddingLeftInfo, paddingTopName), "Họ và Tên:", font=fontInfo, fill=fillText)
    draw.text((paddingLeftInfo + textWidthName + 50, paddingTopName), student.hoTen, font=fontInfoDetail, fill=fillText)


    paddingTopName = paddingTopStudentCard + paddingTopText * 2
    textWidthBirthday, textHeightBirthday = fontInfo.getsize("Ngày Sinh:")
    draw.text((paddingLeftInfo, paddingTopName), "Ngày Sinh:", font=fontInfo, fill=fillText)
    draw.text((paddingLeftInfo + textWidthBirthday + 50, paddingTopName), student.ngaySinh, font=fontInfoDetail, fill=fillText)


    paddingTopName = paddingTopStudentCard + paddingTopText * 3
    textWidthKhoa, textHeightKhoa = fontInfo.getsize("Khoa:")
    draw.text((paddingLeftInfo, paddingTopName), "Khoa:", font=fontInfo, fill=fillText)
    draw.text((paddingLeftInfo + textWidthKhoa + 50, paddingTopName), student.khoa, font=fontInfoDetail, fill=fillText)

    paddingTopName = paddingTopStudentCard + paddingTopText * 4
    textWidthKhoa, textHeightKhoa = fontInfo.getsize("Ngành:")
    draw.text((paddingLeftInfo, paddingTopName), "Ngành:", font=fontInfo, fill=fillText)
    draw.text((paddingLeftInfo + textWidthKhoa + 50, paddingTopName), student.nganh, font=fontInfoDetail, fill=fillText)

    paddingTopName = paddingTopStudentCard + paddingTopText * 5
    textWidthKhoa, textHeightKhoa = fontInfo.getsize("Niên khoá:")
    draw.text((paddingLeftInfo, paddingTopName), "Niên khoá:", font=fontInfo, fill=fillText)
    draw.text((paddingLeftInfo + textWidthKhoa + 50, paddingTopName), student.nienKhoa, font=fontInfoDetail, fill=fillText)

    paddingTopName = paddingTopStudentCard + paddingTopText * 6
    textWidthKhoa, textHeightKhoa = fontInfo.getsize("Mã sinh viên:")
    draw.text((paddingLeftInfo, paddingTopName), "Mã sinh viên:", font=fontInfo, fill=fillText)
    draw.text((paddingLeftInfo + textWidthKhoa + 50, paddingTopName), student.maSV, font=fontInfoDetail, fill=fillText)

    paddingTopName = paddingTopStudentCard + paddingTopText * 7
    textWidthKhoa, textHeightKhoa = fontInfo.getsize("Đại học 3 năm, tốt nghiệp sớm, việc làm ngay!")
    # draw.text((paddingLeftInfo, paddingTopName), "Mã sinh viên:", font=fontInfo, fill=fillText)
    draw.text(((width - textWidthKhoa - widthQr) / 2, paddingTopName), "Đại học 3 năm, tốt nghiệp sớm, việc làm ngay!", font=fontInfoDetail, fill=fillText)

    img.paste(imgQr, qr_pos)


    # draw.text((170, 100), student_name, font=font, fill=(0, 0, 0))
    nameStudentCard = f"{unidecode(student.hoTen).replace(' ', '')}"
    # Tạo thư mục mới
    folder_path = f"{outputPath}/{unidecode(student.khoa).replace(' ', '')}/{unidecode(student.nganh).replace(' ', '')}/{student.lop}"
    os.makedirs(folder_path, exist_ok=True)

    # Lưu file ảnh
    # file_name = 'image1.jpg'
    file_path = os.path.join(folder_path, f"{nameStudentCard}.png")

    # Image.save cai la no bi reload
    img.save(file_path)
    
    # img.save(f'TheSinhVien/output/{nameStudentCard}.png')
