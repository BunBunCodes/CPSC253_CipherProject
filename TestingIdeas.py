import re

def encrypt(phrase):   
    str = ""
    for i in range(len(phrase)):
        letter = phrase[i]
        # cinvert to ASCII
        hexNum = ord(letter)
        # we convert to hex here and
        # we strip the unneccesary bit here
        hexCode = hex(hexNum).lstrip("0x")
        str += hexCode   
    str = formatIntoHexColorCodes(str)
    return str

def decrypt(phrase):
    newPhrase = removeWhiteSpaces(phrase)
    str = ""
    for i in range(0, len(newPhrase), 2):
        # each hex code comes in pairs of 2
        part =  newPhrase[i : i + 2]
        # converting back to characters
        ch = chr(int(part, 16))
        str += ch
    return str

def formatIntoHexColorCodes(str):
    newStr = ""
    if(len(str) % 6 != 0):
        
        # this makes it so that we have mutiples of 6
        # adds on 00 (NUL) to finish of a set of
        # 6 numbers
        for i in range(int((len(str) % 6))):
            str += "00"
    
    # this for loop just adds on
    # a blank space after every
    # 6th character        
    for i in range(0, len(str), 6):
        newStr += str[i : i + 6] + " "
    
    printColoredHexCodes(newStr)
    return newStr.strip()

def removeWhiteSpaces(str):
    # Here we remove everything
    # the blankspaces
    # and the NUL
    str = str.replace("00", "")
    newStr = str.replace(' ','')
    return newStr

def readFile(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read().strip()

def writeFile(filename, content):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

def printColoredHexCodes(str):
    # here we split up our hex codes
    # ANSI ESCAPE CODES SHOULD ONLY WORK ON THE TERMINAL,
    # WHICH IS WHY WE DONT TRY TO HAVE THEM SHOW UP IN OUR TXT FILES
    hexCodes = str.split()
    for code in hexCodes:
        # we are using regex to check if they are valid hex codes
        # we check that they only have letters and numbers
        # we also check that they are 6 cars long
        if re.match(r'^[0-9A-Fa-f]{6}$', code):
            
            # here we convert hex into RGB
            rgb = tuple(int(code[i:i+2], 16) for i in (0, 2, 4))
            # ANSI color code
            # \033[XXXm
            # this escape code format used for our color code and rest code
            color_code = f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"
            reset_code = "\033[0m"  # ANSI reset code
            # printing to terminal here
            print(color_code + code + reset_code, end=" ")

if __name__ == '__main__':
    while True:
        choice = input("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
                        "\nWhat would you like to do today?\n"
                        "Type 'e' for encryption, 'd' for decryption, or any other key to exit: ").strip().lower()
        
        if choice == 'e':  
            input_text = readFile("input.txt")
            if input_text is not None:
                encrypted_text = encrypt(input_text)
                writeFile("encrypted.txt", encrypted_text)
                print("\nEncryption complete. Your output has been saved to 'encrypted.txt'.")

        elif choice == 'd':  
            encrypted_text = readFile("encrypted.txt")
            if encrypted_text is not None:
                decrypted_text = decrypt(encrypted_text)
                writeFile("output.txt", decrypted_text)
                print("Decryption complete. Your output has been saved to 'output.txt'.")

        else:
            print("Exiting program.")
            break