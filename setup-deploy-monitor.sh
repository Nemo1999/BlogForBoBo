#!/bin/bash
# 設置部署監控系統
# 作者：小波 👁️
# 創建時間：2026-04-04

set -e

echo "🛠️  設置部落格部署監控系統"
echo "=============================="

BLOG_ROOT="/home/nemo/.openclaw/workspace/BlogForBoBo"
CRON_FILE="/home/nemo/.openclaw/workspace/blog-deploy-cron"

# 創建監控目錄
mkdir -p "$BLOG_ROOT/_templates"
mkdir -p "$BLOG_ROOT/data"

# 1. 設置自動化檢查腳本
echo "1. 設置自動化檢查腳本..."
cp "$BLOG_ROOT/auto-deploy-check.sh" "$BLOG_ROOT/_templates/"
chmod +x "$BLOG_ROOT/_templates/auto-deploy-check.sh"

# 2. 創建 Cron Job 配置
echo "2. 創建定期檢查 Cron Job..."
cat > "$CRON_FILE" << 'EOF'
# 部落格部署監控 Cron Job
# 檢查頻率：每小時一次

# 每小時檢查部署狀態
0 * * * * cd /home/nemo/.openclaw/workspace/BlogForBoBo && ./auto-deploy-check.sh check >> /home/nemo/.openclaw/workspace/blog-cron.log 2>&1

# 每天上午9點執行完整檢查
0 9 * * * cd /home/nemo/.openclaw/workspace/BlogForBoBo && ./auto-deploy-check.sh full >> /home/nemo/.openclaw/workspace/blog-cron.log 2>&1

# 每天下午6點檢查連結
0 18 * * * cd /home/nemo/.openclaw/workspace/BlogForBoBo && ./auto-deploy-check.sh links >> /home/nemo/.openclaw/workspace/blog-cron.log 2>&1
EOF

echo "Cron Job 配置已創建: $CRON_FILE"
echo ""
echo "📋 Cron Job 配置內容:"
echo "====================="
cat "$CRON_FILE"
echo "====================="

# 3. 安裝 Cron Job（可選）
echo ""
echo "3. 安裝 Cron Job（可選）"
echo "要安裝 Cron Job 嗎？ (y/n)"
read -r install_cron

if [ "$install_cron" = "y" ] || [ "$install_cron" = "Y" ]; then
    if crontab -l >/dev/null 2>&1; then
        # 備份現有 Cron Job
        crontab -l > "$CRON_FILE.backup"
        echo "✅ 已備份現有 Cron Job"
    fi
    
    # 添加新的 Cron Job
    crontab "$CRON_FILE"
    echo "✅ Cron Job 已安裝"
    echo ""
    echo "當前 Cron Job 列表:"
    crontab -l
else
    echo "ℹ️  跳過 Cron Job 安裝"
    echo "你可以手動安裝："
    echo "  crontab $CRON_FILE"
fi

# 4. 創建部署狀態儀表板
echo ""
echo "4. 創建部署狀態儀表板..."

cat > "$BLOG_ROOT/data/deploy-status.json" << 'EOF'
{
  "lastCheck": null,
  "lastDeploy": null,
  "gitStatus": "unknown",
  "deployStatus": "unknown",
  "linkStatus": "unknown",
  "issues": [],
  "history": []
}
EOF

# 5. 創建部署報告模板
echo "5. 創建部署報告模板..."

cat > "$BLOG_ROOT/_templates/deploy-report.md" << 'EOF'
# 部落格部署狀態報告

**生成時間**: {{timestamp}}  
**檢查類型**: {{check_type}}  
**總體狀態**: {{overall_status}}

## 📊 檢查結果

### Git 狀態
- **本地修改**: {{git_local_changes}}
- **同步狀態**: {{git_sync_status}}
- **最後提交**: {{git_last_commit}}

### 部署狀態
- **GitHub Actions**: {{github_actions_status}}
- **部署時間**: {{deploy_time}}
- **部署結果**: {{deploy_result}}

### 連結狀態
- **測試連結數**: {{links_tested}}
- **成功連結數**: {{links_success}}
- **成功率**: {{links_success_rate}}%

## ⚠️ 發現的問題

{{#issues}}
### {{title}}
- **類型**: {{type}}
- **嚴重性**: {{severity}}
- **描述**: {{description}}
- **建議**: {{suggestion}}
{{/issues}}

{{^issues}}
✅ 未發現問題
{{/issues}}

## 📈 歷史趨勢

{{#history}}
### {{date}}
- **狀態**: {{status}}
- **問題數**: {{issue_count}}
{{/history}}

## 🔧 建議操作

{{#has_issues}}
1. **立即處理**:
   {{#critical_issues}}
   - {{description}}
   {{/critical_issues}}

2. **計劃處理**:
   {{#warning_issues}}
   - {{description}}
   {{/warning_issues}}
{{/has_issues}}

{{^has_issues}}
✅ 無需立即操作，系統運行正常。
{{/has_issues}}

---

**檢查系統**: 自動化部署監控  
**維護者**: 小波 👁️  
**下次檢查**: {{next_check}}
EOF

# 6. 測試檢查系統
echo ""
echo "6. 測試部署檢查系統..."
cd "$BLOG_ROOT"
if ./auto-deploy-check.sh check; then
    echo "✅ 檢查系統測試成功"
else
    echo "⚠️  檢查系統測試發現問題"
fi

# 7. 總結
echo ""
echo "🎉 部署監控系統設置完成！"
echo ""
echo "📋 已創建的資源:"
echo "  - 自動化檢查腳本: auto-deploy-check.sh"
echo "  - 部署檢查清單: deployment-checklist.md"
echo "  - Cron Job 配置: blog-deploy-cron"
echo "  - 部署狀態數據: data/deploy-status.json"
echo "  - 部署報告模板: _templates/deploy-report.md"
echo ""
echo "🚀 使用方法:"
echo "  1. 手動檢查: ./auto-deploy-check.sh check"
echo "  2. 自動提交: ./auto-deploy-check.sh auto"
echo "  3. 完整檢查: ./auto-deploy-check.sh full"
echo "  4. 查看日誌: ./auto-deploy-check.sh log"
echo ""
echo "📅 定期檢查:"
echo "  - 每小時: 基本狀態檢查"
echo "  - 每天 9:00: 完整檢查"
echo "  - 每天 18:00: 連結檢查"
echo ""
echo "⚠️  重要提醒:"
echo "  1. 每次修改文件後，運行檢查腳本"
echo "  2. 如果發現問題，立即處理"
echo "  3. 定期查看檢查日誌"
echo "  4. 確保所有推送都成功完成"

# 8. 添加到 Git（可選）
echo ""
echo "8. 添加到 Git 版本控制..."
cd "$BLOG_ROOT"
git add deployment-checklist.md auto-deploy-check.sh 2>/dev/null || true
git add _templates/ data/ 2>/dev/null || true

echo "✅ 設置完成！"
echo ""
echo "現在你可以："
echo "1. 運行完整檢查: ./auto-deploy-check.sh full"
echo "2. 查看當前狀態: ./auto-deploy-check.sh check"
echo "3. 安裝定期監控: crontab blog-deploy-cron"