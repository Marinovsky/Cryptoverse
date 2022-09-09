from PIL import Image
import requests
from PIL import ImageOps
from IPython.display import display
import urllib.request
import numpy as np
from Utils import utils
from Cryptoanalysis import CryptoanalysisHill

def EncryptImage(key, url):
    """
    Description
    -----------
    Given m(the dimension of the key matrix), the key(matrix) and a
    url of the image, it encrypts the image of the url using the key.
    Finally, the encrypted image is displayed and then saved in
    'result.pgm' file

    Parameters
    ----------
    key : 2-dimensional list or np.array ie [[1, 2], [5, 6]]
        The mxm matrix to use as a key in the Hill cipher
    url : string
        The url of the image to encrypt
    """

    try:
        utils.IsValidMatrix(key)
    except:
        return -1

    m = len(key)
    response = requests.get(url)
    urllib.request.urlretrieve(url,"image.jpg")
    img = Image.open("image.jpg")
    encryptedImg = img.convert("L")

    # Resize image as needed, the image width must be a multiple
    # of m
    if encryptedImg.width % m != 0:
        diff = m - (encryptedImg.width % m)
        encryptedImg = ImageOps.expand(encryptedImg, border=(0,0, diff, 0), fill = 0)
    
    # Iterate over each row of the image height taking at each step
    # m pixels to transform them into a new m pixels
    for y in range(0, encryptedImg.height):
        rowPixels = []
        for x in range(0, encryptedImg.width):
            if x % m == 0 and x > 0:
                # Transform the m pixels making the dot product between them and the
                # key matrix
                newRowPixels = list(np.dot(rowPixels, key))
                newRowPixels = [(i % 255) for i in newRowPixels]
                for i in range(x - m, x):
                    encryptedImg.putpixel((i,y), int(newRowPixels[i - (x-m)]))
                rowPixels = []
            
            rowPixels.append(encryptedImg.getpixel((x,y)))
    
    # Show the image and save it in a .pgm file
    encryptedImg.show()
    encryptedImg.save("result1.pgm")

def DecryptImage(decryptKey, imgPath):
    """
    Description
    -----------
    Given m(the dimension of the key matrix), the  decrypt key(the 
    inverse modulus 255 of the matrix used to encrypt) and the path
    of the image it decrypts the image in the path using the key
    and then displays it

    Parameters
    ----------
    decryptKey : 2-dimensional list or np.array
        The inverse modulus 255 of the matrix used to encrypt
    imgPath : string
        The path of the image to decrypt in the local host
    """

    try:
        utils.IsValidMatrix(key)
    except:
        return -1

    m = len(key)
    img = Image.open(imgPath)
    decryptedImg = img

    # Iterate over each row of the image height taking at each step
    # m pixels to transform them into a new m pixels
    for y in range(0, decryptedImg.height):
        rowPixels = []
        for x in range(0, decryptedImg.width):
            if x % m == 0 and x > 0:
                # Transform the m pixels making the dot product between them and the
                # key matrix
                newRowPixels = list(np.dot(rowPixels, decryptKey))
                newRowPixels = [(int(i) % 255) for i in newRowPixels]
                for i in range(x - m, x):
                    decryptedImg.putpixel((i,y), int(newRowPixels[i - (x-m)]) % 255)
                rowPixels = []
            
            rowPixels.append(decryptedImg.getpixel((x,y)))
    
    #decryptedImg.show() # Instead, return the image

def EncryptText(m, key, text):
    """
    Description
    -----------
    Given m(the dimension of the key matrix), the key(matrix)
    and the text, it encrypts the text using the key and then
    returns it

    Parameters
    ----------
    key : 2-dimensional list or np.array
        The mxm matrix to use as a key in the Hill cipher
    text : string
        The text to encrypt. If the text length is not a m multiple
        it will add 'f' characters as needed to make it a m multiple
    """

    try:
        utils.IsValidMatrix(key)
    except:
        return -1

    m = len(key)
    text = utils.preProcessText(text)
    encryptedText = ""

    # Resize the text as needed, the text length must be a multiple
    # of m
    if len(text) % m != 0:
        diff = m - (len(text) % m)
        text += diff*"f"
    
    # Iterate over the text taking at each step m characters to transform
    # them into a new m characters
    rowCharacters = []
    for x in range(0, len(text) + 1):
        if x % m == 0 and x > 0:
            # Transform the m characters codes making the dot product between
            # them and the key matrix
            newRowCharacters = list(np.dot(rowCharacters, key))
            newRowCharacters = [(i % 26) for i in newRowCharacters]
            for i in range(x - m, x):
                encryptedText += utils.GetLetter(int(newRowCharacters[i - (x-m)]))
            rowCharacters = []
        
        if(x != len(text)):
            rowCharacters.append(utils.GetCode(text[x]))
    
    # Return the encrypted text
    return encryptedText

def DecryptText(m, decryptKey, text):
    """
    Description
    -----------
    Given m(the dimension of the key matrix), the decrpyt key(matrix)
    and the encrypted text, it decrypts the text using the decrypt key
    and then returns it

    Parameters
    ----------
    key : 2-dimensional list or np.array
        The mxm matrix to use as a a decrypt key in the Hill cipher
    text : string
        The text to decrypt, it must be of length m
    """

    try:
        utils.IsValidMatrix(key)
    except:
        return -1

    m = len(key)
    decryptedText = ""
    
    # Iterate over the text taking at each step m characters to transform
    # them into a new m characters
    rowCharacters = []
    for x in range(0, len(text) + 1):
        if x % m == 0 and x > 0:
            # Transform the m characters codes making the dot product between
            # them and the key matrix
            newRowCharacters = list(np.dot(rowCharacters, decryptKey))
            newRowCharacters = [(i % 26) for i in newRowCharacters]
            for i in range(x - m, x):
                decryptedText += utils.GetLetter(int(newRowCharacters[i - (x-m)]))
            rowCharacters = []
        
        if(x != len(text)):
            rowCharacters.append(utils.GetCode(text[x]))
    
    # Return the encrypted text
    return decryptedText

"""
# Example 1
m = 3
n = 255
key = [[10,4,12],[3,14,4],[8,9,0]]
inverseKey = ComputeInverseKey(m, n, key)

EncryptImage(m, key, "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/600px-Cat03.jpg")
DecryptImage(m, inverseKey, "result.pgm")


# Example 2
m = 2
n = 26
key = [[11, 8], [3, 7]]
inverseKey = ComputeInverseKey(m, n, key)
text = "july"

encryptedText = EncryptText(m, key, text)
print(encryptedText)
decryptedText = DecryptText(m, inverseKey, encryptedText)
print(decryptedText)
"""
m = 3
n = 255
key = [[10,4,12],[3,14,4],[8,9,0]]
inverseKey = CryptoanalysisHill.ComputeInverseKey(m, n, key)

EncryptImage(key, "https://upload.wikimedia.org/wikipedia/commons/5/56/Tux.jpg")
DecryptImage(inverseKey, "result1.pgm")