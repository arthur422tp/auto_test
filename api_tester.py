import requests
import json

class ApiTester:
    def __init__(self, url):
        self.url = url

    def run_tests(self, method=None, data=None):
        # 預設測試 GET
        if method is None or method == "GET":
            self.test_get()
        # 預設測試 POST
        if method is None or method == "POST":
            self.test_post(data)

    def test_get(self):
        print(f"測試 GET {self.url}")
        try:
            resp = requests.get(self.url)
            print(f"狀態碼: {resp.status_code}")
            print(f"回應內容: {resp.text}")
        except Exception as e:
            print(f"GET 請求失敗: {e}")

    def test_post(self, data):
        print(f"測試 POST {self.url}")
        try:
            payload = json.loads(data) if data else {"test": "value"}
            resp = requests.post(self.url, json=payload)
            print(f"狀態碼: {resp.status_code}")
            print(f"回應內容: {resp.text}")
        except Exception as e:
            print(f"POST 請求失敗: {e}") 