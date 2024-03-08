import os
from dotenv import load_dotenv

# 環境変数ファイルのパスを指定します。
env_path = '../.env'
# 環境変数ファイルを読み込みます。
load_dotenv(dotenv_path=env_path)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")