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

## 安裝

1. 確保已安裝 Python 3.6 或更高版本
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

## 自定義和擴展

你可以根據自己的需求自定義和擴展這個工具：

- 添加更多測試類型
- 集成到 CI/CD 流程中
- 添加更多報告格式（例如 JSON、CSV）
- 添加更多驗證邏輯

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
   
   def main():
       parser = argparse.ArgumentParser(description="API 測試工具")
       parser.add_argument("--url", required=True, help="API 基礎 URL")
       parser.add_argument("--token", help="API 認證令牌")
       parser.add_argument("--env", default="dev", choices=["dev", "staging", "prod"], help="環境")
       
       args = parser.parse_args()
       
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

# my_custom_debugger.py
from api_debugger import ApiDebugger

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