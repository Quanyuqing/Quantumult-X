# 维护交接

本地源码：`/srv/codex-workspace/Quantumult-X`。远端：`Quanyuqing/Quantumult-X`，维护分支 `fenliu`。

用户要求维护个人代理、直连列表，并根据 PT-depiler 站点列表生成 PT 规则；已明确 PT 默认代理。个人直连例外优先。

入口见 `docs/RULES.md`。个人源列表为 `SelfDirect.list`、`SelfProxy.list`；PT 来源为固定提交的 `sources/pt-sites.json`。运行 `python3 scripts/build_rules.py` 生成 `PT.list` 和 `QuantumultX/*.list`。两个 INI 模板已接入。独立 Clash YAML 未接入。

已校验来源覆盖、ROT13 解码、去重、生成幂等性及 INI 引用顺序；未在用户 iOS QX 客户端实测。INI 保持原有 CRLF，检查空白时用 `git -c core.whitespace=cr-at-eol diff --check`。

勿将仓库中的订阅 token 复制到说明、日志或新文件。

个人代理列表现已加入用户从 MoviePilot 提供的 39 个站点，使用 DOMAIN 精确主机名匹配，QX 输出 host；不要改为后缀匹配，也不要去掉 www、pt 等前缀。PT 大全仍单独保留。清理阶段用户要求逐项决定删除或保留；advertising.list、Clash YAML、两个 INI 和 SelfDirect.list 明确保留。

用户随后要求删除 Moment：个人代理列表现为 38 个站点。憨憨目前保留用户提供的 hhan.club；核对 PT-depiler 主域名为 hhanclub.net，Jackett 同时列出 hhanclub.net 与 hhan.club，旧域名为 hhanclub.top。尚未按查询结果改动憨憨规则。
