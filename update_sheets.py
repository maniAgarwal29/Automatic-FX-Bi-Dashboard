# ===================================================================================
#  Automated Currency Exchange Rate Collector (for Google Sheets)
#
#  This script connects to the Google Sheets API using your secret key file,
#  fetches 15 years of currency data, and automatically updates your
#  online spreadsheet.
# ===================================================================================

import pandas as pd
import requests
from datetime import date, timedelta, datetime
import gspread
from google.oauth2.service_account import Credentials
import sys

# --- Step 1: Configuration ---

# The name of your secret key file. It must be in the same folder as this script.
SERVICE_ACCOUNT_FILE = 'automated-fx-dashboard-468013-1bcbf87fb795.json'

# The full web address (URL) of your Google Sheet.
GOOGLE_SHEET_URL = 'https://docs.google.com/spreadsheets/d/1aBFZccGl8TH3bSrtpPaWFTzCMwqLBMmuAQ7jGbc4QgY/edit?gid=0#gid=0'

# The settings for the data we want to fetch.
START_DATE_HISTORY = "2010-01-01"
BASE_CURRENCY_TO_FETCH = "USD"
TARGET_CURRENCIES_TO_FETCH = ["INR", "EUR", "GBP", "JPY", "AUD", "CAD", "CNY"]

def connect_to_google_sheets():
    print("🔑 Authenticating with Google...")
    try:
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file"]
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
        client = gspread.authorize(creds)
        print("✅ Success! Authenticated.")
        return client
    except Exception as e:
        print(f"❌ FATAL ERROR during authentication: {e}")
        sys.exit()

def get_the_spreadsheet(client):
    print(f"📄 Opening your Google Sheet by its URL...")
    try:
        spreadsheet = client.open_by_url(GOOGLE_SHEET_URL)
        worksheet = spreadsheet.sheet1
        print("✅ Successfully opened the sheet.")
        return worksheet
    except Exception as e:
        print(f"❌ FATAL ERROR while opening the sheet: {e}")
        sys.exit()

def get_latest_date_from_sheet(worksheet):
    print("🔍 Checking for the last saved date...")
    try:
        date_column = worksheet.col_values(1)[1:]
        if not date_column:
            print("📋 Sheet is empty. Will fetch all data.")
            return datetime.strptime(START_DATE_HISTORY, "%Y-%m-%d").date()
        else:
            latest_date = datetime.strptime(max(date_column), "%Y-%m-%d").date()
            print(f"🔍 Last saved date found: {latest_date}.")
            return latest_date + timedelta(days=1)
    except Exception as e:
        print(f"⚠ Could not check for the last date. Will fetch all data. Error: {e}")
        return datetime.strptime(START_DATE_HISTORY, "%Y-%m-%d").date()

def fetch_data_and_save(worksheet, start_date_to_fetch):
    today = date.today()
    if start_date_to_fetch > today:
        print("✅ Your spreadsheet is already up to date.")
        return

    print(f"🌍 Fetching new data from {start_date_to_fetch.strftime('%Y-%m-%d')} to {today.strftime('%Y-%m-%d')}...")
    api_url = f"https://api.frankfurter.app/{start_date_to_fetch.strftime('%Y-%m-%d')}..{today.strftime('%Y-%m-%d')}?from={BASE_CURRENCY_TO_FETCH}&to={','.join(TARGET_CURRENCIES_TO_FETCH)}"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        if 'rates' not in data or not data['rates']:
            print("📭 No new data was available from the API.")
            return

        df = pd.DataFrame(data['rates']).T
        df = df.reset_index().rename(columns={'index': 'Date'})
        df['Base'] = data['base']
        df = df.sort_values(by='Date')

        rows_to_add = []
        for index, row in df.iterrows():
            new_row = [row['Date'], row['Base']]
            for currency in TARGET_CURRENCIES_TO_FETCH:
                if currency in row and pd.notna(row[currency]):
                    new_row.append(f"{row[currency]:.6f}")
                else:
                    new_row.append(None)
            rows_to_add.append(new_row)

        print(f"✍ Writing {len(rows_to_add)} new day(s) of data to your Google Sheet...")
        worksheet.append_rows(rows_to_add, value_input_option='USER_ENTERED')
        
        print("🎉 Success! Your Google Sheet is now up to date.")
    except Exception as e:
        print(f"❌ A problem occurred during the fetch or save process. Error: {e}")

if __name__ == "__main__":
    print("--- Starting the Automated Google Sheet Updater ---")
    g_client = connect_to_google_sheets()
    g_worksheet = get_the_spreadsheet(g_client)
    start_date = get_latest_date_from_sheet(g_worksheet)
    fetch_data_and_save(g_worksheet, start_date)
    print("--- Script has finished its work. ---")