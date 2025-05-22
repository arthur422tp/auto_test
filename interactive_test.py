#!/usr/bin/env python
"""
互動式 API 測試腳本
讓用戶輸入 API 端口並進行自動測試
"""

import sys
from port_detector import ApiPortDetector

def main():
    print("API 互動式測試工具")
    print("=" * 50)
    
    # 獲取主機名
    host = input("請輸入 API 主機名 (默認為 localhost): ").strip()
    if not host:
        host = "localhost"
    
    # 獲取端口號
    while True:
        try:
            port_input = input("請輸入要測試的 API 端口: ").strip()
            if not port_input:
                print("錯誤: 必須輸入端口號")
                continue
            
            port = int(port_input)
            if port < 1 or port > 65535:
                print("錯誤: 端口號必須在 1-65535 之間")
                continue
            
            break
        except ValueError:
            print("錯誤: 端口號必須是數字")
    
    # 創建 API 端口檢測器
    detector = ApiPortDetector(host=host)
    
    # 檢測端點
    print(f"\n正在檢測端口 {port} 上的 API 端點...")
    endpoints = detector.detect_api_endpoints(port)
    
    if not endpoints:
        print(f"在端口 {port} 上未檢測到 API 端點")
        return
    
    print(f"在端口 {port} 上檢測到 {len(endpoints)} 個端點:")
    for endpoint, methods in endpoints.items():
        print(f"  {endpoint}: {', '.join(methods)}")
    
    # 詢問是否要分析日誌文件
    use_log = input("\n是否要分析日誌文件以獲取更精確的 API 信息? (y/n, 默認為 y): ").strip().lower()
    if use_log != "n":
        log_file = input("請輸入日誌文件路徑 (默認為 api_debug.log): ").strip()
        if not log_file:
            log_file = "api_debug.log"
        
        print(f"正在分析日誌文件 {log_file}...")
        log_endpoints = detector.analyze_log_for_endpoints(log_file)
        port_endpoints = log_endpoints.get(port, {})
        
        if port_endpoints:
            print(f"在日誌文件中找到了端口 {port} 的 API 信息")
        else:
            print(f"在日誌文件中未找到端口 {port} 的 API 信息")
    else:
        port_endpoints = {}
    
    # 合併日誌中的端點信息和檢測到的端點信息
    endpoint_data = {}
    for endpoint, methods in endpoints.items():
        if endpoint in port_endpoints:
            # 如果日誌中有這個端點，使用日誌中的信息
            endpoint_data[endpoint] = port_endpoints[endpoint]
        else:
            # 否則使用檢測到的信息
            endpoint_data[endpoint] = {
                "methods": methods,
                "data_templates": {}
            }
    
    # 詢問是否要運行測試
    run_test = input("\n是否要運行測試? (y/n, 默認為 y): ").strip().lower()
    if run_test != "n":
        # 生成測試用例
        test_cases = detector.generate_test_cases(port, endpoint_data)
        print(f"生成了 {len(test_cases)} 個測試用例")
        
        # 運行測試
        print("\n開始運行測試...")
        summary = detector.run_tests(port, test_cases)
        
        # 顯示結果摘要
        print("\n測試結果摘要:")
        print(f"總測試數: {summary['total_tests']}")
        print(f"通過測試數: {summary['passed_tests']}")
        print(f"失敗測試數: {summary['failed_tests']}")
        print(f"成功率: {summary['success_rate'] * 100:.2f}%")
        print(f"報告文件: api_test_report_port_{port}.html")
    else:
        print("測試已取消")
    
    print("\n互動式測試完成！")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n測試已中斷")
        sys.exit(0) 