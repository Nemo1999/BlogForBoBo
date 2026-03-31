# ⚡ 快速參考指南

## 🎯 核心原則

### 1. URL 規則
```
✅ 正確：/BlogForBoBo/philosophy/bohm/material/2026/03/31/title.html
❌ 錯誤：/philosophy/bohm/material/2026/03/31/title.html
```

### 2. 分類設計
```
素材篇：    [philosophy, bohm, material]
完整翻譯：  [philosophy, bohm, complete, translation]
討論篇：    [philosophy, bohm, discussion]
```

### 3. 連結創建
```
內部連結：/BlogForBoBo/完整路徑
外部連結：[文字](https://完整URL)
```

## 📁 文件創建流程

### 步驟 1：選擇模板
```bash
# 頁面（導航頁面）
cp _templates/page-template.md new-page.md

# 文章（時間序列內容）
cp _templates/post-template.md _posts/YYYY-MM-DD-title.md
```

### 步驟 2：編輯內容
1. 更新 front matter
2. 填寫內容
3. 設置連結
4. 添加導航

### 步驟 3：檢查
```bash
python3 _templates/check-urls.py
```

### 步驟 4：部署
```bash
git add .
git commit -m "描述變更"
git push origin main
```

## 🛠️ 常用命令

### 本地測試
```bash
# 安裝依賴（首次）
bundle install

# 啟動本地服務器
bundle exec jekyll serve

# 訪問本地測試
open http://localhost:4000/BlogForBoBo/
```

### 檢查工具
```bash
# 檢查所有文件
python3 _templates/check-urls.py

# 檢查單個文件
python3 _templates/check-urls.py | grep "文件名"
```

### Git 操作
```bash
# 查看狀態
git status

# 添加更改
git add 文件名
git add .  # 所有更改

# 提交
git commit -m "清晰描述"

# 推送
git push origin main

# 查看歷史
git log --oneline -10
```

## 📝 Front Matter 參考

### 頁面模板
```yaml
---
layout: page
title: "頁面標題"
permalink: /BlogForBoBo/路徑/
navigation_order: 1  # 可選
---
```

### 文章模板
```yaml
---
layout: post
title: "文章標題"
date: YYYY-MM-DD
categories: [領域, 作者, 類型, 子類型]  # 所有都會成為URL
author: "作者名稱"
excerpt: "摘要文字"
---
```

## 🔗 連結範例

### 正確範例
```markdown
# 內部連結
- [首頁](/BlogForBoBo/)
- [目錄](/BlogForBoBo/toc/)
- [素材篇](/BlogForBoBo/philosophy/bohm/material/2026/03/31/bohm-chapter-1-material.html)

# 外部連結
- [GitHub](https://github.com/Nemo1999/BlogForBoBo)
- [玻姆檔案](https://www.bohm.org/)
```

### 錯誤範例
```markdown
# 缺少 baseurl
- [/index/]
- [/toc/]

# 相對路徑（可能失效）
- [../other-page]
- [material/2026/03/31/title.html]

# 分類不完整
- [/philosophy/bohm/title.html]  # 缺少 material/ 層級
```

## 🚨 常見錯誤速查

### 錯誤：404 頁面找不到
**檢查**：
1. 分類是否完整？
2. 連結是否包含 `/BlogForBoBo/`？
3. 文件是否在正確位置？

### 錯誤：連結失效
**檢查**：
1. 是否使用絕對路徑？
2. 目標頁面是否存在？
3. 分類路徑是否正確？

### 錯誤：內容未更新
**解決**：
1. 清除瀏覽器緩存
2. 等待 5-10 分鐘
3. 檢查 GitHub Actions

## 📊 分類速查表

### 玻姆項目
| 內容類型 | 分類數組 | 預期 URL 前綴 |
|---------|---------|--------------|
| 素材篇 | `[philosophy, bohm, material]` | `/philosophy/bohm/material/` |
| 完整翻譯 | `[philosophy, bohm, complete, translation]` | `/philosophy/bohm/complete/translation/` |
| 討論篇 | `[philosophy, bohm, discussion]` | `/philosophy/bohm/discussion/` |
| 分析篇 | `[philosophy, bohm, analysis]` | `/philosophy/bohm/analysis/` |

### 擴展項目
| 項目 | 分類前綴 | 說明 |
|------|---------|------|
| 康德 | `[philosophy, kant]` | 康德哲學 |
| 科學 | `[science]` | 科學內容 |
| 文學 | `[literature]` | 文學內容 |

## ⏱️ 時間估算

### 創建新頁面
- **簡單頁面**：10-15 分鐘
- **文章內容**：30-60 分鐘
- **複雜項目**：2-4 小時

### 部署流程
- **提交更改**：1 分鐘
- **GitHub Actions**：2-5 分鐘
- **生效時間**：1-5 分鐘
- **測試時間**：5-10 分鐘

### 維護任務
- **每日檢查**：5 分鐘
- **每周測試**：15 分鐘
- **每月維護**：1-2 小時

## 🆘 緊急處理

### 網站無法訪問
1. 檢查 GitHub Actions 狀態
2. 檢查 GitHub Pages 設置
3. 等待 15 分鐘後重試
4. 如有需要，回滾到上個版本

### 內容錯誤
1. 立即創建修復提交
2. 快速部署
3. 通知相關人員
4. 記錄問題原因

### 安全問題
1. 立即暫停相關功能
2. 調查問題原因
3. 實施修復
4. 加強安全措施

---

**記住**：預防勝於治療。遵循模板和規則，可以避免大多數問題。遇到問題時，參考相關文檔和檢查清單。👁️