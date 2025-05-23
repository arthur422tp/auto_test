import requests
import json
import time
from typing import Optional, Dict, Any

class ApiTester:
    def __init__(self, url: str, timeout: int = 10, headers: Optional[Dict[str, str]] = None):
        self.url = url
        self.timeout = timeout
        self.headers = headers or {}
        self.results = []

    def _make_request(self, method: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """統一的請求處理方法"""
        start_time = time.time()
        result = {
            'method': method,
            'url': self.url,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'success': False,
            'status_code': None,
            'response_time': 0,
            'response_data': None,
            'error': None
        }
        
        try:
            print(f"\n🚀 測試 {method} {self.url}")
            print(f"⏱️  開始時間: {result['timestamp']}")
            
            if data:
                print(f"📤 請求資料: {json.dumps(data, indent=2, ensure_ascii=False)}")
            
            # 發送請求
            response = requests.request(
                method=method.upper(),
                url=self.url,
                json=data if data else None,
                headers=self.headers,
                timeout=self.timeout
            )
            
            # 計算回應時間
            response_time = time.time() - start_time
            result['response_time'] = round(response_time, 3)
            result['status_code'] = response.status_code
            
            # 處理回應內容
            try:
                result['response_data'] = response.json()
            except json.JSONDecodeError:
                result['response_data'] = response.text
            
            # 判斷是否成功
            result['success'] = 200 <= response.status_code < 300
            
            # 輸出結果
            status_emoji = "✅" if result['success'] else "❌"
            print(f"{status_emoji} 狀態碼: {result['status_code']}")
            print(f"⚡ 回應時間: {result['response_time']}秒")
            
            # 格式化回應內容
            if isinstance(result['response_data'], dict):
                print(f"📥 回應內容: {json.dumps(result['response_data'], indent=2, ensure_ascii=False)}")
            else:
                print(f"📥 回應內容: {result['response_data']}")
                
        except requests.exceptions.Timeout:
            result['error'] = f"請求逾時 (>{self.timeout}秒)"
            print(f"❌ {result['error']}")
        except requests.exceptions.ConnectionError:
            result['error'] = "連線失敗 - 請檢查伺服器是否運行"
            print(f"❌ {result['error']}")
        except requests.exceptions.RequestException as e:
            result['error'] = f"請求錯誤: {str(e)}"
            print(f"❌ {result['error']}")
        except Exception as e:
            result['error'] = f"未知錯誤: {str(e)}"
            print(f"❌ {result['error']}")
        
        self.results.append(result)
        return result

    def test_get(self):
        """測試 GET 請求"""
        return self._make_request('GET')

    def test_post(self, data: Optional[Dict] = None):
        """測試 POST 請求"""
        if data is None:
            data = {"test": "value", "timestamp": int(time.time())}
        return self._make_request('POST', data)

    def test_put(self, data: Optional[Dict] = None):
        """測試 PUT 請求"""
        if data is None:
            data = {"test": "updated_value", "timestamp": int(time.time())}
        return self._make_request('PUT', data)

    def test_patch(self, data: Optional[Dict] = None):
        """測試 PATCH 請求"""
        if data is None:
            data = {"test": "patched_value"}
        return self._make_request('PATCH', data)

    def test_delete(self):
        """測試 DELETE 請求"""
        return self._make_request('DELETE')

    def run_tests(self, method: Optional[str] = None, data: Optional[str] = None):
        """執行測試"""
        print(f"\n🎯 開始 API 測試")
        print(f"🌐 目標 URL: {self.url}")
        print("=" * 50)
        
        # 解析資料
        parsed_data = None
        if data:
            try:
                parsed_data = json.loads(data)
            except json.JSONDecodeError:
                print(f"⚠️  警告: 無法解析 JSON 資料，使用預設資料")
        
        # 執行指定方法或全部方法
        if method:
            method = method.upper()
            if method == 'GET':
                self.test_get()
            elif method == 'POST':
                self.test_post(parsed_data)
            elif method == 'PUT':
                self.test_put(parsed_data)
            elif method == 'PATCH':
                self.test_patch(parsed_data)
            elif method == 'DELETE':
                self.test_delete()
            else:
                print(f"❌ 不支援的 HTTP 方法: {method}")
        else:
            # 預設測試 GET 和 POST
            self.test_get()
            self.test_post(parsed_data)
        
        # 輸出測試摘要
        self.print_summary()

    def print_summary(self):
        """輸出測試摘要"""
        if not self.results:
            return
            
        print("\n" + "=" * 50)
        print("📊 測試摘要")
        print("=" * 50)
        
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r['success'])
        failed_tests = total_tests - successful_tests
        
        print(f"總測試數: {total_tests}")
        print(f"✅ 成功: {successful_tests}")
        print(f"❌ 失敗: {failed_tests}")
        print(f"📈 成功率: {(successful_tests/total_tests*100):.1f}%")
        
        # 顯示平均回應時間
        valid_times = [r['response_time'] for r in self.results if r['response_time'] > 0]
        if valid_times:
            avg_time = sum(valid_times) / len(valid_times)
            print(f"⚡ 平均回應時間: {avg_time:.3f}秒")
        
        # 顯示失敗的測試
        if failed_tests > 0:
            print(f"\n❌ 失敗的測試:")
            for result in self.results:
                if not result['success']:
                    error_msg = result['error'] or f"HTTP {result['status_code']}"
                    print(f"   • {result['method']}: {error_msg}")

    def get_results(self) -> list:
        """取得測試結果"""
        return self.results 