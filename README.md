# VRInfo

一个用于追踪 **2025 年至今 VR 交互设计研究动向** 的轻量网站。

## 功能
- 首页提供 2025 年至今的研究趋势总结（聚焦 arXiv / ACM / IEEE）。
- 展示“今日成果卡片”，每张卡片附原文链接。
- 卡片抓取严格筛选 2025-01-01 之后的论文结果。
- 支持通过脚本按日期生成卡片数据。

## 如何访问网页
```bash
cd /workspace/VRInfo
python3 -m http.server 8000
# 浏览器打开 http://localhost:8000
```

如果你在远程开发机上运行，请先做端口转发，再访问映射后的 URL。

## 生成每日成果卡片
```bash
python3 scripts/generate_daily_card.py --date $(date +%F)
```

脚本会更新：
- `data/cards.json`

## 自动化（可选）
已提供 GitHub Actions 工作流：`.github/workflows/daily-card.yml`，默认每天自动更新一次卡片数据。


## 输出“今年起至今日”成果卡片
```bash
python3 scripts/generate_ytd_report.py --start $(date +%Y)-01-01 --end $(date +%F)
```

该命令会输出：
- 今日成果卡片（若已有论文则附原文直链）
- arXiv / ACM / IEEE 官方检索入口链接（可用于网络受限时手动查看原文）
