#!/usr/bin/env python
"""
自動 API 測試示例腳本
展示如何使用 API 端口檢測功能自動測試 API
"""

from port_detector import ApiPortDetector

def main():
    print("API 自動測試示例")
    print("=" * 50)
    
    # 創建 API 端口檢測器，指定端口範圍
    detector = ApiPortDetector(
        host="localhost",
        port_range=(8000, 9000)
    )
    
    # 方法 1: 自動檢測所有端口和端點並測試
    print("\n方法 1: 自動檢測所有端口和端點")
    print("-" * 50)
    results = detector.auto_detect_and_test()
    
    if not results:
        print("未檢測到任何活動的 API 端口或端點")
    else:
        for port, result in results.items():
            summary = result["summary"]
            print(f"\n端口 {port} 測試結果:")
            print(f"  總測試數: {summary['total_tests']}")
            print(f"  通過測試數: {summary['passed_tests']}")
            print(f"  失敗測試數: {summary['failed_tests']}")
            print(f"  成功率: {summary['success_rate'] * 100:.2f}%")
    
    # 方法 2: 手動指定端口，自動檢測端點
    print("\n方法 2: 手動指定端口，自動檢測端點")
    print("-" * 50)
    port = 8000  # 假設我們知道 API 運行在端口 8000
    
    # 檢測端點
    endpoints = detector.detect_api_endpoints(port)
    
    if not endpoints:
        print(f"在端口 {port} 上未檢測到 API 端點")
    else:
        print(f"在端口 {port} 上檢測到 {len(endpoints)} 個端點:")
        for endpoint, methods in endpoints.items():
            print(f"  {endpoint}: {', '.join(methods)}")
        
        # 為檢測到的端點生成測試用例
        endpoint_data = {}
        for endpoint, methods in endpoints.items():
            endpoint_data[endpoint] = {
                "methods": methods,
                "data_templates": {}
            }
        
        test_cases = detector.generate_test_cases(port, endpoint_data)
        print(f"\n生成了 {len(test_cases)} 個測試用例")
        
        # 運行測試
        summary = detector.run_tests(port, test_cases)
        print("\n測試結果:")
        print(f"  總測試數: {summary['total_tests']}")
        print(f"  通過測試數: {summary['passed_tests']}")
        print(f"  失敗測試數: {summary['failed_tests']}")
        print(f"  成功率: {summary['success_rate'] * 100:.2f}%")
    
    # 方法 3: 從日誌文件分析端點和輸入
    print("\n方法 3: 從日誌文件分析端點和輸入")
    print("-" * 50)
    log_endpoints = detector.analyze_log_for_endpoints("api_debug.log")
    
    if not log_endpoints:
        print("日誌文件中未找到 API 端點信息")
    else:
        print(f"從日誌文件中分析出 {len(log_endpoints)} 個端口的 API 信息:")
        for port, endpoints in log_endpoints.items():
            print(f"\n端口 {port}:")
            for endpoint, data in endpoints.items():
                methods = data.get("methods", [])
                print(f"  {endpoint}: {', '.join(methods)}")
                
                # 顯示數據模板
                for method, template in data.get("data_templates", {}).items():
                    print(f"    {method} 數據模板: {template}")
            
            # 為這個端口生成測試用例
            test_cases = detector.generate_test_cases(port, endpoints)
            print(f"\n為端口 {port} 生成了 {len(test_cases)} 個測試用例")
            
            # 可以選擇運行測試
            # summary = detector.run_tests(port, test_cases)
    
    print("\n自動測試完成！")
    print("請查看生成的 HTML 報告以獲取詳細測試結果。")

if __name__ == "__main__":
    main() 