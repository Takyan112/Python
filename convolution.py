import numpy as np

class Convolution:
    def __init__(self, kernel_size, padding_size, stride_size):
        self.ndim = len(kernel_size)
        self.kernel_size = np.array(kernel_size)
        self.padding_size = np.array(padding_size)
        self.stride_size = np.array(stride_size)
        self.pad_width = np.c_[padding_size,padding_size] # [pad , ... , pad]
        f = lambda x: x if x < 0 else None
        self.slices = [[...,]+[np.s_[i:f(i-self.kernel_size[dim]+1):self.stride_size[dim]]
                        for dim,i in enumerate(slice_)]
                        for slice_ in np.indices(self.kernel_size).T.reshape(-1,self.ndim)]
        self.weights = np.random.standard_normal(self.kernel_size)
        
    def conv(self, picture):
        pic = np.pad(picture,
                pad_width = np.r_[np.zeros((picture.ndim-self.ndim,2),dtype=np.int_), self.pad_width],
                mode = 'constant',
                constant_values=0)
        #generator is faster
        weighted_sum = np.sum((pic[tuple(slice_)]*weight
                        for slice_,weight in zip(self.slices,self.weights.flat))
                        ,axis=0)   
        return weighted_sum

