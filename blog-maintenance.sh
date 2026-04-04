#!/bin/bash
# 部落格維護腳本
# 作者：小波 👁️
# 創建時間：2026-04-04

set -e

BLOG_ROOT="/home/nemo/.openclaw/workspace/BlogForBoBo"
LOG_FILE="/home/nemo/.openclaw/workspace/blog-maintenance.log"

# 初始化日誌
init_log() {
    echo "========================================" >> "$LOG_FILE"
    echo "部落格維護開始: $(date)" >> "$LOG_FILE"
    echo "========================================" >> "$LOG_FILE"
}

# 記錄日誌
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
    echo "$1"
}

# 檢查部署狀態
check_deployment() {
    log "🔍 檢查部落格部署狀態..."
    
    # 檢查 GitHub Actions 狀態
    local actions_status=$(curl -s "https://api.github.com/repos/Nemo1999/BlogForBoBo/actions/runs" | jq -r '.workflow_runs[0].status' 2>/dev/null || echo "unknown")
    local actions_conclusion=$(curl -s "https://api.github.com/repos/Nemo1999/BlogForBoBo/actions/runs" | jq -r '.workflow_runs[0].conclusion' 2>/dev/null || echo "unknown")
    
    log "GitHub Actions 狀態: $actions_status ($actions_conclusion)"
    
    # 檢查主要頁面可訪問性
    local test_pages=(
        "/BlogForBoBo/"
        "/BlogForBoBo/toc/"
        "/BlogForBoBo/philosophy/bohm/chapter1/2026/04/02/bohm-chapter-1-part2-translated.html"
    )
    
    local base_url="https://nemo1999.github.io"
    local accessible=0
    local total=${#test_pages[@]}
    
    for page in "${test_pages[@]}"; do
        local url="${base_url}${page}"
        if curl -s -I "$url" 2>/dev/null | head -1 | grep -q "200\|301\|302"; then
            log "✅ 可訪問: $url"
            accessible=$((accessible + 1))
        else
            log "❌ 不可訪問: $url"
        fi
        sleep 1  # 避免請求過快
    done
    
    local success_rate=$((accessible * 100 / total))
    log "📊 可訪問性: $accessible/$total ($success_rate%)"
    
    if [ "$success_rate" -lt 80 ]; then
        log "⚠️  可訪問性較低，可能需要重新部署"
        return 1
    fi
    
    return 0
}

# 檢查連結
check_links() {
    log "🔗 檢查部落格連結..."
    
    cd "$BLOG_ROOT"
    
    if [ -f "link-manager.py" ]; then
        python3 link-manager.py --scan --blog-root .
        log "連結檢查完成"
    else
        log "❌ 連結管理器不存在"
        return 1
    fi
}

# 修復連結
fix_links() {
    log "🔧 修復部落格連結..."
    
    cd "$BLOG_ROOT"
    
    if [ -f "link-manager.py" ]; then
        python3 link-manager.py --fix --blog-root .
        log "連結修復完成"
    else
        log "❌ 連結管理器不存在"
        return 1
    fi
}

# 生成報告
generate_report() {
    log "📋 生成維護報告..."
    
    cd "$BLOG_ROOT"
    
    if [ -f "link-manager.py" ]; then
        python3 link-manager.py --report --blog-root .
        log "報告生成完成"
    else
        log "❌ 連結管理器不存在"
        return 1
    fi
}

# 清理緩存
clean_cache() {
    log "🧹 清理緩存文件..."
    
    # 清理 Jekyll 緩存
    if [ -d "$BLOG_ROOT/_site" ]; then
        rm -rf "$BLOG_ROOT/_site"
        log "✅ 清理 _site 目錄"
    fi
    
    if [ -d "$BLOG_ROOT/.jekyll-cache" ]; then
        rm -rf "$BLOG_ROOT/.jekyll-cache"
        log "✅ 清理 .jekyll-cache 目錄"
    fi
    
    # 清理備份文件
    find "$BLOG_ROOT" -name "*_backup_*" -type f -mtime +7 -delete 2>/dev/null && log "✅ 清理舊備份文件"
    find "$BLOG_ROOT" -name "*.bak" -type f -mtime +7 -delete 2>/dev/null && log "✅ 清理 .bak 文件"
}

# 備份重要文件
backup_files() {
    log "💾 備份重要文件..."
    
    local backup_dir="/home/nemo/.openclaw/workspace/blog-backups"
    local timestamp=$(date +%Y%m%d_%H%M%S)
    
    mkdir -p "$backup_dir"
    
    # 備份重要文件
    important_files=(
        "toc.md"
        "_config.yml"
        "Gemfile"
        "Gemfile.lock"
    )
    
    for file in "${important_files[@]}"; do
        if [ -f "$BLOG_ROOT/$file" ]; then
            cp "$BLOG_ROOT/$file" "$backup_dir/${file}.${timestamp}.bak"
        fi
    done
    
    # 備份文章目錄
    if [ -d "$BLOG_ROOT/_posts" ]; then
        tar -czf "$backup_dir/posts_${timestamp}.tar.gz" -C "$BLOG_ROOT" "_posts"
    fi
    
    log "✅ 備份完成: $backup_dir"
}

# 檢查文件結構
check_structure() {
    log "🏗️  檢查文件結構..."
    
    local issues=0
    
    # 檢查必要目錄
    required_dirs=(
        "_posts"
        "_layouts"
        "_includes"
    )
    
    for dir in "${required_dirs[@]}"; do
        if [ ! -d "$BLOG_ROOT/$dir" ]; then
            log "❌ 缺少目錄: $dir"
            issues=$((issues + 1))
        else
            log "✅ 目錄存在: $dir"
        fi
    done
    
    # 檢查必要文件
    required_files=(
        "_config.yml"
        "Gemfile"
        "index.md"
        "toc.md"
    )
    
    for file in "${required_files[@]}"; do
        if [ ! -f "$BLOG_ROOT/$file" ]; then
            log "❌ 缺少文件: $file"
            issues=$((issues + 1))
        else
            log "✅ 文件存在: $file"
        fi
    done
    
    # 檢查文章數量
    local post_count=$(find "$BLOG_ROOT/_posts" -name "*.md" -type f 2>/dev/null | wc -l)
    log "📄 文章數量: $post_count"
    
    if [ "$issues" -gt 0 ]; then
        log "⚠️  發現 $issues 個結構問題"
        return 1
    else
        log "✅ 文件結構正常"
        return 0
    fi
}

# 完整維護流程
full_maintenance() {
    log "🔄 開始完整維護流程..."
    
    init_log
    
    # 1. 備份
    backup_files
    
    # 2. 檢查結構
    check_structure
    structure_ok=$?
    
    # 3. 檢查連結
    check_links
    
    # 4. 修復連結
    fix_links
    
    # 5. 清理緩存
    clean_cache
    
    # 6. 生成報告
    generate_report
    
    # 7. 檢查部署
    check_deployment
    deployment_ok=$?
    
    log "✅ 完整維護流程完成"
    
    # 總結
    echo ""
    echo "📋 維護結果摘要"
    echo "================"
    echo "文件結構: $( [ $structure_ok -eq 0 ] && echo "✅ 正常" || echo "❌ 有問題" )"
    echo "部署狀態: $( [ $deployment_ok -eq 0 ] && echo "✅ 正常" || echo "❌ 有問題" )"
    echo "日誌文件: $LOG_FILE"
    echo ""
    
    if [ $structure_ok -ne 0 ] || [ $deployment_ok -ne 0 ]; then
        return 1
    fi
    
    return 0
}

# 顯示幫助
show_help() {
    echo "部落格維護工具"
    echo "================"
    echo "用法: $0 {命令}"
    echo ""
    echo "命令:"
    echo "  full       完整維護流程（備份、檢查、修復、清理）"
    echo "  check      檢查部署狀態和連結"
    echo "  fix        修復連結問題"
    echo "  clean      清理緩存文件"
    echo "  backup     備份重要文件"
    echo "  structure  檢查文件結構"
    echo "  report     生成維護報告"
    echo "  log        查看維護日誌"
    echo "  help       顯示幫助信息"
    echo ""
    echo "示例:"
    echo "  $0 full    執行完整維護"
    echo "  $0 check   檢查部落格狀態"
}

# 查看日誌
show_log() {
    if [ -f "$LOG_FILE" ]; then
        echo "最近維護日誌:"
        echo "=============="
        tail -50 "$LOG_FILE"
    else
        echo "無日誌文件"
    fi
}

# 主函數
main() {
    local command="${1:-help}"
    
    case "$command" in
        "full")
            full_maintenance
            ;;
        "check")
            init_log
            check_structure
            check_links
            check_deployment
            ;;
        "fix")
            init_log
            fix_links
            ;;
        "clean")
            init_log
            clean_cache
            ;;
        "backup")
            init_log
            backup_files
            ;;
        "structure")
            init_log
            check_structure
            ;;
        "report")
            init_log
            generate_report
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