# Poweranalysis: Warmup

> ## Description
>
> This encryption algorithm leaks a "bit" of data every time it does a computation. Use this to figure out the encryption key. Download the encryption program here encrypt.py. The flag will be of the format picoCTF{\<encryption key\>} where \<encryption key\> is 32 lowercase hex characters comprising the 16-byte encryption key being used by the program.
>
> ## Hints
>
> - The "encryption" algorithm is simple and the correlation between the leakage and the key can be very easily modeled.

## Solution

Before we get into writing code to solve this problem, we first need to understand what information we need to obtain and how we will use it to get our answer. The encryption takes your input, takes every two bytes of it and `XOR`'s it by every two corresponding bytes of a secret key, which we want to find. Then, it takes `Sbox` and takes the number we got and indexs that number inside of Sbox.

This is the byte that will be in the ciphertext. Instead of giving the encrypted ciphertext, it gives an amount of 'leakage'. This is defined as whether or not the LSB of the encrypted two bytes of ciphertext is one or not. If it is, then one is added to the amount of 'leakage'. We are then given the leakage as an integer.

At first, getting a single number as an output may not seem like a lot of data we can work with, but if we consistenly send a lot of requests and collect the results, we can theoretically use it to obtain the flag. The concept of this solution is that we can change the value of two bytes, and keep all the others the same, we can monitor the two bytes that give a higher leakage value and the ones that give a lower one. If it has a higher leakage value, then the 1st bit of the ciphertext must be 1, as that is how the leakage value is calculated. This narrows down the amount of potential values in Sbox.

This only narrows down the Sbox by about half, but if we combine this with data from a lot of other results, we can derive the key value for those two bytes. Repeating this for all the other two bytes, we can get the key, which is the flag. Now that we have the solution concept, let's look at some code.

```python
from pwn import *

PORT = int(input('Port number: '))
Sbox = [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76, 0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0, 0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15, 0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75, 0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84, 0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF, 0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8, 0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2, 0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73, 0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB, 0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79, 0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08, 0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A, 0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E, 0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF, 0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16]
plaintext_bytes = [0xDD, 0xE2, 0x1F, 0x25, 0x47, 0xA9, 0x9B, 0x14, 0x75, 0x5E, 0x90, 0x7D, 0x98, 0x50, 0x0A, 0x4E, 0x3B, 0x4A, 0x1E, 0x8F, 0xE4, 0x54, 0x3F, 0x7C, 0x67, 0x95, 0xF6, 0x85, 0x07, 0xF9, 0x9D, 0x86, 0x96, 0x8B, 0x33, 0x6B, 0x51, 0xC7, 0x72, 0x80, 0x8E, 0x92, 0x6C, 0xC9, 0x17, 0x60, 0x11, 0x8C, 0x22, 0x6D, 0x41, 0x6A, 0x68, 0x8D, 0x6F, 0x49, 0x9E, 0x9F, 0xF2, 0x8A, 0x78, 0x2D, 0x3A, 0x94, 0x2B]
key_bytes = [hex(i)[2:] + hex(j)[2:] for i in range(0, 16) for j in range(0,16)]
```

This imports pwntools so that we can send requests quickly to the server and asks for the port number to connect to. It also takes the Sbox from the provided encryption file, defines 64 random two bytes of plaintext that I generated randomly that we can send to the server(I only used 64 because using 256 plaintext values would take too long to send to the server), and includes all the potential two bytes of keys that could be possible. The two bytes of keys and two bytes of plaintexts are all hex values from 0x00 to 0xff.

```python
for c in range(len(Sbox)):
    Sbox[c] = Sbox[c] & 1
```

These lines are not as important, but they change the Sbox so that every value becomes a 1 or a 0 based off of the first bit of each number, to make comparison easier later on.

```python
def get_leakage():
    leakage_list = []
    for b in range(1, 17):
        leaks = []
        for a in plaintext_bytes:
            r = remote('saturn.picoctf.net', PORT)
            r.recvuntil(b'Please provide 16 bytes of plaintext encoded as hex:')
            r.send(bytes('00'*(b-1) + format(a, '02x') + '00'*(16-b) + '\n', 'utf-8'))
            leakage = r.recvline()
            r.close()
            leaks.append(int(leakage.decode().split(': ')[1].split('\n')[0]))
        value = min(leaks)
        for j in range(len(leaks)):
            leaks[j] = leaks[j] - value
        leakage_list.append(leaks)
    return leakage_list
```

Oh boy. This code defines a function called get_leakage that uses the pwntools library to communicate with the picoCTF server. It loops through every two bytes we are looking at, and inside that loop, sends requests to the server with each request having a tester value from plaintext_bytes in the position specified by the byte value we are testing. It then takes the result and stores it inside a list. In the end, we have a two dimensional array, with 16 values inside the main array for every two bytes, and 64 values inside of each of those arrays for every plaintext that we send in. Note that I have reduced all the values in the list to a one or a zero to make comparison easier later on. Also note that if you want to run it yourself, pwntools might take a couple minutes due to the large amount of requests.

```python
leaks = get_leakage()
key = ''
```

These lines call the function from the previous code block, and initiallize the variable `key` so we can write to it later on.

```python
for byte in range(16):
    for key_byte in range(len(key_bytes)):
        row = []
        for plaintext_byte in range(len(plaintext_bytes)):
            xor = plaintext_bytes[plaintext_byte] ^ int(key_bytes[key_byte], 16)
            final = Sbox[xor]
            if final == leaks[byte][plaintext_byte]:
                row.append(True)
            else:
                row.append(False)
        if all(row):
            key += str(key_bytes[key_byte])
            continue
```

This is the code that does the comparison between what we got with the requests, and the Sbox values that will comply. In order for a key value to pass, all the leakage values that we got for the plaintext values must match up with the Sbox values for the XOR. We then check if all the values match for that key value, and if it does, we know that we have found the key for those two bytes. This repeats for all 16 pairs of bytes. The last line prints the flag, and the challenge is solved.
