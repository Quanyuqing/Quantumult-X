# 个人代理与直连规则

PT 默认代理。个人直连作为例外优先于 PT 代理；个人代理也放在公共分流之前。同一地址不要同时写入两个个人列表。

| 手工维护的文件 | 用途 |
| --- | --- |
| `SelfDirect.list` | 个人直连例外，保留原有 VPS IP 与域名规则 |
| `SelfProxy.list` | 个人代理例外，目前为空，可继续添加 |
| `sources/pt-sites.json` | PT 站来源快照，记录全部 338 站及当前、旧网址和关闭标记 |

个人列表使用不带策略名称的规则，每行一条，例如：

```text
DOMAIN-SUFFIX,example.com
DOMAIN,api.example.com
IP-CIDR,192.0.2.0/24,no-resolve
IP-CIDR6,2001:db8::/32,no-resolve
```

修改后在仓库根目录运行：

```sh
python3 scripts/build_rules.py
```

将个人列表和生成结果一起提交。`QuantumultX/*.list`、`PT.list` 是生成文件，不直接编辑。QX 原生 IP 规则不输出 Clash 的 `no-resolve` 参数。

## QX 导入

将下面三行追加到你现有配置的 `[filter_remote]` 段，不要重复创建段。把它们放在公共规则资源之前，并在 QX 中确认匹配顺序。已有 `[filter_local]` 规则也可能影响最终匹配。

```ini
https://raw.githubusercontent.com/Quanyuqing/Quantumult-X/fenliu/QuantumultX/Direct.list, tag=个人直连, force-policy=direct, enabled=true
https://raw.githubusercontent.com/Quanyuqing/Quantumult-X/fenliu/QuantumultX/Proxy.list, tag=个人代理, force-policy=代理, enabled=true
https://raw.githubusercontent.com/Quanyuqing/Quantumult-X/fenliu/QuantumultX/PT.list, tag=PT代理, force-policy=代理, enabled=true
```

`代理` 必须是你 QX 中已经存在的代理策略组或节点名。若实际叫 `节点选择` 或其他名字，将上面两处 `force-policy=代理` 改为实际名称。`force-policy` 会覆盖规则文件中的策略名称，因此无需修改生成文件。选择实际代理节点后生效，仓库不包含你的节点配置。

官方格式参考：https://github.com/crossutility/Quantumult-X/blob/master/sample.conf

## 订阅转换模板

`self.ini` 与 `4125.ini` 已引用根目录的三个列表，顺序是个人直连、个人代理、PT 代理，再匹配其他公共规则。PT 与个人代理交给原有 `🚀 节点选择` 策略组。该策略组仍保留原有 DIRECT 选项，需要选择代理节点才会实际走代理。

根目录 `Config for Clash.yaml` 是另一份独立配置，没有使用上述 INI 模板；本次未接入此独立配置。

## PT 覆盖范围与更新

来源固定为 PT-depiler 提交 `25430f987fb1a8313cf27ba7200cba8f7ec80347`，提取日期 2026-11-08。

生成规则覆盖 249 个未被来源标记关闭的私有站点，311 个去重后的当前域名。公开 BT 站、89 个已标记关闭的 PT 站、旧网址不进入生效规则。来源中的关闭状态不代表逐站联网验证的结果。

仅按配置网址的 hostname 生成 `DOMAIN-SUFFIX` / `host-suffix`，忽略协议、端口、路径；不猜测父域名、tracker 或 CDN 地址。该规则覆盖 PT 网页访问，无法保证覆盖站点的独立 tracker，更不会配置其他 BT 客户端的代理。

更新某个站点时，在 `sources/pt-sites.json` 中修改其 `urls` 或 `isDead`，再运行生成脚本。批量更新上游时，需要重新核对并替换来源快照，同时更新提交号与提取日期；生成脚本本身不联网。
