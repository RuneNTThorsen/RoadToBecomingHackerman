import sys
import struct

MAGIC = "LSFR"

class KeyStream:
    feedBacks = [ int('100000000000000000000011', 2),
                  int('100000000000000000000101', 2),
                  int('100000000000000000001001', 2),
                ]    
    def __init__(self, k):
        key = k
        n = struct.unpack('I', key)[0]
        self.regs = [ (n>>3)  & 0xffffff,
                      (n>>7)  & 0x0fffff,
                      (n>>11) & 0x00ffff ]

    def stepRegs(self):
        for i in range(3):
            self.stepReg(i)
        
    def stepReg(self, regnr):
        fb = self.feedBacks[regnr]
        reg = self.regs[regnr]
        x = reg & fb
        xor = 0
        while x > 0:
            xor ^= x
            x >>= 1
        newbit = xor & 1
        reg = (reg + reg + newbit) & 0xffffff
        self.regs[regnr] = reg

    def nextKey(self):
        key = 0
        for i in range(8):
            key += key
            a = self.regs[0] & 1
            b = self.regs[1] & 1
            c = self.regs[2] & 1
            bit = a ^ b ^ c
            key ^= bit
            self.stepRegs()
        return key & 0xff

    def getKeyStream(self, size):
        return [self.nextKey() for i in range(size)]
   
def decrypt(cnt, k):
    """
    cnt is the contents of the file that is to be decrypted
    (after getting rid of the first 3 bytes),
    k is the key that is to be used for decryption.
    """
    l = len(cnt)
    keystream = KeyStream(k).getKeyStream(l)
    plaintext = []
    for i in range(l):
        key = keystream[i]
        c = cnt[i]
        x = ord(c) ^ key
        plaintext.append(chr(x))
    return ''.join(plaintext)

def print_usage():
    print("Usage:")
    print("  %s <in-file> <out-file>" % sys.argv[0])
    sys.exit(0)

def brute(cnt):
    # Trying all the keys for which a = 0 yields 0.390625 percent
    percentage_of_keys_tried = 0.390625
    # Get the MAGIC bytes of the cnt
    length = len(MAGIC)
    cont = cnt[:length]
    # Start bruteforcing the 4 bytes used for encryption
    for a in range(256):
        for b in range(256):
            for c in range(256):
                for d in range(256):
                    # Create the possible key to be used for decryption
                    # by using 4 ints and converting them to a bytearray
                    k = [a, b, c, d]
                    k = bytearray(k)
                    # Try and see if decryption with the brute forced key works
                    keystream = KeyStream(k).getKeyStream(length)
                    plain = []
                    for i in range(length):
                        key = keystream[i]
                        e = cont[i]
                        x = ord(e) ^ key
                        plain.append(chr(x))
                    plain_magic = ''.join(plain)
                    # If the decrypted text is MAGIC bytes, the right key
                    # has been found and decryption will be done, terminating
                    # the procedure by returning
                    if plain_magic == MAGIC:
                        print("Decryption key found!")
                        return decrypt(cnt[len(MAGIC):], k)
        # If reaching this point, no key with the current a has been found yet,
        # so the relative portion of possible keys tried will be calculated in
        # percent
        if a > 0:
            percentage_of_keys_tried = (a / 256) * 100        
        # Give running updates on progress
        print("No key found yet. Tried %s percent of possible keys" % percentage_of_keys_tried)
        # Just one extra check to see if everything actually works as intended
        # If this point is reached then no key has worked
        if a == b == c == d == 255:
            print("No key was found")
            sys.exit(1)

def main():
    if len(sys.argv) != 3:
        print_usage()
        
    ifile  = sys.argv[1]
    ofile  = sys.argv[2]
    
    f = open(ifile, "rb")
    cnt = f.read()
    f.close()
    
    print("Decrypting file %s to %s"  % (ifile, ofile))
    # First 3 bytes not needed to get the final message
    cnt = cnt[3:]

    cont = brute(cnt)
    
    f = open(ofile, "wb")
    f.write(cont)
    f.close()

main()
