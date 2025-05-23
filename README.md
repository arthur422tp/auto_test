# 🚀 API 自動 Debug 工具 v2.0

這是一個強化版的 API Debug 工具，讓您只需輸入 API 伺服器的 port 和 route，系統就會自動對該 API 端點進行全面測試。

## ✨ 功能特色

### 🎯 **核心功能**
- 支援所有常用 HTTP 方法（GET、POST、PUT、PATCH、DELETE）
- 自動測量回應時間與顯示詳細結果
- 智能錯誤處理與連線檢測
- 彩色終端輸出與表情符號指示

### 🔐 **認證支援**
- Bearer Token 認證
- Basic 認證
- 自訂 HTTP Headers

### 📊 **進階功能**
- 批次測試（從 JSON/YAML 配置檔案）
- 美觀的 HTML 測試報告生成
- 測試結果統計與分析
- 自動失敗測試高亮顯示

### ⚡ **效能優化**
- 可設定請求逾時時間
- 詳細的回應時間測量
- 成功率統計

---

## 📦 安裝方式

1. 請先安裝 Python 3.11 或以上版本
2. 安裝 uv（如果尚未安裝）：
```bash
pip install uv
```

3. 安裝專案相依套件：
```bash
uv sync
```

---

## 🚀 快速開始

### 基本用法

```bash
# 測試 GET 請求
uv run python auto_debug.py --port 5001 --route /api/test

# 測試 POST 請求並帶資料
uv run python auto_debug.py --port 5001 --route /api/users --method POST --data '{"name":"測試使用者","email":"test@example.com"}'

# 測試 HTTPS API
uv run python auto_debug.py --protocol https --host api.example.com --port 443 --route /api/data

# 包含認證的測試
uv run python auto_debug.py --port 5001 --route /api/protected --auth-bearer "your-token-here"
```

### 進階用法

```bash
# 測試所有 HTTP 方法
uv run python auto_debug.py --port 5001 --route /api/users --method GET
uv run python auto_debug.py --port 5001 --route /api/users --method POST --data '{"name":"test"}'
uv run python auto_debug.py --port 5001 --route /api/users/1 --method PUT --data '{"name":"updated"}'
uv run python auto_debug.py --port 5001 --route /api/users/1 --method DELETE

# 自訂 Headers
uv run python auto_debug.py --port 5001 --route /api/data --headers '{"Content-Type":"application/xml","X-Custom":"value"}'

# Basic 認證
uv run python auto_debug.py --port 5001 --route /api/auth --auth-basic "username:password"

# 設定逾時時間
uv run python auto_debug.py --port 5001 --route /api/slow --timeout 30
```

---

## 📋 批次測試

### 建立配置檔案

```bash
# 建立範例配置檔案
uv run python batch_tester.py --create-sample
```

### 執行批次測試

```bash
# 從 JSON 配置檔案執行
uv run python batch_tester.py sample_config.json

# 從 YAML 配置檔案執行
uv run python batch_tester.py tests.yaml
```

### 配置檔案範例 (JSON)

```json
{
  "base_url": "http://localhost:5001",
  "timeout": 10,
  "headers": {
    "Content-Type": "application/json"
  },
  "tests": [
    {
      "name": "測試 GET 使用者列表",
      "endpoint": "/api/users",
      "method": "GET"
    },
    {
      "name": "測試 POST 建立使用者",
      "endpoint": "/api/users",
      "method": "POST",
      "data": {
        "name": "測試使用者",
        "email": "test@example.com"
      }
    },
    {
      "name": "測試需要認證的端點",
      "endpoint": "/api/protected",
      "method": "GET",
      "headers": {
        "Authorization": "Bearer your-token"
      }
    }
  ]
}
```

---

## 📊 HTML 報告生成

```bash
# 從測試結果生成 HTML 報告
uv run python report_generator.py test_report.json my_report.html
```

生成的 HTML 報告包含：
- 📈 測試統計圖表
- 🎯 詳細的測試結果
- ⚡ 回應時間分析
- 🔍 失敗測試的詳細資訊
- 📱 響應式設計（支援手機瀏覽）

---

## 🛠️ 參數說明

### auto_debug.py 參數

| 參數 | 類型 | 說明 | 必填 | 預設值 |
|------|------|------|------|--------|
| `--port` | int | API 伺服器 port | ✅ | 無 |
| `--route` | str | API 路由路徑 | ✅ | 無 |
| `--method` | str | HTTP 方法 (GET/POST/PUT/PATCH/DELETE) | ❌ | 自動測試 GET+POST |
| `--data` | str | 請求資料 (JSON 格式) | ❌ | 自動生成 |
| `--host` | str | API 主機位址 | ❌ | localhost |
| `--protocol` | str | 協定 (http/https) | ❌ | http |
| `--timeout` | int | 請求逾時秒數 | ❌ | 10 |
| `--headers` | str | 自訂 Headers (JSON 格式) | ❌ | 無 |
| `--auth-bearer` | str | Bearer Token 認證 | ❌ | 無 |
| `--auth-basic` | str | Basic 認證 (格式: user:pass) | ❌ | 無 |
| `--verbose` | flag | 詳細輸出模式 | ❌ | False |
| `--quiet` | flag | 安靜模式 | ❌ | False |

---

## 📁 檔案結構

```
api_debug_tool/
├── auto_debug.py          # 🎯 主程式入口
├── api_tester.py          # 🧪 API 測試核心邏輯
├── batch_tester.py        # 📋 批次測試工具
├── report_generator.py    # 📊 HTML 報告生成器
├── pyproject.toml         # 📦 uv 專案設定
├── uv.lock               # 🔒 套件版本鎖定
├── .gitignore            # 🚫 Git 忽略檔案
└── README.md             # 📖 說明文件
```

---

## 🎨 輸出範例

```
🚀 API 自動 Debug 工具
==================================================
🌐 目標: http://localhost:5001/api/users
⏱️  逾時: 10秒
🎯 方法: 自動測試 (GET + POST)

🎯 開始 API 測試
🌐 目標 URL: http://localhost:5001/api/users
==================================================

🚀 測試 GET http://localhost:5001/api/users
⏱️  開始時間: 2024-01-01 12:00:00
✅ 狀態碼: 200
⚡ 回應時間: 0.156秒
📥 回應內容: {
  "users": [
    {"id": 1, "name": "使用者1"},
    {"id": 2, "name": "使用者2"}
  ]
}

🚀 測試 POST http://localhost:5001/api/users
⏱️  開始時間: 2024-01-01 12:00:01
📤 請求資料: {
  "test": "value",
  "timestamp": 1704096001
}
✅ 狀態碼: 201
⚡ 回應時間: 0.234秒
📥 回應內容: {
  "message": "使用者建立成功",
  "id": 3
}

==================================================
📊 測試摘要
==================================================
總測試數: 2
✅ 成功: 2
❌ 失敗: 0
📈 成功率: 100.0%
⚡ 平均回應時間: 0.195秒
```

---

## 🔧 開發者資訊

### 安裝開發相依套件

```bash
uv sync --group dev
```

### 程式碼格式化

```bash
uv run black .
```

### 程式碼檢查

```bash
uv run flake8 .
```

---

## 🆕 更新日誌

### v2.0.0 (2024-01-01)
- ✨ 支援所有 HTTP 方法（GET、POST、PUT、PATCH、DELETE）
- 🔐 新增認證支援（Bearer Token、Basic Auth）
- 📊 新增 HTML 測試報告生成
- 📋 新增批次測試功能
- ⚡ 新增回應時間測量
- 🎨 改善終端輸出與錯誤處理
- 🐛 修正各種小問題

### v1.0.0 (2023-12-01)
- 🎯 基本 GET/POST 測試功能
- 📝 簡單的終端輸出

---

## 📄 授權

MIT License

---

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

---

## ❓ 常見問題

### Q: 如何測試需要認證的 API？
A: 使用 `--auth-bearer` 或 `--auth-basic` 參數，或透過 `--headers` 自訂認證標頭。

### Q: 如何批次測試多個端點？
A: 建立 JSON 或 YAML 配置檔案，然後使用 `batch_tester.py` 執行。

### Q: 如何生成測試報告？
A: 批次測試會自動生成 JSON 報告，可使用 `report_generator.py` 轉換為 HTML 報告。

### Q: 支援 HTTPS 嗎？
A: 支援！使用 `--protocol https` 參數即可。 