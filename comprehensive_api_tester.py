#!/usr/bin/env python3
"""
綜合API測試工具 - 支援自動檢測HTTP方法和多場景測試
"""

import argparse
import json
import sys
import asyncio
from smart_api_tester import SmartApiTester
from batch_tester import BatchTester
from report_generator import ReportGenerator
from concurrent_api_tester import ConcurrentApiTester

def print_banner():
    """列印工具橫幅"""
    banner = """
🚀 綜合API測試工具 v2.0
================================================================================
功能特色:
✅ 自動檢測API支援的HTTP方法 (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS)
❌ 缺少欄位測試 - 檢測必要欄位驗證
🌀 格式錯誤測試 - 驗證資料型別檢查
🧪 邊界值測試 - 測試極值和特殊情況
🚫 不存在資源測試 - 驗證404錯誤處理
📊 詳細測試報告生成 (JSON + HTML)
================================================================================
"""
    print(banner)

def run_smart_test(args):
    """執行智能單一API測試"""
    print(f"🎯 智能測試模式: {args.base_url}{args.endpoint}")
    
    tester = SmartApiTester(
        base_url=args.base_url,
        endpoint=args.endpoint,
        timeout=args.timeout
    )
    
    # 執行全面測試
    tester.run_comprehensive_tests()
    
    # 生成報告
    report_file = tester.generate_detailed_report()
    
    # 如果需要生成HTML報告
    if args.html_report:
        try:
            # 讀取JSON報告
            with open(report_file, 'r', encoding='utf-8') as f:
                report_data = json.load(f)
            
            # 直接使用詳細測試結果，ReportGenerator期望的是結果列表
            test_results = report_data['detailed_results']
            
            generator = ReportGenerator(test_results)
            html_file = report_file.replace('.json', '.html')
            generator.generate_html_report(html_file)
            print(f"📄 HTML報告已生成: {html_file}")
            
        except Exception as e:
            print(f"⚠️ HTML報告生成失敗: {e}")

def run_batch_test(args):
    """執行批次測試"""
    print(f"📋 批次測試模式: {args.config_file}")
    
    try:
        tester = BatchTester(args.config_file, max_workers=args.concurrency)
        tester.run_batch_tests()
        
        # 生成JSON報告
        report_file = args.output or "batch_test_report.json"
        tester.generate_report(report_file)
        
        # 生成HTML報告
        if args.html_report:
            try:
                with open(report_file, 'r', encoding='utf-8') as f:
                    report_data = json.load(f)
                
                # 對於批次測試，使用results欄位
                test_results = report_data.get('results', [])
                
                generator = ReportGenerator(test_results)
                html_file = report_file.replace('.json', '.html')
                generator.generate_html_report(html_file)
                print(f"📄 HTML報告已生成: {html_file}")
                
            except Exception as e:
                print(f"⚠️ HTML報告生成失敗: {e}")
                
    except Exception as e:
        print(f"❌ 批次測試失敗: {e}")
        sys.exit(1)

def run_stress_test(args):
    """執行壓力測試"""
    print(f"🚀 壓力測試模式: {args.base_url}{args.endpoint}")

    tester = ConcurrentApiTester(
        base_url=args.base_url,
        endpoint=args.endpoint,
        method=args.method,
        num_requests=args.requests,
        concurrency=args.concurrency,
        timeout=args.timeout,
    )

    asyncio.run(tester.run_tests())

    report_file = args.output or "stress_test_report.json"
    tester.generate_report(report_file)

    if args.html_report:
        html_file = report_file.replace('.json', '.html')
        tester.generate_html_report(report_file, html_file)
        print(f"📄 HTML報告已生成: {html_file}")

def create_sample_configs():
    """創建範例配置檔案"""
    # 智能測試配置
    smart_config = {
        "test_configs": [
            {
                "name": "📋 合約API完整測試",
                "base_url": "http://localhost:8000",
                "endpoint": "/api/list_contracts",
                "test_scenarios": {
                    "auto_detect_methods": True,
                    "normal_value_tests": True,
                    "missing_field_tests": True,
                    "format_error_tests": True,
                    "boundary_value_tests": True,
                    "nonexistent_resource_tests": True
                }
            }
        ],
        "global_settings": {
            "timeout": 30,
            "headers": {
                "Content-Type": "application/json"
            }
        }
    }
    
    # 基本批次測試配置
    batch_config = {
        "base_url": "http://localhost:8000",
        "timeout": 10,
        "headers": {
            "Content-Type": "application/json"
        },
        "tests": [
            {
                "name": "✅ GET 合約列表",
                "endpoint": "/api/list_contracts",
                "method": "GET"
            },
            {
                "name": "❌ POST 測試 (應該失敗)",
                "endpoint": "/api/list_contracts",
                "method": "POST",
                "data": {"test": "data"}
            },
            {
                "name": "🚫 不存在路徑測試",
                "endpoint": "/api/nonexistent",
                "method": "GET"
            }
        ]
    }
    
    # 儲存配置檔案
    with open('smart_test_config.json', 'w', encoding='utf-8') as f:
        json.dump(smart_config, f, indent=2, ensure_ascii=False)
    
    with open('basic_batch_config.json', 'w', encoding='utf-8') as f:
        json.dump(batch_config, f, indent=2, ensure_ascii=False)
    
    print("📝 範例配置檔案已建立:")
    print("   • smart_test_config.json - 智能測試配置")
    print("   • basic_batch_config.json - 基本批次測試配置")

def main():
    """主程式入口"""
    parser = argparse.ArgumentParser(
        description='綜合API測試工具 - 支援自動檢測HTTP方法和多場景測試',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用範例:
  # 智能單一API測試
  python comprehensive_api_tester.py smart http://localhost:8000 /api/list_contracts
  
  # 批次測試
  python comprehensive_api_tester.py batch tests.json
  
  # 生成範例配置檔案
  python comprehensive_api_tester.py create-samples

  # 帶HTML報告的測試
  python comprehensive_api_tester.py smart http://localhost:8000 /api/users --html-report

  # 壓力測試
  python comprehensive_api_tester.py stress http://localhost:8000 /api/list_contracts --requests 500 --concurrency 50
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用指令')
    
    # 智能測試指令
    smart_parser = subparsers.add_parser('smart', help='智能單一API測試')
    smart_parser.add_argument('base_url', help='API基礎URL (例: http://localhost:8000)')
    smart_parser.add_argument('endpoint', help='API端點 (例: /api/list_contracts)')
    smart_parser.add_argument('--timeout', type=int, default=30, help='請求逾時時間 (預設: 30秒)')
    smart_parser.add_argument('--html-report', action='store_true', help='生成HTML報告')
    
    # 批次測試指令
    batch_parser = subparsers.add_parser('batch', help='批次配置檔案測試')
    batch_parser.add_argument('config_file', help='測試配置檔案 (JSON/YAML)')
    batch_parser.add_argument('--output', help='輸出報告檔案名稱')
    batch_parser.add_argument('--html-report', action='store_true', help='生成HTML報告')

    # 壓力測試指令
    stress_parser = subparsers.add_parser('stress', help='並發壓力測試')
    stress_parser.add_argument('base_url', help='API基礎URL (例: http://localhost:8000)')
    stress_parser.add_argument('endpoint', help='API端點 (例: /api/list_contracts)')
    stress_parser.add_argument('--method', default='GET', help='HTTP 方法 (預設: GET)')
    stress_parser.add_argument('--requests', type=int, default=100, help='總請求數 (預設: 100)')
    stress_parser.add_argument('--concurrency', type=int, default=10, help='同時並發數 (預設: 10)')
    stress_parser.add_argument('--timeout', type=int, default=10, help='逾時秒數 (預設: 10)')
    stress_parser.add_argument('--output', help='輸出報告檔案名稱')
    stress_parser.add_argument('--html-report', action='store_true', help='生成HTML報告')
    
    # 建立範例檔案指令
    samples_parser = subparsers.add_parser('create-samples', help='建立範例配置檔案')
    
    args = parser.parse_args()
    
    # 顯示橫幅
    print_banner()
    
    if not args.command:
        parser.print_help()
        return
    
    # 執行對應指令
    if args.command == 'smart':
        run_smart_test(args)
    elif args.command == 'batch':
        run_batch_test(args)
    elif args.command == 'stress':
        run_stress_test(args)
    elif args.command == 'create-samples':
        create_sample_configs()
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 