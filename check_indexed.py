import pandas as pd
import time
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

# OAuth 2.0 client secrets file downloaded from Google Cloud Console
CLIENT_SECRETS_FILE = 'C:\\Path\\To\\Your\\client_secrets.json' # IMPORTANT: Update with your path

# The scope for the Search Console API
SCOPES = ['https://www.googleapis.com/auth/webmasters']

# The path to your CSV file containing URLs to check
# The CSV should have a column named 'URL'
URLS_FILE_PATH = 'C:\\Path\\To\\Your\\URLs.csv' # IMPORTANT: Update with your path

# The full URL of the site property in Google Search Console (e.g., 'https://your-website.com/')
# Must match a verified property in your Search Console account.
# For domain properties, use 'sc-domain:your-domain.com'
SITE_URL = 'https://your-website.com/' # IMPORTANT: Update with your website URL

# Name for the output file
OUTPUT_FILE_NAME = 'inspection_results.csv'

# --- SCRIPT START ---

def authenticate():
    """Handles the OAuth 2.0 authentication flow."""
    print("Starting authentication...")
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    print("Authentication successful.")
    return build('searchconsole', 'v1', credentials=credentials)

def inspect_url(service, url, site_url):
    """Performs a single URL inspection API call and returns the results."""
    try:
        request_body = {"inspectionUrl": url, "siteUrl": site_url}
        response = service.urlInspection().index().inspect(body=request_body).execute()
        return response
    except HttpError as e:
        # Handle API errors (e.g., quota limits, invalid URLs)
        print(f"  -> Error inspecting URL {url}: {e}")
        return {"error": str(e)}

def main():
    """Main function to run the script."""
    # 1. Authenticate and build the API service
    search_console_service = authenticate()

    # 2. Read the URLs from the CSV file
    try:
        urls_df = pd.read_csv(URLS_FILE_PATH)
        if 'URL' not in urls_df.columns:
            print(f"Error: The CSV file at '{URLS_FILE_PATH}' must contain a column named 'URL'.")
            return
        urls_to_check = urls_df['URL'].dropna().unique().tolist()
        print(f"Found {len(urls_to_check)} unique URLs to inspect.")
    except FileNotFoundError:
        print(f"Error: The file at '{URLS_FILE_PATH}' was not found.")
        return

    # 3. Iterate through URLs, inspect them, and collect results
    inspection_data = []
    total_urls = len(urls_to_check)

    for i, url in enumerate(urls_to_check):
        print(f"Inspecting URL {i+1}/{total_urls}: {url}")
        
        response = inspect_url(search_console_service, url, SITE_URL)
        
        result_row = {'URL': url}

        if "error" in response:
            result_row['Coverage'] = 'API_ERROR'
            result_row['Verdict'] = response['error']
        else:
            inspection_result = response.get("inspectionResult", {})
            index_status = inspection_result.get("indexStatusResult", {})
            
            # Extract detailed information based on current API documentation
            result_row['Coverage'] = index_status.get("coverageState", "N/A")
            result_row['Verdict'] = index_status.get("verdict", "N/A")
            result_row['Indexing State'] = index_status.get("indexingState", "N/A")
            result_row['Last Crawl Time'] = index_status.get("lastCrawlTime", "N/A")
            result_row['Google Canonical'] = index_status.get("googleCanonical", "N/A")
            result_row['User Canonical'] = index_status.get("userCanonical", "N/A")

        inspection_data.append(result_row)
        
        # IMPORTANT: Be respectful of the API quota. 1-2 seconds is a safe delay.
        time.sleep(1.5)

    # 4. Create a DataFrame from the results and save it
    results_df = pd.DataFrame(inspection_data)
    
    # Merge with original data to keep other columns if they exist
    final_df = pd.merge(urls_df, results_df, on='URL', how='left')
    
    final_df.to_csv(OUTPUT_FILE_NAME, index=False)
    print(f"\nProcess complete. Results saved to '{OUTPUT_FILE_NAME}'.")

if __name__ == '__main__':
    main()
