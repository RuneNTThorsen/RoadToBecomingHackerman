import hashlib
import sys
import struct

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
        for i in xrange(3):
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
        for i in xrange(8):
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
   
def decrypt(msg, psw):
    plain = encrypt(msg, psw)
    return plain

def encrypt(msg, psw):
    keystream = KeyStream(psw)
    cipher = []
    for char in msg:
        key = keystream.nextKey()
        x = ord(char) ^ key
        cipher.append( chr(x) )
    return ''.join(cipher)
    
def passwdCheck(psw):
    pswchars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for p in psw:
        if p not in pswchars:
            print "ERROR: non valid password char: %s" % p
            print "valid chars: %s" % pswchars
            sys.exit(0)
    if len(psw) <= 4:
        return "LOW"
    elif len(psw) <= 6:
        return "MED"
    else:
        return "HIG"

def print_usage():
    print "Usage:"
    print "  encrypt:  %s enc <password> <in-file> <out-file>" % sys.argv[0]
    print "  decrypt:  %s dec <password> <in-file> <out-file>" % sys.argv[0]
    sys.exit(0)

def main():
    if len(sys.argv) != 5:
        print_usage()

    mode   = sys.argv[1]
    psw    = sys.argv[2]
    ifile  = sys.argv[3]
    ofile  = sys.argv[4]

    pswl   = passwdCheck(psw)

    f   = open(ifile, "rb")
    cnt = f.read()
    f.close()

    if mode == "enc":
        print "Encrypting file %s to %s"  % (ifile, ofile)
        # Insert MAGIC bytes so we can check if later decryption is OK
        cnt = encrypt(MAGIC + cnt, psw)
        cnt = pswl + cnt
    elif mode == "dec":
        print "Decrypting file %s to %s"  % (ifile, ofile)
        cnt = cnt[3:]
        cnt = decrypt(cnt, psw)
        # If decrypted text do not start with MAGIC bytes
        # decryption has failed
        if cnt[:len(MAGIC)] != MAGIC:
            print "Decryption failed! Probably wrong password specified."
            sys.exit(1)
        cnt = cnt[len(MAGIC):]
    else:
        print_usage()

    f   = open(ofile, "wb")
    f.write(cnt)
    f.close()

main()
