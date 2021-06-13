import os

WS_HOST=str(os.environ.get('HEROKU_APP_NAME', 'localhost'))
WS_PORT=int(os.environ.get('PORT', 8765))