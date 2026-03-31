# 📋 Jekyll 頁面創建模板與規則指南

## 🎯 目標
確保所有頁面都有正確的 URL、連結和結構，避免重複錯誤。

## 📁 文件結構規則

### 1. 頁面類型與位置

#### A. 主要頁面（根目錄）
```
位置：根目錄
用途：首頁、目錄、關於等主要導航頁面
模板：使用 page-template.md
範例：index.md, toc.md, about.md
```

#### B. 部落格文章（_posts/）
```
位置：_posts/
用途：時間序列的文章、翻譯、內容
模板：使用 post-template.md
命名：YYYY-MM-DD-title.md
範例：2026-03-31-bohm-chapter-1-material.md
```

#### C. 靜態頁面（可選）
```
位置：任何目錄，但建議保持結構清晰
用途：特殊頁面、資源頁面
模板：使用 page-template.md
範例：resources/philosophy-guide.md
```

## 🏗️ 模板文件

### 模板 1：主要頁面模板 (page-template.md)

```markdown
---
layout: page
title: "頁面標題"
permalink: /正確的路徑/
navigation_order: 1  # 導航順序（可選）
---

# 頁面標題

## 內容區域

你的內容在這裡...

## 導航連結

✅ **正確做法**：
- [首頁](/BlogForBoBo/)
- [目錄](/BlogForBoBo/toc/)
- [其他頁面](/BlogForBoBo/other-page/)

❌ **錯誤做法**：
- [/index/] - 缺少 baseurl
- [toc] - 相對路徑，可能失效

---

**頁面信息**
- 創建日期：YYYY-MM-DD
- 最後更新：YYYY-MM-DD
- 狀態：✅ 完成 / 🔄 進行中 / 📝 計劃中

[返回首頁](/BlogForBoBo/)
```

### 模板 2：部落格文章模板 (post-template.md)

```markdown
---
layout: post
title: "文章標題"
date: YYYY-MM-DD
categories: [category1, category2, category3]  # 注意：所有分類都會成為URL的一部分
author: "作者名稱"
excerpt: "文章摘要，顯示在列表頁面"
---

# 文章標題

*可選副標題或說明*

## 重要提醒

### URL 規則
你的文章URL將是：`/category1/category2/category3/YYYY/MM/DD/title.html`

### 分類設計指南
1. **一致性**：相關文章使用相同分類前綴
2. **層級控制**：避免過深嵌套（建議2-4層）
3. **語義清晰**：分類名稱要有意義

### 內部連結
✅ **正確**：使用完整路徑
- [其他文章](/BlogForBoBo/category1/category2/YYYY/MM/DD/other-title.html)
- [目錄頁](/BlogForBoBo/toc/)

❌ **錯誤**：使用相對路徑或錯誤路徑
- [其他文章](../other-title.html)
- [/category1/other-title.html] - 可能缺少分類層級

## 文章內容

你的文章內容在這裡...

## 導航

### 相關文章
- [上一篇](/BlogForBoBo/...)
- [下一篇](/BlogForBoBo/...)
- [返回列表](/BlogForBoBo/blog/)

### 主要導航
- [首頁](/BlogForBoBo/)
- [目錄](/BlogForBoBo/toc/)
- [所有文章](/BlogForBoBo/blog/)

---

## 📄 版權聲明 (Copyright Notice)

### English
[版權聲明內容]

### 中文
[中文版權聲明]

---

**文章信息**
- 分類：category1 > category2 > category3
- 創建：YYYY-MM-DD
- 更新：YYYY-MM-DD
- 字數：約 XXXX 字

[返回文章列表](/BlogForBoBo/blog/)
```

## 🔗 連結創建規則

### 規則 1：絕對路徑原則
```
✅ 正確：/BlogForBoBo/path/to/page
❌ 錯誤：/path/to/page 或 path/to/page
```

### 規則 2：分類完整性
```
文章分類：[philosophy, bohm, material]
生成URL：/philosophy/bohm/material/YYYY/MM/DD/title.html

所有連結必須包含完整分類路徑！
```

### 規則 3：測試驗證
```
創建頁面後必須：
1. 等待部署（5-10分鐘）
2. 測試所有內部連結
3. 測試從首頁訪問
4. 測試從相關頁面訪問
```

## 🛠️ 工具與檢查清單

### 創建新頁面檢查清單
- [ ] 選擇正確模板（page 或 post）
- [ ] 設置正確的 `permalink`（page）或 `categories`（post）
- [ ] 所有連結使用絕對路徑 `/BlogForBoBo/...`
- [ ] 包含返回首頁的連結
- [ ] 添加版權聲明（如果需要）
- [ ] 設置正確的 meta 信息

### 部署後測試清單
- [ ] 首頁可訪問
- [ ] 新頁面可訪問
- [ ] 所有內部連結有效
- [ ] 導航連結正確
- [ ] 響應式設計正常

## 📝 分類設計系統

### 玻姆項目分類結構
```
philosophy/
  ├── bohm/
  │   ├── material/          # 素材篇
  │   ├── complete/          # 完整翻譯
  │   │   └── translation/   # 翻譯內容
  │   ├── discussion/        # 討論篇
  │   └── analysis/          # 分析篇
  └── other-philosopher/     # 其他哲學家
```

### 使用範例
```yaml
# 素材篇
categories: [philosophy, bohm, material]

# 完整翻譯  
categories: [philosophy, bohm, complete, translation]

# 討論篇
categories: [philosophy, bohm, discussion]
```

## 🚨 常見錯誤與解決方案

### 錯誤 1：404 頁面找不到
**原因**：URL 路徑錯誤，缺少分類層級或 baseurl
**解決**：檢查分類設置和連結路徑

### 錯誤 2：連結失效
**原因**：使用相對路徑或錯誤的絕對路徑
**解決**：所有連結使用 `/BlogForBoBo/` 開頭

### 錯誤 3：分類混亂
**原因**：不同文章使用不一致的分類
**解決**：建立分類規範，保持一致

## 📊 品質保證流程

### 階段 1：創建階段
1. 選擇模板
2. 填寫內容
3. 設置分類和連結
4. 自我檢查

### 階段 2：提交階段
1. Git 提交（清晰的信息）
2. 推送到 GitHub
3. 記錄變更內容

### 階段 3：測試階段
1. 等待部署完成
2. 測試所有功能
3. 記錄測試結果
4. 必要時修復

## 🔄 持續改進

### 記錄學習
每次遇到問題，更新：
1. 問題描述
2. 根本原因
3. 解決方案
4. 預防措施

### 模板優化
根據實際使用反饋：
1. 更新模板內容
2. 添加新功能
3. 簡化流程
4. 提高可靠性

---

**最後提醒**：模板是工具，理解原理更重要。掌握 Jekyll 的 URL 生成規則，才能從根本上避免錯誤。👁️