import time
import requests
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

# === Construct Sales Navigator URL ===
def construct_sales_nav_url(company_name):
    base_url = "https://www.linkedin.com/sales/search/companies"
    query = company_name.replace(" ", "%20")
    return f"{base_url}?keywords={query}"

# === Trigger PhantomBuster ===
def trigger_phantombuster_agent(api_key, agent_id, sales_nav_url):
    url = f"https://api.phantombuster.com/api/v2/agents/launch"
    headers = {"X-Phantombuster-Key-1": api_key}
    payload = {
        "id": agent_id,
        "argument": {
            "spreadsheetUrl": sales_nav_url,
            "numberOfProfiles": 100,
            "sessionCookie": "YOUR_LINKEDIN_SESSION_COOKIE"  # or remove if already set
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["containerId"]

# === Poll PhantomBuster Until Done ===
def poll_phantombuster_result(api_key, container_id):
    result_url = f"https://api.phantombuster.com/api/v2/containers/fetch-output?id={container_id}"
    headers = {"X-Phantombuster-Key-1": api_key}
    for _ in range(30):  # ~3 minutes
        resp = requests.get(result_url, headers=headers)
        if resp.status_code == 200 and "csvUrl" in resp.json():
            return resp.json()["csvUrl"]
        time.sleep(6)
    raise TimeoutError("PhantomBuster took too long to respond.")

# === Clean and Format CSV Data ===
def clean_data(csv_url):
    df = pd.read_csv(csv_url)
    keep_cols = ['firstName', 'lastName', 'linkedinUrl', 'jobTitle', 'companyName', 'location']
    df = df[[col for col in keep_cols if col in df.columns]]
    df.dropna(subset=["linkedinUrl"], inplace=True)
    df["fullName"] = df["firstName"] + " " + df["lastName"]
    return df[["fullName", "jobTitle", "companyName", "location", "linkedinUrl"]]

# === Write to Google Sheet ===
def export_to_google_sheets(df, sheet_id, creds_file):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = service_account.Credentials.from_service_account_file(creds_file, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    # Clear previous content
    sheet.values().clear(spreadsheetId=sheet_id, range='Sheet1').execute()

    # Prepare data
    values = [df.columns.tolist()] + df.values.tolist()
    body = {'values': values}
    sheet.values().update(
        spreadsheetId=sheet_id,
        range='Sheet1!A1',
        valueInputOption='RAW',
        body=body
    ).execute()

# === Run Agent Entry Point ===
def run_agent(company_name, website, phantom_key, phantom_id, sheet_id, creds_file):
    print(f"[INFO] Starting lead scrape for: {company_name}")
    search_url = construct_sales_nav_url(company_name)
    container_id = trigger_phantombuster_agent(phantom_key, phantom_id, search_url)
    csv_url = poll_phantombuster_result(phantom_key, container_id)
    df = clean_data(csv_url)
    export_to_google_sheets(df, sheet_id, creds_file)
    print(f"[SUCCESS] Exported {len(df)} leads to Google Sheets.")