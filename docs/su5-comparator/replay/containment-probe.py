#!/usr/bin/env python3
"""Negative access probes, run as an external checker by real Lake/bwrap."""
from pathlib import Path
import errno, fcntl, json, os, socket, struct, sys
if '--reject' in sys.argv:
    print('INTENTIONAL_KERNEL_REJECTION',flush=True)
    sys.exit(7)
parent=json.loads(Path('/evidence/outer-namespaces.json').read_text())
current={k:os.readlink('/proc/self/ns/'+k) for k in parent}
assert all(current[k]!=parent[k] for k in parent), (current,parent)
for target in ['/checks/containment-forbidden-write','/evidence/containment-forbidden-write','/tools/containment-forbidden-write',sys.argv[-1]]:
    try:
        with open(target,'r+b' if target==sys.argv[-1] else 'xb'):
            pass
    except OSError:
        print('WRITE_DENIED',target)
    else:
        raise AssertionError('Unexpected write access: '+target)
interfaces=socket.if_nameindex()
flags={}
with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
    for _,name in interfaces:
        request=struct.pack('16sH14x',name.encode(),0)
        flags[name]=struct.unpack('16sH14x',fcntl.ioctl(s,0x8913,request))[1]
assert all(name=='lo' or not value & 1 for name,value in flags.items()), flags
assert len(Path('/proc/net/route').read_text().splitlines())<=1
with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.settimeout(1)
    assert s.connect_ex(('192.0.2.1',443))==errno.ENETUNREACH
assert os.environ.get('SU5_PRIVATE_SENTINEL') is None
scratch=Path('/tmp/containment-scratch'); scratch.write_text('temporary only'); scratch.unlink()
print('CONTAINMENT_PASSED',json.dumps({'namespaces':current,'interface_flags':flags,'external_route':'unreachable'}),flush=True)
