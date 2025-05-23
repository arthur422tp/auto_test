# API 自動 Debug 工具

這是一個極簡易的 API Debug 工具，讓你只需輸入 API 伺服器的 port 和 route，系統就會自動對該 API 端點進行測試。

## 功能特色
- 支援 GET 與 POST 測試
- 自動顯示狀態碼與回應內容
- 可自訂 POST 測試資料

## 安裝方式

1. 請先安裝 Python 3.11 或以上版本
2. 安裝必要套件：

```bash
pip install -r requirements.txt
```

## 快速開始

### 指令格式

```bash
python auto_debug.py --port <PORT> --route <API路徑> [--method GET|POST] [--data '{JSON資料}']
```

### 範例

#### 測試 GET
```bash
python auto_debug.py --port 5001 --route /api/test
```

#### 測試 POST 並帶資料
```bash
python auto_debug.py --port 5001 --route /api/test --method POST --data '{"foo": "bar"}'
```

## 參數說明
| 參數      | 說明                   | 必填 | 預設值 |
|-----------|------------------------|------|--------|
| --port    | API 伺服器 port        | 是   | 無     |
| --route   | API 路由               | 是   | 無     |
| --method  | HTTP 方法 (GET/POST)   | 否   | GET+POST都測試 |
| --data    | POST 測試資料 (JSON)   | 否   | {"test": "value"} |

## 輸出結果
- 終端機會顯示每個請求的狀態碼與回應內容

---

## 檔案結構
- auto_debug.py：主程式，負責參數解析與測試流程
- api_tester.py：API 測試邏輯
- requirements.txt：必要套件

---

## 版權
MIT 