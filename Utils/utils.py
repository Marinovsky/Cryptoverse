def GetCode(c):
    """
    Description
    -----------
    Using the correspondence a <-> 0, b <-> 1, ... , z <-> 25
    we associate to each character its corresponding numeric
    value.

    This function returns the corresponding numeric value 
    associated with the given character, according to the
    scheme described above.
    """
    return ord(c) - 97

def GetLetter(n):
    """
    Description
    -----------
    Using the correspondence a <-> 0, b <-> 1, ... , z <-> 25
    we associate to each character its corresponding numeric
    value.

    This function returns the corresponding letter asociated
    with the given value, according to the scheme described 
    above.
    """
    return chr(n + 97)

def preProcessText(text):
    """
    Description
    -----------
    This function returns the given text in lowercase without
    spaces.
    """
    text = text.replace(' ', '')
    text = text.lower()
    processedText = ""
    for c in text:
        if ord(c) >= 97 and ord(c) <= 97 + 25:
            processedText += c
    return processedText

def IsValidMatrix(m):
    if len(m) != len(m[0]):
        raise "The matrix is not square"