from Utils import utils

def GetKey(keyword):
    """
    Description
    -----------
    This function returns the numerical equivalent representation
    of the given keyword, this is a list where the i-th value is
    the code of the i-th letter in the keyword.
    
    See GetCode() to see the scheme used for the codes associated
    with the letters.

    Parameters
    ----------
    m : int
        Length of the keyword
    keyword : list
        The numerical equivalent representation of the given keyword
    keyword : string
        The keyword to encrypt
    """
    if type(keyword) == list:
        return keyword
    else:
        keyword = keyword.lower()
        key = []
        for c in keyword:
            key.append(utils.GetCode(c))
        
        return key

def Encrypt(keyword, text):
    """
    Description
    -----------
    This functions encrypts the given text with the provided keyword of length m

    Parameters
    ----------
    keyword : string
        The keyword to encrypt
    text : string
        Text to encrypt with Vigenere Cipher
    """
    m = len(keyword)
    text = utils.preProcessText(text)
    key = GetKey(keyword)

    encryptedText = ""
    for i in range(0, len(text)):
        encryptedText += utils.GetLetter((utils.GetCode(text[i]) + (key[i % m])) % 26)
    
    return encryptedText

def Decrypt(keyword, text):
    """
    Description
    -----------
    This functions decrypts the given text with the provided keyword of length m

    Parameters
    ----------
    keyword : string
        The keyword to encrypt
    text : string
        Text to decrypt with Vigenere Cipher
    """
    m = len(keyword)
    key = GetKey(keyword)

    decryptedText = ""
    for i in range(0, len(text)):
        decryptedText += utils.GetLetter((utils.GetCode(text[i]) - (key[i % m])) % 26)

    return decryptedText

"""
EXAMPLE
print(Encrypt("CIPHER", "This Cryptosystem is not secure"))
print(Decrypt("CIPHER", "vpxzgiaxivwpubttmjpwizitwzt"))
"""