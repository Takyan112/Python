import convolution, numpy as np
from PIL import Image


font = np.asarray(Image.open('ascii.png').convert('L'))/192


# font = (1-font)-np.average(font)


kernels = [convolution.Convolution((12,8,1),(0,0,0),(12+4,8,1)) for i in range(95)]
for i,kernel in enumerate(kernels):
    kernel.weights = font[:,i*8:(i+1)*8].T[...,None]
    epsilon = np.finfo(np.float_).eps
    kernel.weights = np.divide(kernel.weights, epsilon+np.average(kernel.weights**2))

image = np.asarray(Image.open('../pathtoyourphoto.png').convert('L'))/255


# image = (1-image)-np.average(image)


results = np.array([kernel.conv(image[...,None]) for kernel in kernels])
result = np.argmax(results**2, axis=0)+32

txt = '\n'.join([''.join([chr(char) for char in row]) for row in result])
print(txt)

#with open('output.txt', 'w') as o:
#    o.write(txt)
    
