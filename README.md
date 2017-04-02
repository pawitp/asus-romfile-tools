# ASUS Romfile Tools
A tool to decrypt and encrypt setting backup files (romfile.cfg) from
certain ASUS routers (tested on DSL-AC52U). This allows the settings
to be edited in a text editor, which may be easier and provide more
flexibility than editing the setting through the web interface.

## Usage
### Encrypt
`python asus-romfile-tools.py --encrypt [--rand 15] [--model DSL-AC52U] decrypted.cfg encrypted.cfg`

The `--rand` and `--model` parameters are optional.

### Decrypt
`python asus-romfile-tools.py --decrypt encrypted.cfg decrypted.cfg`

## Encryption Mechanism
The encryption (actually, obfuscation) mechanism was discovered
thanks to GPL sources released from ASUS. Particularly, the file
format and the encryption method is detailed in
<https://github.com/smx-smx/asuswrt-rt/blob/master/apps/public/boa-asp/src/util.c>
and will be briefly explained in this document.

### Encryption
First, a random number between 15 - 29 (inclusive) is generated. The
random number, from here on, will be referred to as random key or
*rand*.

To the resulting file, a header will be written as follows:

| Size (bytes) | Content                                   |
|--------------|-------------------------------------------|
| 16           | Zero-padded model name (e.g. DSL-AC52U)   |
| 16           | Magic string "EnCrYpTRomFIle\0\0"         |
| 4            | File length (as big-endian integer)       |
| 4            | Random key (as big-endian integer) |

After that, each byte in the original file will be written with the
following changes:

| Original Byte | Output                                     |
|---------------|--------------------------------------------|
| 0x00          | Randomly choose between 0xfd, 0xfe or 0xff |
| Others        | (0xff - orig_byte + *rand*) & 0xff         |

### Decryption
To decrypt, the header must be read to extract the random key.

After that, the content can be read with the following changes:

| Encrypted Byte     | Output                                  |
|--------------------|-----------------------------------------|
| 0xfd, 0xfe or 0xff | 0x00                                    |
| Others             | (0xff - encrypted_byte + *rand*) & 0xff |