# 虚拟环境与质量复验
推荐Python 3.11+；仅stdlib，无需pip安装。不要把本地.venv提交进Git。
```bash
python3 -m venv .venv
. .venv/bin/activate
python -m unittest discover -s tests -v
python scripts/score_opportunities.py data/opportunities.csv
```
本轮已于隔离虚拟环境 Python 3.13.5 验证 5/5 单元测试通过、8条商机CSV可评分。注意**所有hard_gate=unknown**，总分排序不产生“客户意愿已验证”结论。
CI/未来Agent复验：每次修改脚本、CSV、门槛规则都跑测试；修改硬门槛需红队审查；数据不得含客户未授权信息。源文件每轮更新后检测链接健康度/发布时间，避免沿用过期政策。
