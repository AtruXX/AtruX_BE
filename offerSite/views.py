import gspread
from oauth2client.service_account import ServiceAccountCredentials
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
import tempfile

# Configurare Google Sheets API
SPREADSHEET_ID = '1cJXwzEXl6QIAWzZ2tksgCp_8BrfYMXiODH7p3asbxG8'  # ID-ul fișierului tău Google Sheets
CREDENTIALS_FILE = 'offerSite/offers-454115-2e54df6d665b.json'  # Calea către fișierul JSON descărcat
#CREDENTIALS_FILE = json.loads(CREDENTIALS_FILE_json)
#with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as temp_file:
#    temp_file.write(CREDENTIALS_FILE_json)
 #   file_path = temp_file.name  # Salvează calea fișierului

#CREDENTIALS_FILE = file_path

# Conectează-te la Google Sheets
def connect_to_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
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
            os.remove(file_path)  # Șterge fișierul temporar
            return JsonResponse({"message": "Datele au fost salvate în Google Sheets!"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Metodă nerecunoscută!"}, status=405)