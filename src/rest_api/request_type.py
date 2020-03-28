class Request:
    def __init__(self, page, limit, ip_src_in, packets_between, bytes_between, stamp_between):
        self.page = page
        self.limit = limit
        self.ip_src_in = ip_src_in
        self.packets_between = packets_between
        self.bytes_between = bytes_between
        self.stamp_between = stamp_between
