from docx import Document
from uuid import uuid4
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


def create_docx(data):
    doc = Document()
    doc.add_paragraph(f"User ID: {data['user_id']}")
    doc.add_paragraph(f"Name: {data['name']}")
    doc.add_paragraph(f"Phone_number: {data['phone_number']}")
    doc.add_paragraph(f"Answers: {data['answers']}")
    doc.add_paragraph(f"Recommendations: {data['recommendations']}")

    filename = f"{uuid4().hex}.docx"
    doc.save(filename)

    return filename


def upload_to_drive(filename):
    creds = Credentials.from_service_account_file("your_service_account.json")
    drive_service = build("drive", "v3", credentials=creds)

    file_metadata = {"name": filename}
    media = MediaFileUpload(filename)
    drive_service.files().create(body=file_metadata, media_body=media).execute()


def generate_and_upload(data):
    filename = create_docx(data)
    upload_to_drive(filename)
