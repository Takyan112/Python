import tkinter as tk
import numpy as np

WIDTH = 720
HEIGHT = 480
MAX_ITER = 32

#https://stackoverflow.com/questions/53308708/how-to-display-an-image-from-a-numpy-array-in-tkinter
def _photo_image(image: np.ndarray):
    height, width = image.shape[:2]
    data = 'P6 {0} {1} 255 '.format(width,height).encode() + image.astype(np.uint8).tobytes()
    return tk.PhotoImage(width=width, height=height, data=data, format='PPM')

#https://www.rapidtables.com/convert/color/hsv-to-rgb.html
def _hsv_to_rgb(hsv: np.ndarray): # hsv(0-180,0-255,0-255)=>rgb(0-255)
    h = (1/ 30)*hsv[...,0]
    c = (1/255)*hsv[...,2]*hsv[...,1]
    x = c*(1-abs(h%2-1))
    m = hsv[...,2]-c
    
    h = np.int_(h)%6
    idx = np.indices(h.shape)
    hsv[tuple(np.r_[idx,(h[None,:]-5)//2])] = c+m
    hsv[tuple(np.r_[idx,(1-h[None,:])%3])] = x+m
    hsv[tuple(np.r_[idx,h[None,:]//2-1])] = m
    return hsv

root = tk.Tk()
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

#Try swap c and z !!! also change the power
p = 2 # p = np.e
c = np.dot(np.mgrid[-WIDTH/2:WIDTH/2,-HEIGHT/2:HEIGHT/2].T,[1,1j])*3/HEIGHT
z = np.full((HEIGHT,WIDTH), 0+0j,dtype=np.cdouble)

#z = np.full((HEIGHT,WIDTH), -0.7+0.27015j,dtype=np.cdouble)
#c, z = z, c

num = np.zeros((HEIGHT,WIDTH),dtype=np.uint8)
mask = np.full((HEIGHT,WIDTH),True,dtype=np.bool_)

for i in range(MAX_ITER):
    z[mask] = z[mask]**p+c[mask]
    mask[np.abs(z)>2] = False
    num[mask] += 1

array = np.full((HEIGHT,WIDTH,3),255,dtype=np.uint8)
array[...,0] = num/MAX_ITER*180
array[...,2] = ~mask*255
_hsv_to_rgb(array)

img = _photo_image(array)

canvas.create_image(0, 0, anchor=tk.NW, image=img)
root.update()
root.mainloop()
