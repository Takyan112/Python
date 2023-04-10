# inspired by Acerola's youtube video [I Tried Sorting Pixels](https://www.youtube.com/watch?v=HMmmBDRy-jE&t=9s)
# very good channel👍
import sys
from PIL import Image

def sortPixel(path = 'image.jpg'):
    slash = '\\' if '\\' in path else '/'
    
    pic = Image.open(path)  # picture
    lum = pic.convert('L')  # luminous
    new = pic.copy()        # result

    print(pic.size)

    arr = []
    z = 0
    prev = lum.getpixel((0,0))

    for y in range(pic.size[1]):
        for x in range(pic.size[0]):
            curr = lum.getpixel((x,y))
            if (prev<128)!=(curr<128):
                z += 1
            arr.append((z*256+lum.getpixel((x, y)), pic.getpixel((x,y))))
            prev = curr
        z += 1

    print(z)

    # sort with lum then z
    arr.sort(key=lambda x: x[0])

    for y in range(pic.size[1]):
        for x in range(pic.size[0]):
            new.putpixel((x,y), arr[x+y*pic.size[0]][1])
    
    new.save((slash+'sorted_').join(path.rsplit(slash,1)))

if __name__=='__main__':
    sortPixel(sys.argv[1])