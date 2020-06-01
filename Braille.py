def answer(plaintext):
    brailleresponse = ""
    for i in range(0, len(plaintext)):
        if plaintext[i].isupper():
            brailleresponse = brailleresponse + '000001'
        brailleresponse = brailleresponse + braillecodes[charcodes.index(plaintext[i].lower())]
    return brailleresponse
# The Alphabet Lookup Table
charcodes = [' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
              'u', 'v', 'w', 'x', 'y', 'z']
braillecodes = ['000000','100000','110000','100100','100110','100010','110100','110110','110010','010100','010110','101000','111000','101100',
                '101110','101010','111100','111110','111010','011100','011110','101001','111001','010111','101101','101111','101011']

# Print my handle
print(answer("Braille"))
print (len("000001110000111010100000010100111000111000100010"))
print (len("000001110000111010100000010100111000111000100010"))