# monitor_screen
Python 3.9.6
Node v19.7.0


# docker-compose 启动方式



    修改backend目录的.env文件的跨域配置BACKEND_CORS_ORIGINS加上本机IP域名如：http://10.1.16.50:8081 使前端能访问后端
    修改backend目录的.env文件的数据库配置，确保访问的对应的数据库存在，如：  SQLALCHEMY_DATABASE_URI=sqlite:////usr/sql/sql_app.db
    修改backend目录的alembic.ini文件sqlalchemy.url的值，确保访问的对应的数据库存在，如： sqlalchemy.url = sqlite:////usr/sql/sql_app.db
    项目根目录运行命令  docker-compose up
