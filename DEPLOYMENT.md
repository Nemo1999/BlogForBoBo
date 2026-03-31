# 部署指南

## GitHub Pages 設置

### 步驟 1：啟用 GitHub Pages
1. 前往倉庫設置：https://github.com/Nemo1999/BlogForBoBo/settings/pages
2. 在 "Source" 部分，選擇 "GitHub Actions"
3. 保存設置

### 步驟 2：等待部署完成
- GitHub Actions 會自動構建和部署
- 查看工作流程狀態：https://github.com/Nemo1999/BlogForBoBo/actions
- 部署完成後，網站將在以下地址可用：https://nemo1999.github.io/BlogForBoBo/

## 本地開發

### 環境設置
```bash
# 安裝 Ruby 和 Bundler
sudo apt install ruby ruby-bundler

# 安裝 Jekyll
gem install jekyll bundler

# 克隆倉庫
git clone https://github.com/Nemo1999/BlogForBoBo.git
cd BlogForBoBo

# 安裝依賴
bundle install
```

### 本地運行
```bash
# 啟動本地服務器
bundle exec jekyll serve

# 在瀏覽器中打開
# http://localhost:4000/BlogForBoBo/
```

### 構建靜態文件
```bash
# 構建網站
bundle exec jekyll build

# 構建到特定目錄
bundle exec jekyll build --destination ./_site
```

## 添加新內容

### 創建新討論文章
在 `_discussions` 目錄中創建新的 Markdown 文件：

```markdown
---
layout: post
title: "文章標題"
date: YYYY-MM-DD
categories: [分類1, 分類2]
tags: [標籤1, 標籤2]
excerpt: "文章摘要"
---

# 文章內容

## 對話記錄
記錄對話內容...

## 分析與討論
深入分析...

## 參考資料
- 參考文獻
- 相關連結
```

### 文件命名約定
- 使用日期和標題：`YYYY-MM-DD-title-slug.md`
- 例如：`2025-03-31-fragmentation-wholeness.md`

## 工作流程

### 標準工作流程
1. 創建新文章或修改現有內容
2. 本地測試：`bundle exec jekyll serve`
3. 提交更改：`git add . && git commit -m "描述"`
4. 推送到 GitHub：`git push`
5. GitHub Actions 自動部署

### 批量添加內容
```bash
# 添加所有新討論文章
for file in _discussions/*.md; do
  git add "$file"
done

git commit -m "添加新的討論文章"
git push
```

## 故障排除

### 常見問題

#### 1. GitHub Pages 不更新
- 檢查 GitHub Actions 工作流程狀態
- 確認 `_config.yml` 中的 `baseurl` 設置正確
- 等待幾分鐘讓 CDN 緩存更新

#### 2. 本地 Jekyll 錯誤
```bash
# 清理緩存
bundle exec jekyll clean

# 重新安裝依賴
bundle install

# 更新 gems
bundle update
```

#### 3. CSS 樣式不生效
- 檢查 `assets/custom.css` 是否正確加載
- 確認佈局文件中正確引用了 CSS
- 清理瀏覽器緩存

#### 4. 圖片或資源加載失敗
- 確認資源路徑正確
- 檢查文件權限
- 使用相對路徑而非絕對路徑

### 日誌檢查
```bash
# 查看 Jekyll 構建日誌
bundle exec jekyll build --verbose

# 查看 GitHub Actions 日誌
# 在 https://github.com/Nemo1999/BlogForBoBo/actions 中查看工作流程運行詳情
```

## 性能優化

### 圖片優化
- 使用適當的圖片格式（WebP、AVIF）
- 壓縮圖片大小
- 使用懶加載

### CSS/JS 優化
- 最小化 CSS 和 JavaScript
- 使用 CDN 加載常用庫
- 實現代碼分割

### 緩存策略
- 設置適當的 HTTP 緩存頭
- 使用服務工作者進行離線支持
- 實現資源預加載

## 監控和分析

### 網站分析
- 添加 Google Analytics
- 使用 GitHub Pages 內置分析
- 監控加載性能和錯誤率

### SEO 優化
- 確保正確的 meta 標籤
- 創建 sitemap.xml
- 使用結構化數據

## 備份和恢復

### 定期備份
```bash
# 備份整個倉庫
git clone --mirror https://github.com/Nemo1999/BlogForBoBo.git BlogForBoBo-backup

# 備份構建文件
tar -czf _site-backup.tar.gz _site/
```

### 恢復網站
```bash
# 從備份恢復
git clone BlogForBoBo-backup BlogForBoBo-restored

# 重新構建
cd BlogForBoBo-restored
bundle install
bundle exec jekyll build
```

## 安全最佳實踐

### 倉庫安全
- 定期更新依賴項
- 使用 Dependabot 自動安全更新
- 審查第三方代碼

### 內容安全
- 驗證用戶生成內容（如果有的話）
- 避免敏感信息泄露
- 使用 HTTPS

## 擴展功能

### 未來可能的擴展
1. **評論系統**：添加 Disqus 或自建評論
2. **搜索功能**：實現站內搜索
3. **多語言支持**：完整的多語言版本
4. **API 集成**：與其他服務集成
5. **訂閱功能**：RSS 和郵件訂閱

---

**最後更新**：2025年3月31日  
**維護者**：小波 👁️