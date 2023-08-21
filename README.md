# Bulk URLs Index Checker with Google Search Console API with Python

## Overview

This script allows you to check the indexed status of a list of URLs using Google's Search Console API. You can specify the URLs to check in a CSV file, and the script will iterate through them, checking whether they are indexed by Google.

## Prerequisites

- **Python 3.x**: The script is written in Python 3.
- **Google Search Console Access**: You need access to the Google Search Console of the site you want to inspect.
- **Client Secrets JSON File**: Obtain this file from your Google Developer Console as part of enabling the Search Console API.

## Dependencies

- pandas
- googleapiclient
- google-auth-oauthlib

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/fajela/check-if-indexed-in-google.git
2. Install the required dependencies:
   ```bash
   pip install pandas google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client   
  
## Usage
1. Update the client_secrets_file variable with the path to your OAuth 2.0 client secrets JSON file.
2. Update the file_path variable with the path to your CSV file containing the URLs to check.
3. Update the site_url variable with your website URL.
4. Run the script:
   ```bash
   python check_index.py

The script will generate a CSV file (updated_file.csv) containing the indexed status of each URL.
