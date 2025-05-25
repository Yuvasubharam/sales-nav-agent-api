# LinkedIn Sales Navigator Lead Generation Agent

An automated tool that generates leads from LinkedIn Sales Navigator using PhantomBuster and exports them to Google Sheets.

## Features

- Automated lead generation from LinkedIn Sales Navigator
- Integration with PhantomBuster for data extraction
- Data cleaning and formatting
- Export to Google Sheets
- RESTful API interface

## Prerequisites

1. PhantomBuster account and API key
2. LinkedIn Sales Navigator account
3. Google Cloud project with Sheets API enabled
4. Python 3.7+

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your credentials
4. Place your Google Service Account credentials in `credentials.json`

## Configuration

1. PhantomBuster Setup:
   - Create a new PhantomBuster agent
   - Get your API key and agent ID
   - Add them to your `.env` file

2. Google Sheets Setup:
   - Create a new Google Sheet
   - Share it with your service account email
   - Add the Sheet ID to your `.env` file

## Usage

1. Start the Flask server:
   ```bash
   python main.py
   ```

2. Make a POST request to `/process` with the following JSON body:
   ```json
   {
     "company_name": "Target Company",
     "website": "https://company.com",
     "phantom_key": "your_phantombuster_api_key",
     "phantom_id": "your_agent_id",
     "sheet_id": "your_google_sheet_id",
     "creds_file": "path_to_credentials.json"
   }
   ```

## Response Format

Success Response:
```json
{
  "status": "success"
}
```

Error Response:
```json
{
  "status": "error",
  "message": "Error details"
}
```

## Data Fields

The tool extracts and exports the following data:
- Full Name
- Job Title
- Company Name
- Location
- LinkedIn URL

## Error Handling

- Invalid credentials will return appropriate error messages
- Network issues are handled with timeouts
- Missing data fields are handled gracefully

## Security Notes

- Keep your API keys and credentials secure
- Don't commit `.env` or `credentials.json` to version control
- Use environment variables in production

## License

MIT License

## Disclaimer

Use this tool in accordance with LinkedIn's terms of service and usage limits.