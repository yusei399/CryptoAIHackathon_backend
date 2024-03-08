# Pythonのベースイメージを使用
FROM python:3.9

# 音声ファイル変換用のffmegをインストール
RUN apt-get update \
    && apt-get install -y ffmpeg

# 作業ディレクトリを設定
WORKDIR /app

# pipをアップグレード
RUN pip install --upgrade pip

# 依存関係ファイルをコピー
COPY requirements.txt .

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのコードをコピー
COPY ./app /app

# ホストとのポートマッピング用にポートを公開
EXPOSE 8000

# アプリケーションを起動
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]
