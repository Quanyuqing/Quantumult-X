# proxy-rules

个人代理、直连和广告屏蔽规则，支持 Quantumult X 和订阅转换模板。

## QX 订阅

| 用途 | 订阅地址 |
| --- | --- |
| 个人代理 | [Proxy.list](https://raw.githubusercontent.com/Quanyuqing/proxy-rules/fenliu/Proxy.list) |
| 个人直连 | [Direct.list](https://raw.githubusercontent.com/Quanyuqing/proxy-rules/fenliu/Direct.list) |
| 广告屏蔽 | [advertising.list](https://raw.githubusercontent.com/Quanyuqing/proxy-rules/fenliu/advertising.list) |

个人代理包含用户提供的 38 个 PT 站点，使用精确域名匹配，保留 `www`、`pt` 等完整主机名前缀。Moment 已移除，憨憨保留 `hhan.club`。没有附加 PT 大全规则。

QX 导入个人代理时，将策略指定为现有的代理策略组；直连指定 `direct`。广告列表使用“广告屏蔽”策略，导入时可指定为 `reject`。详细步骤见 [规则说明](docs/RULES.md)。

## 维护

- `SelfProxy.list`：手工维护的个人代理源规则。
- `SelfDirect.list`：手工维护的个人直连源规则。
- `Proxy.list`、`Direct.list`：脚本生成的 QX 订阅文件。
- `self.ini`、`4125.ini`：订阅转换模板，引用两个个人源列表和原有公共规则。
- `Config for Clash.yaml`：保留的独立 Clash 配置。
- `advertising.list`：保留的广告屏蔽规则。

修改源列表后，运行并将源文件、生成文件一起提交：

```sh
python3 scripts/build_rules.py
```

此处仅维护域名与 IP 分流规则；PT 站点的独立 tracker 域名需按需要另行添加。

## 隐私维护

本仓库只保存可公开的分流规则及示例模板。真实节点、私人 IP、订阅 token 和私人订阅地址不放入仓库。`Config for Clash.yaml` 的订阅地址是不可用的占位示例，使用前请在本地替换。

本次已重写历史以清理曾经公开的订阅凭据和私人 IP；旧克隆不要合并或推回远端，应重新克隆。凭据是否失效取决于原服务是否已重置，清理 Git 不会自动撤销凭据。
