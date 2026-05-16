from playwright.sync_api import sync_playwright, Playwright
import random
from openpyxl import Workbook
from openpyxl.styles import Font
from twilio.rest import Client
import os
from dotenv import load_dotenv
import json
load_dotenv()

def run(playwright: Playwright):
    if os.path.exists("seen_jobs.json"):
        with open("seen_jobs.json", "r") as f:
            seen_jobs = set(json.load(f))
    else:
        seen_jobs = set()
    wb = Workbook()
    sheet = wb.active
    sheet.title = "Job Listings"
    chromium = playwright.chromium
    browser = chromium.launch(headless=True,  timeout=30000)
    page = browser.new_page()
    page.goto("https://remoteok.com/")
    page.wait_for_timeout(5000)
    headers = ["Role", "Company", "Salary", "Location", "Link", "Days Since Posted"]
    sheet.column_dimensions["A"].width = 100
    sheet.column_dimensions["B"].width = 100
    sheet.column_dimensions["C"].width = 100
    sheet.column_dimensions["D"].width = 100
    sheet.column_dimensions["E"].width = 100
    sheet.column_dimensions["F"].width = 100
    sheet.append(headers)
    for cell in sheet[1]:
        cell.font  = Font(bold=True)
    while True:
        try:
            page.locator("#premium-popup-close").click()
        except:
            pass

        for _ in range(5):
            page.keyboard.press("End")
            page.wait_for_timeout(random.randint(2000,3000))
        jobs = page.locator("table#jobsboard tr.job").all()
        for job in jobs:
            role = job.locator("h2").inner_text()
            company = job.locator("h3[itemprop='name']").inner_text().strip()
            salary_locator = job.locator("div.salary")
            salary = salary_locator.inner_text(timeout=30000) if salary_locator.count() > 0 else "No salary"
            location_locator = job.locator("div.location").first
            location = location_locator.inner_text(timeout=30000) if location_locator.count() > 0 else "No location"
            link_locator = job.locator("a[itemprop='url']")
            links = "https://remoteok.com" + link_locator.get_attribute("href")
            days_posted = job.locator("time").first.inner_text()
            if "h" in days_posted and links not in seen_jobs:
                send_whatsapp(f"New job: {role} at {company} — {links}")
                seen_jobs.add(links)
            sheet.append([role, company, salary, location, links, days_posted])
        with open(f"seen_jobs.json", "w") as f:
            json.dump(list(seen_jobs), f)
        wb.save("Remote Job listings.xlsx")
        break

def send_whatsapp(message):
    client = Client(os.getenv("account_sid"), os.getenv("auth_token"))
    client.messages.create(
        from_="whatsapp:+14155238886",
        to=f"whatsapp:{os.getenv('MY_PHONE_NUMBER')}",
        body=message
    )

with sync_playwright() as playwright:
    run(playwright)

