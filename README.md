# myaccounts
[#Side Project]()&emsp;[#舊專案翻新]()

![pylint](https://img.shields.io/badge/PyLint-7.26-orange?logo=python&logoColor=white)
[![Django CI](https://github.com/bessyhuang/myaccounts/actions/workflows/django.yml/badge.svg)](https://github.com/bessyhuang/myaccounts/actions/workflows/django.yml)
![codecov](https://codecov.io/gh/你的帳號/myaccounts/branch/main/graph/badge.svg)

## 專案基本資料
- 專案名稱：我的記帳本
- 基本功能：新增 Create、讀取 Read、刪除 Delete、Login、Logout
- 涵蓋技術：
  - [Postgres DB](https://www.postgresql.org/docs/current/)
  - GitHub Actions (CI)：[pylint](https://github.com/Silleellie/pylint-github-action)、[Django x Postgres CI](https://github.com/bessyhuang/myaccounts/blob/master/.github/workflows/django.yml)
- 技術亮點：
  - 使用 GitHub Action 完成一個簡單的 CI，CI 確保了每一次程式碼更改都會被自動測試，這樣可以早期發現問題，提高軟體品質和可靠性。（機敏資料移至 Settings -> Environments -> Environment secrets 存放，而非寫在 Yaml 中）
  - 從 MySQL DB 轉而使用 Postgres DB，係看重它更加開放且貼近社群、商業應用導向（transaction，資料的交易機制，擁有更嚴格的測試驗證和設計機制）、可擴展性（地理空間資料類型 PostGIS）等優點。
- Future Work：更新 Update、查詢 Query、串接＆建立 API

## 功能介紹
![image](https://github.com/bessyhuang/myaccounts/assets/42068007/7c110e62-870f-46e1-96de-5182ba281799)
![image](https://github.com/bessyhuang/myaccounts/assets/42068007/b6ecf4f6-d7bd-4639-bc42-7c288547c732)

## 使用教學



我的筆記：
>>  URL: https://hackmd.io/s/SJnKEOBDQ#Django-%E7%B6%B2%E7%AB%99%E9%96%8B%E7%99%BC

### 補充
- MariaDB 安裝於 Django 的操作步驟：django mariadb ubuntu 18.04.odt
