from PIL import Image

def str_bin(message):
    bin_message = []
    for letter in message:
        bin_message.append(format(ord(letter),"08b"))
    return bin_message

def bin_str(bin_message):
    message = []
    for binary in bin_message:
        message.append(chr(int(binary,2)))
    return  "".join(message)


def can_encode(bin_message,pixels):
    if (len(bin_message)*8<=(len(pixels)*3 - len(pixels))):
        return True
    return False

def encoding_bit(pixel,binary):
    if pixel%2!= 0 and binary=='0':
        return -1
    elif pixel%2 == 0 and binary!='0':
        return 1
    return 0

def generate_pix(bin_message,img):
    iter_pixels = iter(img.getdata())
    size_message = 0
    while size_message<len(bin_message):    
        pixs = [pixel for pixel in next(iter_pixels)+next(iter_pixels)+next(iter_pixels)]
        for i in range(8):      
            cont = encoding_bit(pixs[i],bin_message[size_message][i]) 
            pixs[i]+=cont

        if size_message == (len(bin_message)-1):
            if pixs[-1]%2!=0:
                pixs[-1]-=1
        else:
            if pixs[-1]%2==0:
                pixs[-1]+=1
        size_message+=1
        yield(pixs[0:3])
        yield(pixs[3:6])
        yield(pixs[6:9])


def encode_img(img,bin_message):
    new_img = img.copy()
    pixels = new_img.getdata()

    if can_encode(bin_message,pixels):
        width,height = new_img.size
        x,y = (0,0)
        cont = 0
        for pix in generate_pix(bin_message,img):
            new_img.putpixel((x,y),tuple(pix))
            if x==width:
                y+=1
                x=0
            else:
                x+=1 
        return new_img

    return None
    

def decode_img(new_img):
    bin_letter = []
    bin_message = []
    iter_pixels = iter(new_img.getdata())

    while True:
        pixs = [pixel for pixel in next(iter_pixels)+next(iter_pixels)+next(iter_pixels)]
        for i in range(8):
            bin_letter.append(str(pixs[i]%2))

        bin_message.append(''.join(bin_letter))
        bin_letter = []
        if pixs[-1]%2==0:
            return bin_message
        



if __name__ == '__main__':
    option = int(input('Select your option (encode:1 | decode: 2): '))
    if option == 1:
        image_path = input("Enter the path to the image: ")
        print(100*'-')
        message = input("Enter with your message to encode: ")
        bin_message = str_bin(message)
        img = Image.open(image_path)
        new_img = encode_img(img,bin_message)
        if new_img:
            encoded_name = input('Name of the encoded image: ')
            new_img.save(encoded_name ,format='PNG')
            print('Encoded Successfuly!')
        else:
            print('ERROR')
    elif option == 2:
        image_path = input('Enter the path to the encoded image: ')
        encoded_img = Image.open(image_path)
        bin_message = decode_img(encoded_img)
        print('The message found was:',bin_str(bin_message))