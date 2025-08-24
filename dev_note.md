# 開發過程筆記

## 1. PostgreSQL（創建資料庫與使用者權限）

PostgreSQL 安裝完後，需要創建本專案所需的資料庫名稱，以及創建使用者並賦予其使用此資料庫的所有權限。
```postgresql
postgres=# create database [DB_NAME];
postgres=# create user [DB_USERNAME] with encrypted password 'my-password';
postgres=# grant all privileges on database [DB_NAME] to [DB_USERNAME];
```

因為需要使用 psycopg2（通常是透過 Django 的 manage.py migrate）對 PostgreSQL 資料庫執行 CREATE TABLE 指令，但該使用者目前沒有權限在 public schema 中建立資料表，故需要執行以下指令。
```postgresql
# 給你的資料庫使用者在 public schema 中的 CREATE 權限。
postgres=# grant CREATE ON SCHEMA public TO [DB_USERNAME];
```

接者，將資料庫的結構與 Django 的模型同步（套用到資料庫，建立/變更表格）。
```python
python manage.py makemigrations
python manage.py migrate
```

成功後，結果如下：
```postgresql
accounting=# \dt
                       List of relations
 Schema |            Name            | Type  |      Owner       
--------+----------------------------+-------+------------------
 public | auth_group                 | table | accounting_admin
 public | auth_group_permissions     | table | accounting_admin
 public | auth_permission            | table | accounting_admin
 public | auth_user                  | table | accounting_admin
 public | auth_user_groups           | table | accounting_admin
 public | auth_user_user_permissions | table | accounting_admin
 public | chia_app_category          | table | accounting_admin
 public | chia_app_record            | table | accounting_admin
 public | django_admin_log           | table | accounting_admin
 public | django_content_type        | table | accounting_admin
 public | django_migrations          | table | accounting_admin
 public | django_session             | table | accounting_admin
(12 rows)
```

## 2. Pytest 測試
遇到的錯誤：
```
psycopg2.errors.InsufficientPrivilege: permission denied to create database
```
意思是「測試時 Django 嘗試建立測試資料庫（預設是 test_<DB_NAME>）時，PostgreSQL 使用者沒有建立資料庫的權限」。

原因：
Django pytest / manage.py test 會自動建立一個測試資料庫，而你的 PostgreSQL 用戶權限不足，無法建立新資料庫，因此測試啟動就失敗。

解決方法：
- 方法 1：給 PostgreSQL 使用者 CREATE DATABASE 權限，再重新跑測試

	```postgresql
	-- 登入 postgres
	accounting=# psql -U postgres

	-- 給你的 user 權限
	accounting=# ALTER USER [DB_USERNAME] CREATEDB;
	```

	```bash
	pytest accounts/tests/

	===================== test session starts =====================
	platform darwin -- Python 3.12.1, pytest-8.4.1, pluggy-1.6.0
	django: version: 5.0.6, settings: project_chia.settings (from ini)
	rootdir: /Users/bessyhuang/專案計畫/myaccounts/project_chia
	configfile: pytest.ini
	plugins: django-4.11.1
	collected 3 items                                                                                                                                                      

	chia_app/tests/test_models.py ...                        [100%]

	===================== 3 passed in 0.30s =======================
	```
- 方法 2：使用已存在的測試資料庫
	> 修改 settings.py 或在 pytest 設定中指定，然後在 PostgreSQL 中先建立這個資料庫，這樣 Django 就不用自己建立測試資料庫了。

	```python
	# settings.py
	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.postgresql',
	        'NAME': 'accounting',       	# 正式 DB
	        'TEST': {
	            'NAME': 'accounting_test',  # 已存在的 DB
	        },
	        'USER': 'myuser',
	        'PASSWORD': 'mypassword',
	        'HOST': 'localhost',
	        'PORT': '5432',
	    }
	}
	```

	```postgresql
	accounting=# CREATE DATABASE accounting_test;
	```