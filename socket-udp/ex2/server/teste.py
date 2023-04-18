import math
fSize = 12314
packetNumbers = [i for i in range(math.ceil(fSize/1024))]

for p in packetNumbers:
    print(1024*p, 1024*(p+1))