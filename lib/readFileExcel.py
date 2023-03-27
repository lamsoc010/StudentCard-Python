# pip install wheel
# pip install pandas
# pip install openpyxl
import model.Student as student
import pandas as pd


def readExcel(url):
    try:
        # đọc file excel
        # skiprows: bỏ qua n dòng đầu tiên
        # usecols: chỉ đọc cột 1 => 8
        # dtype: định dạng kiểu dữ liệu
        require_cols = [1, 2, 3, 4, 5, 6, 7, 8, 9]  # thêm cột trạng thái vào danh sách cột
        dataframe1 = pd.read_excel(
            url,  skiprows=1, usecols=require_cols)
        listStudent = []
        for i in range(len(dataframe1)):
            status = dataframe1.iloc[i, 8]  # lấy giá trị trạng thái tại cột 9
                # kiểm tra các trường có giá trị hay không
            if any(dataframe1.iloc[i, :].isnull()):
                continue  # bỏ qua hàng này và chuyển sang hàng tiếp theo
            sv = student.Student(dataframe1.iloc[i, 0], dataframe1.iloc[i, 1], dataframe1.iloc[i, 2], dataframe1.iloc[i, 3],
                        dataframe1.iloc[i, 4], dataframe1.iloc[i, 5], dataframe1.iloc[i, 6], dataframe1.iloc[i, 7], status)
            listStudent.append(sv)
                # cập nhật trạng thái trên file Excel
                # dataframe1.at[i, 8] = 1  # đặt giá trị trạng thái tại hàng i là 1
        # # lưu file Excel
        # with pd.ExcelWriter(url) as writer:
        #     dataframe1.to_excel(writer, index=False)
        return listStudent
    except Exception as e:
        return "Lỗi rồi: " + str(e)

def readExcel2(url):
    try:
        # đọc file excel
        # skiprows: bỏ qua n dòng đầu tiên
        # usecols: chỉ đọc cột 1 => 8
        # dtype: định dạng kiểu dữ liệu
        require_cols = [1, 2, 3, 4, 5, 6, 7, 8, 9]  # thêm cột trạng thái vào danh sách cột
        dataframe1 = pd.read_excel(
            url,  skiprows=1, usecols=require_cols)
        listStudent = []
        for i in range(len(dataframe1)):
            sv = student.Student(dataframe1.iloc[i, 0], dataframe1.iloc[i, 1], dataframe1.iloc[i, 2], dataframe1.iloc[i, 3],
                        dataframe1.iloc[i, 4], dataframe1.iloc[i, 5], dataframe1.iloc[i, 6], dataframe1.iloc[i, 7], dataframe1.iloc[i, 8])
            listStudent.append(sv)
        return listStudent
    except Exception as e:
        return "Lỗi rồi: " + str(e)


import pandas as pd

def writeExcel(url, listStudent):
    # Đọc dữ liệu từ file Excel vào DataFrame
    df = pd.read_excel(url, skiprows= 1)

    # Duyệt qua danh sách sinh viên
    for student in listStudent:
        # Tìm các dòng có cùng mã sinh viên với sinh viên hiện tại và cập nhật trạng thái của sinh viên trong DataFrame
        df.iloc[(df.iloc[:, 1] == student.maSV).values, 9] = 1

    # Ghi DataFrame vào file Excel
    df.to_excel(url, index=False, header=True, startrow=1)

def readExcel1(url):
    return url


# listStudent = SortListStudent(listStudent)
# printListStudent(listStudent)
# statistical(listStudent)