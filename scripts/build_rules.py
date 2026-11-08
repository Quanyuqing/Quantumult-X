#!/usr/bin/env python3
"""Generate root-level QX rules from the personal source lists."""
import ipaddress
from pathlib import Path

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
    lines = ['# 自动生成：请维护 SelfProxy.list 或 SelfDirect.list',
             '# 运行 python3 scripts/build_rules.py 更新。']
    for kind, value, *options in rules:
        lines.append(','.join([QX_TYPES[kind], value, policy]))
    path.write_text('\n'.join(lines) + '\n')


def main():
    direct = read_rules(ROOT / 'SelfDirect.list')
    proxy = read_rules(ROOT / 'SelfProxy.list')
    write_qx(ROOT / 'Direct.list', direct, 'direct')
    write_qx(ROOT / 'Proxy.list', proxy, '代理')
    print(f"Personal rules: {len(direct)} direct, {len(proxy)} proxy")


if __name__ == '__main__':
    main()
