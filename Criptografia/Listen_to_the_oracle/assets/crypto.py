#!/bin/env python3
import random
import base64
import secret

class BadPaddingException(Exception):
    pass


class BadDecryptedException(Exception):
    pass

BLOCK = 16

def encrypt(m):

    # Init and detect padding
    diff = (BLOCK - len(m)) % BLOCK
    if diff == 0:
        diff = BLOCK

    padding = int.to_bytes(diff, length=1, byteorder='little')
    padding = diff*padding

    aux_m = m + padding

    # Cipher text
    c = b""
    IV = b"".join([int.to_bytes(random.randint(0, 0xff), length=1, byteorder='little') for i in range(0x10)])
    cbc_code = IV
    while len(aux_m) > 0:
        block = aux_m[:BLOCK]
        aux_m = aux_m[BLOCK:]
        c_aux = b""

        for i in range(BLOCK):
            chunk = block[i]


            # CBC
            chunk = cbc_code[i] ^ chunk
            chunk = (chunk + secret.K[i]) % 0xff


            c_aux += int.to_bytes(chunk, length=1, byteorder='little')

        c += c_aux
        cbc_code = c_aux

    res = base64.b64encode(IV+c)

    return res

def decrypt(c):
    m = b""

    # Cipher text
    aux_c = base64.b64decode(c)

    # > BLOCK because first block is the IV
    while len(aux_c) > BLOCK:
        block = aux_c[-BLOCK:]
        aux_c = aux_c[:-BLOCK]
        cbc_code = aux_c[-BLOCK:] if len(aux_c) >= BLOCK else secret.K

        aux_m = b""
        for i in range(BLOCK):

            chunk = block[i]

            # CBC
            chunk = (chunk - secret.K[i]) % 0xff
            chunk = chunk ^ cbc_code[i]

            aux_m += int.to_bytes(chunk, length=1, byteorder='little')

        m = aux_m + m

    # Init and detect padding
    diff = int(m[-1])

    if diff > 0:
        # Check padding
        for x in range(diff):
            if m[-(1+x)] != diff:
                raise BadPaddingException("Bad padding!")
    else:
            raise BadPaddingException("Bad padding!")

    # [0 : -PADDING]
    m = m[:-(diff)]

    return m

