FROM python:3.9.17

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

# 首次运行还需要进入容器运行脚本创建超级管理员账号 python3 scripts/create_super_user.py ，创建账号后请登陆该账号修改密码
RUN alembic upgrade head

EXPOSE 80

#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

#以下内容为设置定时脚本使用
# 安装 cron
RUN apt-get update && apt-get -y install cron

# 复制 cronfile 到 cron.d目录
COPY ./scripts/cronfile /etc/cron.d/cronfile

# 给文件授权
RUN chmod 0644 /etc/cron.d/cronfile

# 应用cron job
RUN crontab /etc/cron.d/cronfile

# 创建cron日志文件
RUN touch /var/log/cron.log

# 在容器启动cron并打印日志
#CMD cron && tail -f /var/log/cron.log
#CMD cron && uvicorn main:app --host 0.0.0.0 --port 80
CMD ["/bin/bash", "-c", "cron;uvicorn main:app --host 0.0.0.0 --port 80"]
# 生成镜像命令         docker build -t monitor_screen_backend:v1.0.0 .
# 使用镜像运行容器命令   docker run -d --name monitor_screen_backend -p 8000:80 monitor_screen_backend:v1.0.0