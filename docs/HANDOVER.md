# 维护交接

本地源码：`/srv/codex-workspace/Quantumult-X`。远端：`Quanyuqing/proxy-rules`，分支 `fenliu`。

当前只维护个人代理、直连和用户要求保留的广告规则、两个 INI、独立 Clash YAML。清理时用户要求逐项决定，勿自行删除已明确保留的文件。

个人代理源 `SelfProxy.list` 含 38 个 MP 站点，全部 DOMAIN 精确匹配，保留 www、pt 等前缀。Moment 已删除。憨憨保留用户提供的 hhan.club；PT-depiler 使用 hhanclub.net，Jackett 同时收录两者，未经用户要求不要替换。

个人直连源为 `SelfDirect.list`，用户已在 GitHub 清空全部规则；生成的 Direct.list 同步清空，个人 IP 与域名不再保留。运行 `python3 scripts/build_rules.py` 生成根目录 `Proxy.list`、`Direct.list`。两个 INI 已引用个人源列表；Clash YAML 是独立配置。

PT 大全、sources/pt-sites.json 和 QuantumultX 目录已按简化要求移除；不要重新生成或恢复后缀匹配的 PT 大全。旧 QX 订阅需更换为根目录链接，移除旧 PT 订阅。说明见 docs/RULES.md。

INI 保持原有 CRLF，空白检查用 `git -c core.whitespace=cr-at-eol diff --check`。未在用户 iOS QX 客户端实测。不要把 Clash YAML 中的订阅 token 复制到日志、文档或新文件。

用户指出直连列表泄露 VPS IP，已从当前源文件和 QX 生成文件移除。旧 Git 提交仍可能包含 IP，未经明确授权不强制推送重写历史。以后不要把私人 VPS IP 写入公开仓库。
