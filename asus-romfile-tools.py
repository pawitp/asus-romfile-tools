#!/usr/bin/env python

import argparse, struct, random


# Header format for use in struct
HEADER = '!16s16sII'
HEADER_SIZE = struct.calcsize(HEADER)

# Magic string to store in the header
MAGIC_STR = 'EnCrYpTRomFIle\x00\x00'


def main():
    parser = argparse.ArgumentParser(description='Decrypt and encrypt setting backup files (romfile.cfg) from certain ASUS routers')
    parser.add_argument('action', metavar='action', type=str, choices=('encrypt', 'decrypt'),
                        help='action (encrypt or decrypt)')
    parser.add_argument('in_file', metavar='input', type=str,
                        help='input configuration file')
    parser.add_argument('out_file', metavar='output', type=str,
                        help='output configuration file')
    parser.add_argument('--model', metavar='model', type=str, default='DSL-AC52U',
                        help='router model (only used for encryption, default: DSL-AC52U)')
    parser.add_argument('--rand', metavar='key', type=int, choices=range(15, 30),
                        help='random key (only used for encryption, default: generated)')
    args = parser.parse_args()

    if args.action == 'decrypt':
        decrypt(args.in_file, args.out_file)
    elif args.action == 'encrypt':
        encrypt(args.in_file, args.out_file, args.model, args.rand)

def decrypt(in_file, out_file):
    with open(in_file, 'r') as content_file:
        content = bytearray(content_file.read())

    (model, magic, length, key) = struct.unpack(HEADER, content[:HEADER_SIZE])
    print "Model: %s\nMagic: %s\nLength: %d\nKey: %s" % (model, magic, length, key)
    
    data = content[HEADER_SIZE:]
    if len(data) != length:
        print "Warning: file length (%d) does not match length in header (%d)" % (len(encrypted), length)

    for i in xrange(0, len(data)):
        byte = data[i]
        if byte == 0xfd or byte == 0xfe or byte == 0xff:
            byte = 0x00
        else:
            byte = (0xff - byte + key) & 0xff
        data[i] = chr(byte)

    with open(out_file, 'w') as content_file:
        content_file.write(data)

def encrypt(in_file, out_file, model, key):
    with open(in_file, 'r') as content_file:
        content = bytearray(content_file.read())

    if not key:
        key = random.randint(15, 29)

    length = len(content)

    print "Length: %d\nKey: %s" % (length, key)

    header = struct.pack(HEADER, model, MAGIC_STR, length, key)

    for i in xrange(0, length):
        byte = content[i]
        if byte == 0:
            byte = 0xff # 0xfd, 0xfe or 0xff will work
        else:
            byte = (0xff - byte + key) & 0xff
        content[i] = chr(byte)

    with open(out_file, 'w') as content_file:
        content_file.write(header)
        content_file.write(content)
    
if __name__ == '__main__':
    main()