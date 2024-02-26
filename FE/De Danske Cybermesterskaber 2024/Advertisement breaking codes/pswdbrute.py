import hashlib
import sys
import struct
import itertools

MAGIC = "LSFR"

class KeyStream:
    feedBacks = [ int('100000000000000000000011', 2),
                  int('100000000000000000000101', 2),
                  int('100000000000000000001001', 2),
                ]    
    def __init__(self, psw):
        key = self.psw2key(psw)
        n = struct.unpack('I', key)[0]
        self.regs = [ (n>>3)  & 0xffffff,
                      (n>>7)  & 0x0fffff,
                      (n>>11) & 0x00ffff ]

    def psw2key(self, psw):
        h = hashlib.md5(psw).digest()
        return h[6:10]

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
        return [self.nextKey() for i in xrange(size)]

def print_usage():
    print "Usage:"
    print " %s <ciphertext-file>" % sys.argv[0]
    sys.exit(0)

def main():
    if len(sys.argv) != 2:
        print_usage()

    ifile  = sys.argv[1]

    f   = open(ifile, "rb")
    cnt = f.read()
    f.close()

    pswchars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    print "Trying to find the password for file %s"  % ifile
    cnt = cnt[3:]
    cnt = cnt[:len(MAGIC)]

    for l in range(5):
        for pot_psw in map(''.join, itertools.product(pswchars, repeat=l)):
            generator = KeyStream(pot_psw)
            plain = []
            keyStream = generator.getKeyStream(len(MAGIC))
            for i in range(len(cnt)):
                key = keyStream[i]
                encChar = cnt[i]
                x = ord(encChar) ^ key
                plain.append( chr(x) )
            cont = ''.join(plain)
            # If decrypted text do not start with MAGIC bytes
            # decryption has failed. Otherwise break and print the password
            if cont != MAGIC:
                continue
            else:
                print("Found a password that works. It is: %s" % pot_psw)
                sys.exit(0)

main()
