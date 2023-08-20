import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# OAuth 2.0 client secrets file
client_secrets_file = 'C:\\Path\\To\\Your\\client_secrets.json' # Update with your path
scopes = ['https://www.googleapis.com/auth/webmasters']

# Start the OAuth 2.0 flow
flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
credentials = flow.run_local_server()

# Read the URLs from the CSV file
file_path = 'C:\\Path\\To\\Your\\URLs.csv' # Update with your path
urls_to_check_df = pd.read_csv(file_path)
urls_to_check = urls_to_check_df['URL'].dropna().apply(str).tolist()
site_url = 'https://your-website.com/' # Update with your website URL

# Build the Search Console API service
search_console_service = build('searchconsole', 'v1', credentials=credentials)

# Iterate through URLs and check the indexed status
for url in urls_to_check:
    request_body = {"inspectionUrl": url, "siteUrl": site_url}
    response = search_console_service.urlInspection().index().inspect(body=request_body).execute()
    
    inspection_result = response.get("inspectionResult", {})
    index_status_result = inspection_result.get("indexStatusResult", {})
    verdict = index_status_result.get("verdict", "Unknown")
    urls_to_check_df.loc[urls_to_check_df['URL'] == url, 'Indexed'] = verdict

# Save the updated CSV
output_file_name = 'updated_file.csv'
urls_to_check_df.to_csv(output_file_name, index=False)

print("File saved successfully!")
