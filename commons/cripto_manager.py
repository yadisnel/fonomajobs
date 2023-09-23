import zlib


class CriptoManager:
    # Singleton instance
    _self = None

    # Singleton instance
    def __new__(cls):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    def __init__(self):
        pass

    def compute_crc(self, data: bytes):
        return zlib.crc32(data)
