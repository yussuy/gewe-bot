from gewechat_client import GewechatClient
import logging
import os
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
from serverchan_sdk import sc_send
from util.weather import getWeather
from util.contacts import find_chatroomid, find_inspecter


def remind_bot(app_id, client, schedule_members, nickname_relate):
    
    # 获取巡检群id
    chatroom_id = find_chatroomid(client, app_id, 'xxxx微信群')

    # 获取巡检人群昵称nickname
    today_add_1=(datetime.now()+timedelta(days=1)).strftime("%m-%d")
    inspecter = schedule_members.get(today_add_1)
    if inspecter is None:
        return None
    print(inspecter)
    nickname = nickname_relate.get(inspecter)
    if nickname is None:
        return None
    print(nickname)
    
    # 获取巡检人昵称
    chatroom_name, wxid = find_inspecter(client, app_id, chatroom_id, nickname)
    print("巡检人信息:", chatroom_name, wxid)

    # 获取明天天气
    whole_today_add_1=(datetime.now()+timedelta(days=1)).strftime("%Y-%m-%d")
    weather = getWeather(whole_today_add_1)
    msg = '@' + chatroom_name + ' \n明日巡检，记得早睡早起。\n' + '-----------------------------------------\n' + weather
    
    send_msg_result = client.post_text(app_id, chatroom_id, msg, wxid)
    if send_msg_result.get('ret') != 200:
        print("发送消息失败:", send_msg_result)
        return
    print("发送消息成功:", send_msg_result)
    logger.info("巡检人:" + inspecter + " 日期:" + today_add_1)
    logger.info('执行提醒服务。。。')

def main():
    # 创建日志记录器
    global logger
    logger = logging.getLogger(__name__)
    # 设置日志级别
    logger.setLevel(logging.DEBUG)
    # 创建日志文件句柄
    file_handler = logging.FileHandler('log.txt')
    # 设置日志格式
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
    file_handler.setFormatter(formatter)
    # 将句柄添加到日志记录器中
    logger.addHandler(file_handler)
    # 添加日志输出
    logger.info('开始执行程序')

    schedule_members = {}
    with open(os.path.join(os.path.dirname(__file__), 'requirements', 'schedule.txt'), 'r') as f:
        for line in f:
            key, value = line.strip().split(' ')
            schedule_members[key] = value

    nickname_relate = {}
    with open(os.path.join(os.path.dirname(__file__), 'requirements', 'name_relate.txt'), 'r') as f:
        for line in f:
            key, value = line.strip().split(' ')
            nickname_relate[key] = value


    # 配置参数
    base_url = os.environ.get("BASE_URL", "http://192.168.xxx.xxx:2531/v2/api")
    token = os.environ.get("GEWECHAT_TOKE", "xxxxxxxxxxxxxxx")
    app_id = os.environ.get("APP_ID", "xxxxxxxxxxxxxx")

    # 创建 GewechatClient 实例
    client = GewechatClient(base_url, token)

    # 登录, 自动创建二维码，扫码后自动登录
    app_id, error_msg = client.login(app_id=app_id)
    if error_msg:
        print("登录失败")
        return
    try:
        # remind_bot(app_id, client, schedule_members, nickname_relate)
        # 定时任务，循环发送消息
        scheduler = BlockingScheduler()
        scheduler.add_job(remind_bot, "cron", kwargs= {"client": client, "app_id":app_id, "schedule_members": schedule_members, "nickname_relate": nickname_relate}, 
                          hour=22, misfire_grace_time=15*60,timezone='Asia/Shanghai')
        # scheduler.add_job(remind_bot, 'interval', kwargs= {"client": client, "app_id":app_id, "schedule_members": schedule_members, "nickname_relate": nickname_relate}, 
        #                   minutes=2, misfire_grace_time=15*60, timezone='Asia/Shanghai')
        scheduler.start()
        
    except Exception as e:
        print("Failed to fetch contacts list:", str(e))
    
    logger.info('程序执行结束')

if __name__ == "__main__":
    main()