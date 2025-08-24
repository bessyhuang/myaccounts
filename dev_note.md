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

## 3. 設定 GitHub Actions (CI)
目標：
1. 用 `pytest` 替代內建 Django test
2. 加入 Codecov 工具的 `coverage`，來測量與呈現程式碼測試覆蓋率（code coverage）
3. 更新 GitHub Actions (django.yml)
4. 顯示 Coverage Badge

- Codecov 是什麼？
	- Codecov 是一個 雲端服務平台，用來收集、分析、追蹤程式碼測試覆蓋率。
	- 它可以與多種 CI/CD 系統（GitHub Actions、GitLab CI、CircleCI 等）整合。
	- 它支援多種程式語言的測試報告（Python、JavaScript、Java、Go 等）。
- Coverage 是什麼？
	- **Coverage（覆蓋率）**指的是程式碼中有多少行、多少分支被測試程式執行過。
	- 常見指標：
		- Line coverage：程式碼中被測試過的行數百分比。
		- Branch coverage：程式碼條件分支（if/else）被測試過的比例。
	- 例子：
		- 如果你只測試 add(1, 2)，行 coverage 是 100%，branch coverage 也可能是 100%（因為沒有分支）。
		- 如果函數內有 if 分支，沒有測試到所有條件，branch coverage 就會低於 100%。

		```python
		def add(a, b):
		    return a + b
		```
		
流程：
1. 第一步：安裝必要套件，並把這些加入 dev-requirements.txt
	```python
	pip install pytest pytest-django coverage
	```
2. 第二步：設定 pytest
	> 在專案根目錄下建立 pytest.ini
	```ini
	[pytest]
	DJANGO_SETTINGS_MODULE = myaccounts.settings
	python_files = tests.py test_*.py *_tests.py
	```
3. 第三步：建立測試檔案 `accounts/tests/test_models.py`
	```python
	import pytest
	from accounts.models import YourModelName

	@pytest.mark.django_db
	def test_model_str():
	    obj = YourModelName.objects.create(...)  # 填寫必要欄位
	    assert str(obj) == "你預期的名稱"
	```
4. 第四步：更新 GitHub Actions workflow `.github/workflows/django.yml`
5. 第五步：設定 Codecov 並顯示 Badge
	- [https://app.codecov.io/gh](https://app.codecov.io/gh)
		> 登入 GitHub 後，找到你的 myaccounts repo，開啟它。
		> 接著，選擇「Using GitHub Actions」、「Pytest」，需要 copy 「SECRET_KEY」，並且到 GitHub Settings -> Actions secrets and variables 設定 Repository secrets。
	- 在 README.md 加入 badge：
		```
		![codecov](https://codecov.io/gh/你的帳號/myaccounts/branch/分支名稱/graph/badge.svg)
		```

最終成果
- 每次 push 都會自動：
	- 安裝依賴套件
	- 建立 Postgres container
	- 使用 pytest 測試
	- 顯示 test 覆蓋率（coverage）
	- 上傳到 Codecov 並可視化
- README 會有漂亮的 Coverage badge

延伸任務（加分）
- 加入 pre-commit 自動執行 lint / format
- 設定 deployment 自動釋出到 Heroku、Railway、或自己的 VPS

## 4. 加入 pre-commit 自動執行 lint / format（Local）
目標：
加入 pre-commit 可以在你每次 git commit 前自動執行 lint、format、甚至安全檢查，確保程式碼品質穩定。

流程：
1. 第一步：安裝 pre-commit
	```bash
	pip install pre-commit
	```
2. 第二步：在專案根目錄新增檔案 `.pre-commit-config.yaml`
	- `black` → 自動格式化 Python 程式碼 (會自動修改檔案格式)
	- `flake8` → 靜態檢查 Python 程式碼規範
	- `prettier` → 格式化前端或文件檔案（可選） (會自動修改檔案格式)
	- `trailing-whitespace` / `end-of-file-fixer` → 清理多餘空格 / 檔案尾空行
3. 第三步：安裝 git hook
	> 這會在 `.git/hooks/pre-commit` 建立 hook，每次 commit 前自動執行。
	```bash
	pre-commit install
	```
4. 第四步：手動執行一次檢查（可選）
	> 這樣可以先格式化與檢查整個專案，避免 commit 時被大量錯誤擋住。
	```bash
	pre-commit run --all-files
	```
5. 第五步：整合到 CI（可選）
	> 在 .github/workflows/ci.yml 裡，也可以加一個 step 執行 pre-commit，保證 PR / push 也符合規範
	```yaml
	- name: Run pre-commit checks
	  uses: pre-commit/action@v3.0.0
	  with:
	    extra_args: "--all-files"
	```

好處
- 本地 commit 就自動格式化 / 檢查，不必手動記得 run black / flake8
- CI pipeline 可以統一驗證程式碼規範
- 對團隊合作非常友好，減少「我本地 OK，但 CI fail」情況
