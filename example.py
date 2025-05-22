from api_debugger import ApiDebugger

def main():
    """
    示例：如何使用 API 調試工具測試一個後端 API
    """
    # 初始化 API 調試器
    api_debugger = ApiDebugger(
        base_url="http://localhost:8000",  # 替換為你的 API 基礎 URL
        headers={
            "Content-Type": "application/json",
            # 可以添加其他默認請求頭
        }
    )
    
    # 可選：添加認證令牌
    # api_debugger.add_auth_token("your_token_here")
    
    # 定義測試用例
    test_cases = [
        # 基本功能測試
        {
            "endpoint": "/api/users",
            "method": "GET",
            "expected_status": 200,
            "test_name": "獲取用戶列表",
            "description": "測試獲取用戶列表 API"
        },
        {
            "endpoint": "/api/users/1",
            "method": "GET",
            "expected_status": 200,
            "test_name": "獲取單個用戶",
            "description": "測試獲取單個用戶 API"
        },
        {
            "endpoint": "/api/users",
            "method": "POST",
            "data": {
                "name": "測試用戶",
                "email": "test@example.com",
                "password": "password123"
            },
            "expected_status": 201,
            "expected_response": {
                "success": True
            },
            "test_name": "創建用戶",
            "description": "測試創建用戶 API"
        },
        
        # 邊界情況和錯誤處理測試
        {
            "endpoint": "/api/users",
            "method": "POST",
            "data": {
                # 缺少必要字段
                "name": "測試用戶"
                # 缺少 email 和 password
            },
            "expected_status": 400,  # 預期失敗
            "test_name": "創建用戶-缺少必要字段",
            "description": "測試創建用戶時缺少必要字段的情況"
        },
        {
            "endpoint": "/api/users/999",
            "method": "GET",
            "expected_status": 404,  # 預期找不到資源
            "test_name": "獲取不存在的用戶",
            "description": "測試獲取不存在的用戶 API"
        },
        {
            "endpoint": "/api/users/1",
            "method": "PUT",
            "data": {
                "name": "更新的用戶名",
                "email": "updated@example.com"
            },
            "expected_status": 200,
            "test_name": "更新用戶",
            "description": "測試更新用戶 API"
        },
        {
            "endpoint": "/api/users/1",
            "method": "PUT",
            "data": {
                "email": "invalid-email"  # 無效的電子郵件格式
            },
            "expected_status": 400,
            "test_name": "更新用戶-無效數據",
            "description": "測試使用無效數據更新用戶"
        },
        
        # 安全性測試
        {
            "endpoint": "/api/admin/users",
            "method": "GET",
            "expected_status": 401,  # 未授權
            "test_name": "未授權訪問管理員 API",
            "description": "測試未授權訪問管理員 API"
        },
        {
            "endpoint": "/api/users",
            "method": "POST",
            "data": {
                "name": "<script>alert('XSS')</script>",
                "email": "xss@test.com",
                "password": "password123"
            },
            "expected_status": 400,  # 應該拒絕 XSS 嘗試
            "test_name": "XSS 攻擊測試",
            "description": "測試 XSS 攻擊防護"
        },
        
        # 性能測試
        {
            "endpoint": "/api/users?limit=1000",
            "method": "GET",
            "expected_status": 200,
            "test_name": "大量數據請求",
            "description": "測試請求大量數據的性能"
        },
        
        # 特殊字符和編碼測試
        {
            "endpoint": "/api/users",
            "method": "POST",
            "data": {
                "name": "特殊字符 !@#$%^&*()",
                "email": "special@example.com",
                "password": "password123"
            },
            "expected_status": 201,
            "test_name": "特殊字符處理",
            "description": "測試特殊字符處理"
        },
        {
            "endpoint": "/api/users",
            "method": "POST",
            "data": {
                "name": "中文名稱測試",
                "email": "chinese@example.com",
                "password": "password123"
            },
            "expected_status": 201,
            "test_name": "中文字符處理",
            "description": "測試中文字符處理"
        }
    ]
    
    # 運行測試套件
    summary = api_debugger.run_test_suite(test_cases)
    
    # 生成報告
    api_debugger.generate_report("api_test_report.html")
    
    print(f"測試完成! 成功率: {summary['success_rate'] * 100:.2f}%")
    print(f"報告已生成: api_test_report.html")

if __name__ == "__main__":
    main() 