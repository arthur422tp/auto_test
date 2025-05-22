#!/usr/bin/env python
"""
特定API路由測試腳本
讓使用者手動輸入特定的API路由進行自動化測試
"""

import sys
import json
from port_detector import ApiPortDetector
from api_debugger import ApiDebugger, logger

def main():
    print("特定API路由測試工具")
    print("=" * 50)
    
    # 獲取主機名
    host = input("請輸入 API 主機名 (默認為 localhost): ").strip()
    if not host:
        host = "localhost"
    
    # 獲取端口號
    while True:
        try:
            port_input = input("請輸入 API 端口: ").strip()
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
    
    # 獲取API路由
    while True:
        api_route = input("請輸入要測試的 API 路由 (例如 /api/search_contracts): ").strip()
        if not api_route:
            print("錯誤: 必須輸入 API 路由")
            continue
        
        # 確保路由以 / 開頭
        if not api_route.startswith('/'):
            api_route = '/' + api_route
            
        break
    
    # 獲取HTTP方法
    valid_methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]
    while True:
        method = input(f"請輸入 HTTP 方法 ({'/'.join(valid_methods)}, 默認為 GET): ").strip().upper()
        if not method:
            method = "GET"
            break
        
        if method in valid_methods:
            break
        else:
            print(f"錯誤: 不支持的 HTTP 方法，請輸入 {', '.join(valid_methods)} 之一")
    
    # 創建 API 端口檢測器
    detector = ApiPortDetector(host=host)
    
    # 檢查端口是否開放
    print(f"\n檢查端口 {port} 是否開放...")
    sock_check = detector.scan_ports()
    if port not in sock_check:
        print(f"警告: 端口 {port} 似乎未開放。仍將嘗試測試，但可能會失敗。")
    
    # 如果是需要請求體的方法，詢問是否需要輸入數據
    request_data = None
    if method in ["POST", "PUT", "PATCH"]:
        need_data = input("\n此 HTTP 方法通常需要請求數據。是否要提供數據? (y/n, 默認為 y): ").strip().lower()
        if need_data != "n":
            # 嘗試從日誌文件中獲取數據模板
            print("正在從日誌文件中查找數據模板...")
            log_endpoints = detector.analyze_log_for_endpoints()
            data_template = None
            
            for p, endpoints in log_endpoints.items():
                if p == port and api_route in endpoints:
                    if method in endpoints[api_route].get("data_templates", {}):
                        data_template = endpoints[api_route]["data_templates"][method]
                        print(f"找到數據模板: {json.dumps(data_template, ensure_ascii=False, indent=2)}")
                        break
            
            # 如果找到模板，詢問是否使用
            if data_template:
                use_template = input("是否使用此數據模板? (y/n, 默認為 y): ").strip().lower()
                if use_template != "n":
                    request_data = data_template
            
            # 如果沒有模板或不使用模板，嘗試智能生成
            if not request_data:
                print("正在智能生成數據...")
                request_data = detector.generate_smart_input_data(api_route, method)
                print(f"生成的數據: {json.dumps(request_data, ensure_ascii=False, indent=2)}")
                
                use_generated = input("是否使用此生成的數據? (y/n, 默認為 y): ").strip().lower()
                if use_generated == "n":
                    # 手動輸入JSON數據
                    print("請輸入JSON格式的請求數據 (輸入空行結束):")
                    lines = []
                    while True:
                        line = input()
                        if not line:
                            break
                        lines.append(line)
                    
                    if lines:
                        try:
                            request_data = json.loads("\n".join(lines))
                        except json.JSONDecodeError as e:
                            print(f"JSON解析錯誤: {e}")
                            print("將使用空數據")
                            request_data = {}
                    else:
                        request_data = {}
    
    # 詢問預期的狀態碼
    while True:
        try:
            expected_status_input = input("\n請輸入預期的 HTTP 狀態碼 (默認為 200): ").strip()
            if not expected_status_input:
                expected_status = 200
                break
            
            expected_status = int(expected_status_input)
            if expected_status < 100 or expected_status >= 600:
                print("錯誤: HTTP 狀態碼必須在 100-599 之間")
                continue
            
            break
        except ValueError:
            print("錯誤: 狀態碼必須是數字")
    
    # 創建測試用例
    test_case = {
        "endpoint": api_route,
        "method": method,
        "expected_status": expected_status,
        "test_name": f"{method} {api_route}",
        "description": f"測試 {method} {api_route} 端點"
    }
    
    if request_data is not None:
        test_case["data"] = request_data
    
    # 詢問是否要運行測試
    run_test = input("\n是否要運行測試? (y/n, 默認為 y): ").strip().lower()
    if run_test != "n":
        # 創建 API 調試器
        base_url = f"http://{host}:{port}"
        api_debugger = ApiDebugger(
            base_url=base_url,
            headers={"Content-Type": "application/json"}
        )
        
        # 運行測試
        print("\n開始運行測試...")
        result = api_debugger.test_endpoint(**test_case)
        
        # 顯示測試結果
        print("\n測試結果:")
        print(f"測試名稱: {result.get('test_name', '未命名測試')}")
        print(f"URL: {result.get('url', '')}")
        print(f"方法: {result.get('method', '')}")
        print(f"狀態碼: {result.get('status_code', '')} (預期: {result.get('expected_status', '')})")
        print(f"狀態匹配: {'是' if result.get('status_match', False) else '否'}")
        
        if "error" in result:
            print(f"錯誤: {result['error']}")
        else:
            print("\n請求數據:")
            print(json.dumps(result.get('request_data', {}), ensure_ascii=False, indent=2))
            
            print("\n響應數據:")
            if isinstance(result.get('response_data'), dict) or isinstance(result.get('response_data'), list):
                print(json.dumps(result.get('response_data', {}), ensure_ascii=False, indent=2))
            else:
                print(result.get('response_data', ''))
            
            if result.get('expected_response'):
                print("\n預期響應:")
                print(json.dumps(result.get('expected_response', {}), ensure_ascii=False, indent=2))
            
            print(f"\n測試結果: {'成功' if result.get('success', False) else '失敗'}")
        
        # 詢問是否要進行更多測試
        more_tests = input("\n是否要對同一端點進行更多測試? (y/n, 默認為 n): ").strip().lower()
        if more_tests == "y":
            # 創建一個無效輸入的測試
            if method in ["POST", "PUT", "PATCH"] and request_data:
                print("\n正在生成無效輸入測試...")
                invalid_data = {}
                if request_data:
                    # 只取原始數據的第一個字段
                    for key in list(request_data.keys())[:1]:
                        invalid_data[key] = request_data[key]
                
                invalid_test_case = {
                    "endpoint": api_route,
                    "method": method,
                    "data": invalid_data,
                    "expected_status": 400,
                    "test_name": f"{method} {api_route} (無效輸入)",
                    "description": f"測試使用無效輸入的 {method} {api_route}"
                }
                
                print(f"無效輸入測試數據: {json.dumps(invalid_data, ensure_ascii=False, indent=2)}")
                run_invalid = input("是否要運行無效輸入測試? (y/n, 默認為 y): ").strip().lower()
                
                if run_invalid != "n":
                    print("\n開始運行無效輸入測試...")
                    invalid_result = api_debugger.test_endpoint(**invalid_test_case)
                    
                    # 顯示測試結果
                    print("\n無效輸入測試結果:")
                    print(f"測試名稱: {invalid_result.get('test_name', '未命名測試')}")
                    print(f"狀態碼: {invalid_result.get('status_code', '')} (預期: {invalid_result.get('expected_status', '')})")
                    print(f"狀態匹配: {'是' if invalid_result.get('status_match', False) else '否'}")
                    print(f"測試結果: {'成功' if invalid_result.get('success', False) else '失敗'}")
    else:
        print("測試已取消")
    
    print("\n特定 API 路由測試完成！")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n測試已中斷")
        sys.exit(0) 