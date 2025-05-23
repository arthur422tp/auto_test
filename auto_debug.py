import argparse
import json
import sys
from api_tester import ApiTester

def parse_headers(headers_str):
    """解析 headers 字串"""
    if not headers_str:
        return {}
    try:
        return json.loads(headers_str)
    except json.JSONDecodeError:
        print(f"❌ 錯誤: 無法解析 headers JSON 格式")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="🚀 API 自動 Debug 工具 - 快速測試 API 端點",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例用法:
  基本測試:
    %(prog)s --port 5001 --route /api/test
    
  測試特定方法:
    %(prog)s --port 5001 --route /api/users --method POST --data '{"name":"test"}'
    
  包含認證:
    %(prog)s --port 5001 --route /api/protected --headers '{"Authorization":"Bearer token"}'
    
  設定逾時:
    %(prog)s --port 5001 --route /api/slow --timeout 30
        """
    )
    
    # 必要參數
    parser.add_argument("--port", type=int, required=True, 
                       help="API 伺服器 port")
    parser.add_argument("--route", type=str, required=True, 
                       help="API 路由路徑 (例: /api/users)")
    
    # 可選參數
    parser.add_argument("--method", type=str, 
                       choices=["GET", "POST", "PUT", "PATCH", "DELETE"], 
                       help="HTTP 方法 (預設: 自動測試 GET 和 POST)")
    parser.add_argument("--data", type=str, 
                       help="POST/PUT/PATCH 測試資料 (JSON 格式)")
    parser.add_argument("--headers", type=str, 
                       help="自訂 HTTP headers (JSON 格式)")
    parser.add_argument("--timeout", type=int, default=10, 
                       help="請求逾時秒數 (預設: 10)")
    parser.add_argument("--host", type=str, default="localhost", 
                       help="API 主機位址 (預設: localhost)")
    parser.add_argument("--protocol", type=str, default="http", 
                       choices=["http", "https"], 
                       help="協定 (預設: http)")
    
    # 快速認證選項
    parser.add_argument("--auth-bearer", type=str, 
                       help="Bearer token 認證")
    parser.add_argument("--auth-basic", type=str, 
                       help="Basic 認證 (格式: username:password)")
    
    # 輸出選項
    parser.add_argument("--verbose", "-v", action="store_true", 
                       help="詳細輸出模式")
    parser.add_argument("--quiet", "-q", action="store_true", 
                       help="安靜模式 (僅顯示結果)")
    
    args = parser.parse_args()
    
    # 驗證參數
    if args.quiet and args.verbose:
        print("❌ 錯誤: --quiet 和 --verbose 不能同時使用")
        sys.exit(1)
    
    # 建構 URL
    url = f"{args.protocol}://{args.host}:{args.port}{args.route}"
    
    # 處理 headers
    headers = parse_headers(args.headers)
    
    # 處理認證
    if args.auth_bearer:
        headers["Authorization"] = f"Bearer {args.auth_bearer}"
    elif args.auth_basic:
        import base64
        if ":" not in args.auth_basic:
            print("❌ 錯誤: Basic 認證格式應為 username:password")
            sys.exit(1)
        auth_str = base64.b64encode(args.auth_basic.encode()).decode()
        headers["Authorization"] = f"Basic {auth_str}"
    
    # 顯示開始資訊
    if not args.quiet:
        print("🚀 API 自動 Debug 工具")
        print("=" * 50)
        print(f"🌐 目標: {url}")
        print(f"⏱️  逾時: {args.timeout}秒")
        if headers:
            print(f"📋 Headers: {json.dumps(headers, indent=2, ensure_ascii=False)}")
        if args.method:
            print(f"🎯 方法: {args.method}")
        else:
            print(f"🎯 方法: 自動測試 (GET + POST)")
        print()
    
    # 建立測試器
    tester = ApiTester(url, timeout=args.timeout, headers=headers)
    
    try:
        # 執行測試
        tester.run_tests(method=args.method, data=args.data)
        
        # 根據結果決定退出代碼
        results = tester.get_results()
        failed_tests = sum(1 for r in results if not r['success'])
        
        if failed_tests > 0:
            sys.exit(1)  # 有失敗的測試
        else:
            sys.exit(0)  # 全部成功
            
    except KeyboardInterrupt:
        print("\n⚠️  使用者中斷測試")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ 未預期的錯誤: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 