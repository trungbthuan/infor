import pandas as pd
# import openpyxl
import os

file_path = 'students.xlsx'
df = pd.read_excel(file_path)

def export_excel(file_path):
    df = pd.read_excel(file_path)
    # Bước chuẩn hóa dữ liệu (nếu cột điểm đang là văn bản '8,35')
    for col in ['mathematics', 'physics', 'chemistry']:
        # Thay ',' thành '.' và chuyển sang kiểu số thực (float)
        df[col] = df[col].astype(str).str.replace(',', '.').astype(float)
    # Sau đó mới tính trung bình
    df['average_score'] = round(df[['mathematics', 'physics', 'chemistry']].mean(axis=1),2)
    # Hoặc có thể làm như sau:
    # df['average_score'] = round((df['mathematics'] + df['physics'] + df['chemistry']) / 3,2)
    # Lưu kết quả ra file Excel mới
    df.to_excel('danh_sach_co_diem_tb.xlsx', index=False)

export_excel(file_path)
 
def get_fields(file_path):
    try:
        df = pd.read_excel(file_path)
        print(df.head(0))

        print("Danh sách tên từng người:")
        # Lặp qua từng hàng của DataFrame
        for index, row in df.iterrows():
            # 'row' là một Series chứa dữ liệu của hàng hiện tại
            print(row['full_name'] + " - " + str(row['ma_sv']))


    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy tệp tại đường dẫn: {file_path}")
    except Exception as e:
        print(f"Đã xảy ra lỗi khi đọc tệp: {e}")

get_fields(file_path)