import socket
import requests
import json
import logging
import re
import time
import random
import string
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional
from api_debugger import ApiDebugger, logger

class ApiPortDetector:
    """API 端口檢測器，用於自動檢測 API 端口和輸入參數"""
    
    def __init__(self, host: str = "localhost", port_range: Tuple[int, int] = (8000, 9000)):
        """
        初始化 API 端口檢測器
        
        Args:
            host: API 主機名，默認為 localhost
            port_range: 要檢測的端口範圍，默認為 8000-9000
        """
        self.host = host
        self.port_range = port_range
        self.active_ports = []
        self.api_endpoints = {}
        self.input_templates = {}
        
    def scan_ports(self) -> List[int]:
        """
        掃描指定範圍內的開放端口
        
        Returns:
            開放的端口列表
        """
        logger.info(f"開始掃描端口範圍 {self.port_range[0]}-{self.port_range[1]}...")
        open_ports = []
        
        for port in range(self.port_range[0], self.port_range[1] + 1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((self.host, port))
            if result == 0:
                open_ports.append(port)
                logger.info(f"發現開放端口: {port}")
            sock.close()
        
        self.active_ports = open_ports
        return open_ports
    
    def detect_api_endpoints(self, port: int) -> Dict[str, List[str]]:
        """
        檢測指定端口上的 API 端點
        
        Args:
            port: 要檢測的端口
            
        Returns:
            檢測到的 API 端點字典，格式為 {endpoint: [支持的HTTP方法列表]}
        """
        logger.info(f"檢測端口 {port} 上的 API 端點...")
        base_url = f"http://{self.host}:{port}"
        endpoints = {}
        
        # 嘗試常見的 API 路徑
        common_paths = [
            "/api", "/api/v1", "/api/v2", "/api/users", "/api/auth",
            "/users", "/auth", "/products", "/orders", "/data",
            "/api/auth/login", "/api/auth/register", "/api/auth/logout",
            "/api/products", "/api/orders", "/api/categories"
        ]
        
        for path in common_paths:
            try:
                # 嘗試 OPTIONS 請求來獲取支持的方法
                response = requests.options(f"{base_url}{path}", timeout=2)
                if response.status_code < 500:  # 不是服務器錯誤
                    allowed_methods = response.headers.get("Allow", "").split(", ")
                    if allowed_methods and allowed_methods[0]:
                        endpoints[path] = allowed_methods
                        continue
                
                # 如果 OPTIONS 不工作，嘗試 GET 請求
                response = requests.get(f"{base_url}{path}", timeout=2)
                if response.status_code != 404:  # 不是 Not Found
                    endpoints[path] = ["GET"]
                    
                    # 嘗試 POST 請求，看是否支持
                    try:
                        response = requests.post(f"{base_url}{path}", json={}, timeout=2)
                        if response.status_code != 404 and response.status_code != 405:
                            if "POST" not in endpoints[path]:
                                endpoints[path].append("POST")
                    except:
                        pass
            except Exception as e:
                logger.debug(f"檢測端點 {path} 時出錯: {str(e)}")
        
        if endpoints:
            self.api_endpoints[port] = endpoints
            
        return endpoints
    
    def analyze_log_for_endpoints(self, log_file: str = "api_debug.log") -> Dict[str, Any]:
        """
        從日誌文件中分析 API 端點和輸入
        
        Args:
            log_file: 日誌文件路徑
            
        Returns:
            分析結果，包含端點、方法和輸入數據
        """
        logger.info(f"從日誌文件 {log_file} 分析 API 端點和輸入...")
        endpoints_data = {}
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                log_content = f.read()
                
            # 提取 URL 模式
            url_pattern = r"URL: (http://[^/]+)(/[^\s]+)"
            urls = re.findall(url_pattern, log_content)
            
            # 提取方法和數據
            for base_url, endpoint in urls:
                # 提取端口
                port_match = re.search(r":(\d+)", base_url)
                if port_match:
                    port = int(port_match.group(1))
                    
                    # 尋找相關的方法和數據
                    # 查找這個 URL 後面的方法
                    method_pattern = rf"URL: {re.escape(base_url + endpoint)}[\s\S]{{0,50}}方法: ([A-Z]+)"
                    method_match = re.search(method_pattern, log_content)
                    
                    if method_match:
                        method = method_match.group(1)
                        
                        # 如果是 POST 或 PUT，尋找請求數據
                        data = None
                        if method in ["POST", "PUT", "PATCH"]:
                            # 查找這個 URL 和方法後面的數據
                            data_pattern = rf"URL: {re.escape(base_url + endpoint)}[\s\S]{{0,200}}請求數據: ({{[\s\S]*?}})"
                            data_match = re.search(data_pattern, log_content)
                            if data_match:
                                try:
                                    data_str = data_match.group(1)
                                    data = json.loads(data_str)
                                except:
                                    logger.debug(f"無法解析數據: {data_str}")
                        
                        # 保存端點信息
                        if port not in endpoints_data:
                            endpoints_data[port] = {}
                        
                        if endpoint not in endpoints_data[port]:
                            endpoints_data[port][endpoint] = {"methods": [], "data_templates": {}}
                        
                        if method not in endpoints_data[port][endpoint]["methods"]:
                            endpoints_data[port][endpoint]["methods"].append(method)
                        
                        if data and method not in endpoints_data[port][endpoint]["data_templates"]:
                            endpoints_data[port][endpoint]["data_templates"][method] = data
        except Exception as e:
            logger.error(f"分析日誌文件時出錯: {str(e)}")
        
        return endpoints_data
    
    def generate_random_string(self, length=8):
        """生成隨機字符串"""
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
    
    def generate_random_email(self):
        """生成隨機電子郵件地址"""
        return f"test_{self.generate_random_string(8)}@example.com"
    
    def generate_random_password(self, length=10):
        """生成隨機密碼"""
        return self.generate_random_string(length)
    
    def generate_random_phone(self):
        """生成隨機電話號碼"""
        return f"09{random.randint(10000000, 99999999)}"
    
    def generate_random_date(self):
        """生成隨機日期"""
        year = random.randint(2020, 2025)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        return f"{year}-{month:02d}-{day:02d}"
    
    def generate_smart_input_data(self, endpoint: str, method: str) -> Dict[str, Any]:
        """
        根據端點和方法智能生成輸入數據
        
        Args:
            endpoint: API 端點
            method: HTTP 方法
            
        Returns:
            生成的輸入數據
        """
        # 如果不是需要數據的方法，返回空
        if method not in ["POST", "PUT", "PATCH"]:
            return {}
        
        data = {}
        endpoint_lower = endpoint.lower()
        
        # 用戶相關端點
        if "user" in endpoint_lower or "auth" in endpoint_lower or "login" in endpoint_lower or "register" in endpoint_lower:
            if "login" in endpoint_lower:
                data = {
                    "email": self.generate_random_email(),
                    "password": self.generate_random_password()
                }
            elif "register" in endpoint_lower:
                data = {
                    "name": f"Test User {self.generate_random_string(5)}",
                    "email": self.generate_random_email(),
                    "password": self.generate_random_password()
                }
            else:
                data = {
                    "name": f"Test User {self.generate_random_string(5)}",
                    "email": self.generate_random_email(),
                    "password": self.generate_random_password(),
                    "phone": self.generate_random_phone()
                }
        
        # 產品相關端點
        elif "product" in endpoint_lower:
            data = {
                "name": f"Test Product {self.generate_random_string(5)}",
                "description": f"This is a test product description {self.generate_random_string(20)}",
                "price": round(random.uniform(10, 1000), 2),
                "category_id": random.randint(1, 10),
                "stock": random.randint(1, 100)
            }
        
        # 訂單相關端點
        elif "order" in endpoint_lower:
            data = {
                "user_id": random.randint(1, 10),
                "products": [
                    {
                        "product_id": random.randint(1, 100),
                        "quantity": random.randint(1, 5)
                    },
                    {
                        "product_id": random.randint(1, 100),
                        "quantity": random.randint(1, 5)
                    }
                ],
                "shipping_address": f"Test Address {self.generate_random_string(10)}",
                "payment_method": random.choice(["credit_card", "paypal", "bank_transfer"])
            }
        
        # 評論相關端點
        elif "comment" in endpoint_lower or "review" in endpoint_lower:
            data = {
                "user_id": random.randint(1, 10),
                "product_id": random.randint(1, 100),
                "rating": random.randint(1, 5),
                "content": f"This is a test comment/review {self.generate_random_string(30)}"
            }
        
        # 類別相關端點
        elif "categor" in endpoint_lower:
            data = {
                "name": f"Test Category {self.generate_random_string(5)}",
                "description": f"This is a test category description {self.generate_random_string(20)}"
            }
        
        # 如果沒有匹配的特定模式，提供一個通用的數據模板
        else:
            data = {
                "name": f"Test {self.generate_random_string(5)}",
                "description": f"Test description {self.generate_random_string(20)}",
                "value": random.randint(1, 100),
                "date": self.generate_random_date(),
                "active": random.choice([True, False])
            }
        
        return data
    
    def generate_test_cases(self, port: int, endpoints_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        根據檢測到的端點和輸入生成測試用例
        
        Args:
            port: API 端口
            endpoints_data: 端點數據
            
        Returns:
            測試用例列表
        """
        logger.info(f"為端口 {port} 生成測試用例...")
        test_cases = []
        
        for endpoint, data in endpoints_data.items():
            methods = data.get("methods", [])
            data_templates = data.get("data_templates", {})
            
            for method in methods:
                # 準備測試用例
                test_case = {
                    "endpoint": endpoint,
                    "method": method,
                    "test_name": f"{method} {endpoint}",
                    "description": f"測試 {method} {endpoint} 端點"
                }
                
                # 設置預期狀態碼
                if method == "GET":
                    test_case["expected_status"] = 200
                elif method == "POST":
                    test_case["expected_status"] = 201
                elif method == "DELETE":
                    test_case["expected_status"] = 204
                else:
                    test_case["expected_status"] = 200
                
                # 如果有數據模板，使用它
                if method in data_templates:
                    test_case["data"] = data_templates[method]
                # 否則智能生成輸入數據
                elif method in ["POST", "PUT", "PATCH"]:
                    test_case["data"] = self.generate_smart_input_data(endpoint, method)
                
                test_cases.append(test_case)
                
                # 對於 GET 請求，添加一個 ID 參數的測試
                if method == "GET" and not endpoint.endswith("/"):
                    id_endpoint = f"{endpoint}/1"
                    test_cases.append({
                        "endpoint": id_endpoint,
                        "method": "GET",
                        "expected_status": 200,
                        "test_name": f"GET {id_endpoint}",
                        "description": f"測試獲取單個資源 {id_endpoint}"
                    })
                
                # 對於 POST 請求，添加一個無效輸入的測試
                if method == "POST" and "data" in test_case:
                    # 創建一個缺少部分字段的數據
                    invalid_data = {}
                    if test_case["data"]:
                        # 只取原始數據的第一個字段
                        for key in list(test_case["data"].keys())[:1]:
                            invalid_data[key] = test_case["data"][key]
                    
                    test_cases.append({
                        "endpoint": endpoint,
                        "method": "POST",
                        "data": invalid_data,
                        "expected_status": 400,
                        "test_name": f"POST {endpoint} (無效輸入)",
                        "description": f"測試使用無效輸入的 POST {endpoint}"
                    })
        
        return test_cases
    
    def run_tests(self, port: int, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        在指定端口上運行測試用例
        
        Args:
            port: API 端口
            test_cases: 測試用例列表
            
        Returns:
            測試結果摘要
        """
        logger.info(f"在端口 {port} 上運行 {len(test_cases)} 個測試用例...")
        base_url = f"http://{self.host}:{port}"
        
        api_debugger = ApiDebugger(
            base_url=base_url,
            headers={"Content-Type": "application/json"}
        )
        
        summary = api_debugger.run_test_suite(test_cases)
        api_debugger.generate_report(f"api_test_report_port_{port}.html")
        
        return summary
    
    def auto_detect_and_test(self) -> Dict[int, Dict[str, Any]]:
        """
        自動檢測 API 端口並運行測試
        
        Returns:
            各端口的測試結果
        """
        results = {}
        
        # 1. 掃描開放端口
        open_ports = self.scan_ports()
        if not open_ports:
            logger.warning(f"在範圍 {self.port_range[0]}-{self.port_range[1]} 內未發現開放端口")
            return results
        
        # 2. 從日誌文件分析端點和輸入
        log_endpoints = self.analyze_log_for_endpoints()
        
        # 3. 對每個開放端口進行測試
        for port in open_ports:
            # 檢查是否在日誌中找到這個端口的信息
            if port in log_endpoints:
                logger.info(f"從日誌中找到端口 {port} 的信息")
                test_cases = self.generate_test_cases(port, log_endpoints[port])
            else:
                # 如果日誌中沒有，嘗試檢測端點
                logger.info(f"日誌中未找到端口 {port} 的信息，嘗試檢測端點")
                endpoints = self.detect_api_endpoints(port)
                if not endpoints:
                    logger.warning(f"在端口 {port} 上未檢測到 API 端點")
                    continue
                
                # 為檢測到的端點生成測試用例
                endpoint_data = {}
                for endpoint, methods in endpoints.items():
                    endpoint_data[endpoint] = {
                        "methods": methods,
                        "data_templates": {}
                    }
                
                test_cases = self.generate_test_cases(port, endpoint_data)
            
            # 運行測試
            if test_cases:
                logger.info(f"在端口 {port} 上運行 {len(test_cases)} 個測試用例")
                summary = self.run_tests(port, test_cases)
                results[port] = {
                    "summary": summary,
                    "test_cases": test_cases
                }
            
        return results 