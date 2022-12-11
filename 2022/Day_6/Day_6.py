class rolling_buffer:

    count = 0
    filled = False

    def __init__(self,buffer_size):
        self.buffer_size = buffer_size
        self.buffer = ['' for _ in range(buffer_size)]

    def add(self,char):
        self.buffer[self.count] = char

        self.count = self.count + 1
        if self.count >= self.buffer_size:
            self.count = 0
            if not self.filled:
                self.filled = True

    def is_start_marker(self):
        if self.filled:
            buffer_set = set(self.buffer)
            if len(buffer_set) == self.buffer_size:
                return True

        return False


file = open("input", 'r')
buffer = file.readline()

RBuff_packet_start = rolling_buffer(4)
RBuff_msg_start = rolling_buffer(14)

packet_start_idx = 0
msg_start_idx = 0
for idx, char in enumerate(buffer):

    if not packet_start_idx:
        RBuff_packet_start.add(char)
        if RBuff_packet_start.is_start_marker():
            packet_start_idx = idx + 1

    if not msg_start_idx:
        RBuff_msg_start.add(char)
        if RBuff_msg_start.is_start_marker():
            msg_start_idx = idx + 1

    if packet_start_idx and msg_start_idx:
        break

print(f"Q6.1: {packet_start_idx}")
print(f"Q6.2: {msg_start_idx}")

pass
