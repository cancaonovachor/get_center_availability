# 公民館空き状況照会

## 使用プロダクト
- CloudRun
- headless-chromium
- chrome_driver
- selenium

## エンドポイント
- /nishinomiya?reservMon=12&reservDay=15
  - nishinomiya: 公民館
    - Flaskのエンドポイント分けて各公民館増やしていく想定
  - reservMon: 検索する月
  - reservDay: 検索する日

## 起動方法
- headless-chromium.zipを解凍(サイズが大きいためgitにpush厳禁)
- Dockerをインストール
- docker build -t get_center .
- docker run -itd -e PORT=8000 -e NISHI_ID="<まなびネットのID>" -e NISHI_PASS="<まなびネットのパスワード>" -p 8000:8000 get_center:latest

## 動作確認用
- Dockerファイル末尾の `CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app` をコメントアウトする
  - gunicornが走ると煩わしいため
- docker内に入る
  - docker ps #コンテナ名確認
  - docker exec -i -t コンテナ名 bash
- python app.py

## デプロイ
- `CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app` をコメントアウトしている場合は戻す
- Container Registoryに配置
  - gcloud builds submit --tag gcr.io/<GCPプロジェクトID>/get_center
- CloudRunにデプロイ
- CloudRunの環境変数セット(初回のみなので基本必要なし)
  - gcloud beta run services update <サービス名> --update-env-vars NISHI_ID="<まなびネットのID>",NISHI_PASS="<まなびネットのPASS>"