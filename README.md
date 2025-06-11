
# 這是我測試Claude4時所生成的

# 🚀 API Debug Tool - 智能API測試工具

一個功能強大的API測試工具，支援自動檢測HTTP方法和多場景測試。

## ✨ 主要功能

### 🎯 智能單一API測試
- **自動檢測HTTP方法**: 自動檢測API支援的HTTP方法 (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS)
- **多場景測試**:
  - ✅ **正常值測試**: 傳入符合規範的參數，確認能正確回傳資料
  - ❌ **缺少欄位測試**: 刻意不傳某些必要欄位，觀察是否報錯
  - 🌀 **格式錯誤測試**: 傳錯誤資料型別，確認錯誤處理是否完善
  - 🧪 **邊界值測試**: 傳入極小/極大值，空字串，null 等情況
  - 🚫 **不存在資源測試**: 傳入不存在的ID，看是否回傳404或自定義錯誤訊息

### 📋 批次測試
- JSON/YAML配置檔案支援
- 批次執行多個測試案例
- 支援自定義headers和認證
- 詳細的測試統計和報告

### 📊 報告生成
- JSON格式詳細報告
- 美觀的HTML互動式報告
- 測試統計和效能分析
- 失敗案例詳細分析

## 🛠️ 安裝

確保已安裝 `uv` 套件管理器：
```bash
pip install uv
```

安裝專案依賴：
```bash
uv sync
```

## 📖 使用方法

### 🎯 智能單一API測試

對單一API端點進行全面的自動化測試：

```bash
# 基本智能測試
uv run python comprehensive_api_tester.py smart http://localhost:8000 /api/list_contracts

# 生成HTML報告
uv run python comprehensive_api_tester.py smart http://localhost:8000 /api/list_contracts --html-report

# 設定逾時時間
uv run python comprehensive_api_tester.py smart http://localhost:8000 /api/users --timeout 60
```

### 🚀 壓力測試

對端點進行高併發壓力測試：

```bash
# 以 50 並發發送 500 次請求
uv run python comprehensive_api_tester.py stress http://localhost:8000 /api/list_contracts --requests 500 --concurrency 50 --html-report
```

### 📋 批次測試

使用配置檔案批次執行多個測試：

```bash
# 基本批次測試
uv run python comprehensive_api_tester.py batch tests.json

# 生成HTML報告
uv run python comprehensive_api_tester.py batch tests.json --html-report

# 指定輸出檔案
uv run python comprehensive_api_tester.py batch tests.json --output my_report.json
```

### 📝 生成範例配置檔案

```bash
# 建立範例配置檔案
uv run python comprehensive_api_tester.py create-samples
```

這會建立：
- `basic_batch_config.json` - 基本批次測試配置
- `smart_test_config.json` - 智能測試配置範例

## 📄 配置檔案格式

### 基本批次測試配置

```json
{
  "base_url": "http://localhost:8000",
  "timeout": 10,
  "headers": {
    "Content-Type": "application/json",
    "Authorization": "Bearer your-token"
  },
  "tests": [
    {
      "name": "✅ GET 用戶列表",
      "endpoint": "/api/users",
      "method": "GET"
    },
    {
      "name": "📝 POST 建立用戶",
      "endpoint": "/api/users",
      "method": "POST",
      "data": {
        "name": "測試用戶",
        "email": "test@example.com"
      }
    }
  ]
}
```

### 智能測試配置

```json
{
  "test_configs": [
    {
      "name": "📋 用戶API完整測試",
      "base_url": "http://localhost:3000",
      "endpoint": "/api/users",
      "test_scenarios": {
        "auto_detect_methods": true,
        "normal_value_tests": true,
        "missing_field_tests": true,
        "format_error_tests": true,
        "boundary_value_tests": true,
        "nonexistent_resource_tests": true
      }
    }
  ]
}
```

## 🔧 進階功能

### 認證支援

支援多種認證方式：

```json
{
  "headers": {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "X-API-Key": "your-api-key"
  }
}
```

### 自定義測試資料

可以自定義各種測試場景的資料：

```json
{
  "custom_test_data": {
    "normal": {
      "name": "正常用戶",
      "email": "normal@example.com",
      "age": 25
    },
    "boundary": {
      "age": [0, 1, 120, 999, -1],
      "name": ["", "A", "超長名稱..."]
    },
    "invalid": {
      "email": ["invalid-email", 123, null],
      "age": ["not_a_number", null]
    }
  }
}
```

## 📊 測試報告

### JSON報告
詳細的機器可讀格式，包含：
- 測試摘要統計
- 每個測試案例的詳細結果
- 請求/回應資料
- 效能指標

### HTML報告
美觀的網頁格式報告，包含：
- 互動式測試結果瀏覽
- 視覺化統計圖表
- 可折疊的詳細資訊
- 回應式設計，支援行動裝置

## 🔍 測試場景解析

### ✅ 正常值測試
驗證API在收到正確格式的請求時能正常運作：
- 傳送符合API規範的參數
- 驗證回應狀態碼為2xx
- 檢查回應資料格式

### ❌ 缺少欄位測試
檢測API的輸入驗證機制：
- 故意省略必要欄位
- 驗證是否回傳適當的錯誤訊息
- 確認狀態碼為4xx

### 🌀 格式錯誤測試
驗證API的資料型別檢查：
- 傳送錯誤的資料型別（如字串代替數字）
- 傳送無效的JSON格式
- 驗證錯誤處理機制

### 🧪 邊界值測試
測試API的邊界情況處理：
- 極大/極小數值
- 空字串和null值
- 超長字串
- 特殊字元

### 🚫 不存在資源測試
驗證API的資源查找機制：
- 請求不存在的資源ID
- 驗證404錯誤回應
- 檢查錯誤訊息的適當性

## 🎭 使用範例

### 範例1：測試合約API

```bash
# 對合約API進行全面測試
uv run python comprehensive_api_tester.py smart http://localhost:8000 /api/list_contracts --html-report
```

這會：
1. 自動檢測支援的HTTP方法
2. 執行各種測試場景
3. 生成詳細的HTML報告

### 範例2：批次測試多個端點

建立 `api_tests.json`：
```json
{
  "base_url": "http://localhost:8000",
  "timeout": 30,
  "tests": [
    {
      "name": "合約列表",
      "endpoint": "/api/list_contracts",
      "method": "GET"
    },
    {
      "name": "用戶資料",
      "endpoint": "/api/users/1",
      "method": "GET"
    },
    {
      "name": "建立用戶",
      "endpoint": "/api/users",
      "method": "POST",
      "data": {"name": "測試", "email": "test@example.com"}
    }
  ]
}
```

執行：
```bash
uv run python comprehensive_api_tester.py batch api_tests.json --html-report
```

## 🏗️ 專案結構

```
api_debug_tool/
├── comprehensive_api_tester.py   # 主要CLI工具
├── smart_api_tester.py          # 智能API測試器
├── concurrent_api_tester.py     # 並發壓力測試器
├── api_tester.py                # 基本API測試功能
├── batch_tester.py              # 批次測試功能
├── report_generator.py          # 報告生成器
├── auto_debug.py                # 簡單測試工具
├── pyproject.toml               # 專案配置
└── README.md                    # 說明文件
```

## 🔧 開發

### 專案依賴
- `requests` - HTTP請求
- `pyyaml` - YAML配置檔案支援
- `aiohttp` - 非同步 HTTP 客戶端
- `uv` - 套件管理

### 執行測試
```bash
# 測試基本功能
uv run python api_tester.py

# 測試智能功能
uv run python smart_api_tester.py http://localhost:8000 /api/test

# 測試批次功能
uv run python batch_tester.py test_config.json
```

## 💡 提示與技巧

1. **逾時設定**: 對於回應較慢的API，建議增加逾時時間
2. **認證**: 在headers中正確設定認證資訊
3. **測試資料**: 使用真實但非敏感的測試資料
4. **報告分析**: 重點關注失敗的測試案例，分析API的改進空間
