__author__ = 'yrch'

import urllib2
import sys


def strxor(a, b):
    if len(a) > len(b):
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
    else:
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])


TARGET = 'http://crypto-class.appspot.com/po?er='

expectedMessage = "The Magic Words are Squeamish Ossifrage"

# --------------------------------------------------------------
# padding oracle
# --------------------------------------------------------------
class PaddingOracle(object):
    def query(self, q):
        target = TARGET + urllib2.quote(q)  # Create query URL
        req = urllib2.Request(target)  # Send HTTP request to server
        try:
            f = urllib2.urlopen(req)  # Wait for response
            print 'Success!!!'
            print q

        except urllib2.HTTPError, e:
            # print "We got: %d" % e.code       # Print response code
            if e.code == 404:
                print "We got: %d" % e.code       # Print response code
                return True  # good padding
            return False  # bad padding


if __name__ == "__main__":
    ct = "f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4"

    c = [];
    c.append(ct[:32])
    c.append(ct[32:64])
    c.append(ct[64:96])
    c.append(ct[96:128])

    for i in range(0, len(c)):
        c[i] = c[i].decode("hex")

    m = ["", "", ""]
    po = PaddingOracle()

    n = 0
    for i in range(0, 3):
        for j in range(1, 17):
            padding = chr(0)*(16-j) + chr(j)*j
            for g in range(0, 256):

                que = strxor(c[i], strxor(chr(0) * (16 - j) + chr(g) + m[i], padding))
                que = que + c[i + 1]
                que = que.encode("hex")

                #print q
                #print que
                if po.query(que):
                    print 'pos[',j,']=',chr(g).encode("hex")
                    m[i] = chr(g) + m[i]
                    print m[i]
                    break





    #
    # for i in range(0, 3):
    #     for j in range(1, 17):  # padding 0xj
    #         print 'otro'
    #         for g in range(0, 256):
    #             n += 1
    #             print n,
    #
    #             que = strxor(c[i],
    #                          strxor(chr(0) * (16 - j) + chr(g) + m[i], chr(0) * (16 - j) + chr(j) * j))
    #             que = que + c[i + 1];
    #             que = que.encode("hex")
    #             print que
    #             if (po.query(que)):
    #                 m[i] = chr(g) + m[i]
    #                 print m[i]
    #                 break
    #
    # print
    # print
    #
    # for i in range(0, 3):
    #     print m[i]
