import requests
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Any, Union, Optional

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("api_debug.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("API_DEBUG")

class ApiDebugger:
    """API 調試工具，用於測試 API 端點的各種輸入情況"""
    
    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None):
        """
        初始化 API 調試器
        
        Args:
            base_url: API 的基礎 URL，例如 http://localhost:8000
            headers: 請求頭，例如授權信息等
        """
        self.base_url = base_url.rstrip('/')
        self.headers = headers or {}
        self.test_results = []
        self.session = requests.Session()
        
    def add_auth_token(self, token: str, prefix: str = "Bearer"):
        """添加認證令牌到請求頭"""
        self.headers["Authorization"] = f"{prefix} {token}"
        
    def test_endpoint(self, 
                     endpoint: str, 
                     method: str = "GET", 
                     data: Any = None, 
                     expected_status: int = 200,
                     expected_response: Any = None,
                     description: str = "",
                     test_name: str = "") -> Dict[str, Any]:
        """
        測試單個 API 端點
        
        Args:
            endpoint: API 端點路徑，例如 /api/users
            method: HTTP 方法，例如 GET, POST, PUT, DELETE
            data: 請求數據，對於 POST/PUT 請求
            expected_status: 預期的 HTTP 狀態碼
            expected_response: 預期的響應數據（部分匹配）
            description: 測試描述
            test_name: 測試名稱
            
        Returns:
            測試結果字典
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        method = method.upper()
        start_time = time.time()
        
        try:
            if not test_name:
                test_name = f"{method} {endpoint}"
                
            logger.info(f"執行測試: {test_name}")
            logger.info(f"請求 URL: {url}")
            logger.info(f"請求方法: {method}")
            
            if data:
                logger.info(f"請求數據: {json.dumps(data, ensure_ascii=False, indent=2)}")
            
            response = self.session.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data if method in ["POST", "PUT", "PATCH"] and data else None,
                params=data if method == "GET" and data else None
            )
            
            duration = time.time() - start_time
            status_code = response.status_code
            
            try:
                response_data = response.json()
            except:
                response_data = response.text
                
            # 檢查響應
            status_match = status_code == expected_status
            response_match = True
            
            if expected_response and status_match:
                if isinstance(expected_response, dict) and isinstance(response_data, dict):
                    # 檢查預期響應是否是響應數據的子集
                    response_match = all(
                        k in response_data and response_data[k] == v 
                        for k, v in expected_response.items()
                    )
                else:
                    response_match = expected_response == response_data
            
            result = {
                "test_name": test_name,
                "description": description,
                "url": url,
                "method": method,
                "request_data": data,
                "status_code": status_code,
                "expected_status": expected_status,
                "status_match": status_match,
                "response_data": response_data,
                "expected_response": expected_response,
                "response_match": response_match,
                "duration": duration,
                "timestamp": datetime.now().isoformat(),
                "success": status_match and response_match
            }
            
            # 記錄測試結果
            self.test_results.append(result)
            
            # 輸出測試結果
            if result["success"]:
                logger.info(f"測試通過: {test_name}")
            else:
                logger.error(f"測試失敗: {test_name}")
                if not status_match:
                    logger.error(f"狀態碼不匹配: 預期 {expected_status}, 實際 {status_code}")
                if not response_match:
                    logger.error(f"響應數據不匹配")
                    logger.error(f"預期: {json.dumps(expected_response, ensure_ascii=False, indent=2)}")
                    logger.error(f"實際: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
            
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"測試出錯: {str(e)}")
            
            result = {
                "test_name": test_name,
                "description": description,
                "url": url,
                "method": method,
                "request_data": data,
                "error": str(e),
                "duration": duration,
                "timestamp": datetime.now().isoformat(),
                "success": False
            }
            
            self.test_results.append(result)
            return result
    
    def run_test_suite(self, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        運行一組測試用例
        
        Args:
            test_cases: 測試用例列表，每個測試用例是一個字典，包含 test_endpoint 方法的參數
            
        Returns:
            測試結果摘要
        """
        start_time = time.time()
        logger.info(f"開始運行測試套件，共 {len(test_cases)} 個測試用例")
        
        for i, test_case in enumerate(test_cases):
            logger.info(f"運行測試 {i+1}/{len(test_cases)}")
            self.test_endpoint(**test_case)
            
        duration = time.time() - start_time
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r.get("success", False))
        
        summary = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": total_tests - passed_tests,
            "success_rate": passed_tests / total_tests if total_tests > 0 else 0,
            "duration": duration,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"測試套件運行完成")
        logger.info(f"總測試數: {summary['total_tests']}")
        logger.info(f"通過測試數: {summary['passed_tests']}")
        logger.info(f"失敗測試數: {summary['failed_tests']}")
        logger.info(f"成功率: {summary['success_rate'] * 100:.2f}%")
        logger.info(f"總耗時: {summary['duration']:.2f} 秒")
        
        return summary
    
    def generate_report(self, output_file: str = "api_test_report.html") -> None:
        """生成 HTML 測試報告"""
        passed_tests = sum(1 for r in self.test_results if r.get("success", False))
        total_tests = len(self.test_results)
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>API 測試報告</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f5f5f5; padding: 20px; border-radius: 5px; }}
                .summary {{ margin: 20px 0; }}
                .test-case {{ margin-bottom: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
                .test-case.success {{ border-left: 5px solid green; }}
                .test-case.failure {{ border-left: 5px solid red; }}
                .details {{ margin-top: 10px; font-family: monospace; white-space: pre-wrap; }}
                .success-rate {{ font-size: 24px; font-weight: bold; }}
                .success-rate.good {{ color: green; }}
                .success-rate.bad {{ color: red; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ text-align: left; padding: 8px; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>API 測試報告</h1>
                <p>生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="summary">
                <h2>測試摘要</h2>
                <p>總測試數: {total_tests}</p>
                <p>通過測試數: {passed_tests}</p>
                <p>失敗測試數: {total_tests - passed_tests}</p>
                <p class="success-rate {'good' if passed_tests == total_tests else 'bad'}">
                    成功率: {(passed_tests / total_tests * 100) if total_tests > 0 else 0:.2f}%
                </p>
            </div>
            
            <h2>測試詳情</h2>
        """
        
        for i, result in enumerate(self.test_results):
            success = result.get("success", False)
            html += f"""
            <div class="test-case {'success' if success else 'failure'}">
                <h3>{i+1}. {result.get('test_name', '未命名測試')} - {'成功' if success else '失敗'}</h3>
                <p>{result.get('description', '')}</p>
                <table>
                    <tr><th>URL</th><td>{result.get('url', '')}</td></tr>
                    <tr><th>方法</th><td>{result.get('method', '')}</td></tr>
                    <tr><th>狀態碼</th><td>{result.get('status_code', '')} (預期: {result.get('expected_status', '')})</td></tr>
                    <tr><th>耗時</th><td>{result.get('duration', 0):.2f} 秒</td></tr>
                </table>
                
                <div class="details">
                    <h4>請求數據:</h4>
                    <pre>{json.dumps(result.get('request_data', {}), ensure_ascii=False, indent=2)}</pre>
                    
                    <h4>響應數據:</h4>
                    <pre>{json.dumps(result.get('response_data', {}), ensure_ascii=False, indent=2)}</pre>
                    
                    {f'<h4>預期響應:</h4><pre>{json.dumps(result.get("expected_response", {}), ensure_ascii=False, indent=2)}</pre>' if result.get('expected_response') else ''}
                    
                    {f'<h4>錯誤:</h4><pre>{result.get("error", "")}</pre>' if 'error' in result else ''}
                </div>
            </div>
            """
            
        html += """
        </body>
        </html>
        """
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
            
        logger.info(f"測試報告已生成: {output_file}") 