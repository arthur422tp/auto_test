import argparse
import json
import time
from typing import Optional, Dict, Any, List

import requests
from api_tester import ApiTester
from report_generator import ReportGenerator

class SmartApiTester:
    """智能API測試器 - 支援自動方法檢測和多場景測試"""
    
    def __init__(self, base_url: str, endpoint: str, timeout: int = 10, headers: Optional[Dict[str, str]] = None):
        self.base_url = base_url.rstrip('/')
        self.endpoint = endpoint
        self.full_url = f"{self.base_url}{endpoint}"
        self.timeout = timeout
        self.headers = headers or {"Content-Type": "application/json"}
        self.supported_methods = []
        self.test_results = []
        
    def detect_supported_methods(self) -> List[str]:
        """自動檢測API支援的HTTP方法"""
        print(f"\n🔍 正在檢測 {self.full_url} 支援的HTTP方法...")
        print("=" * 60)
        
        methods_to_test = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS']
        supported = []
        
        for method in methods_to_test:
            try:
                response = requests.request(
                    method=method,
                    url=self.full_url,
                    headers=self.headers,
                    timeout=self.timeout,
                    json={} if method in ['POST', 'PUT', 'PATCH'] else None
                )
                
                if response.status_code != 405:  # Method Not Allowed
                    supported.append(method)
                    status_emoji = "✅" if response.status_code < 400 else "⚠️"
                    print(f"{status_emoji} {method}: {response.status_code}")
                else:
                    print(f"❌ {method}: 405 (不支援)")
                    
            except Exception as e:
                print(f"❌ {method}: 錯誤 - {str(e)}")
        
        self.supported_methods = supported
        print(f"\n📋 支援的方法: {', '.join(supported) if supported else '無'}")
        return supported
    
    def run_comprehensive_tests(self):
        """執行全面性測試"""
        print(f"\n🎯 開始針對 {self.full_url} 的全面測試")
        print("=" * 80)
        
        # 1. 檢測支援的方法
        self.detect_supported_methods()
        
        if not self.supported_methods:
            print("❌ 無法檢測到任何支援的HTTP方法，停止測試")
            return
        
        # 2. 對每個支援的方法執行各種測試場景
        for method in self.supported_methods:
            self._test_method_scenarios(method)
        
        # 3. 生成總結報告
        self._print_comprehensive_summary()
    
    def _test_method_scenarios(self, method: str):
        """對特定HTTP方法執行各種測試場景"""
        print(f"\n🧪 測試 {method} 方法的各種場景")
        print("-" * 50)
        
        scenarios = [
            ("✅ 正常值測試", self._test_normal_case),
            ("❌ 缺少欄位測試", self._test_missing_fields),
            ("🌀 格式錯誤測試", self._test_format_errors),
            ("🧪 邊界值測試", self._test_boundary_values),
            ("🚫 不存在資源測試", self._test_nonexistent_resource)
        ]
        
        for scenario_name, test_func in scenarios:
            print(f"\n{scenario_name}")
            test_func(method)
    
    def _test_normal_case(self, method: str):
        """正常值測試"""
        normal_data = {
            "name": "測試用戶",
            "email": "test@example.com",
            "age": 25,
            "active": True,
            "tags": ["測試", "用戶"]
        }
        
        if method in ['GET', 'DELETE', 'HEAD', 'OPTIONS']:
            self._execute_test(method, None, "正常參數")
        else:
            self._execute_test(method, normal_data, "正常資料")
    
    def _test_missing_fields(self, method: str):
        """缺少欄位測試"""
        if method in ['GET', 'DELETE', 'HEAD', 'OPTIONS']:
            return
        
        incomplete_data_sets = [
            {},  # 完全空的資料
            {"name": "測試用戶"},  # 只有部分欄位
            {"email": "test@example.com"}  # 不同的部分欄位
        ]
        
        for i, data in enumerate(incomplete_data_sets, 1):
            self._execute_test(method, data, f"缺少欄位 #{i}")
    
    def _test_format_errors(self, method: str):
        """格式錯誤測試"""
        if method in ['GET', 'DELETE', 'HEAD', 'OPTIONS']:
            return
        
        invalid_data_sets = [
            {"name": 123, "email": "invalid-email", "age": "not-a-number"},  # 錯誤資料型別
            {"name": "", "email": "", "age": -1},  # 無效值
            {"name": None, "email": None, "age": None},  # null 值
            "invalid json string",  # 無效的JSON字串
        ]
        
        for i, data in enumerate(invalid_data_sets, 1):
            self._execute_test(method, data, f"格式錯誤 #{i}")
    
    def _test_boundary_values(self, method: str):
        """邊界值測試"""
        if method in ['GET', 'DELETE', 'HEAD', 'OPTIONS']:
            return
        
        boundary_data_sets = [
            {"name": "x" * 1000, "age": 999999},  # 極大值
            {"name": "", "age": 0},  # 極小值/空值
            {"name": "A", "age": 1},  # 最小正值
            {"name": "🚀🎯❌✅", "age": -999999},  # 特殊字符和負值
        ]
        
        for i, data in enumerate(boundary_data_sets, 1):
            self._execute_test(method, data, f"邊界值 #{i}")
    
    def _test_nonexistent_resource(self, method: str):
        """不存在資源測試"""
        # 測試不存在的ID
        nonexistent_endpoints = [
            f"{self.endpoint}/99999",
            f"{self.endpoint}/nonexistent-id",
            f"{self.endpoint}/00000000-0000-0000-0000-000000000000"
        ]
        
        for endpoint in nonexistent_endpoints:
            url = f"{self.base_url}{endpoint}"
            self._execute_single_request(method, url, None, f"不存在資源: {endpoint}")
    
    def _execute_test(self, method: str, data: Any, description: str):
        """執行單一測試"""
        self._execute_single_request(method, self.full_url, data, description)
    
    def _execute_single_request(self, method: str, url: str, data: Any, description: str):
        """執行單一請求"""
        start_time = time.time()
        result = {
            'method': method,
            'url': url,
            'description': description,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'success': False,
            'status_code': None,
            'response_time': 0,
            'response_data': None,
            'error': None,
            'request_data': data
        }
        
        try:
            # 處理特殊情況（字串而非字典）
            json_data = None
            if isinstance(data, dict):
                json_data = data
            elif isinstance(data, str):
                # 嘗試解析字串為JSON
                try:
                    json_data = json.loads(data)
                except:
                    # 如果無法解析，發送原始字串
                    pass
            
            response = requests.request(
                method=method.upper(),
                url=url,
                json=json_data if json_data else None,
                data=data if isinstance(data, str) and not json_data else None,
                headers=self.headers,
                timeout=self.timeout
            )
            
            response_time = time.time() - start_time
            result['response_time'] = round(response_time, 3)
            result['status_code'] = response.status_code
            
            # 處理回應內容
            try:
                result['response_data'] = response.json()
            except json.JSONDecodeError:
                result['response_data'] = response.text[:200] + "..." if len(response.text) > 200 else response.text
            
            # 判斷成功與否
            result['success'] = 200 <= response.status_code < 300
            
            # 輸出結果
            status_emoji = "✅" if result['success'] else "❌"
            print(f"  {status_emoji} {description}: {result['status_code']} ({result['response_time']}s)")
            
        except Exception as e:
            result['error'] = str(e)
            print(f"  ❌ {description}: 錯誤 - {str(e)}")
        
        self.test_results.append(result)
    
    def _print_comprehensive_summary(self):
        """列印全面測試摘要"""
        if not self.test_results:
            return
        
        print("\n" + "=" * 80)
        print("📊 全面測試摘要報告")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        successful_tests = sum(1 for r in self.test_results if r['success'])
        failed_tests = total_tests - successful_tests
        
        print(f"🎯 測試目標: {self.full_url}")
        print(f"📋 支援方法: {', '.join(self.supported_methods)}")
        print(f"📊 總測試數: {total_tests}")
        print(f"✅ 成功測試: {successful_tests}")
        print(f"❌ 失敗測試: {failed_tests}")
        print(f"📈 整體成功率: {(successful_tests/total_tests*100):.1f}%")
        
        # 按方法分組統計
        method_stats = {}
        for result in self.test_results:
            method = result['method']
            if method not in method_stats:
                method_stats[method] = {'total': 0, 'success': 0}
            method_stats[method]['total'] += 1
            if result['success']:
                method_stats[method]['success'] += 1
        
        print(f"\n📋 各HTTP方法測試結果:")
        for method, stats in method_stats.items():
            success_rate = (stats['success'] / stats['total'] * 100) if stats['total'] > 0 else 0
            status = "✅" if success_rate >= 80 else "⚠️" if success_rate >= 50 else "❌"
            print(f"   {status} {method}: {stats['success']}/{stats['total']} ({success_rate:.1f}%)")
        
        # 測試場景統計
        scenario_stats = {}
        for result in self.test_results:
            scenario = result['description'].split(':')[0] if ':' in result['description'] else result['description']
            if scenario not in scenario_stats:
                scenario_stats[scenario] = {'total': 0, 'success': 0}
            scenario_stats[scenario]['total'] += 1
            if result['success']:
                scenario_stats[scenario]['success'] += 1
        
        print(f"\n🧪 各測試場景結果:")
        for scenario, stats in scenario_stats.items():
            success_rate = (stats['success'] / stats['total'] * 100) if stats['total'] > 0 else 0
            status = "✅" if success_rate >= 80 else "⚠️" if success_rate >= 50 else "❌"
            print(f"   {status} {scenario}: {stats['success']}/{stats['total']} ({success_rate:.1f}%)")
        
        # 顯示關鍵問題
        print(f"\n🚨 關鍵發現:")
        
        # 檢查是否有405錯誤（方法不支援）
        method_errors = [r for r in self.test_results if r['status_code'] == 405]
        if method_errors:
            print(f"   ⚠️ 檢測到不支援的HTTP方法")
        
        # 檢查是否有400錯誤（請求格式問題）
        format_errors = [r for r in self.test_results if r['status_code'] == 400]
        if format_errors:
            print(f"   ⚠️ 檢測到請求格式問題 ({len(format_errors)} 個)")
        
        # 檢查是否有404錯誤（資源不存在）
        not_found_errors = [r for r in self.test_results if r['status_code'] == 404]
        if not_found_errors:
            print(f"   ✅ 不存在資源測試正常 ({len(not_found_errors)} 個404回應)")
        
        # 檢查是否有500錯誤（伺服器錯誤）
        server_errors = [r for r in self.test_results if r['status_code'] and r['status_code'] >= 500]
        if server_errors:
            print(f"   🚨 檢測到伺服器錯誤 ({len(server_errors)} 個)")
        
        # 效能分析
        valid_times = [r['response_time'] for r in self.test_results if r['response_time'] > 0]
        if valid_times:
            avg_time = sum(valid_times) / len(valid_times)
            max_time = max(valid_times)
            min_time = min(valid_times)
            print(f"\n⚡ 效能分析:")
            print(f"   平均回應時間: {avg_time:.3f}秒")
            print(f"   最快回應時間: {min_time:.3f}秒")
            print(f"   最慢回應時間: {max_time:.3f}秒")
    
    def generate_detailed_report(self, output_file: str = None):
        """生成詳細的測試報告"""
        if not output_file:
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            output_file = f"smart_api_test_report_{timestamp}.json"
        
        report = {
            'test_info': {
                'target_url': self.full_url,
                'supported_methods': self.supported_methods,
                'test_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'total_tests': len(self.test_results)
            },
            'summary': {
                'total_tests': len(self.test_results),
                'successful_tests': sum(1 for r in self.test_results if r['success']),
                'failed_tests': sum(1 for r in self.test_results if not r['success']),
                'success_rate': (sum(1 for r in self.test_results if r['success']) / len(self.test_results) * 100) if self.test_results else 0
            },
            'detailed_results': self.test_results
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 詳細測試報告已儲存至: {output_file}")
        return output_file

def main() -> None:
    """命令列介面入口"""
    parser = argparse.ArgumentParser(description="智能 API 測試器")
    parser.add_argument("base_url", help="API 基礎 URL，如 http://localhost:8000")
    parser.add_argument("endpoint", help="API 端點，如 /api/list_contracts")
    parser.add_argument("--timeout", type=int, default=10, help="請求逾時秒數")
    parser.add_argument("--html-report", action="store_true", help="輸出 HTML 報告")
    args = parser.parse_args()

    tester = SmartApiTester(args.base_url, args.endpoint, timeout=args.timeout)
    tester.run_comprehensive_tests()

    report_file = tester.generate_detailed_report()

    if args.html_report:
        with open(report_file, "r", encoding="utf-8") as f:
            report_data = json.load(f)
        generator = ReportGenerator(report_data["detailed_results"])
        html_file = report_file.replace(".json", ".html")
        generator.generate_html_report(html_file)
        print(f"📄 HTML報告已生成: {html_file}")

if __name__ == "__main__":
    main() 
