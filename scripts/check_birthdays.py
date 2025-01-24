import json
from datetime import datetime, timedelta, timezone
from lunarcalendar import Converter, Solar, Lunar

def check_birthdays():
    # 获取当前时间
    today = datetime.now(timezone.utc).date()
    # 提前提醒天数
    reminder_days = entry["reminder_days"]
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
            solar_date = Solar(today.year, int(birthday.split("-")[1]), int(birthday.split("-")[2]))
            lunar_date = Converter.Solar2Lunar(solar_date)
            birthday_date = Converter.Lunar2Solar(Lunar(today.year, lunar_date.month, lunar_date.day, lunar_date.isleap)).to_date()
        else:
            birthday_date = datetime.strptime(birthday, "%Y-%m-%d").date()

        # 检查是否是今天或提前几天
        if birthday_date in remind_dates:
            print(f"Sending email for {name}")
            # 输出到环境变量以供GitHub Actions使用
            print(f"name={name}", flush=True)  # 将名字保存到环境变量
            print(f"send_email=true", flush=True)  # 设置发送邮件标志
            
if __name__ == "__main__":
    check_birthdays()
