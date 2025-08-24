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