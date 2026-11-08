# 个人代理与直连规则

## 文件用途

| 文件 | 用途 |
| --- | --- |
| `SelfProxy.list` | 手工维护的个人代理规则，当前 38 个 PT 站，全部精确匹配 |
| `SelfDirect.list` | 手工维护的个人直连规则，当前为空，原 IP 与域名规则已移除 |
| `Proxy.list` | 生成的 QX 代理订阅，默认策略名为“代理” |
| `Direct.list` | 生成的 QX 直连订阅，默认策略为 `direct` |
| `advertising.list` | 独立保留的广告屏蔽列表 |

个人直连例外在两个 INI 模板中优先于个人代理；两者均在公共规则之前。同一地址不要同时写入两个个人源列表。

## 精确匹配

用户指定的 38 个 PT 网站在 `SelfProxy.list` 使用 `DOMAIN`，QX 输出 `host`。保留网址的完整主机名，包括 `www`、`pt` 等前缀；不扩展到父域名或子域名。规则不区分同一主机名下的协议、端口和 URL 路径。

```text
# 代理源文件写法
DOMAIN,pt.example.com
```

生成后为 `host,pt.example.com,代理`，仅匹配 `pt.example.com`，不匹配 `example.com` 或 `other.pt.example.com`。

PT 大全、相关来源快照和模板引用均已移除。现有 INI 中仍有原有公共分流规则；未命中个人规则的地址仍可能被其他公共规则匹配。独立 tracker、CDN 或跳转后的其他主机名不自动加入个人列表。

## QX 导入

将以下两行加入现有配置的 `[filter_remote]` 段，把个人规则排在公共规则之前，并确认客户端实际匹配顺序。已有 `[filter_local]` 规则也可能影响匹配。

```ini
https://raw.githubusercontent.com/Quanyuqing/proxy-rules/fenliu/Direct.list, tag=个人直连, force-policy=direct, enabled=true
https://raw.githubusercontent.com/Quanyuqing/proxy-rules/fenliu/Proxy.list, tag=个人代理, force-policy=代理, enabled=true
```

将 `force-policy=代理` 改为你现有的代理策略组或节点名称，并选择实际代理节点。`force-policy` 覆盖文件内的策略名称，无需编辑生成文件。

广告列表按需单独导入：

```ini
https://raw.githubusercontent.com/Quanyuqing/proxy-rules/fenliu/advertising.list, tag=广告屏蔽, force-policy=reject, enabled=true
```

旧的 `QuantumultX/Proxy.list`、`QuantumultX/Direct.list` 订阅需要替换为上述根目录新地址；同时移除旧 `QuantumultX/PT.list` 订阅。原 `PT.list` 地址已停用。

官方格式参考：https://github.com/crossutility/Quantumult-X/blob/master/sample.conf

## 日常维护

只编辑 `SelfProxy.list`、`SelfDirect.list`，不要直接编辑 `Proxy.list`、`Direct.list`。

代理列表使用 `DOMAIN,完整主机名`，不要改成后缀匹配。直连列表当前为空；个人 VPS IP 不写入公开仓库。支持 `DOMAIN`、`DOMAIN-SUFFIX`、`IP-CIDR`、`IP-CIDR6`，源文件不填写策略名称；IP 规则可保留 `no-resolve`，QX 输出会省略这个 Clash 参数。

```sh
python3 scripts/build_rules.py
```

把修改后的源文件和两个生成文件一并提交。脚本只做本地格式转换与去重，不联网、不自动添加域名。

## 保留的配置

`self.ini` 与 `4125.ini` 引用 `SelfDirect.list`、`SelfProxy.list`；个人代理交给 `🚀 节点选择`。该组保留原有 DIRECT 选项，需选择代理节点才会走代理。

`Config for Clash.yaml` 是独立配置，没有接入个人列表；广告列表、两个 INI 和该 Clash 配置均按用户要求保留。
