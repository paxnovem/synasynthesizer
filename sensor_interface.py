import sys
import ftd2xx as FT

class SensorInterface(object):
    def __init__(self):
        self.sensor = None
        self.buffer = []

    def connect(self, id=None):
        """Connects to a sensor

        Use the optional id argument to specify a non-default sensor"""
        if id == None:
            id = 0;
        try:
            self.sensor = FT.open(id)
        except FT.DeviceError:
            print("Error: Device not found")
            raise

        self.sensor.setUSBParameters(8192)
        self.sensor.setLatencyTimer(2)
    def close(self):
        "Closes the connection to the sensor"
        if self.sensor:
            self.sensor.close()
        self.sensor = None

    def getAllImages(self):
        "Returns a list of all images found in the FTDI buffer"
        self.readBuffer()
        images = []
        while True:
            p = self.getPacket()
            if not p:
                return images
            if p[0] == 2: # image packet
                rows = p[14]
                cols = p[15]
                imgBuf = p[16:]
                pixels = []
                for i in range(rows):
                    pixels.append(imgBuf[(i*cols):((i+1)*cols)])
                img = { 'timeStamp' : p[5] + (p[6] << 16),
                        'sequence' : p[10],
                        'rows' : rows,
                        'cols' : cols,
                        'image' : pixels }
                images.append(img)

    def getPacket(self):
        while True:
            if len(self.buffer) == 0:
                return None

            # find BOM: 7 FFs followed by A5
            ffCount = 0
            while len(self.buffer) > 0:
                b = self.buffer.pop(0)
                if b == 0xFF:
                    ffCount += 1
                    if ffCount == 15:
                        print("Warning: Sensor buffer overflow")
                elif ffCount >= 7 and b == 0xA5:
                    break
                else:
                    ffCount == 0

            # Read length word
            if len(self.buffer) < 2:
                print("Discarded packet because buffer is empty")
                continue

            length = self.buffer[1] + (self.buffer[0] << 8)
            if length > len(self.buffer):
                print("Discarded packet longer than buffer (%d bytes vs %d bytes)" % (length, len(self.buffer)))
                continue # packet is longer than our buffer
            if length < 32:
                print("Discarded packet shorter than minimum (%d bytes vs 32 bytes)" % (length))
                continue # packet is shorter than minimum size

            packet = self.buffer[0:length]

            calcCrc = crc16(packet[4:])
            txCrc = packet[3] + (packet[2] << 8)
            if calcCrc != txCrc:
                print("Warning: Transmitted CRC %04X != %04X Calculated" % (txCrc, calcCrc))
                continue
            packet = self.removeEscapedFFs(packet)

            # convert packet to words from bytes
            lo = packet[5::2]
            hi = packet[4::2]
            packet = [lo[i] + (hi[i] << 8) for i in range(len(lo))]

            # accept the packet, remove it from buffer
            self.buffer[0:length] = []
            print("Accepting packet, %d bytes long" % length)
            return packet

    def removeEscapedFFs(self, packet):
        # packets have 00 bytes inserted after each 4 FFs because
        # strings of FFs are used by hardware for signaling purposes
        i = 4
        while i < len(packet)-4:
            if packet[i] != 0xFF or packet[i+1] != 0xFF or packet[i+2] != 0xFF or packet[i+3] != 0xFF:
                i += 1
                continue
            print(packet[i+4])
            if packet[i+4] != 0:
                print("Warning, saw incorrect escape in FF sequence: %d" % packet[i+4])
            del packet[i+4]
            i += 1
        return packet

    def readBuffer(self):
        if not self.sensor:
            return
        # flush out buffer so we don't get old images
        rx = 65536
        while rx == 65536:
            (rx, tx, stat) = self.sensor.getStatus()
            buf = self.sensor.read(rx)
            print("Read %d bytes" % len(buf))
            if rx == 65536:
                print("Discarding buffer...")

        if sys.version_info[0] < 3:
            buf = [ord(x) for x in buf]
        self.buffer.extend(buf)