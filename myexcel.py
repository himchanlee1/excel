from openpyxl import load_workbook
from myeasyocr import extract_shipment_info
from datetime import datetime

def format_date(date_input):
    try:
        return datetime.strptime(date_input, "%y.%m.%d").strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError(f"날짜 형식을 인식할 수 없습니다: {date_input}")


def update_excel(file_path, waybill_number, shipment_weight, pickup_date, ready_time, blood_collection_date):
    book = load_workbook(file_path)
    sheet = book.active

    shipment_weight_num = float(shipment_weight)
    temperature_status = 'F' if shipment_weight_num >= 4.1 else 'A' if shipment_weight_num == 1.0 else 'Unknown'

    sheet['D5'] = waybill_number
    sheet['E5'] = temperature_status
    sheet['K5'] = format_date(pickup_date)
    sheet['L5'] = '12:00' if ready_time == '오전' else '16:00' if ready_time == '오후' else ready_time
    sheet['M5'] = format_date(blood_collection_date)
    
    book.save(file_path)
    book.close()

def read_pickup_date(file_path='C:\Python\bill\코반스 픽업요청서 양식.xlsx'):
    book = load_workbook(file_path)
    sheet = book.active

    date = str(sheet['K5'].value)
    return date

def read_excel(file_path):
    # House Air Bill #, Expected Date of delivery 불러오기
    book = load_workbook(file_path)
    sheet = book.active

    billNum = sheet['D5'].value
    date = list(str(sheet['K5'].value).split('-'))
    print('date:', date)
    yy = date[0]
    mm = date[1]
    dd = date[2]

    mm_dict = {
        '01': 'JAN',
        '02': 'FEB',
        '03': 'MAR',
        '04': 'APR',
        '05': 'MAY',
        '06': 'JUN',
        '07': 'JUL',
        '08': 'AUG',
        '09': 'SEP',
        '10': 'OCT',
        '11': 'NOV',
        '12': 'DEC',
    }

    return billNum, '{}{}{}'.format(dd, mm_dict[mm], yy)



def main():
    # 이미지와 엑셀 파일 경로를 직접 지정합니다.
    image_path = r'C:\Python\bill\waybill.jpg'
    file_path = r'C:\Python\bill\코반스 픽업요청서 양식.xlsx'

    shipment_weight, waybill_number = extract_shipment_info(image_path)
    
    pickup_date = input("픽업 날짜를 YY.MM.DD 형식으로 입력하세요: ")
    ready_time = input("준비된 시간이 오전인가요 오후인가요? (오전/오후로 입력): ")
    blood_collection_date = input("채혈 날짜를 YY.MM.DD 형식으로 입력하세요: ")

    try:
        update_excel(file_path, waybill_number, shipment_weight, pickup_date, ready_time, blood_collection_date)

        print('saved waybill:', waybill_number)

        print("엑셀 파일이 성공적으로 업데이트 되었습니다.")
    except Exception as e:
        print(f"에러가 발생했습니다: {e}")

# if __name__ == "__main__":
#     main()

