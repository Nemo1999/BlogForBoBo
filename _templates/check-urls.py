#!/usr/bin/env python3
"""
URL 檢查腳本
用於驗證 Jekyll 頁面的 URL 和連結正確性
"""

import os
import re
import sys
from pathlib import Path

def extract_front_matter(file_path):
    """提取文件的 front matter"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 匹配 front matter
    pattern = r'^---\n(.*?)\n---'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        return None
    
    front_matter = match.group(1)
    result = {}
    
    # 簡單解析 YAML
    for line in front_matter.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            # 處理數組值
            if value.startswith('[') and value.endswith(']'):
                # 簡單的數組解析
                items = value[1:-1].split(',')
                value = [item.strip().strip("'\"") for item in items if item.strip()]
            
            result[key] = value
    
    return result

def calculate_post_url(file_path, front_matter):
    """計算文章的預期 URL"""
    if not front_matter:
        return None
    
    # 獲取文件名
    filename = Path(file_path).name
    match = re.match(r'(\d{4})-(\d{2})-(\d{2})-(.+)\.md', filename)
    if not match:
        return None
    
    year, month, day, title = match.groups()
    
    # 獲取分類
    categories = front_matter.get('categories', [])
    if isinstance(categories, str):
        # 如果是字符串，嘗試解析
        if categories.startswith('[') and categories.endswith(']'):
            categories = categories[1:-1].split(',')
            categories = [cat.strip().strip("'\"") for cat in categories]
        else:
            categories = [categories]
    
    # 構建 URL 路徑
    if categories:
        category_path = '/'.join(categories)
        url = f"/{category_path}/{year}/{month}/{day}/{title}.html"
    else:
        url = f"/{year}/{month}/{day}/{title}.html"
    
    return url

def check_post_file(file_path):
    """檢查文章文件"""
    print(f"\n📄 檢查文件: {file_path}")
    
    front_matter = extract_front_matter(file_path)
    if not front_matter:
        print("  ⚠️  無法解析 front matter")
        return False
    
    # 檢查必要字段
    required_fields = ['layout', 'title', 'date']
    for field in required_fields:
        if field not in front_matter:
            print(f"  ❌ 缺少必要字段: {field}")
            return False
    
    # 檢查分類
    if 'categories' not in front_matter:
        print("  ⚠️  沒有設置分類")
    else:
        categories = front_matter['categories']
        if isinstance(categories, list):
            print(f"  ✅ 分類: {categories}")
            if len(categories) > 5:
                print(f"  ⚠️  分類層級過深 ({len(categories)} 層)")
        else:
            print(f"  ⚠️  分類格式可能不正確: {categories}")
    
    # 計算預期 URL
    expected_url = calculate_post_url(file_path, front_matter)
    if expected_url:
        print(f"  📍 預期 URL: {expected_url}")
        
        # 添加 baseurl
        full_url = f"/BlogForBoBo{expected_url}"
        print(f"  🔗 完整 URL: {full_url}")
    
    return True

def check_page_file(file_path):
    """檢查頁面文件"""
    print(f"\n📄 檢查文件: {file_path}")
    
    front_matter = extract_front_matter(file_path)
    if not front_matter:
        print("  ⚠️  無法解析 front matter")
        return False
    
    # 檢查必要字段
    required_fields = ['layout', 'title', 'permalink']
    for field in required_fields:
        if field not in front_matter:
            print(f"  ❌ 缺少必要字段: {field}")
            return False
    
    permalink = front_matter['permalink']
    print(f"  📍 Permalink: {permalink}")
    
    # 檢查 permalink 是否包含 baseurl
    if not permalink.startswith('/BlogForBoBo/'):
        print(f"  ⚠️  Permalink 可能缺少 baseurl: {permalink}")
        print(f"  💡 建議: /BlogForBoBo{permalink}")
    
    return True

def find_markdown_files(directory):
    """查找所有 Markdown 文件"""
    md_files = []
    for root, dirs, files in os.walk(directory):
        # 跳過模板目錄和隱藏目錄
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '_templates']
        
        for file in files:
            if file.endswith('.md'):
                full_path = os.path.join(root, file)
                md_files.append(full_path)
    
    return md_files

def main():
    """主函數"""
    print("🔍 Jekyll URL 檢查工具")
    print("=" * 50)
    
    # 設置工作目錄
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(base_dir)
    
    print(f"項目目錄: {project_dir}")
    
    # 查找所有 Markdown 文件
    md_files = find_markdown_files(project_dir)
    print(f"找到 {len(md_files)} 個 Markdown 文件")
    
    # 分類檢查
    posts_dir = os.path.join(project_dir, '_posts')
    post_files = []
    page_files = []
    
    for file_path in md_files:
        if '_posts' in file_path:
            post_files.append(file_path)
        else:
            page_files.append(file_path)
    
    print(f"\n📚 文章文件 (_posts/): {len(post_files)} 個")
    print(f"📄 頁面文件: {len(page_files)} 個")
    
    # 檢查文章文件
    print("\n" + "=" * 50)
    print("檢查文章文件")
    print("=" * 50)
    
    post_errors = 0
    for file_path in post_files:
        if not check_post_file(file_path):
            post_errors += 1
    
    # 檢查頁面文件
    print("\n" + "=" * 50)
    print("檢查頁面文件")
    print("=" * 50)
    
    page_errors = 0
    for file_path in page_files:
        if not check_page_file(file_path):
            page_errors += 1
    
    # 總結
    print("\n" + "=" * 50)
    print("檢查總結")
    print("=" * 50)
    
    total_errors = post_errors + page_errors
    if total_errors == 0:
        print("✅ 所有文件檢查通過！")
    else:
        print(f"❌ 發現 {total_errors} 個問題：")
        print(f"  - 文章文件: {post_errors} 個問題")
        print(f"  - 頁面文件: {page_errors} 個問題")
    
    print("\n💡 建議：")
    print("1. 部署前運行此腳本檢查所有文件")
    print("2. 修復所有警告和錯誤")
    print("3. 測試實際的 URL 可訪問性")
    
    return total_errors

if __name__ == '__main__':
    sys.exit(main())