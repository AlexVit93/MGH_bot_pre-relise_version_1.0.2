# import os
# from docx import Document
# from uuid import uuid4
# from google.oauth2.service_account import Credentials
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload


# def create_docx(data):
#     doc = Document()
#     doc.add_paragraph(f"User ID: {data['user_id']}")
#     doc.add_paragraph(f"Name: {data['name']}")
#     doc.add_paragraph(f"Phone_number: {data['phone_number']}")
#     doc.add_paragraph(f"Age: {data['age']}")

#     for question, answer in data["answers"].items():
#         doc.add_paragraph(f"{question}: {answer}")

#     doc.add_paragraph(f"Recommendations: {data['recommendations']}")

#     filename = f"{uuid4().hex}.docx"
#     doc.save(filename)

#     return filename


# def upload_to_drive(filename):
#     creds = Credentials.from_service_account_file("local-volt-399322-5c1d9c000102.json")
#     drive_service = build("drive", "v3", credentials=creds)

#     file_metadata = {"name": filename, "parents": ["1Ly8tlk0aCEEql5_cN7_EnO8H_rQ9Shn0"]}
#     media = MediaFileUpload(filename)
#     drive_service.files().create(body=file_metadata, media_body=media).execute()


# def generate_and_upload(data):
#     filename = create_docx(data)
#     upload_to_drive(filename)
#     os.remove(filename)

from google.oauth2.service_account import Credentials
import gspread
from gspread import Spreadsheet, Worksheet
from googleapiclient.discovery import build


def get_or_create_worksheet(
    sheet: Spreadsheet, title: str, rows: int, cols: int
) -> Worksheet:
    """Получить или создать лист в таблице"""
    try:
        worksheet = sheet.worksheet(title)
    except gspread.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title=title, rows=rows, cols=cols)
    return worksheet


def append_data_to_sheet(data):
    """Добавить данные в Google Sheet и вернуть его ID"""
    # creds = Credentials.from_service_account_file("local-volt-399322-5c1d9c000102.json")
    gc = gspread.service_account(filename="local-volt-399322-5c1d9c000102.json")

    try:
        sheet = gc.open("Данные клиентов")
    except gspread.SpreadsheetNotFound:
        sheet = gc.create("Данные клиентов")

    worksheet = get_or_create_worksheet(
        sheet, "Лист1", 1000, 10
    )  # устанавливаем размерность рабочего листа

    # Если лист пустой, создаем заголовки
    if worksheet.row_count == 0:
        worksheet.append_row(["User ID", "Name", "Phone_number", "Age"])

    # Добавляем данные в лист
    row_data = [data["user_id"], data["name"], data["phone_number"], data["age"]]
    worksheet.append_row(row_data)

    for question, answer in data["answers"].items():
        worksheet.append_row([question, answer])

    return sheet.id  # Возвращаем ID листа


def move_sheet_to_folder(sheet_id, folder_id):
    """Переносим Google Sheet в желаемую папку на Google Drive"""
    creds = Credentials.from_service_account_file("local-volt-399322-5c1d9c000102.json")
    drive_service = build("drive", "v3", credentials=creds)
    try:
        # Получить текущие родительские папки файла
        file = drive_service.files().get(fileId=sheet_id, fields="parents").execute()
        previous_parents = ",".join(file.get("parents"))

        # Обновляем файл, добавляем новую папку и удаляем старую
        file = (
            drive_service.files()
            .update(
                fileId=sheet_id,
                addParents=folder_id,
                removeParents=previous_parents,
                fields="id, parents",
            )
            .execute()
        )

    except Exception as e:
        print("Error moving file:", e)


def generate_and_upload(data):
    sheet_id = append_data_to_sheet(data)  # Теперь функция возвращает ID листа
    folder_id = "1X5ob9lThUW54-RO_jfiSaaDISNEgGEs1"
    move_sheet_to_folder(sheet_id, folder_id)
