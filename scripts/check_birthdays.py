import json  # 导入json模块，用于读取和解析JSON文件
import os  # 导入os模块，用于访问环境变量
from datetime import datetime, timedelta, timezone  # 导入datetime模块中的类，用于处理日期和时间
from zhdate import ZhDate  # 导入zhdate库，用于农历与公历之间的转换

def check_birthdays():
    # 获取当前日期（UTC时区）
    today = datetime.now(timezone.utc).date()
    
    # 打开并读取包含生日信息的JSON文件
    with open("birthdays.json") as f:
        config = json.load(f)  # 解析JSON文件内容
        reminder_days = config["reminder_days"]  # 获取需要提前多少天开始提醒
        birthdays = config["birthdays"]  # 获取生日列表

    # 计算从今天起至未来reminder_days天内的所有日期
    remind_dates = [today + timedelta(days=i) for i in range(reminder_days + 1)]
    
    # 初始化两个列表，分别存储提前提醒和当天生日的名字
    advance_names = []
    today_names = []

    # 遍历每个生日条目
    for entry in birthdays:
        name = entry["name"]  # 获取名字
        birthday = entry["birthday"]  # 获取生日字符串
        lunar = entry.get("lunar", True)  # 获取是否是农历生日，默认为True

        # 如果是农历生日，则将其转换为对应的公历日期
        if lunar:
            year, month, day = map(int, birthday.split("-"))
            solar_date = ZhDate(year, month, day).to_datetime().date()
        else:
            # 如果是公历生日，则直接解析生日字符串为日期对象
            solar_date = datetime.strptime(birthday, "%Y-%m-%d").date()

        # 检查计算出的公历日期是否在需要提醒的日期范围内
        if solar_date in remind_dates:
            # 如果是今天的生日，添加到today_names列表中
            if solar_date == today:
                today_names.append(name)
            else:
                # 否则添加到advance_names列表中
                advance_names.append(name)

    # 将结果写入GitHub Actions的输出环境变量文件
    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        # 如果有提前提醒的名字，设置相应的输出参数
        if advance_names:
            print(f'SEND_ADVANCE_EMAIL=true', file=fh)  # 设置发送提前提醒邮件的标志
            print(f'ADVANCE_NAMES={"、".join(advance_names)}', file=fh)  # 写入提前提醒的名字
        # 如果有当天生日的名字，设置相应的输出参数
        if today_names:
            print(f'SEND_TODAY_EMAIL=true', file=fh)  # 设置发送当天生日提醒邮件的标志
            print(f'TODAY_NAMES={"、".join(today_names)}', file=fh)  # 写入当天生日的名字

if __name__ == "__main__":
    check_birthdays()  # 当脚本作为主程序运行时，调用check_birthdays函数