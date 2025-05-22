import argparse
from port_detector import ApiPortDetector

def main():
    """
    API 調試工具主程序
    自動檢測 API 端口並進行測試
    """
    parser = argparse.ArgumentParser(description="API 調試工具 - 自動檢測端口和輸入")
    parser.add_argument("--host", default="localhost", help="API 主機名，默認為 localhost")
    parser.add_argument("--port-min", type=int, default=8000, help="端口掃描範圍最小值，默認為 8000")
    parser.add_argument("--port-max", type=int, default=9000, help="端口掃描範圍最大值，默認為 9000")
    parser.add_argument("--log-file", default="api_debug.log", help="日誌文件路徑，默認為 api_debug.log")
    
    args = parser.parse_args()
    
    print(f"API 調試工具啟動中...")
    print(f"主機: {args.host}")
    print(f"端口範圍: {args.port_min}-{args.port_max}")
    print(f"日誌文件: {args.log_file}")
    
    # 創建 API 端口檢測器
    detector = ApiPortDetector(
        host=args.host,
        port_range=(args.port_min, args.port_max)
    )
    
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
