import sys
import ustruct

# mock implementation using binary file

_mock = {}

if sys.platform in ['trezor', 'pyboard']:  # stmhal
    _file = '/flash/trezor.config'
else:
    _file = '/var/tmp/trezor.config'


def _load():
    global _mock
    try:
        with open(_file, 'rb') as f:
            while True:
                d = f.read(4)
                if len(d) != 4:
                    break
                k, l = ustruct.unpack('<HH', d)
                v = f.read(l)
                _mock[k] = v
    except OSError:
        pass


def _save():
    global _mock
    with open(_file, 'wb') as f:
        for k, v in _mock.items():
            f.write(ustruct.pack('<HH', k, len(v)))
            f.write(v)

_load()


def get(app_id, key, default=None):
    global _mock
    return _mock.get((app_id << 8) | key, default)


def set(app_id, key, value):
    global _mock
    _mock[(app_id << 8) | key] = value
    _save()

def wipe():
    global _mock
    _mock = {}
    _save()
