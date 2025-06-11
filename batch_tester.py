import json
import yaml
import os
import concurrent.futures
from typing import List, Dict, Any
from api_tester import ApiTester

class BatchTester:
    def __init__(self, config_file: str, max_workers: int = 1):
        self.config_file = config_file
        self.max_workers = max_workers
        self.config = self.load_config()
        self.all_results = []

    def load_config(self) -> Dict[str, Any]:
        """載入配置檔案"""
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"找不到配置檔案: {self.config_file}")
        
        _, ext = os.path.splitext(self.config_file)
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                if ext.lower() in ['.yaml', '.yml']:
                    return yaml.safe_load(f)
                elif ext.lower() == '.json':
                    return json.load(f)
                else:
                    raise ValueError(f"不支援的檔案格式: {ext}")
        except Exception as e:
            raise ValueError(f"無法解析配置檔案: {e}")

    def _execute_test_case(self, index: int, total: int, test_case: Dict[str, Any]) -> List[Dict[str, Any]]:
        """在執行緒中執行單一測試案例"""
        print(f"🧪 執行測試案例 {index}/{total}: {test_case.get('name', f'Test {index}')}")
        print("-" * 40)

        # 建構 URL
        base_url = test_case.get('base_url', self.config.get('base_url', 'http://localhost'))
        endpoint = test_case.get('endpoint', '/')
        url = f"{base_url.rstrip('/')}{endpoint}"

        tester = ApiTester(
            url=url,
            timeout=test_case.get('timeout', self.config.get('timeout', 10)),
            headers=test_case.get('headers', self.config.get('headers', {}))
        )

        method = test_case.get('method')
        data = test_case.get('data')

        tester.run_tests(method=method, data=json.dumps(data) if data else None)

        test_results = tester.get_results()
        for result in test_results:
            result['test_case_name'] = test_case.get('name', f'Test {index}')
            result['test_case_index'] = index

        print()
        return test_results

    def run_batch_tests(self):
        """執行批次測試"""
        print("🚀 批次 API 測試工具")
        print("=" * 60)
        
        # 取得測試案例
        test_cases = self.config.get('tests', [])
        if not test_cases:
            print("❌ 配置檔案中沒有找到測試案例")
            return
        
        print(f"📋 找到 {len(test_cases)} 個測試案例")
        print()
        
        total_cases = len(test_cases)

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [
                executor.submit(self._execute_test_case, i, total_cases, tc)
                for i, tc in enumerate(test_cases, 1)
            ]

            for future in concurrent.futures.as_completed(futures):
                self.all_results.extend(future.result())

        print()
        
        # 顯示總體摘要
        self.print_overall_summary()

    def print_overall_summary(self):
        """顯示總體測試摘要"""
        if not self.all_results:
            return
        
        print("=" * 60)
        print("📊 總體測試摘要")
        print("=" * 60)
        
        total_tests = len(self.all_results)
        successful_tests = sum(1 for r in self.all_results if r['success'])
        failed_tests = total_tests - successful_tests
        
        print(f"總測試數: {total_tests}")
        print(f"✅ 成功: {successful_tests}")
        print(f"❌ 失敗: {failed_tests}")
        print(f"📈 整體成功率: {(successful_tests/total_tests*100):.1f}%")
        
        # 按測試案例分組顯示
        test_cases = {}
        for result in self.all_results:
            case_name = result.get('test_case_name', 'Unknown')
            if case_name not in test_cases:
                test_cases[case_name] = {'total': 0, 'success': 0}
            test_cases[case_name]['total'] += 1
            if result['success']:
                test_cases[case_name]['success'] += 1
        
        print("\n📋 各測試案例結果:")
        for case_name, stats in test_cases.items():
            success_rate = (stats['success'] / stats['total'] * 100) if stats['total'] > 0 else 0
            status = "✅" if success_rate == 100 else "⚠️" if success_rate > 0 else "❌"
            print(f"   {status} {case_name}: {stats['success']}/{stats['total']} ({success_rate:.1f}%)")
        
        # 顯示失敗的測試
        if failed_tests > 0:
            print(f"\n❌ 失敗的測試詳情:")
            for result in self.all_results:
                if not result['success']:
                    error_msg = result['error'] or f"HTTP {result['status_code']}"
                    print(f"   • {result['test_case_name']} - {result['method']}: {error_msg}")

    def generate_report(self, output_file: str = None):
        """生成測試報告"""
        if not output_file:
            output_file = "test_report.json"
        
        report = {
            'summary': {
                'total_tests': len(self.all_results),
                'successful_tests': sum(1 for r in self.all_results if r['success']),
                'failed_tests': sum(1 for r in self.all_results if not r['success']),
                'success_rate': (sum(1 for r in self.all_results if r['success']) / len(self.all_results) * 100) if self.all_results else 0
            },
            'results': self.all_results
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📄 測試報告已儲存至: {output_file}")

def create_sample_config():
    """建立範例配置檔案"""
    sample_config = {
        "base_url": "http://localhost:5001",
        "timeout": 10,
        "headers": {
            "Content-Type": "application/json"
        },
        "tests": [
            {
                "name": "測試 GET 端點",
                "endpoint": "/api/test",
                "method": "GET"
            },
            {
                "name": "測試 POST 建立使用者",
                "endpoint": "/api/users",
                "method": "POST",
                "data": {
                    "name": "測試使用者",
                    "email": "test@example.com"
                }
            },
            {
                "name": "測試認證端點",
                "endpoint": "/api/protected",
                "method": "GET",
                "headers": {
                    "Authorization": "Bearer your-token-here"
                }
            }
        ]
    }
    
    with open('sample_config.json', 'w', encoding='utf-8') as f:
        json.dump(sample_config, f, indent=2, ensure_ascii=False)
    
    print("📝 範例配置檔案已建立: sample_config.json")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python batch_tester.py <config_file> [--create-sample]")
        print("範例: python batch_tester.py tests.json")
        print("建立範例配置: python batch_tester.py --create-sample")
        sys.exit(1)
    
    if sys.argv[1] == "--create-sample":
        create_sample_config()
        sys.exit(0)
    
    config_file = sys.argv[1]
    
    try:
        tester = BatchTester(config_file)
        tester.run_batch_tests()
        tester.generate_report()
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        sys.exit(1) 