import os
import sys
import time
import urllib
from urllib.parse import urlparse
import jenkins
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from core.config import settings
from crud.crud_project import crud_project
from crud.crud_record import crud_record
from models.record_model import RecordModel
from api.deps import get_db
from models import *


def get_jenkins_data(url, job_name):
    jenkins_server = jenkins.Jenkins(url, username=settings.JENKINS_ACCOUNT, password=settings.JENKINS_PWD)
    try:
        builds = jenkins_server.get_job_info(job_name)['builds'][:3]
        for build in builds:
            build_info = jenkins_server.get_build_info(job_name, build['number'])
            if build_info['result']:
                return build_info
    except jenkins.JenkinsException as e:
        raise ValueError(f'获取Jenkins的Job【{job_name}】信息失败，错误信息是：{e}')


def synchronous_data(db):
    projects = crud_project.list(db)
    for project in projects:
        if project.enable:
            try:
                print(f'开始同步项目【{project.name}】')
                parse_info = urlparse(project.jenkins_url)
                jenkins_url = parse_info.scheme + '://' + parse_info.netloc
                job_name = urllib.parse.unquote(os.path.basename(os.path.dirname(parse_info.path)), encoding='utf-8', errors='replace')
                record = get_jenkins_data(jenkins_url, job_name)
                record_status = 999
                record_duration = int(record['duration']/1000)
                if record['result'] == 'SUCCESS' and record_duration <= project.duration_limit:
                    record_status = 0
                elif record['result'] == 'SUCCESS' and record_duration > project.duration_limit:
                    record_status = 2
                elif record['result'] == 'FAILURE':
                    record_status = 1
                else:
                    record_status = 999
                if not crud_record.is_build_exist(db, project.id, record['number']):
                    crud_record.create(db, RecordModel(
                        build_id=record['number'],
                        duration=record_duration,
                        status=record_status,
                        url=record['url'],
                        check_time=int(record['timestamp']/1000),
                        create_time=int(time.time()),
                        project_id=project.id,
                    ))
            except Exception as e:
                print(f'同步项目【{project.name}】数据错误，错误信息是：{e}')
    print('同步完成！')


def delete_record(db):
    """
    超过配置 RECORD_SAVE_TIME天的记录会被删除
    """
    now = int(time.time())
    past_day = now - settings.RECORD_SAVE_TIME * 24 * 3600
    result = crud_record.delete_old_record(db, past_day)
    print(f"删除了{len(result)}条记录")


if __name__ == '__main__':
    db = next(get_db())
    synchronous_data(db)
    delete_record(db)



