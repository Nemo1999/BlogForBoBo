#!/usr/bin/env python3
"""
實際測試所有玻姆相關連結
"""

import requests
import time

def test_link(base_url, path, description):
    """測試單個連結"""
    url = f"{base_url}{path}"
    print(f"🔍 測試: {description}")
    print(f"   URL: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"   ✅ 狀態: {response.status_code} - 可訪問")
            return True, url
        elif response.status_code == 404:
            print(f"   ❌ 狀態: {response.status_code} - 未找到（可能還在部署）")
            return False, url
        else:
            print(f"   ⚠️  狀態: {response.status_code}")
            return False, url
    except requests.exceptions.RequestException as e:
        print(f"   ❌ 錯誤: {e}")
        return False, url
    print()

def main():
    base_url = "https://nemo1999.github.io"
    
    print("🌐 實際測試玻姆翻譯連結")
    print("========================")
    print()
    
    # 所有需要測試的連結
    links = [
        # 新文章
        {
            "path": "/BlogForBoBo/philosophy/bohm/translation/chapter1/part2/2026/04/02/bohm-chapter-1-part2-translated.html",
            "desc": "新文章：第9-16頁翻譯"
        },
        # 目錄和導航
        {
            "path": "/BlogForBoBo/toc/",
            "desc": "目錄頁面"
        },
        {
            "path": "/BlogForBoBo/",
            "desc": "部落格首頁"
        },
        # 現有玻姆文章
        {
            "path": "/BlogForBoBo/philosophy/bohm/material/2026/03/31/bohm-chapter-1-material.html",
            "desc": "素材篇（精華版）"
        },
        {
            "path": "/BlogForBoBo/philosophy/bohm/complete/translation/2026/03/31/bohm-chapter-1-complete-part1.html",
            "desc": "完整翻譯第一部分"
        },
        {
            "path": "/BlogForBoBo/philosophy/bohm/complete/translation/2026/03/31/bohm-chapter-1-complete-part2.html",
            "desc": "完整翻譯第二部分框架"
        },
        {
            "path": "/BlogForBoBo/philosophy/bohm/complete/translation/2026/03/31/bohm-chapter-1-complete-part3.html",
            "desc": "完整翻譯第三部分框架"
        },
        {
            "path": "/BlogForBoBo/philosophy/bohm/complete/translation/2026/03/31/bohm-chapter-1-complete-part4.html",
            "desc": "完整翻譯第四部分框架"
        }
    ]
    
    results = []
    working_links = []
    broken_links = []
    
    for link in links:
        success, url = test_link(base_url, link["path"], link["desc"])
        results.append((link["desc"], success, url))
        
        if success:
            working_links.append((link["desc"], url))
        else:
            broken_links.append((link["desc"], url))
        
        time.sleep(1)  # 避免請求過快
    
    print()
    print("📊 測試結果總結")
    print("--------------")
    print(f"✅ 可訪問: {len(working_links)} 個")
    print(f"❌ 不可訪問: {len(broken_links)} 個")
    print()
    
    if working_links:
        print("✅ 可訪問的連結:")
        for desc, url in working_links:
            print(f"   • {desc}")
            print(f"     {url}")
        print()
    
    if broken_links:
        print("❌ 不可訪問的連結（需要檢查）:")
        for desc, url in broken_links:
            print(f"   • {desc}")
            print(f"     {url}")
        print()
    
    # 檢查GitHub Actions狀態
    print("🔧 問題診斷")
    print("-----------")
    print("如果新文章不可訪問，可能原因:")
    print("1. GitHub Pages 部署還在進行中（通常需要2-10分鐘）")
    print("2. 文件路徑或分類設置錯誤")
    print("3. GitHub Actions 工作流失敗")
    print()
    print("💡 解決方案:")
    print("1. 檢查部署狀態: https://github.com/Nemo1999/BlogForBoBo/actions")
    print("2. 驗證文件路徑和分類設置")
    print("3. 等待幾分鐘後重試")
    print("4. 手動觸發重新部署")

if __name__ == "__main__":
    main()