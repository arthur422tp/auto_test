import argparse
from api_tester import ApiTester

def main():
    parser = argparse.ArgumentParser(description="自動 API Debug 工具")
    parser.add_argument("--port", type=int, required=True, help="API 伺服器 port")
    parser.add_argument("--route", type=str, required=True, help="API 路由")
    parser.add_argument("--method", type=str, choices=["GET", "POST"], help="HTTP 方法")
    parser.add_argument("--data", type=str, help="POST 測試資料（JSON 格式）")
    args = parser.parse_args()

    url = f"http://localhost:{args.port}{args.route}"
    tester = ApiTester(url)
    tester.run_tests(method=args.method, data=args.data)

if __name__ == "__main__":
    main() 