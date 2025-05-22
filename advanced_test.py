import argparse
import json
import time
import random
import string
from api_debugger import ApiDebugger

def generate_random_string(length=8):
    """生成隨機字符串"""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def generate_random_email():
    """生成隨機電子郵件地址"""
    return f"test_{generate_random_string(8)}@example.com"

def generate_random_user():
    """生成隨機用戶數據"""
    return {
        "name": f"Test User {generate_random_string(5)}",
        "email": generate_random_email(),
        "password": generate_random_string(10)
    }

class AdvancedApiTester:
    """高級 API 測試器，提供更多自動化測試功能"""
    
    def __init__(self, base_url, token=None):
        """初始化測試器"""
        self.api_debugger = ApiDebugger(
            base_url=base_url,
            headers={"Content-Type": "application/json"}
        )
        
        if token:
            self.api_debugger.add_auth_token(token)
            
        # 存儲測試過程中創建的資源的 ID
        self.created_resources = {
            "users": [],
            "posts": [],
            "comments": []
        }
        
    def setup(self):
        """測試前的設置，例如創建測試數據"""
        print("設置測試環境...")
        # 這裡可以添加測試前的設置代碼
        
    def teardown(self):
        """測試後的清理，例如刪除測試數據"""
        print("清理測試環境...")
        # 刪除測試過程中創建的資源
        for user_id in self.created_resources["users"]:
            self.api_debugger.test_endpoint(
                endpoint=f"/api/users/{user_id}",
                method="DELETE",
                expected_status=204
            )
            
        for post_id in self.created_resources["posts"]:
            self.api_debugger.test_endpoint(
                endpoint=f"/api/posts/{post_id}",
                method="DELETE",
                expected_status=204
            )
            
        for comment_id in self.created_resources["comments"]:
            self.api_debugger.test_endpoint(
                endpoint=f"/api/comments/{comment_id}",
                method="DELETE",
                expected_status=204
            )
    
    def run_user_crud_tests(self):
        """運行用戶 CRUD 測試"""
        print("運行用戶 CRUD 測試...")
        
        # 創建用戶
        user_data = generate_random_user()
        create_result = self.api_debugger.test_endpoint(
            endpoint="/api/users",
            method="POST",
            data=user_data,
            expected_status=201,
            test_name="創建用戶",
            description="測試創建新用戶"
        )
        
        # 檢查是否成功創建
        if create_result.get("success"):
            user_id = create_result.get("response_data", {}).get("id")
            if user_id:
                self.created_resources["users"].append(user_id)
                
                # 獲取用戶
                self.api_debugger.test_endpoint(
                    endpoint=f"/api/users/{user_id}",
                    method="GET",
                    expected_status=200,
                    expected_response={"id": user_id, "name": user_data["name"]},
                    test_name="獲取用戶",
                    description="測試獲取剛創建的用戶"
                )
                
                # 更新用戶
                update_data = {"name": f"Updated {user_data['name']}"}
                self.api_debugger.test_endpoint(
                    endpoint=f"/api/users/{user_id}",
                    method="PUT",
                    data=update_data,
                    expected_status=200,
                    test_name="更新用戶",
                    description="測試更新用戶信息"
                )
                
                # 刪除用戶
                self.api_debugger.test_endpoint(
                    endpoint=f"/api/users/{user_id}",
                    method="DELETE",
                    expected_status=204,
                    test_name="刪除用戶",
                    description="測試刪除用戶"
                )
                
                # 刪除後再次獲取用戶，應該返回 404
                self.api_debugger.test_endpoint(
                    endpoint=f"/api/users/{user_id}",
                    method="GET",
                    expected_status=404,
                    test_name="獲取已刪除用戶",
                    description="測試獲取已刪除的用戶"
                )
                
                # 從已創建資源列表中移除
                self.created_resources["users"].remove(user_id)
    
    def run_authentication_tests(self):
        """運行身份驗證測試"""
        print("運行身份驗證測試...")
        
        # 註冊
        user_data = generate_random_user()
        register_result = self.api_debugger.test_endpoint(
            endpoint="/api/auth/register",
            method="POST",
            data=user_data,
            expected_status=201,
            test_name="用戶註冊",
            description="測試用戶註冊功能"
        )
        
        # 登錄
        login_result = self.api_debugger.test_endpoint(
            endpoint="/api/auth/login",
            method="POST",
            data={
                "email": user_data["email"],
                "password": user_data["password"]
            },
            expected_status=200,
            test_name="用戶登錄",
            description="測試用戶登錄功能"
        )
        
        # 檢查是否成功登錄並獲取令牌
        if login_result.get("success"):
            token = login_result.get("response_data", {}).get("token")
            if token:
                # 使用令牌創建新的 API 調試器
                auth_debugger = ApiDebugger(
                    base_url=self.api_debugger.base_url,
                    headers={"Content-Type": "application/json"}
                )
                auth_debugger.add_auth_token(token)
                
                # 測試需要身份驗證的端點
                auth_debugger.test_endpoint(
                    endpoint="/api/auth/me",
                    method="GET",
                    expected_status=200,
                    expected_response={"email": user_data["email"]},
                    test_name="獲取當前用戶信息",
                    description="測試使用令牌獲取當前用戶信息"
                )
                
                # 測試登出
                auth_debugger.test_endpoint(
                    endpoint="/api/auth/logout",
                    method="POST",
                    expected_status=200,
                    test_name="用戶登出",
                    description="測試用戶登出功能"
                )
                
                # 登出後再次使用令牌，應該失敗
                auth_debugger.test_endpoint(
                    endpoint="/api/auth/me",
                    method="GET",
                    expected_status=401,
                    test_name="使用無效令牌",
                    description="測試使用登出後的令牌"
                )
    
    def run_input_validation_tests(self):
        """運行輸入驗證測試"""
        print("運行輸入驗證測試...")
        
        # 測試各種無效輸入
        invalid_inputs = [
            # 缺少必要字段
            {
                "data": {"name": "Test User"},
                "description": "缺少必要字段 (email, password)"
            },
            # 無效的電子郵件格式
            {
                "data": {
                    "name": "Test User",
                    "email": "invalid-email",
                    "password": "password123"
                },
                "description": "無效的電子郵件格式"
            },
            # 密碼太短
            {
                "data": {
                    "name": "Test User",
                    "email": "test@example.com",
                    "password": "123"
                },
                "description": "密碼太短"
            },
            # 名稱太長
            {
                "data": {
                    "name": "T" * 256,  # 假設名稱最大長度為 255
                    "email": "test@example.com",
                    "password": "password123"
                },
                "description": "名稱太長"
            },
            # XSS 嘗試
            {
                "data": {
                    "name": "<script>alert('XSS')</script>",
                    "email": "test@example.com",
                    "password": "password123"
                },
                "description": "XSS 嘗試"
            },
            # SQL 注入嘗試
            {
                "data": {
                    "name": "Test User",
                    "email": "test@example.com' OR '1'='1",
                    "password": "password123"
                },
                "description": "SQL 注入嘗試"
            }
        ]
        
        for i, invalid_input in enumerate(invalid_inputs):
            self.api_debugger.test_endpoint(
                endpoint="/api/users",
                method="POST",
                data=invalid_input["data"],
                expected_status=400,  # 預期驗證失敗
                test_name=f"無效輸入測試 {i+1}",
                description=f"測試無效輸入: {invalid_input['description']}"
            )
    
    def run_rate_limit_tests(self):
        """運行速率限制測試"""
        print("運行速率限制測試...")
        
        # 快速連續發送多個請求
        for i in range(20):
            self.api_debugger.test_endpoint(
                endpoint="/api/users",
                method="GET",
                test_name=f"速率限制測試 {i+1}",
                description=f"快速連續請求 {i+1}/20"
            )
            time.sleep(0.1)  # 短暫延遲
            
        # 檢查是否觸發了速率限制
        result = self.api_debugger.test_endpoint(
            endpoint="/api/users",
            method="GET",
            expected_status=429,  # 預期觸發速率限制
            test_name="速率限制檢查",
            description="檢查是否觸發了速率限制"
        )
        
        # 如果沒有觸發速率限制，記錄一個提示
        if result.get("status_code") != 429:
            print("注意: 未觸發速率限制，API 可能沒有實現速率限制或限制閾值較高")
    
    def run_all_tests(self):
        """運行所有測試"""
        try:
            self.setup()
            
            # 基本 CRUD 測試
            self.run_user_crud_tests()
            
            # 身份驗證測試
            self.run_authentication_tests()
            
            # 輸入驗證測試
            self.run_input_validation_tests()
            
            # 速率限制測試
            self.run_rate_limit_tests()
            
            # 生成報告
            self.api_debugger.generate_report("advanced_api_test_report.html")
            
            summary = {
                "total_tests": len(self.api_debugger.test_results),
                "passed_tests": sum(1 for r in self.api_debugger.test_results if r.get("success", False)),
                "failed_tests": sum(1 for r in self.api_debugger.test_results if not r.get("success", False))
            }
            
            print(f"測試完成!")
            print(f"總測試數: {summary['total_tests']}")
            print(f"通過測試數: {summary['passed_tests']}")
            print(f"失敗測試數: {summary['failed_tests']}")
            print(f"成功率: {(summary['passed_tests'] / summary['total_tests'] * 100) if summary['total_tests'] > 0 else 0:.2f}%")
            print(f"報告已生成: advanced_api_test_report.html")
            
        finally:
            self.teardown()

def main():
    """主函數"""
    parser = argparse.ArgumentParser(description="高級 API 測試工具")
    parser.add_argument("--url", required=True, help="API 基礎 URL，例如 http://localhost:8000")
    parser.add_argument("--token", help="API 認證令牌（可選）")
    
    args = parser.parse_args()
    
    tester = AdvancedApiTester(base_url=args.url, token=args.token)
    tester.run_all_tests()

if __name__ == "__main__":
    main()
