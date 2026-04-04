#!/bin/bash
# 自動化部署檢查腳本
# 作者：小波 👁️
# 創建時間：2026-04-04

set -e

LOG_FILE="/home/nemo/.openclaw/workspace/blog-deploy.log"
BLOG_ROOT="/home/nemo/.openclaw/workspace/BlogForBoBo"

# 初始化日誌
init_log() {
    echo "========================================" >> "$LOG_FILE"
    echo "自動部署檢查開始: $(date)" >> "$LOG_FILE"
    echo "========================================" >> "$LOG_FILE"
}

# 記錄日誌
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
    echo "$1"
}

# 檢查 Git 狀態
check_git_status() {
    log "🔍 檢查 Git 狀態..."
    
    cd "$BLOG_ROOT"
    
    # 檢查是否有未暫存的修改
    local unstaged=$(git status --porcelain | grep -v '^[AMDRC]' | wc -l)
    if [ "$unstaged" -gt 0 ]; then
        log "⚠️  發現 $unstaged 個未暫存的修改"
        git status --short
        return 1
    fi
    
    # 檢查是否有未提交的修改
    if ! git diff --quiet || ! git diff --cached --quiet; then
        log "⚠️  發現未提交的修改"
        git status --short
        return 1
    fi
    
    log "✅ Git 狀態正常"
    return 0
}

# 檢查本地與遠端同步
check_git_sync() {
    log "🔄 檢查 Git 同步狀態..."
    
    cd "$BLOG_ROOT"
    
    # 獲取遠端更新
    git fetch origin
    
    # 比較本地和遠端
    LOCAL=$(git rev-parse @)
    REMOTE=$(git rev-parse @{u})
    
    if [ "$LOCAL" = "$REMOTE" ]; then
        log "✅ 本地與遠端同步"
        return 0
    else
        log "⚠️  本地與遠端不同步"
        log "本地: $LOCAL"
        log "遠端: $REMOTE"
        return 1
    fi
}

# 檢查 GitHub Actions 狀態
check_github_actions() {
    log "⚙️  檢查 GitHub Actions 狀態..."
    
    local response
    response=$(curl -s "https://api.github.com/repos/Nemo1999/BlogForBoBo/actions/runs" 2>/dev/null) || {
        log "❌ 無法獲取 GitHub Actions 狀態"
        return 1
    }
    
    local status=$(echo "$response" | jq -r '.workflow_runs[0].status' 2>/dev/null || echo "unknown")
    local conclusion=$(echo "$response" | jq -r '.workflow_runs[0].conclusion' 2>/dev/null || echo "unknown")
    local html_url=$(echo "$response" | jq -r '.workflow_runs[0].html_url' 2>/dev/null || echo "")
    
    log "最新工作流狀態: $status ($conclusion)"
    
    if [ "$status" = "completed" ] && [ "$conclusion" = "success" ]; then
        log "✅ GitHub Actions 部署成功"
        return 0
    elif [ "$status" = "in_progress" ] || [ "$status" = "queued" ]; then
        log "🔄 GitHub Actions 正在運行"
        return 0
    else
        log "⚠️  GitHub Actions 狀態異常: $status ($conclusion)"
        if [ -n "$html_url" ]; then
            log "詳細信息: $html_url"
        fi
        return 1
    fi
}

# 檢查關鍵連結
check_critical_links() {
    log "🔗 檢查關鍵連結..."
    
    cd "$BLOG_ROOT"
    
    local links=(
        "https://nemo1999.github.io/BlogForBoBo/"
        "https://nemo1999.github.io/BlogForBoBo/toc/"
        "https://nemo1999.github.io/BlogForBoBo/philosophy/bohm/material/2026/03/31/bohm-chapter-1-material.html"
        "https://nemo1999.github.io/BlogForBoBo/philosophy/bohm/complete/translation/2026/03/31/bohm-chapter-1-complete-part1.html"
        "https://nemo1999.github.io/BlogForBoBo/philosophy/bohm/chapter1/2026/04/02/bohm-chapter-1-part2-translated.html"
    )
    
    local failed=0
    local total=${#links[@]}
    
    for link in "${links[@]}"; do
        if python3 -c "
import requests, sys
try:
    r = requests.get('$link', timeout=10)
    if r.status_code == 200:
        print('✅')
    else:
        print('❌')
        sys.exit(1)
except:
    print('❌')
    sys.exit(1)
" 2>/dev/null; then
            log "  ✅ $link"
        else
            log "  ❌ $link"
            failed=$((failed + 1))
        fi
        sleep 1  # 避免請求過快
    done
    
    local success_rate=$(( (total - failed) * 100 / total ))
    log "📊 連結可訪問性: $success_rate% ($((total - failed))/$total)"
    
    if [ "$success_rate" -lt 80 ]; then
        return 1
    fi
    
    return 0
}

# 自動提交和推送（可選）
auto_commit_and_push() {
    log "🚀 執行自動提交和推送..."
    
    cd "$BLOG_ROOT"
    
    # 檢查是否有修改
    if git diff --quiet && git diff --cached --quiet; then
        log "ℹ️  沒有需要提交的修改"
        return 0
    fi
    
    # 添加所有修改
    git add .
    
    # 生成提交訊息
    local commit_message="自動提交: $(date '+%Y-%m-%d %H:%M:%S')
    
自動化部署檢查發現的修改：
$(git status --short)"
    
    # 提交
    git commit -m "$commit_message"
    
    # 推送
    if git push origin main; then
        log "✅ 自動提交和推送成功"
        return 0
    else
        log "❌ 自動推送失敗"
        return 1
    fi
}

# 顯示幫助
show_help() {
    echo "自動化部署檢查工具"
    echo "====================="
    echo "用法: $0 {命令}"
    echo ""
    echo "命令:"
    echo "  check     執行完整檢查（Git狀態、同步、部署、連結）"
    echo "  git       只檢查Git狀態和同步"
    echo "  deploy    檢查部署狀態"
    echo "  links     檢查關鍵連結"
    echo "  auto      自動提交和推送修改"
    echo "  full      完整檢查+自動提交（如果發現修改）"
    echo "  log       查看檢查日誌"
    echo "  help      顯示幫助信息"
    echo ""
    echo "示例:"
    echo "  $0 check    檢查所有項目"
    echo "  $0 full     完整檢查並自動處理"
}

# 查看日誌
show_log() {
    if [ -f "$LOG_FILE" ]; then
        echo "最近檢查日誌:"
        echo "=============="
        tail -50 "$LOG_FILE"
    else
        echo "無日誌文件"
    fi
}

# 主檢查函數
main_check() {
    init_log
    
    local all_ok=true
    
    # 檢查 Git 狀態
    if ! check_git_status; then
        all_ok=false
        log "⚠️  Git 狀態檢查失敗"
    fi
    
    # 檢查 Git 同步
    if ! check_git_sync; then
        all_ok=false
        log "⚠️  Git 同步檢查失敗"
    fi
    
    # 檢查 GitHub Actions
    if ! check_github_actions; then
        all_ok=false
        log "⚠️  GitHub Actions 檢查失敗"
    fi
    
    # 檢查關鍵連結
    if ! check_critical_links; then
        all_ok=false
        log "⚠️  關鍵連結檢查失敗"
    fi
    
    if [ "$all_ok" = true ]; then
        log "🎉 所有檢查通過！部署狀態正常。"
        return 0
    else
        log "⚠️  發現問題，需要手動處理。"
        return 1
    fi
}

# 完整檢查+自動處理
full_check() {
    init_log
    
    log "🔄 開始完整檢查和自動處理..."
    
    # 先檢查 Git 狀態
    if ! check_git_status; then
        log "🔄 發現未提交的修改，嘗試自動提交..."
        if auto_commit_and_push; then
            log "✅ 自動提交成功，等待部署..."
            sleep 60  # 等待部署開始
        else
            log "❌ 自動提交失敗，需要手動處理"
            return 1
        fi
    fi
    
    # 檢查其他項目
    check_git_sync
    check_github_actions
    
    # 等待一段時間後檢查連結
    log "⏳ 等待部署完成（120秒）..."
    sleep 120
    
    check_critical_links
    
    log "✅ 完整檢查完成"
}

# 主函數
main() {
    local command="${1:-check}"
    
    case "$command" in
        "check")
            main_check
            ;;
        "git")
            init_log
            check_git_status
            check_git_sync
            ;;
        "deploy")
            init_log
            check_github_actions
            ;;
        "links")
            init_log
            check_critical_links
            ;;
        "auto")
            init_log
            auto_commit_and_push
            ;;
        "full")
            full_check
            ;;
        "log")
            show_log
            ;;
        "help")
            show_help
            ;;
        *)
            echo "未知命令: $command"
            show_help
            exit 1
            ;;
    esac
}

# 執行
main "$@"