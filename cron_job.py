import schedule
import time
# Pull scripts from Google Sheets API (add gspread dep if needed)
schedule.every().day.at("09:00").do(lambda: generate_batch())  # Define batch func
while True:
    schedule.run_pending()
    time.sleep(60)