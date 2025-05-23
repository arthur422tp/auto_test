import json
import datetime
from typing import List, Dict, Any

class ReportGenerator:
    def __init__(self, results: List[Dict[str, Any]]):
        self.results = results
        self.timestamp = datetime.datetime.now()

    def generate_html_report(self, output_file: str = "api_test_report.html"):
        """生成 HTML 測試報告"""
        html_content = self._generate_html()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"📄 HTML 測試報告已生成: {output_file}")

    def _generate_html(self) -> str:
        """生成 HTML 內容"""
        # 計算統計資料
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r['success'])
        failed_tests = total_tests - successful_tests
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        # 計算平均回應時間
        valid_times = [r['response_time'] for r in self.results if r['response_time'] > 0]
        avg_response_time = sum(valid_times) / len(valid_times) if valid_times else 0

        html = f"""
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API 測試報告</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header .subtitle {{
            opacity: 0.9;
            font-size: 1.1em;
        }}
        
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        
        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            transition: transform 0.3s ease;
        }}
        
        .summary-card:hover {{
            transform: translateY(-5px);
        }}
        
        .summary-card .number {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .summary-card .label {{
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .success {{ color: #28a745; }}
        .danger {{ color: #dc3545; }}
        .info {{ color: #17a2b8; }}
        .warning {{ color: #ffc107; }}
        
        .results {{
            padding: 30px;
        }}
        
        .results h2 {{
            margin-bottom: 20px;
            color: #333;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .test-item {{
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            margin-bottom: 15px;
            overflow: hidden;
            transition: all 0.3s ease;
        }}
        
        .test-item:hover {{
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }}
        
        .test-header {{
            padding: 15px 20px;
            background: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
            cursor: pointer;
        }}
        
        .test-header.success {{
            border-left: 4px solid #28a745;
        }}
        
        .test-header.failed {{
            border-left: 4px solid #dc3545;
        }}
        
        .test-method {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: bold;
            color: white;
            margin-right: 10px;
        }}
        
        .method-GET {{ background: #28a745; }}
        .method-POST {{ background: #007bff; }}
        .method-PUT {{ background: #fd7e14; }}
        .method-PATCH {{ background: #6610f2; }}
        .method-DELETE {{ background: #dc3545; }}
        
        .test-url {{
            font-family: monospace;
            color: #666;
            margin-left: 10px;
        }}
        
        .test-status {{
            float: right;
            font-weight: bold;
        }}
        
        .test-details {{
            padding: 20px;
            background: #f8f9fa;
            display: none;
        }}
        
        .test-details.show {{
            display: block;
        }}
        
        .detail-row {{
            margin-bottom: 10px;
        }}
        
        .detail-label {{
            font-weight: bold;
            color: #333;
            display: inline-block;
            width: 120px;
        }}
        
        .detail-value {{
            color: #666;
        }}
        
        .response-content {{
            background: #2d3748;
            color: #e2e8f0;
            padding: 15px;
            border-radius: 5px;
            font-family: monospace;
            font-size: 0.9em;
            white-space: pre-wrap;
            max-height: 300px;
            overflow-y: auto;
            margin-top: 10px;
        }}
        
        .footer {{
            background: #333;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 0.9em;
        }}
        
        @media (max-width: 768px) {{
            .summary {{
                grid-template-columns: 1fr;
            }}
            
            .test-status {{
                float: none;
                display: block;
                margin-top: 5px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 API 測試報告</h1>
            <div class="subtitle">
                生成時間: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        </div>
        
        <div class="summary">
            <div class="summary-card">
                <div class="number info">{total_tests}</div>
                <div class="label">總測試數</div>
            </div>
            <div class="summary-card">
                <div class="number success">{successful_tests}</div>
                <div class="label">成功</div>
            </div>
            <div class="summary-card">
                <div class="number danger">{failed_tests}</div>
                <div class="label">失敗</div>
            </div>
            <div class="summary-card">
                <div class="number warning">{success_rate:.1f}%</div>
                <div class="label">成功率</div>
            </div>
            <div class="summary-card">
                <div class="number info">{avg_response_time:.3f}s</div>
                <div class="label">平均回應時間</div>
            </div>
        </div>
        
        <div class="results">
            <h2>📋 測試結果詳情</h2>
            {self._generate_test_items()}
        </div>
        
        <div class="footer">
            <p>📊 報告由 API 自動 Debug 工具生成</p>
        </div>
    </div>
    
    <script>
        function toggleDetails(element) {{
            const details = element.nextElementSibling;
            details.classList.toggle('show');
        }}
        
        // 自動展開失敗的測試
        document.addEventListener('DOMContentLoaded', function() {{
            const failedTests = document.querySelectorAll('.test-header.failed');
            failedTests.forEach(header => {{
                header.nextElementSibling.classList.add('show');
            }});
        }});
    </script>
</body>
</html>
        """
        
        return html

    def _generate_test_items(self) -> str:
        """生成測試項目的 HTML"""
        items_html = ""
        
        for i, result in enumerate(self.results):
            status_class = "success" if result['success'] else "failed"
            status_text = "✅ 成功" if result['success'] else "❌ 失敗"
            method = result['method']
            
            # 格式化回應內容
            response_content = ""
            if result['response_data']:
                if isinstance(result['response_data'], (dict, list)):
                    response_content = json.dumps(result['response_data'], indent=2, ensure_ascii=False)
                else:
                    response_content = str(result['response_data'])
            
            items_html += f"""
            <div class="test-item">
                <div class="test-header {status_class}" onclick="toggleDetails(this)">
                    <span class="test-method method-{method}">{method}</span>
                    <span class="test-url">{result['url']}</span>
                    <span class="test-status">{status_text}</span>
                </div>
                <div class="test-details">
                    <div class="detail-row">
                        <span class="detail-label">時間:</span>
                        <span class="detail-value">{result['timestamp']}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">狀態碼:</span>
                        <span class="detail-value">{result['status_code'] or 'N/A'}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">回應時間:</span>
                        <span class="detail-value">{result['response_time']}秒</span>
                    </div>
                    {f'<div class="detail-row"><span class="detail-label">錯誤:</span><span class="detail-value">{result["error"]}</span></div>' if result['error'] else ''}
                    {f'<div class="detail-row"><span class="detail-label">回應內容:</span><div class="response-content">{response_content}</div></div>' if response_content else ''}
                </div>
            </div>
            """
        
        return items_html

def generate_report_from_file(results_file: str, output_file: str = "api_test_report.html"):
    """從結果檔案生成報告"""
    try:
        with open(results_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        results = data.get('results', [])
        if not results:
            print("❌ 結果檔案中沒有找到測試結果")
            return
        
        generator = ReportGenerator(results)
        generator.generate_html_report(output_file)
        
    except Exception as e:
        print(f"❌ 生成報告時發生錯誤: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python report_generator.py <results_file> [output_file]")
        print("範例: python report_generator.py test_report.json api_report.html")
        sys.exit(1)
    
    results_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "api_test_report.html"
    
    generate_report_from_file(results_file, output_file) 