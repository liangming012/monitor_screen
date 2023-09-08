FROM python:3.9.17

WORKDIR /usr/src/app

# 创建目录映射到宿主机目录用于存放 sql_app.db
RUN mkdir /usr/sql

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

# 打包镜像前注意修改 alembic.ini 配置里的 sqlalchemy.url
# 首次运行还需要进入容器运行 alembic upgrade head 和 脚本创建超级管理员账号 python3 scripts/create_super_user.py ，创建账号后请登陆该账号修改密码
# 非首次运行如果数据结构有更新需运行 alembic upgrade head
# 宿主机卷对应的$HOME/sql目录如果不存在需要自己手动创建，docker-compose.yml里宿主机的卷目录$HOME/sql最好替换成实际绝对目录
# 容器里的cron定时任务未执行，可能是从windows电脑复制到linux电脑时cronfile文件里的换行符自动变成/r导致的
#    使用sed命令删除crontab文件中的\r字符。运行以下命令来删除\r字符并覆盖原始文件，并重新运行：
#    sed -i 's/\r//g' /etc/cron.d/cronfile
#    crontab /etc/cron.d/cronfile

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

HEALTHCHECK --interval=10s --timeout=30s --retries=3 --start-period=10s \
  CMD curl -fs -k --insecure "https://localhost:80/api/v1/healthy/" || exit 1

# 在容器启动cron并打印日志
#CMD cron && tail -f /var/log/cron.log
#CMD cron && uvicorn main:app --host 0.0.0.0 --port 80
#不启用https协议不用参数 ssl-keyfile 和 ssl-certfile
CMD ["/bin/bash", "-c", "cron;uvicorn main:app --host 0.0.0.0 --port 80"]
#CMD ["/bin/bash", "-c", "cron;uvicorn main:app --host 0.0.0.0 --port 80 --ssl-keyfile /usr/src/app/oasgames.com.key --ssl-certfile /usr/src/app/oasgames.com.crt"]
# 生成镜像命令         docker build -t monitor_screen_backend:v1.0.0 .
# 使用镜像运行容器命令   docker run -d --name monitor_screen_backend -p 8000:80 --mount type=bind,source=$HOME/sql,target=/usr/sql monitor_screen_backend:v1.0.0