import uvicorn

from core.config import settings
from main import app

if __name__ == "__main__":
    if settings.ENABLE_HTTPS:
        uvicorn.run(app, ssl_keyfile='oasgames.com.key', ssl_certfile='oasgames.com.crt')
    else:
        uvicorn.run(app)
