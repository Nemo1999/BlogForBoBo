---
layout: page
title: "連結測試頁面"
permalink: /test-links/
---

# 🔗 連結測試頁面

測試所有部落格連結是否正確：

## 主要頁面
1. [首頁](/BlogForBoBo/) - 應該顯示自我介紹
2. [目錄頁](/BlogForBoBo/toc/) - 應該顯示書籍目錄
3. [測試頁面](/BlogForBoBo/test-links/) - 當前頁面

## 第一章內容
4. [素材篇](/BlogForBoBo/philosophy/bohm/material/2026/03/31/bohm-chapter-1-material.html) - 6個段落中英對照
5. [完整翻譯第一部分](/BlogForBoBo/philosophy/bohm/complete/2026/03/31/bohm-chapter-1-complete-part1.html) - 第1-8頁完整翻譯

## 測試結果
請手動點擊以上連結確認是否可訪問。

## 問題分析
**之前的問題原因**：
1. 沒有使用絕對路徑（缺少 `/BlogForBoBo/` 前綴）
2. Jekyll 需要正確的 `permalink` 設置
3. 根目錄的 `.md` 文件需要明確的 front matter

**修復方法**：
1. 所有連結使用絕對路徑：`/BlogForBoBo/path/to/page`
2. 確保每個頁面都有正確的 `permalink`
3. 使用 `layout: page` 或 `layout: post` 適當

## 預防措施
1. 未來創建頁面時，總是設置 `permalink`
2. 使用絕對路徑而非相對路徑
3. 部署後立即測試所有連結
4. 保持URL結構一致性

[返回首頁](/BlogForBoBo/)