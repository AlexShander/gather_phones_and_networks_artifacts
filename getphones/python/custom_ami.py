import re

from client import AMIClient


class CustomAMIClient(AMIClient):
    def _next_pack(self):
        data = b''
        while not self.finished.is_set():
            recv = self._socket.recv(self._buffer_size)
            if recv == b'':
                self.finished.set()
                continue
            data += recv
            if self.asterisk_line_regex.search(data):
                (pack, data) = self.asterisk_line_regex.split(data, 1)
                yield self._decode_pack(pack)
                break
        while not self.finished.is_set():
            while self.asterisk_pack_regex.search(data):
                data = data.replace('\r\n\r\n\r\n', '\r\n\r\n')
                (pack, data) = self.asterisk_pack_regex.split(data, 1)
                yield self._decode_pack(pack.strip())
            recv = self._socket.recv(self._buffer_size)
            if recv == b'':
                self.finished.set()
                continue
            data += recv
        self._socket.close()
