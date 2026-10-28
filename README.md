# ARNGREN 後端檔案

## 建立虛擬環境
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned<br>
python -m venv venv<br>
.\venv\Scripts\Activate.ps1<br>

## 下載必要套件
python -m pip install -r requirements.txt<br>
檢查套件 : pip list

## 建立資料庫
在Neon建立一個資料庫後，將左上角的Connect裡面的Connection string複製<br>
然後再新增一個.env，輸入'DATABASE_URL='，最後在=後面貼上剛複製的Connection string。

## 測試
### 設定 Product 資料表
python manage.py migrate
### 註冊管理員
python manage.py createsuperuser
### 啟動伺服器
python manage.py runserver

## 部署
到render建立新的網頁服務<br>
+New > Web Service<br>
在 Build Command 輸入 pip install -r requirements.txt && python manage.py collectstatic --noinput<br>
Start Command 輸入 gunicorn config.wsgi:application<br>
回到終端輸入 python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())" 產生自己的secret key<br>
|KEY|VALUE|
|---|---|
|DATABASE_URL|自己的Neon的Connect string|
|SECRET_KEY|剛剛產生的secret key|
|DEBUG|False|
|ALLOWED_HOSTS|.onrender.com|