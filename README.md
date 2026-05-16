Remote Job Scraper
Monitors Remote OK for new job listings and sends Whatsapp alerts when new jobs are posted.
What it collects,
.Job-Title
.Company
.Salary
.Location
.Job link
.Days since posted
Tech Stack
.Python
.Playwright
.openpyxl
.Twilio
.Docker
.Railway
Features
.Infinite scroll pagination to scrape hundreds of listings
.Whatsapp alerts for job posted within the last 24 hours
.Duplicate prevention - never alerts on the same job twice
.Deployed on Railway and runs 24/7 without manual intervention
.Excel export of all scraped listings
How to run
. Clone the repo
. Add .env with require keys
.Install dependencies: 'pip install -r  requirements.txt'
.Install browsers: 'playwright install'
Run 'main.py'
Environment Variables
- 'account_sid' - Twilio Account SID
- 'auth_token' - Twilio Auth Token
- 'MY_PHONE_NUMBER' - Your Whatsapp number in international format
