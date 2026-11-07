#!/usr/bin/env python3
"""Generate QX rules from personal lists and the pinned PT source snapshot."""
import ipaddress
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
QX_TYPES = {'DOMAIN': 'host', 'DOMAIN-SUFFIX': 'host-suffix',
            'IP-CIDR': 'ip-cidr', 'IP-CIDR6': 'ip6-cidr'}


def read_rules(path):
    result = []
    for number, line in enumerate(path.read_text().splitlines(), 1):
        line = line.strip()
        if not line or line.startswith(('#', ';', '//')):
            continue
        fields = [part.strip() for part in line.split(',')]
        if len(fields) not in (2, 3) or fields[0] not in QX_TYPES:
            raise ValueError(f'{path.name}:{number}: unsupported rule: {line}')
        kind, value = fields[:2]
        if len(fields) == 3 and (fields[2] != 'no-resolve' or not kind.startswith('IP-')):
            raise ValueError(f'{path.name}:{number}: invalid option')
        if kind.startswith('IP-'):
            network = ipaddress.ip_network(value, strict=False)
            assert network.version == (6 if kind == 'IP-CIDR6' else 4)
        else:
            value = value.lower()
            if not value or any(c.isspace() for c in value) or '/' in value:
                raise ValueError(f'{path.name}:{number}: invalid hostname')
        rule = (kind, value, *fields[2:])
        if rule not in result:
            result.append(rule)
    return result


def write_qx(path, rules, policy):
    lines = ['# 自动生成：请维护根目录个人列表或 sources/pt-sites.json',
             '# 运行 python3 scripts/build_rules.py 更新；PT 站网页规则不包含独立 tracker 域名。']
    for kind, value, *options in rules:
        lines.append(','.join([QX_TYPES[kind], value, policy]))
    path.write_text('\n'.join(lines) + '\n')


def main():
    source = json.loads((ROOT / 'sources/pt-sites.json').read_text())
    active = [s for s in source['sites'] if not s['isDead']]
    hosts = set()
    for site in active:
        for url in site['urls']:
            parsed = urlsplit(url)
            if parsed.scheme not in ('http', 'https') or not parsed.hostname:
                raise ValueError(f'Invalid PT URL: {url}')
            host = parsed.hostname.lower()
            if host.endswith('.onion'):
                continue
            # Keep configured hostnames; do not guess parent domains or trackers.
            hosts.add(host)
    pt = [('DOMAIN-SUFFIX', host) for host in sorted(hosts)]
    header = ['# PT 网站域名：默认代理',
              f"# 来源：{source['repository']}/tree/{source['commit']}/src/packages/site/definitions",
              f"# {len(active)} 个未标记关闭的私有站点；排除公开 BT、旧网址和已关闭站点。",
              '# 自动生成，请修改来源清单后运行 python3 scripts/build_rules.py']
    (ROOT / 'PT.list').write_text('\n'.join(header + [','.join(r) for r in pt]) + '\n')
    direct = read_rules(ROOT / 'SelfDirect.list')
    proxy = read_rules(ROOT / 'SelfProxy.list')
    write_qx(ROOT / 'QuantumultX/Direct.list', direct, 'direct')
    write_qx(ROOT / 'QuantumultX/Proxy.list', proxy, '代理')
    write_qx(ROOT / 'QuantumultX/PT.list', pt, '代理')
    print(f"PT: {len(active)} sites, {len(pt)} unique domains; personal: {len(direct)} direct, {len(proxy)} proxy")


if __name__ == '__main__':
    main()
