# API 調試工作流程工具

這是一個專門用於調試和測試後端 API 的工作流程工具，可以自動化測試各種輸入情況，檢查 API 的行為是否正確，並生成詳細的測試報告。

## 功能特點

- 支持所有 HTTP 方法（GET, POST, PUT, DELETE 等）
- 自動記錄請求和響應數據
- 檢查狀態碼和響應內容
- 生成美觀的 HTML 測試報告
- 支持批量運行測試用例
- 支持身份驗證令牌
- 提供高級測試功能（隨機數據生成、資源清理等）
- **自動檢測 API 端口和端點**（新功能）
- **智能生成測試數據**（新功能）
- **從日誌文件分析 API 端點和輸入**（新功能）
- **手動指定 API 端口進行自動測試**（新功能）
- **互動式測試界面**（新功能）
- **測試特定 API 路由**（新功能）

## 安裝

1. 確保已安裝 Python 3.11 或更高版本
2. 安裝所需依賴：

```bash
pip install requests
```

## 基本用法

### 使用基本 API 調試器

```python
from api_debugger import ApiDebugger

# 初始化 API 調試器，指向你的 API
api_debugger = ApiDebugger(
    base_url="https://api.myproject.com",
    headers={
        "Content-Type": "application/json",
        "X-API-Key": "你的API密鑰"  # 如果需要
    }
)

# 定義你的 API 測試用例
test_cases = [
    # 測試登錄功能
    {
        "endpoint": "/auth/login",
        "method": "POST",
        "data": {
            "username": "test_user",
            "password": "test_password"
        },
        "expected_status": 200,
        "test_name": "用戶登錄",
        "description": "測試用戶登錄功能"
    },
    
    # 測試獲取產品列表
    {
        "endpoint": "/products",
        "method": "GET",
        "expected_status": 200,
        "test_name": "獲取產品列表",
        "description": "測試獲取產品列表功能"
    },
    
    # 測試創建訂單
    {
        "endpoint": "/orders",
        "method": "POST",
        "data": {
            "product_id": 123,
            "quantity": 2,
            "address": "測試地址"
        },
        "expected_status": 201,
        "test_name": "創建訂單",
        "description": "測試創建訂單功能"
    }
]

# 運行測試
api_debugger.run_test_suite(test_cases)

# 生成報告
api_debugger.generate_report("my_project_api_test_report.html")
```

### 使用高級 API 測試器

```bash
python advanced_test.py --url http://localhost:8000 --token your_token_here
```

### 使用自動檢測功能

```bash
# 自動檢測 API 端口和端點並運行測試
python main.py

# 指定主機和端口範圍
python main.py --host api.example.com --port-min 8000 --port-max 9000

# 指定日誌文件
python main.py --log-file custom_log.log

# 手動指定 API 端口進行測試
python main.py --port 8080
```

### 使用互動式測試界面

```bash
# 啟動互動式測試界面
python interactive_test.py
```

互動式界面會引導您輸入主機名、端口號，並提供選項分析日誌文件和運行測試。

### 測試特定 API 路由

```bash
# 啟動特定 API 路由測試工具（互動式）
python test_specific_route.py

# 使用命令行參數測試特定 API 路由
python main.py --port 8080 --route /api/search_contracts

# 測試 POST 請求並提供數據
python main.py --port 8080 --route /api/contracts/create --method POST --data '{"title":"測試合約","client_id":123,"amount":5000}'

# 測試帶有錯誤處理的請求
python main.py --port 8080 --route /api/contracts/validate --method POST --data '{"contract_id":456}' --expected-status 400
```

特定 API 路由測試工具會引導您輸入主機名、端口號、API 路由路徑、HTTP 方法和請求數據，然後對該特定路由進行測試。

## 命令行參數

### main.py 參數

| 參數 | 說明 | 默認值 |
|------|------|--------|
| `--host` | API 主機名 | localhost |
| `--port` | 指定要測試的API端口 | 無 |
| `--route` | 指定要測試的API路由路徑 | 無 |
| `--method` | HTTP方法 (GET/POST/PUT/DELETE/PATCH) | GET |
| `--port-min` | 端口掃描範圍最小值 | 8000 |
| `--port-max` | 端口掃描範圍最大值 | 9000 |
| `--log-file` | 日誌文件路徑 | api_debug.log |
| `--data` | JSON格式的請求數據 | 無 |
| `--expected-status` | 預期的HTTP狀態碼 | 200 |

## 示例腳本

### example.py

這是一個基本示例，演示如何使用 API 調試器測試一個簡單的用戶 API。

```bash
python example.py
```

### advanced_test.py

這是一個高級示例，演示如何使用更多功能測試 API，包括：

- 用戶 CRUD 操作
- 身份驗證和授權
- 輸入驗證
- 速率限制測試

```bash
python advanced_test.py --url http://localhost:8000
```

### auto_test.py

這是一個自動檢測示例，演示如何使用新的自動檢測功能：

- 自動掃描開放端口
- 自動檢測 API 端點
- 智能生成測試數據
- 從日誌文件分析 API 信息

```bash
python auto_test.py
```

### interactive_test.py

這是一個互動式測試界面，提供簡單的命令行交互：

- 手動輸入 API 主機名和端口
- 檢測 API 端點
- 選擇是否分析日誌文件
- 選擇是否運行測試

```bash
python interactive_test.py
```

### test_specific_route.py

這是一個特定 API 路由測試工具，專門用於測試單個 API 端點：

- 手動輸入 API 主機名、端口和路由路徑
- 選擇 HTTP 方法（GET、POST、PUT、DELETE、PATCH）
- 智能生成請求數據或使用歷史數據模板
- 支持手動輸入請求數據
- 顯示詳細的測試結果
- 支持自動生成無效輸入測試

```bash
python test_specific_route.py
```

## 自動檢測功能

### 端口檢測

工具可以自動掃描指定範圍內的開放端口，找到可能運行 API 的服務。

### 端點檢測

對於檢測到的開放端口，工具會嘗試訪問常見的 API 路徑，檢測支持的 HTTP 方法。

### 智能數據生成

根據端點路徑自動生成適合的測試數據，例如：

- 用戶相關端點：生成用戶名、電子郵件、密碼等
- 產品相關端點：生成產品名稱、描述、價格等
- 訂單相關端點：生成訂單數據、產品列表等

### 日誌分析

從之前的測試日誌中提取 API 端點信息和輸入數據模板，用於生成更精確的測試用例。

### 手動指定端口

您可以手動指定要測試的 API 端口，系統將自動檢測該端口上的 API 端點並生成測試用例。這在您已知 API 端口但不確定端點結構時特別有用。

### 互動式測試

互動式測試界面提供了一種簡單的方式來測試 API，無需編寫命令行參數。它會引導您完成整個測試過程，包括：

1. 輸入 API 主機名和端口
2. 檢測 API 端點
3. 選擇是否分析日誌文件以獲取更精確的 API 信息
4. 選擇是否運行測試
5. 顯示測試結果摘要

這對於快速測試和探索未知的 API 特別有用。

### 特定 API 路由測試

特定 API 路由測試功能允許您針對單個 API 端點進行深入測試：

1. 手動輸入 API 主機名、端口和路由路徑
2. 選擇 HTTP 方法（GET、POST、PUT、DELETE、PATCH）
3. 系統會嘗試從日誌文件中找到相關的請求數據模板
4. 如果沒有找到模板，會根據路由路徑智能生成請求數據
5. 您也可以選擇手動輸入請求數據
6. 運行測試並顯示詳細的測試結果
7. 可以選擇自動生成無效輸入測試，檢查 API 的錯誤處理能力

這個功能特別適合針對特定 API 端點進行深入調試和測試，例如檢查新開發的 API 是否有 bug。

## 使用示例

### 測試特定 API 路由

```bash
# 測試 GET 請求
python main.py --port 8080 --route /api/search_contracts

# 測試 POST 請求並提供數據
python main.py --port 8080 --route /api/contracts/create --method POST --data '{"title":"測試合約","client_id":123,"amount":5000}'

# 測試帶有錯誤處理的請求
python main.py --port 8080 --route /api/contracts/validate --method POST --data '{"contract_id":456}' --expected-status 400
```

## 自定義測試用例

你可以根據自己的 API 創建自定義測試用例。測試用例是一個字典，包含以下字段：

- `endpoint`: API 端點路徑，例如 `/api/users`
- `method`: HTTP 方法，例如 `GET`, `POST`, `PUT`, `DELETE`
- `data`: 請求數據（對於 POST/PUT 請求）
- `expected_status`: 預期的 HTTP 狀態碼
- `expected_response`: 預期的響應數據（部分匹配）
- `test_name`: 測試名稱
- `description`: 測試描述 