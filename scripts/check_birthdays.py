import json
from datetime import datetime, timedelta, timezone
from lunarcalendar import Converter, Solar, Lunar

def check_birthdays():
    # 获取当前时间
    today = datetime.now(timezone.utc).date()
    
    # 读取生日数据和提醒天数
    with open("birthdays.json") as f:
        config = json.load(f)
        reminder_days = config["reminder_days"]
        birthdays = config["birthdays"]

    remind_dates = [today + timedelta(days=i) for i in range(reminder_days + 1)]

    for entry in birthdays:
        name = entry["name"]
        birthday = entry["birthday"]
        lunar = entry.get("lunar", True)

        # 解析生日
        if lunar:
            # 将农历日期转换为公历日期
            lunar_date = Lunar.fromYmd(*[int(x) for x in birthday.split("-")])
            solar_date = Converter.LunarToSolar(lunar_date)
            birthday_date = solar_date.to_date()
        else:
            birthday_date = datetime.strptime(birthday, "%Y-%m-%d").date()

        # 检查是否需要提醒
        if birthday_date in remind_dates:
            print(f"发送邮件给 {name}")
            # 输出到环境变量以供GitHub Actions使用
            os.environ['SEND_EMAIL'] = 'true'
            os.environ['NAME'] = name
            
if __name__ == "__main__":
    check_birthdays()
