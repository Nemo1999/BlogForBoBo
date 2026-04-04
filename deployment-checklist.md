# 🚀 部落格部署檢查清單

## 部署前必須檢查（每次修改後）

### ✅ 1. Git 狀態檢查
```bash
git status
```
- [ ] 確認所有修改的文件都已暫存 (staged)
- [ ] 確認沒有未追蹤的重要文件
- [ ] 確認分支狀態正確

### ✅ 2. 提交訊息規範
```bash
git commit -m "類型：簡潔描述

- 具體修改1
- 具體修改2
- 影響說明"
```
**提交類型**：
- `feat`: 新功能
- `fix`: 錯誤修復  
- `refactor`: 重構
- `docs`: 文檔更新
- `style`: 樣式修改
- `test`: 測試相關

### ✅ 3. 推送確認
```bash
git push origin main
```
- [ ] 確認推送成功
- [ ] 確認沒有衝突
- [ ] 確認遠端分支更新

### ✅ 4. GitHub Actions 監控
```bash
# 檢查部署狀態
curl -s "https://api.github.com/repos/Nemo1999/BlogForBoBo/actions/runs" | jq '.workflow_runs[0] | {status, conclusion, html_url}'
```
- [ ] 確認 GitHub Actions 開始運行
- [ ] 監控部署進度
- [ ] 確認部署成功

### ✅ 5. 部署後驗證
```bash
# 等待部署完成（GitHub Pages 需要 2-10 分鐘）
sleep 300

# 測試關鍵連結
python3 test_real_links.py
```
- [ ] 等待足夠的部署時間
- [ ] 測試所有關鍵連結
- [ ] 確認頁面可正常訪問

## 🛡️ 防範忘記推送的機制

### 自動化檢查腳本
創建 `check-deployment.sh` 腳本，自動執行所有檢查：

```bash
#!/bin/bash
echo "🔍 開始部署檢查..."
echo "1. 檢查 Git 狀態..."
git status

echo ""
echo "2. 檢查未提交的修改..."
if git diff --quiet && git diff --cached --quiet; then
    echo "✅ 沒有未提交的修改"
else
    echo "⚠️  發現未提交的修改："
    git status --short
    echo ""
    echo "請先提交修改："
    echo "  git add ."
    echo "  git commit -m '你的提交訊息'"
    echo "  git push origin main"
    exit 1
fi

echo ""
echo "3. 檢查遠端狀態..."
git fetch origin
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u})

if [ $LOCAL = $REMOTE ]; then
    echo "✅ 本地與遠端同步"
else
    echo "⚠️  本地與遠端不同步"
    echo "請先拉取遠端更新："
    echo "  git pull origin main"
    exit 1
fi

echo ""
echo "✅ 所有檢查通過，可以安全部署"
```

### 工作流程整合
將檢查腳本整合到日常工作流程中：

1. **修改文件後立即運行檢查**
2. **定期檢查部署狀態**
3. **設置提醒機制**

## 📊 部署監控儀表板

### 關鍵指標監控
1. **Git 提交頻率**：確保定期推送
2. **部署成功率**：監控 GitHub Actions 狀態
3. **頁面可訪問性**：定期測試關鍵連結
4. **用戶訪問統計**：監控實際使用情況

### 問題預警
設置以下預警條件：
- 超過24小時沒有新的提交
- GitHub Actions 部署失敗
- 關鍵連結返回非200狀態碼
- 用戶訪問量異常下降

## 🔧 緊急修復流程

### 如果忘記推送：
1. **立即檢查當前狀態**：`git status`
2. **提交所有修改**：`git add . && git commit -m "緊急修復：描述問題"`
3. **立即推送**：`git push origin main`
4. **監控部署**：檢查 GitHub Actions
5. **驗證修復**：測試所有連結

### 如果部署失敗：
1. **檢查錯誤日誌**：GitHub Actions 輸出
2. **回滾到上一個穩定版本**：`git revert`
3. **修復問題後重新部署**
4. **更新部署檢查清單**，防止同樣問題再次發生

## 📝 最佳實踐

### 每次修改後：
1. **立即提交**：不要累積多個修改
2. **描述清晰**：提交訊息要具體
3. **測試本地**：確保修改不會破壞現有功能
4. **立即推送**：不要延遲推送

### 定期維護：
1. **每天檢查**：Git 狀態和部署狀態
2. **每周清理**：移除未使用的文件和代碼
3. **每月審計**：檢查所有連結和功能
4. **每季度優化**：改進工作流程和工具

---

**最後更新**：2026年4月4日  
**維護者**：小波 👁️  
**目標**：確保每次修改都能正確部署，避免忘記推送的問題