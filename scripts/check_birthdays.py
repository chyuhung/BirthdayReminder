import json
from datetime import datetime, timedelta, timezone
from lunarcalendar import Converter, Lunar

def check_birthdays():
    # 获取当前时间
    today = datetime.now(timezone.utc).date()
    
    # 读取生日数据和提醒天数
    with open("birthdays.json") as f:
        config = json.load(f)
        reminder_days = config["reminder_days"]
        birthdays = config["birthdays"]

    remind_dates = [today + timedelta(days=i) for i in range(reminder_days + 1)]

    converter = Converter()

    for entry in birthdays:
        name = entry["name"]
        birthday = entry["birthday"]
        lunar = entry.get("lunar", True)

        # 解析生日
        if lunar:
            # 将农历日期转换为公历日期
            lunar_date = Lunar(year=today.year, month=int(birthday.split("-")[1]), day=int(birthday.split("-")[2]), isleap=False)
            solar_date = converter.lunar_to_solar(lunar_date)
            birthday_date = datetime(solar_date.year, solar_date.month, solar_date.day).date()
        else:
            birthday_date = datetime.strptime(birthday, "%Y-%m-%d").date()

        # 检查是否需要提醒
        if birthday_date in remind_dates:
            print(f"发送邮件给 {name}")
            # 使用 GitHub Actions 输出命令设置环境变量
            print(f"::set-output name=SEND_EMAIL::true")
            print(f"::set-output name=NAME::{name}")
            
if __name__ == "__main__":
    check_birthdays()