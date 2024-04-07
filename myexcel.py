from openpyxl import load_workbook
import easyocr
import re
from datetime import datetime

def format_date(date_input):
    try:
        return datetime.strptime(date_input, "%y.%m.%d").strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError(f"날짜 형식을 인식할 수 없습니다: {date_input}")

def extract_shipment_info(image_path):
    reader = easyocr.Reader(['en'])
    results = reader.readtext(image_path)
    shipment_weight = "0"
    waybill_number = ""

    for bbox, text, prob in results:
        if "Shpt Wght" in text or "kg" in text:
            weight_search = re.search(r'(\d+\.\d+|\d+)\s*kg', text, re.IGNORECASE)
            if weight_search:
                shipment_weight = weight_search.group(1)

        # WAYBILL 텍스트가 포함된 라인에서 숫자 추출
        if "WAYBILL" in text.upper():
            numbers = re.findall(r'\d+', text)
            # 숫자들을 연결하여 WAYBILL 번호 생성
            waybill_candidate = ''.join(numbers)
            # WAYBILL 번호가 일반적으로 10자리임을 확인
            if len(waybill_candidate) == 10:
                waybill_number = waybill_candidate
                break

    if not waybill_number:
        raise ValueError("Waybill 번호를 찾을 수 없습니다.")

    return shipment_weight, waybill_number

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

if __name__ == "__main__":
    main()