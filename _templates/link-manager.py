#!/usr/bin/env python3
"""
連結管理器 - 確保所有連結正確更新和可訪問
"""

import os
import re
import json
import requests
from pathlib import Path
from datetime import datetime

class LinkManager:
    def __init__(self, blog_dir):
        self.blog_dir = Path(blog_dir)
        self.links_db = self.blog_dir / "data" / "links.json"
        self.links_db.parent.mkdir(exist_ok=True)
        
    def scan_all_links(self):
        """掃描所有文件中的連結"""
        print("🔍 掃描部落格中的所有連結...")
        
        all_links = {
            "internal": [],  # 內部連結
            "external": [],  # 外部連結
            "broken": [],    # 斷開的連結
            "files": {}      # 每個文件的連結
        }
        
        # 掃描所有Markdown文件
        for md_file in self.blog_dir.rglob("*.md"):
            if md_file.is_file():
                relative_path = md_file.relative_to(self.blog_dir)
                file_links = self.extract_links_from_file(md_file)
                all_links["files"][str(relative_path)] = file_links
        
        # 保存掃描結果
        self.save_links_db(all_links)
        return all_links
    
    def extract_links_from_file(self, file_path):
        """從文件中提取所有連結"""
        links = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # 匹配Markdown連結 [text](url)
            md_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
            for text, url in md_links:
                links.append({
                    "text": text,
                    "url": url,
                    "type": "markdown",
                    "line": self.get_line_number(content, text)
                })
            
            # 匹配HTML連結 <a href="...">
            html_links = re.findall(r'<a\s+[^>]*href="([^"]*)"[^>]*>', content)
            for url in html_links:
                links.append({
                    "text": "",
                    "url": url,
                    "type": "html",
                    "line": self.get_line_number(content, url)
                })
            
        except Exception as e:
            print(f"❌ 讀取文件 {file_path} 時出錯: {e}")
        
        return links
    
    def get_line_number(self, content, text):
        """獲取文本在內容中的行號"""
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if text in line:
                return i
        return 0
    
    def check_link_accessibility(self, url, base_url="https://nemo1999.github.io"):
        """檢查連結可訪問性"""
        # 處理相對連結
        if url.startswith('/'):
            full_url = base_url + url
        elif url.startswith('http'):
            full_url = url
        else:
            # 相對路徑，需要更多處理
            return None
        
        try:
            response = requests.get(full_url, timeout=5)
            return {
                "url": url,
                "full_url": full_url,
                "status": response.status_code,
                "accessible": response.status_code == 200,
                "checked_at": datetime.now().isoformat()
            }
        except requests.exceptions.RequestException as e:
            return {
                "url": url,
                "full_url": full_url,
                "status": "error",
                "accessible": False,
                "error": str(e),
                "checked_at": datetime.now().isoformat()
            }
    
    def find_broken_links(self):
        """查找斷開的連結"""
        print("🔧 檢查連結可訪問性...")
        
        if not self.links_db.exists():
            print("⚠️  未找到連結數據庫，先運行掃描")
            self.scan_all_links()
        
        with open(self.links_db, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        broken_links = []
        
        for file_path, links in data["files"].items():
            for link in links:
                result = self.check_link_accessibility(link["url"])
                if result and not result["accessible"]:
                    broken_links.append({
                        "file": file_path,
                        "line": link.get("line", 0),
                        "text": link["text"],
                        "url": link["url"],
                        "result": result
                    })
        
        return broken_links
    
    def update_links_in_file(self, file_path, old_url, new_url):
        """更新文件中的連結"""
        try:
            content = Path(file_path).read_text(encoding='utf-8')
            
            # 替換連結
            new_content = content.replace(old_url, new_url)
            
            if new_content != content:
                Path(file_path).write_text(new_content, encoding='utf-8')
                print(f"✅ 更新 {file_path}: {old_url} → {new_url}")
                return True
            else:
                print(f"⚠️  未找到連結: {old_url} 在 {file_path}")
                return False
                
        except Exception as e:
            print(f"❌ 更新文件 {file_path} 時出錯: {e}")
            return False
    
    def save_links_db(self, data):
        """保存連結數據庫"""
        data["last_updated"] = datetime.now().isoformat()
        with open(self.links_db, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"💾 連結數據庫已保存: {self.links_db}")
    
    def generate_link_report(self):
        """生成連結報告"""
        if not self.links_db.exists():
            print("⚠️  未找到連結數據庫")
            return
        
        with open(self.links_db, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "total_files": len(data["files"]),
            "total_links": sum(len(links) for links in data["files"].values()),
            "broken_links": self.find_broken_links(),
            "files_with_links": []
        }
        
        for file_path, links in data["files"].items():
            if links:
                report["files_with_links"].append({
                    "file": file_path,
                    "link_count": len(links)
                })
        
        # 保存報告
        report_file = self.blog_dir / "data" / "link_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"📊 連結報告已生成: {report_file}")
        return report

def main():
    blog_dir = "/home/nemo/.openclaw/workspace/BlogForBoBo"
    manager = LinkManager(blog_dir)
    
    print("🔗 連結管理器")
    print("=============")
    print()
    
    # 掃描所有連結
    print("1. 掃描所有連結...")
    manager.scan_all_links()
    print()
    
    # 檢查可訪問性
    print("2. 檢查連結可訪問性...")
    broken_links = manager.find_broken_links()
    
    if broken_links:
        print(f"❌ 發現 {len(broken_links)} 個斷開的連結:")
        for link in broken_links:
            print(f"   • {link['file']}:{link['line']}")
            print(f"     {link['text']} → {link['url']}")
            print(f"     狀態: {link['result'].get('status', 'unknown')}")
        print()
    else:
        print("✅ 所有連結都可訪問")
        print()
    
    # 生成報告
    print("3. 生成連結報告...")
    report = manager.generate_link_report()
    
    if report and report["broken_links"]:
        print(f"📋 報告摘要:")
        print(f"   總文件數: {report['total_files']}")
        print(f"   總連結數: {report['total_links']}")
        print(f"   斷開連結: {len(report['broken_links'])}")
        print()
        print("💡 建議:")
        print("   1. 修復所有斷開的連結")
        print("   2. 定期運行此腳本檢查")
        print("   3. 部署前驗證所有連結")
    else:
        print("🎉 所有連結正常！")

if __name__ == "__main__":
    main()