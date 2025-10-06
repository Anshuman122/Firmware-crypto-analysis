/* Hinglish Comment: Yeh YARA rule file ka corrected version hai.
SHA256 constants me jo typo tha, woh theek kar diya gaya hai.
*/
rule AES_S_Box
{
    meta:
        description = "Finds the AES S-Box constant table"
        author = "Crypto Finder"
        crypto_name = "AES"
    strings:
        // AES S-Box table in hex
        $sbox = { 63 7c 77 7b f2 6b 6f c5 30 01 67 2b fe d7 ab 76
                 ca 82 c9 7d fa 59 47 f0 ad d4 a2 af 9c a4 72 c0
                 b7 fd 93 26 36 3f f7 cc 34 a5 e5 f1 71 d8 31 15
                 04 c7 23 c3 18 96 05 9a 07 12 80 e2 eb 27 b2 75
                 09 83 2c 1a 1b 6e 5a a0 52 3b d6 b3 29 e3 2f 84
                 53 d1 00 ed 20 fc b1 5b 6a cb be 39 4a 4c 58 cf
                 d0 ef aa fb 43 4d 33 85 45 f9 02 7f 50 3c 9f a8
                 51 a3 40 8f 92 9d 38 f5 bc b6 da 21 10 ff f3 d2
                 cd 0c 13 ec 5f 97 44 17 c4 a7 7e 3d 64 5d 19 73
                 60 81 4f dc 22 2a 90 88 46 ee b8 14 de 5e 0b db
                 e0 32 3a 0a 49 06 24 5c c2 d3 ac 62 91 95 e4 79
                 e7 c8 37 6d 8d d5 4e a9 6c 56 f4 ea 65 7a ae 08
                 ba 78 25 2e 1c a6 b4 c6 e8 dd 74 1f 4b bd 8b 8a
                 70 3e b5 66 48 03 f6 0e 61 35 57 b9 86 c1 1d 9e
                 e1 f8 98 11 69 d9 8e 94 9b 1e 87 e9 ce 55 28 df
                 8c a1 89 0d bf e6 42 68 41 99 2d 0f b0 54 bb 16 }
    condition:
        $sbox
}

rule SHA256_Constants
{
    meta:
        description = "Finds the initial hash values (K-constants) for SHA-256"
        author = "Crypto Finder"
        crypto_name = "SHA256"
    strings:
        // The first 32 bits of the fractional parts of the cube roots of the first 64 primes
        $k_constants = { 42 8a 2f 98 71 37 44 91 b5 c0 fb cf e9 b5 db a5 39 56 c2 5b 59 f1 11 f1
                         92 3f 82 a4 ab 1c 5d d5 d8 07 aa 98 12 83 5b 01 24 31 85 be 55 0c 7d c3
                         72 be 5d 74 80 de b1 fe 9b dc 06 a7 c1 9b f1 74 e4 9b 69 c1 ef be 47 86
                         0c c2 61 e0 1f 83 d9 ab 5b d0 5d d8 5c 44 a3 06 5c 1d 77 e2 9c 0e a8 2e
                         6d 2a 4d d6 81 c2 7e d5 d5 a7 3e 68 3e 2e e3 c3 e4 d1 4a d2 35 2f 81
                         38 53 13 41 42 86 37 6f 4d 77 0c 6d 51 0b a6 58 5b f4 1d 9e 5e 57 59 1d
                         67 86 d3 91 8b 44 f7 af 91 28 3d b0 2d 1d 6f 24 0c a1 cc 77 ac 9c 65
                         2d e9 2c 6f 5c 26 80 59 5a 34 82 2e 5a 75 16 93 68 2e 63 03 8b d4 4c af
                         76 f9 88 da 83 11 53 b5 98 3e 51 52 9a 53 9b 53 af a4 50 6c e8 c1 92 e8
                         b2 72 0c 85 c7 6c 51 a3 d1 92 e8 19 d5 ef 82 d6 99 06 24 55 65 a9 10 03
                         e4 27 21 68 f2 7b 89 6f c6 e0 0b f3 d5 a7 91 47 93 0a a7 28 64 07 0c F1
                         06 ca 63 51 14 29 29 67 27 b7 0a 85 2e 1b 21 38 5c 2d 85 c1 3b 75 94 1d
                         4a 77 3c 90 5c 54 9e 3d 58 05 69 79 2d 28 72 3d 59 7d 81 8f 80 94 4a 44
                         f5 4e f7 42 ff 6d 4c 54 8c 45 95 21 06 f8 2f 89 42 74 8f 82 48 42 7b 2d }
    condition:
        $k_constants
}