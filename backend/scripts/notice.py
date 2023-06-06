import json
import sys
import os
import requests
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from core.config import settings
from crud.crud_notice import crud_notice
from crud.crud_show import crud_show
from crud.crud_record import crud_record
from crud.crud_project import crud_project
from api.deps import get_db
from models import *


def notice_feishu(webhook_url, content, at_all=False):
    """
    发送飞书通知
    操作步骤：在飞书创建群组-》设置-》添加机器人-》添加自定义机器人-》机器人安全设置自定义关键词"报警"
    """
    if at_all:
        content = '<at user_id="all">所有人</at> ' + content
    data = {"msg_type": "text", "content": json.dumps({"text": content}, ensure_ascii=False, indent=2)}
    response = requests.post(webhook_url, data)
    if response.status_code == 200:
        json_data = response.json()
        if json_data['code'] != 0:
            print(f"发送飞书通知失败，错误信息是{response.text}")
    else:
        print(f'发送飞书通知失败，状态码是:{response.status_code} 。错误信息是:{response.text}')


def notice_dingding(webhook_url, content, at_all=False):
    """
    发送钉钉通知
    操作步骤：在钉钉创建群组-》设置-》智能群助手-》添加自定义机器人-》机器人安全设置自定义关键词"报警"
    """
    headers = {"Content-Type": "application/json"}
    data = {"msgtype": "text", "text": {"content": content}, "at": {"isAtAll": at_all}}
    response = requests.post(webhook_url, data=json.dumps(data, ensure_ascii=False, indent=2).encode('UTF-8'),
                             headers=headers)
    if response.status_code == 200:
        json_data = response.json()
        if json_data['errcode'] != 0:
            print(f"发送钉钉通知失败，错误信息是{response.text}")
    else:
        print(f'发送钉钉通知失败，状态码是:{response.status_code} 。错误信息是:{response.text}')


def get_notice_project_ids(db, notice):
    """
    获取报警群组要通知的项目ID列表
    """
    if notice.watch_type == 1:  # 1 按屏幕
        project_ids = []
        shows = crud_show.get_screens_data(db, notice.screen_ids.split(','))
        for show in shows:
            project_ids.append(show.project_id)
        return project_ids
    if notice.watch_type == 2:  # 2 按项目
        return list(map(int, notice.project_ids.split(',')))


def get_project_data(db, project_id, faild_count, timeout_count):
    """
    根据项目ID获取对应项目的信息
    """
    project = crud_project.get(db, unique_id=project_id)
    project_dict = {"name": project.name, "status": 999}
    if project.enable:
        records = crud_record.get_records(db, project_id=project.id,
                                          limit=max(faild_count, timeout_count))
        # status值：0=>成功 1=>失败 2=>超时 999=>失效
        project_dict['check_time'] = records[0].check_time
        project_dict['status'] = records[0].status
        if project_dict['status'] == 1 and faild_count > 1:
            for m in range(min(faild_count, len(records))):
                if records[m].status == 0:
                    project_dict['status'] = 0
                    break
        elif project_dict['status'] == 2 and timeout_count > 1:
            for m in range(min(timeout_count, len(records))):
                if records[m].status == 0:
                    project_dict['status'] = 0
                    break
    return project_dict


def notice_samebody(db):
    notices = crud_notice.list(db)
    for notice in notices:
        if notice.enable:
            content = ''
            for project_id in get_notice_project_ids(db, notice):
                project = get_project_data(db, project_id, notice.faild_count, notice.timeout_count)
                if project['status'] == 0:
                    continue
                if project['status'] == 1:
                    content = content + f"【{project['name']}】失败次数超过阈值{notice.faild_count}次\n"
                elif project['status'] == 2:
                    content = content + f"【{project['name']}】超时次数超过阈值{notice.timeout_count}次\n"
            if content != '' and notice.notice_type == '钉钉':
                notice_dingding(notice.webhook_url, content, notice.at_all)
            elif content != '' and notice.notice_type == '飞书':
                notice_feishu(notice.webhook_url, content, notice.at_all)


if __name__ == '__main__':
    notice_samebody(next(get_db()))



