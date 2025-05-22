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

### 使用互動式測試界面（新功能）

```bash
# 啟動互動式測試界面
python interactive_test.py
```

互動式界面會引導您輸入主機名、端口號，並提供選項分析日誌文件和運行測試。

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

### interactive_test.py（新增）

這是一個互動式測試界面，提供簡單的命令行交互：

- 手動輸入 API 主機名和端口
- 檢測 API 端點
- 選擇是否分析日誌文件
- 選擇是否運行測試

```bash
python interactive_test.py
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

### 互動式測試（新增）

互動式測試界面提供了一種簡單的方式來測試 API，無需編寫命令行參數。它會引導您完成整個測試過程，包括：

1. 輸入 API 主機名和端口
2. 檢測 API 端點
3. 選擇是否分析日誌文件以獲取更精確的 API 信息
4. 選擇是否運行測試
5. 顯示測試結果摘要

這對於快速測試和探索未知的 API 特別有用。

## 自定義測試用例

你可以根據自己的 API 創建自定義測試用例。測試用例是一個字典，包含以下字段：

- `endpoint`: API 端點路徑，例如 `/api/users`
- `method`: HTTP 方法，例如 `GET`, `POST`, `PUT`, `DELETE`
- `data`: 請求數據（對於 POST/PUT 請求）
- `expected_status`: 預期的 HTTP 狀態碼
- `expected_response`: 預期的響應數據（部分匹配）
- `test_name`: 測試名稱
- `description`: 測試描述

## 測試報告

測試完成後，會生成一個 HTML 測試報告，包含以下信息：

- 測試摘要（總測試數、通過測試數、失敗測試數、成功率）
- 每個測試用例的詳細信息（URL、方法、狀態碼、請求數據、響應數據等）
- 測試結果（成功或失敗）

## 最佳實踐

1. **測試各種輸入情況**：包括正常輸入、邊界情況和錯誤輸入
2. **檢查錯誤處理**：確保 API 正確處理錯誤情況
3. **測試身份驗證和授權**：確保只有授權用戶才能訪問受保護的資源
4. **測試輸入驗證**：確保 API 正確驗證輸入數據
5. **測試性能**：確保 API 在高負載下仍能正常工作
6. **清理測試數據**：測試後清理創建的測試數據
7. **使用自動檢測功能**：對於未知或變化的 API，使用自動檢測功能

## 自定義和擴展

你可以根據自己的需求自定義和擴展這個工具：

- 添加更多測試類型
- 集成到 CI/CD 流程中
- 添加更多報告格式（例如 JSON、CSV）
- 添加更多驗證邏輯
- 擴展自動檢測功能

## 許可證

MIT 

## 整合到 CI/CD 流程

1. **創建自動化測試腳本**：

   ```bash
   # 創建一個腳本用於 CI/CD
   touch tools/api_debug_tool/ci_test.py
   ```

2. **編輯 ci_test.py**：

   ```python
   import argparse
   import sys
   from api_debugger import ApiDebugger
   from port_detector import ApiPortDetector
   
   def main():
       parser = argparse.ArgumentParser(description="API 測試工具")
       parser.add_argument("--url", help="API 基礎 URL")
       parser.add_argument("--token", help="API 認證令牌")
       parser.add_argument("--env", default="dev", choices=["dev", "staging", "prod"], help="環境")
       parser.add_argument("--auto-detect", action="store_true", help="自動檢測 API 端口和端點")
       
       args = parser.parse_args()
       
       if args.auto_detect:
           # 使用自動檢測功能
           detector = ApiPortDetector(
               host=args.url.split("://")[1].split(":")[0] if args.url else "localhost"
           )
           results = detector.auto_detect_and_test()
           
           # 檢查結果
           success = True
           for port, result in results.items():
               summary = result["summary"]
               if summary["failed_tests"] > 0:
                   success = False
                   print(f"端口 {port} 測試失敗: {summary['failed_tests']} 個測試未通過")
           
           if not success:
               sys.exit(1)
       else:
           # 使用傳統方式
           if not args.url:
               print("錯誤: 未指定 --url 參數，且未使用 --auto-detect")
               sys.exit(1)
               
           # 初始化 API 調試器
           api_debugger = ApiDebugger(
               base_url=args.url,
               headers={"Content-Type": "application/json"}
           )
           
           if args.token:
               api_debugger.add_auth_token(args.token)
           
           # 載入特定環境的測試用例
           test_cases = load_test_cases(args.env)
           
           # 運行測試
           summary = api_debugger.run_test_suite(test_cases)
           
           # 生成報告
           api_debugger.generate_report(f"api_test_report_{args.env}.html")
           
           # 如果有失敗的測試，返回非零退出碼
           if summary["failed_tests"] > 0:
               print(f"測試失敗! {summary['failed_tests']} 個測試未通過")
               sys.exit(1)
       
       print("所有測試通過!")
   
   def load_test_cases(env):
       # 這裡可以根據不同環境載入不同的測試用例
       # 例如從配置文件或數據庫中載入
       # 這裡只是一個簡單的示例
       if env == "dev":
           return [
               # 開發環境測試用例
           ]
       elif env == "staging":
           return [
               # 預發佈環境測試用例
           ]
       else:
           return [
               # 生產環境測試用例
           ]
   
   if __name__ == "__main__":
       main() 
```

## 自定義 API 調試器

```python
# my_custom_debugger.py
from api_debugger import ApiDebugger
from port_detector import ApiPortDetector

class MyProjectApiDebugger(ApiDebugger):
    """針對我的專案定製的 API 調試器"""
    
    def __init__(self, base_url, api_key=None, **kwargs):
        super().__init__(base_url, **kwargs)
        
        if api_key:
            self.headers["X-API-Key"] = api_key
    
    def test_my_specific_feature(self, param1, param2):
        """測試我的專案特有的功能"""
        # 實現特定測試邏輯
        result1 = self.test_endpoint(
            endpoint=f"/feature/{param1}",
            method="GET",
            expected_status=200
        )
        
        result2 = self.test_endpoint(
            endpoint="/feature/action",
            method="POST",
            data={"param": param2},
            expected_status=201
        )
        
        return result1["success"] and result2["success"]
    
    def auto_test_my_api(self):
        """自動測試我的 API"""
        # 使用自動檢測功能
        detector = ApiPortDetector(
            host=self.base_url.split("://")[1].split(":")[0],
            port_range=(8000, 9000)
        )
        
        # 檢測端點
        port = int(self.base_url.split(":")[-1].split("/")[0])
        endpoints = detector.detect_api_endpoints(port)
        
        # 生成並運行測試用例
        endpoint_data = {}
        for endpoint, methods in endpoints.items():
            endpoint_data[endpoint] = {
                "methods": methods,
                "data_templates": {}
            }
        
        test_cases = detector.generate_test_cases(port, endpoint_data)
        return self.run_test_suite(test_cases) 