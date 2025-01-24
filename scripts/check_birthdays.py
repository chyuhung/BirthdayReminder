import json
import os
from datetime import datetime, timedelta, timezone
from zhdate import ZhDate

def check_birthdays():
    # 获取当前时间
    today = datetime.now(timezone.utc).date()
    
    # 读取生日数据和提醒天数
    with open("birthdays.json") as f:
        config = json.load(f)
        reminder_days = config["reminder_days"]
        birthdays = config["birthdays"]

    remind_dates = [today + timedelta(days=i) for i in range(reminder_days + 1)]

    need_to_send_email = False
    name_to_send = ""

    for entry in birthdays:
        name = entry["name"]
        birthday = entry["birthday"]
        lunar = entry.get("lunar", True)

        if lunar:
            year, month, day = map(int, birthday.split("-"))
            solar_date = ZhDate(today.year, month, day).to_datetime().date()
        else:
            solar_date = datetime.strptime(birthday, "%Y-%m-%d").date()

        if solar_date in remind_dates:
            need_to_send_email = True
            name_to_send = name

    if need_to_send_email:
        with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
            print(f'SEND_EMAIL=true', file=fh)
            print(f'NAME={name_to_send}', file=fh)

if __name__ == "__main__":
    check_birthdays()