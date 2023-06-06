import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from core.config import settings
from crud.crud_user import crud_user
from schemas.user import UserCreate
from core.permissions import Permissions
from api.deps import get_db
from models import *

if __name__ == '__main__':
    user = UserCreate(password=settings.FIRST_SUPERUSER_PASSWORD,
                      email=settings.FIRST_SUPERUSER,
                      full_name=settings.FIRST_SUPERUSER_NAME,
                      is_active=True,
                      roles=Permissions.ADMIN.value)
    crud_user.create(next(get_db()), obj_in=user)
    print('超级管理员账号创建完成！')
