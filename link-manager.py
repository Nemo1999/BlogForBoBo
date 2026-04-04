#!/usr/bin/env python3
"""
部落格連結管理器
作者：小波 👁️
創建時間：2026-04-04

功能：
1. 掃描所有 Markdown 文件中的連結
2. 檢查連結有效性
3. 生成連結報告
4. 修復常見連結問題
"""

import os
import re
import sys
import json
import requests
from pathlib import Path
from urllib.parse import urlparse, urljoin
from typing import List, Dict, Tuple, Set

class BlogLinkManager:
    def __init__(self, blog_root: str):
        self.blog_root = Path(blog_root).resolve()
        self.links_found = []  # 找到的所有連結
        self.broken_links = []  # 無效連結
        self.duplicate_links = {}  # 重複連結
        
    def scan_markdown_files(self) -> List[Path]:
        """掃描所有 Markdown 文件"""
        markdown_files = []
        for root, dirs, files in os.walk(self.blog_root):
            # 跳過 vendor 目錄
            if 'vendor' in root:
                continue
                
            for file in files:
                if file.endswith('.md'):
                    markdown_files.append(Path(root) / file)
        
        print(f"📁 找到 {len(markdown_files)} 個 Markdown 文件")
        return markdown_files
    
    def extract_links_from_file(self, file_path: Path) -> List[Dict]:
        """從文件中提取所有連結"""
        links = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 匹配 Markdown 連結 [text](url)
            md_link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
            for match in re.finditer(md_link_pattern, content):
                link_text = match.group(1)
                link_url = match.group(2)
                
                # 跳過外部連結和錨點
                if link_url.startswith('http') or link_url.startswith('#') or link_url.startswith('mailto:'):
                    continue
                
                # 計算行號
                line_number = content[:match.start()].count('\n') + 1
                
                links.append({
                    'file': str(file_path.relative_to(self.blog_root)),
                    'line': line_number,
                    'text': link_text,
                    'url': link_url,
                    'full_path': self._resolve_link_path(file_path, link_url)
                })
        
        except Exception as e:
            print(f"❌ 讀取文件 {file_path} 時出錯: {e}")
        
        return links
    
    def _resolve_link_path(self, source_file: Path, link_url: str) -> Path:
        """解析連結的完整路徑"""
        # 如果是絕對路徑（以 / 開頭）
        if link_url.startswith('/'):
            # 移除開頭的 /BlogForBoBo/（如果存在）
            if link_url.startswith('/BlogForBoBo/'):
                link_url = link_url[13:]  # 移除 '/BlogForBoBo/'
            return self.blog_root / link_url.lstrip('/')
        
        # 如果是相對路徑
        source_dir = source_file.parent
        return (source_dir / link_url).resolve()
    
    def check_link_validity(self, link_info: Dict) -> bool:
        """檢查連結是否有效"""
        full_path = link_info['full_path']
        
        # 檢查文件是否存在
        if not full_path.exists():
            link_info['error'] = f"文件不存在: {full_path}"
            return False
        
        # 檢查是否是目錄
        if full_path.is_dir():
            # 如果是目錄，檢查是否有 index.html 或 index.md
            index_files = ['index.html', 'index.md', 'README.md']
            for index_file in index_files:
                if (full_path / index_file).exists():
                    return True
            link_info['error'] = f"目錄缺少索引文件: {full_path}"
            return False
        
        return True
    
    def scan_all_links(self):
        """掃描所有連結"""
        print("🔍 開始掃描部落格連結...")
        
        markdown_files = self.scan_markdown_files()
        
        for file_path in markdown_files:
            links = self.extract_links_from_file(file_path)
            self.links_found.extend(links)
        
        print(f"📊 找到 {len(self.links_found)} 個內部連結")
        
        # 檢查連結有效性
        for link in self.links_found:
            if not self.check_link_validity(link):
                self.broken_links.append(link)
        
        print(f"❌ 發現 {len(self.broken_links)} 個無效連結")
        
        # 檢查重複連結
        self._find_duplicate_links()
    
    def _find_duplicate_links(self):
        """查找重複連結"""
        url_count = {}
        
        for link in self.links_found:
            url = link['url']
            if url in url_count:
                url_count[url].append(link)
            else:
                url_count[url] = [link]
        
        # 找出重複的連結
        for url, links in url_count.items():
            if len(links) > 1:
                self.duplicate_links[url] = links
    
    def generate_report(self) -> str:
        """生成報告"""
        report = []
        report.append("# 部落格連結檢查報告")
        report.append(f"生成時間: {self._current_timestamp()}")
        report.append("")
        
        # 總體統計
        report.append("## 📊 總體統計")
        report.append(f"- 掃描文件數: {len(self.scan_markdown_files())}")
        report.append(f"- 找到連結數: {len(self.links_found)}")
        report.append(f"- 無效連結數: {len(self.broken_links)}")
        report.append(f"- 重複連結數: {len(self.duplicate_links)}")
        report.append("")
        
        # 無效連結詳情
        if self.broken_links:
            report.append("## ❌ 無效連結列表")
            for link in self.broken_links:
                report.append(f"### {link['file']}:{link['line']}")
                report.append(f"- 連結文字: {link['text']}")
                report.append(f"- 連結 URL: {link['url']}")
                report.append(f"- 完整路徑: {link['full_path']}")
                report.append(f"- 錯誤信息: {link.get('error', '未知錯誤')}")
                report.append("")
        
        # 重複連結詳情
        if self.duplicate_links:
            report.append("## 🔄 重複連結列表")
            for url, links in self.duplicate_links.items():
                report.append(f"### 連結: {url}")
                report.append(f"出現次數: {len(links)}")
                report.append("出現位置:")
                for link in links:
                    report.append(f"  - {link['file']}:{link['line']} - {link['text']}")
                report.append("")
        
        # 所有連結列表
        report.append("## 📋 所有連結列表")
        report.append("| 文件 | 行號 | 連結文字 | 連結 URL | 狀態 |")
        report.append("|------|------|----------|----------|------|")
        
        for link in self.links_found:
            status = "✅ 有效" if link not in self.broken_links else "❌ 無效"
            report.append(f"| {link['file']} | {link['line']} | {link['text']} | {link['url']} | {status} |")
        
        return "\n".join(report)
    
    def fix_common_issues(self):
        """修復常見問題"""
        print("🔧 開始修復常見連結問題...")
        
        fixes_applied = 0
        
        for link in self.broken_links:
            if self._try_fix_link(link):
                fixes_applied += 1
        
        print(f"✅ 應用了 {fixes_applied} 個修復")
        
        # 重新掃描檢查修復效果
        if fixes_applied > 0:
            print("🔄 重新掃描檢查修復效果...")
            self.links_found = []
            self.broken_links = []
            self.duplicate_links = {}
            self.scan_all_links()
    
    def _try_fix_link(self, link_info: Dict) -> bool:
        """嘗試修復單個連結"""
        full_path = link_info['full_path']
        original_url = link_info['url']
        
        # 嘗試添加 .html 擴展名
        if not full_path.suffix:
            html_path = full_path.with_suffix('.html')
            if html_path.exists():
                # 更新連結
                new_url = original_url + '.html'
                if self._update_link_in_file(link_info, new_url):
                    print(f"✅ 修復: {original_url} → {new_url}")
                    return True
        
        # 嘗試添加 .md 擴展名
        if not full_path.suffix:
            md_path = full_path.with_suffix('.md')
            if md_path.exists():
                new_url = original_url + '.md'
                if self._update_link_in_file(link_info, new_url):
                    print(f"✅ 修復: {original_url} → {new_url}")
                    return True
        
        # 嘗試修復路徑大小寫
        if full_path.exists():
            # 路徑正確但大小寫可能有問題
            actual_path = self._find_case_insensitive_path(full_path)
            if actual_path and actual_path != full_path:
                # 計算相對路徑
                source_file = self.blog_root / link_info['file']
                relative_path = os.path.relpath(actual_path, source_file.parent)
                if self._update_link_in_file(link_info, relative_path):
                    print(f"✅ 修復大小寫: {original_url} → {relative_path}")
                    return True
        
        return False
    
    def _find_case_insensitive_path(self, path: Path) -> Path:
        """查找大小寫不敏感的路徑"""
        if path.exists():
            return path
        
        parent = path.parent
        if not parent.exists():
            return None
        
        target_name = path.name.lower()
        for item in parent.iterdir():
            if item.name.lower() == target_name:
                return item
        
        return None
    
    def _update_link_in_file(self, link_info: Dict, new_url: str) -> bool:
        """在文件中更新連結"""
        try:
            file_path = self.blog_root / link_info['file']
            
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            line_index = link_info['line'] - 1
            original_line = lines[line_index]
            
            # 替換連結 URL
            old_url = link_info['url']
            new_line = original_line.replace(f'({old_url})', f'({new_url})')
            
            if new_line != original_line:
                lines[line_index] = new_line
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                
                return True
        
        except Exception as e:
            print(f"❌ 更新文件 {file_path} 時出錯: {e}")
        
        return False
    
    def _current_timestamp(self):
        """獲取當前時間戳"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def save_report(self, output_file: str = "link-report.md"):
        """保存報告到文件"""
        report = self.generate_report()
        
        output_path = self.blog_root / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📄 報告已保存到: {output_path}")
    
    def print_summary(self):
        """打印摘要"""
        print("\n" + "="*50)
        print("📋 連結檢查摘要")
        print("="*50)
        print(f"📁 部落格根目錄: {self.blog_root}")
        print(f"📄 掃描文件數: {len(self.scan_markdown_files())}")
        print(f"🔗 找到連結數: {len(self.links_found)}")
        print(f"❌ 無效連結數: {len(self.broken_links)}")
        print(f"🔄 重複連結數: {len(self.duplicate_links)}")
        
        if self.broken_links:
            print("\n⚠️  發現無效連結:")
            for link in self.broken_links[:5]:  # 只顯示前5個
                print(f"  - {link['file']}:{link['line']}: {link['text']} → {link['url']}")
            if len(self.broken_links) > 5:
                print(f"  ... 還有 {len(self.broken_links) - 5} 個")
        
        if self.duplicate_links:
            print("\n⚠️  發現重複連結:")
            for url, links in list(self.duplicate_links.items())[:3]:  # 只顯示前3個
                print(f"  - {url}: 出現 {len(links)} 次")

def main():
    """主函數"""
    import argparse
    
    parser = argparse.ArgumentParser(description='部落格連結管理器')
    parser.add_argument('--scan', action='store_true', help='掃描所有連結')
    parser.add_argument('--fix', action='store_true', help='嘗試修復常見問題')
    parser.add_argument('--report', action='store_true', help='生成報告')
    parser.add_argument('--blog-root', default='.', help='部落格根目錄')
    
    args = parser.parse_args()
    
    # 默認掃描
    if not any([args.scan, args.fix, args.report]):
        args.scan = True
        args.report = True
    
    manager = BlogLinkManager(args.blog_root)
    
    if args.scan:
        manager.scan_all_links()
        manager.print_summary()
    
    if args.fix:
        manager.fix_common_issues()
    
    if args.report:
        manager.save_report()

if __name__ == "__main__":
    main()