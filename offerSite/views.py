import gspread
from oauth2client.service_account import ServiceAccountCredentials
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os

# Configurare Google Sheets API
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")  # ID-ul fișierului tău Google Sheets
CREDENTIALS_FILE_json = os.getenv("CREDENTIALS_FILE")  # Calea către fișierul JSON descărcat
CREDENTIALS_FILE = json.loads(CREDENTIALS_FILE_json)

# Conectează-te la Google Sheets
def connect_to_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(CREDENTIALS_FILE, scope)
    client = gspread.authorize(creds)
    return client.open_by_key(SPREADSHEET_ID).sheet1  # Deschide Sheet1

@csrf_exempt
def upload_to_google_sheets(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            telefon = data.get("telefon", "")
            email = data.get("email", "")
            numar_soferi = data.get("numar_soferi", "")

            sheet = connect_to_sheets()
            sheet.append_row([telefon, email, numar_soferi])

            return JsonResponse({"message": "Datele au fost salvate în Google Sheets!"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Metodă nerecunoscută!"}, status=405)