#!/bin/bash
# 設置 GitHub Pages 的腳本

echo "設置 GitHub Pages..."

# 添加 GitHub Pages 配置文件
cat > _config_pages.yml << EOF
# GitHub Pages 特定配置
remote_theme: pages-themes/minima@v0.2.0
plugins:
  - jekyll-remote-theme
  - jekyll-feed
  - jekyll-seo-tag

# 最小配置
title: "波波哲學筆記 | BoBo Philosophy Notes"
description: "大波與小波的哲學對話錄"
baseurl: "/BlogForBoBo"
url: "https://nemo1999.github.io"

# 作者信息
author:
  name: "大波 & 小波"
  email: "byprism.ask@gmail.com"
EOF

echo "創建 .nojekyll 文件以禁用 Jekyll 處理"
touch .nojekyll

echo "設置完成！"
echo "請在 GitHub 倉庫設置中啟用 GitHub Pages："
echo "1. 前往 https://github.com/Nemo1999/BlogForBoBo/settings/pages"
echo "2. 選擇 Source: GitHub Actions"
echo "3. 保存設置"