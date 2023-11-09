def caesar_says(words:str, offset:int) -> str:
    return ''.join([
             chr((ord(char)-65+offset)%26+65) if char.isupper() 
        else chr((ord(char)-97+offset)%26+97) if char.islower()
        else char
        for char in words])

if __name__ == "__main__":
    print(caesar_says("Hello World!", 1))
