#!/usr/bin/env python3
"""
測試部落格文章訪問
"""

import time
import requests

def test_url(url, description):
    """測試URL是否可訪問"""
    print(f"🔍 測試: {description}")
    print(f"   URL: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"   ✅ 狀態: {response.status_code} - 可訪問")
            return True
        else:
            print(f"   ⚠️  狀態: {response.status_code} - 可能還在部署中")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ❌ 錯誤: {e}")
        return False
    print()

def main():
    print("🌐 玻姆翻譯部落格訪問測試")
    print("==========================")
    print()
    
    # 等待一段時間讓部署完成
    print("⏳ 等待部署完成（建議等待2-5分鐘）...")
    print("   如果測試失敗，請稍後再試。")
    print()
    
    # 測試URL列表
    urls_to_test = [
        {
            "url": "https://nemo1999.github.io/BlogForBoBo/",
            "description": "部落格首頁"
        },
        {
            "url": "https://nemo1999.github.io/BlogForBoBo/toc/",
            "description": "目錄頁面"
        },
        {
            "url": "https://nemo1999.github.io/BlogForBoBo/philosophy/bohm/translation/chapter1/part2/2026/04/02/bohm-chapter-1-part2-translated.html",
            "description": "新文章（第9-16頁翻譯）"
        },
        {
            "url": "https://nemo1999.github.io/BlogForBoBo/philosophy/bohm/translation/chapter1/part1/2026/03/31/bohm-chapter-1-part1-translated.html",
            "description": "第一部分翻譯（第1-8頁）"
        }
    ]
    
    # 測試所有URL
    results = []
    for item in urls_to_test:
        success = test_url(item["url"], item["description"])
        results.append((item["description"], success))
        time.sleep(1)  # 避免請求過快
    
    print()
    print("📊 測試結果總結")
    print("--------------")
    
    all_success = True
    for desc, success in results:
        status = "✅ 通過" if success else "❌ 失敗"
        print(f"{status} - {desc}")
        if not success:
            all_success = False
    
    print()
    if all_success:
        print("🎉 所有測試通過！文章已成功部署。")
        print("   現在可以開始審核翻譯內容。")
    else:
        print("⚠️  部分測試失敗。")
        print("   可能原因：")
        print("   1. 部署還在進行中（等待2-5分鐘）")
        print("   2. GitHub Actions 工作流失敗")
        print("   3. 網絡連接問題")
        print()
        print("💡 建議：")
        print("   1. 檢查 GitHub Actions 狀態：https://github.com/Nemo1999/BlogForBoBo/actions")
        print("   2. 稍後再試")
        print("   3. 手動觸發重新部署")

if __name__ == "__main__":
    main()