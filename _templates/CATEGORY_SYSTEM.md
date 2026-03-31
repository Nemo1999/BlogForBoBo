# 🗂️ 分類系統規範

## 🎯 目標
建立一致、可擴展的分類系統，確保URL結構清晰且可預測。

## 📊 分類結構總覽

### 主要分類層級
```
1. 領域 (domain)      - 如：philosophy, science, literature
2. 作者/主題 (author) - 如：bohm, kant, physics
3. 內容類型 (type)    - 如：material, translation, discussion
4. 子類型 (subtype)   - 如：complete, summary, analysis
```

### 玻姆項目分類樹
```
philosophy/                    # 領域：哲學
└── bohm/                     # 作者：大衛·玻姆
    ├── material/             # 類型：素材篇
    │   └── [YYYY-MM-DD-title].html
    ├── complete/             # 類型：完整翻譯
    │   └── translation/      # 子類型：翻譯內容
    │       └── [YYYY-MM-DD-title].html
    ├── discussion/           # 類型：討論篇
    │   └── [YYYY-MM-DD-title].html
    └── analysis/             # 類型：分析篇
        └── [YYYY-MM-DD-title].html
```

## 📝 分類使用規範

### 規則 1：分類數組結構
```yaml
# 正確範例
categories: [philosophy, bohm, material]           # 3層：素材篇
categories: [philosophy, bohm, complete, translation] # 4層：完整翻譯

# 錯誤範例
categories: [bohm, material]                      # 缺少領域層級
categories: [philosophy, bohm, complete, translation, extra] # 過深
```

### 規則 2：分類命名規範
- **英文小寫**：全部使用小寫字母
- **單數形式**：使用單數名詞（如 philosophy 而非 philosophies）
- **簡潔明確**：2-3個單詞為佳，避免過長
- **語義清晰**：一看就懂分類內容

### 規則 3：分類層級限制
- **最小**：2層（領域 + 作者）
- **推薦**：3-4層
- **最大**：5層（特殊情況）
- **保持一致**：相同類型的內容使用相同層級

## 🎨 分類設計範例

### 範例 1：玻姆素材篇
```yaml
title: "玻姆第1章素材篇：碎片化與整體性"
categories: [philosophy, bohm, material]
```
**生成URL**：`/philosophy/bohm/material/2026/03/31/bohm-chapter-1-material.html`

### 範例 2：玻姆完整翻譯
```yaml
title: "玻姆第1章完整翻譯：第一部分"
categories: [philosophy, bohm, complete, translation]
```
**生成URL**：`/philosophy/bohm/complete/translation/2026/03/31/bohm-chapter-1-complete-part1.html`

### 範例 3：玻姆討論篇
```yaml
title: "玻姆第1章討論：碎片化思維的當代應用"
categories: [philosophy, bohm, discussion]
```
**生成URL**：`/philosophy/bohm/discussion/2026/03/31/bohm-chapter-1-discussion.html`

## 🔄 擴展其他項目

### 新哲學家項目
```yaml
# 康德項目
categories: [philosophy, kant, translation]

# 海德格項目  
categories: [philosophy, heidegger, analysis]
```

### 跨領域項目
```yaml
# 科學哲學
categories: [philosophy, science, interdisciplinary]

# 文學哲學
categories: [literature, philosophy, analysis]
```

## 🛠️ 分類選擇指南

### 決策流程
1. **確定領域**：主要學科領域是什麼？
2. **確定作者/主題**：具體的作者或主題是什麼？
3. **確定內容類型**：是什麼類型的內容？
4. **確定是否需要子類型**：是否需要進一步細分？

### 選擇矩陣
| 領域 | 作者/主題 | 內容類型 | 子類型 | 範例分類 |
|------|-----------|----------|--------|----------|
| philosophy | bohm | material | - | [philosophy, bohm, material] |
| philosophy | bohm | complete | translation | [philosophy, bohm, complete, translation] |
| philosophy | kant | analysis | critique | [philosophy, kant, analysis, critique] |
| science | physics | explanation | quantum | [science, physics, explanation, quantum] |

## 📋 分類創建檢查清單

### 創建新分類前
- [ ] 檢查現有分類結構，避免重複
- [ ] 確認分類層級合理（2-4層）
- [ ] 確保分類名稱清晰明確
- [ ] 考慮未來擴展性

### 使用分類時
- [ ] 使用正確的分類數組格式
- [ ] 保持相關內容分類一致
- [ ] 記錄分類決策原因
- [ ] 更新分類文檔

## 🚨 常見分類錯誤

### 錯誤 1：分類不一致
```
文章A：categories: [philosophy, bohm, material]
文章B：categories: [bohm, philosophy, material]  # 順序錯誤
```
**解決**：建立分類順序規範，保持一致

### 錯誤 2：分類過深
```
categories: [philosophy, bohm, complete, translation, part1, sectionA]  # 6層，太深
```
**解決**：合併相關層級，保持3-4層

### 錯誤 3：分類混亂
```
同一個內容使用不同分類：
- [philosophy, bohm, material]
- [bohm, philosophy, resources]  # 混亂
```
**解決**：建立分類映射表，統一標準

## 📊 分類管理工具

### 分類映射表
```yaml
玻姆項目:
  素材篇: [philosophy, bohm, material]
  完整翻譯: [philosophy, bohm, complete, translation]
  討論篇: [philosophy, bohm, discussion]
  分析篇: [philosophy, bohm, analysis]

康德項目:
  翻譯: [philosophy, kant, translation]
  分析: [philosophy, kant, analysis]
```

### 分類驗證腳本（未來）
```bash
# 檢查分類一致性的腳本
./validate-categories.sh
```

## 🔮 未來擴展

### 動態分類系統
考慮實現：
1. 自動分類建議
2. 分類衝突檢測
3. URL 生成預覽
4. 分類使用統計

### 分類重構工具
當需要調整分類時：
1. 批量更新分類
2. 自動重定向設置
3. 連結更新工具
4. 影響分析報告

---

**核心原則**：分類是內容的骨架，好的分類系統讓內容更易於查找、管理和擴展。花時間設計好分類系統，後續工作會事半功倍。👁️