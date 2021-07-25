# pc2webDjango.md

# 簡介

一個模仿 pc2 判斷程式正確與否的網站

基本上就是根據出題者提供的 .in 檔案與 .out 檔案 ， 來判斷程式是否為正解

目前可供 java 使用， python 增加中

---

---

# 環境介紹

該環境於 AWS 上的 `ami-0077ef9ac037e2df6` AMI 測試可搭配 `userdata.txt` 來使用

記得要在 console 上開啟 http 的 80 port

版本：

- OS : CentOS 7
- Apache/2.4.6 (CentOS) mod_wsgi/4.7.1 Python/3.6

---

## 主視覺

![image/view1.png](image/view1.png)
![image/gifview.png](image/gifview.png)

---

# 使用說明

輸入 http://{你的IP}/adminJudge 進入管理頁面

使用預設帳密：`admin1 , password` ，進入管理頁面

model 關係如下：

Course → Homework → Problem

- 從 `Course` 開始 ，在創建新課程時可輸入 1. 課程名稱 ，2.學生清單(Excel）， 學生清單格式可參考 `測試用名單.xlsx` ，為 帳號與姓名的格式，學生預設密碼為 `password`
- `Homework` 歸在 `Course` 底下，每一個 `Homework` 只能有一個 `Course` ，
而 `Course` 可有多個 `Homework` 。可以提供附件作為題目的說明
- `Problem` 為題目，歸於 `Homework` 底下，創建時要求填入：
1.題目名稱 2.可允許執行時間 3.輸入與輸出測資 ，
一個 `Homework` 可有多個 `Problem`