import argparse
from port_detector import ApiPortDetector
from api_debugger import ApiDebugger

def main():
    """
    API 調試工具主程序
    自動檢測 API 端口並進行測試
    """
    parser = argparse.ArgumentParser(description="API 調試工具 - 自動檢測端口和輸入")
    parser.add_argument("--host", default="localhost", help="API 主機名，默認為 localhost")
    parser.add_argument("--port", type=int, help="指定要測試的API端口，如果提供則不進行端口掃描")
    parser.add_argument("--route", help="指定要測試的API路由路徑，例如 /api/search_contracts")
    parser.add_argument("--method", default="GET", choices=["GET", "POST", "PUT", "DELETE", "PATCH"], help="HTTP方法，默認為 GET")
    parser.add_argument("--port-min", type=int, default=8000, help="端口掃描範圍最小值，默認為 8000")
    parser.add_argument("--port-max", type=int, default=9000, help="端口掃描範圍最大值，默認為 9000")
    parser.add_argument("--log-file", default="api_debug.log", help="日誌文件路徑，默認為 api_debug.log")
    parser.add_argument("--data", help="JSON格式的請求數據，用於POST/PUT/PATCH請求")
    parser.add_argument("--expected-status", type=int, default=200, help="預期的HTTP狀態碼，默認為 200")
    
    args = parser.parse_args()
    
    print(f"API 調試工具啟動中...")
    print(f"主機: {args.host}")
    
    # 創建 API 端口檢測器
    detector = ApiPortDetector(
        host=args.host,
        port_range=(args.port_min, args.port_max)
    )
    
    # 檢查是否同時指定了端口和路由
    if args.port and args.route:
        print(f"正在測試特定的API路由: {args.route} on port {args.port}")
        
        # 創建 API 調試器
        base_url = f"http://{args.host}:{args.port}"
        api_debugger = ApiDebugger(
            base_url=base_url,
            headers={"Content-Type": "application/json"}
        )
        
        # 創建測試用例
        test_case = {
            "endpoint": args.route,
            "method": args.method,
            "expected_status": args.expected_status,
            "test_name": f"{args.method} {args.route}",
            "description": f"測試 {args.method} {args.route} 端點"
        }
        
        # 如果提供了數據，嘗試解析JSON
        if args.data and args.method in ["POST", "PUT", "PATCH"]:
            import json
            try:
                test_case["data"] = json.loads(args.data)
            except json.JSONDecodeError as e:
                print(f"警告: 無法解析JSON數據: {e}")
                print("將嘗試智能生成數據...")
                test_case["data"] = detector.generate_smart_input_data(args.route, args.method)
                print(f"生成的數據: {json.dumps(test_case['data'], ensure_ascii=False, indent=2)}")
        elif args.method in ["POST", "PUT", "PATCH"]:
            # 如果是需要數據的方法但未提供數據，嘗試從日誌中獲取或智能生成
            print(f"未提供數據，嘗試從日誌文件中獲取或智能生成...")
            
            # 從日誌中獲取
            log_endpoints = detector.analyze_log_for_endpoints(args.log_file)
            data_found = False
            
            for port, endpoints in log_endpoints.items():
                if port == args.port and args.route in endpoints:
                    if args.method in endpoints[args.route].get("data_templates", {}):
                        test_case["data"] = endpoints[args.route]["data_templates"][args.method]
                        print(f"從日誌中獲取到數據: {json.dumps(test_case['data'], ensure_ascii=False, indent=2)}")
                        data_found = True
                        break
            
            # 如果日誌中沒有，智能生成
            if not data_found:
                test_case["data"] = detector.generate_smart_input_data(args.route, args.method)
                print(f"智能生成的數據: {json.dumps(test_case['data'], ensure_ascii=False, indent=2)}")
        
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
            
            print(f"\n測試結果: {'成功' if result.get('success', False) else '失敗'}")
    
    # 檢查是否指定了特定端口
    elif args.port:
        print(f"正在測試指定的端口: {args.port}")
        
        # 檢測端點
        endpoints = detector.detect_api_endpoints(args.port)
        
        if not endpoints:
            print(f"在端口 {args.port} 上未檢測到 API 端點")
            return
        
        print(f"在端口 {args.port} 上檢測到 {len(endpoints)} 個端點")
        
        # 從日誌文件中分析端點信息
        log_endpoints = detector.analyze_log_for_endpoints(args.log_file)
        port_endpoints = log_endpoints.get(args.port, {})
        
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
        
        # 生成測試用例
        test_cases = detector.generate_test_cases(args.port, endpoint_data)
        print(f"生成了 {len(test_cases)} 個測試用例")
        
        # 運行測試
        summary = detector.run_tests(args.port, test_cases)
        
        # 顯示結果摘要
        print("\n測試結果摘要:")
        print(f"總測試數: {summary['total_tests']}")
        print(f"通過測試數: {summary['passed_tests']}")
        print(f"失敗測試數: {summary['failed_tests']}")
        print(f"成功率: {summary['success_rate'] * 100:.2f}%")
        print(f"報告文件: api_test_report_port_{args.port}.html")
    else:
        print(f"端口範圍: {args.port_min}-{args.port_max}")
        print(f"日誌文件: {args.log_file}")
        
        # 自動檢測端口並運行測試
        results = detector.auto_detect_and_test()
        
        # 顯示結果摘要
        if not results:
            print("未檢測到任何活動的 API 端口或端點")
        else:
            print("\n測試結果摘要:")
            for port, result in results.items():
                summary = result["summary"]
                print(f"\n端口 {port}:")
                print(f"  總測試數: {summary['total_tests']}")
                print(f"  通過測試數: {summary['passed_tests']}")
                print(f"  失敗測試數: {summary['failed_tests']}")
                print(f"  成功率: {summary['success_rate'] * 100:.2f}%")
                print(f"  報告文件: api_test_report_port_{port}.html")


if __name__ == "__main__":
    main()
