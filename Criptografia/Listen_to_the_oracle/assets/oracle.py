#!/bin/env python3
import crypto
import base64
from secret import FLAG

def decrypt(c):
    m = crypto.decrypt(c)
    if m != FLAG.encode():
        raise crypto.BadDecryptedException

    return m

if __name__ == '__main__':

    c = input("Encrypted message > ")
    try:
        m = decrypt(c)
        print("Message correctly decrypted :)")
    except crypto.BadPaddingException:
        print("ERROR: BadPaddingException")
    except crypto.BadDecryptedException:
        print("ERROR: BadDecryptedException")
    except Exception as e:
        print("ERROR: Python exception")

