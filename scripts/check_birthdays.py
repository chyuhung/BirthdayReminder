import json
from datetime import datetime, timedelta, timezone
from lunarcalendar import Converter

def check_birthdays():
    # 获取当前时间
    today = datetime.now(timezone.utc).date()
    reminder_days = 3  # 提前提醒天数
    remind_dates = [today + timedelta(days=i) for i in range(reminder_days + 1)]

    # 读取生日数据
    with open("birthdays.json") as f:
        birthdays = json.load(f)

    for entry in birthdays:
        name = entry["name"]
        birthday = entry["birthday"]
        lunar = entry.get("lunar", False)

        # 解析生日
        if lunar:
            lunar_date = Converter().solar_to_lunar(today.year, int(birthday.split("-")[1]), int(birthday.split("-")[2]))
            birthday_date = datetime(lunar_date.lunar_year, lunar_date.lunar_month, lunar_date.lunar_day).date()
        else:
            birthday_date = datetime.strptime(birthday, "%Y-%m-%d").date()

        # 检查是否是今天或提前几天
        if birthday_date in remind_dates:
            print(f"Sending email for {name}")
            print(f"name={name}" >> "$GITHUB_ENV")  # 将名字保存到环境变量
            print("send_email=true" >> "$GITHUB_ENV")  # 设置发送邮件标志
            print(f"recipient=${{ secrets.TO_EMAIL }}" >> "$GITHUB_ENV")  # 收件人

if __name__ == "__main__":
    check_birthdays()
