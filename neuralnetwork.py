import numpy as np

class NeuralNetwork:
    
    def __init__(self, layer_sizes, learning_rate=0.1, file_path='net.npz'):
        weight_shapes = [(a,b) for a,b in zip(layer_sizes[1:],layer_sizes[:-1])]
        self.weights = [np.random.standard_normal(s)/s[1]**.5 for s in weight_shapes]
        self.biases = [np.zeros((s,1)) for s in layer_sizes[1:]]
        self.learning_rate = learning_rate
        self.file_path = file_path
        self.change_w_v, self.change_b_v = [0]*len(self.weights), [0]*len(self.biases)
        
    def predict(self, a):
        for w,b in zip(self.weights,self.biases): \
            a = self.activation_function(np.matmul(w,a) + b)
        return a

    def forward(self, a):
        self.activation, self.weighted_input = [a], []
        for w,b in zip(self.weights,self.biases):
            z = np.matmul(w,a) + b
            a = self.activation_function(z)
            self.activation.append(a)
            self.weighted_input.append(z)
        return a
    
    def backward(self, loss):
        self.error = [loss*self.activation_derivative(self.weighted_input[-1])]
        # δl=((wl+1)Tδl+1)⊙σ′(zl)
        for w,z in zip(self.weights[:0:-1],self.weighted_input[-2::-1]): \
            self.error.append(np.matmul(w.T,self.error[-1])*self.activation_derivative(z))
        self.error.reverse()
        return np.matmul(self.weights[0].T,self.error[0])

    def update(self): 
        self.change_b = [np.average(x,axis=0) for x in self.error]
        #self.change_w = np.average([[np.outer(xx,yy) for xx,yy in zip(x,y)] for x,y in zip(self.error,self.activation[:-1])],axis=1)
        self.change_w = [np.inner(x.T[0],y.T[0])/x.shape[0] for x,y in zip(self.error,self.activation[:-1])]
        #with momentum
        beta = 0.9
        self.change_w_v = [v*beta + m*self.learning_rate for v, m in zip(self.change_w_v, self.change_w)]
        self.change_b_v = [v*beta + m*self.learning_rate for v, m in zip(self.change_b_v, self.change_b)]
        self.weights = [w-v for w, v in zip(self.weights, self.change_w_v)]
        self.biases  = [b-v for b, v in zip(self.biases, self.change_b_v)]
        #without momentum
        #self.weights = self.weights - np.multiply(self.change_w,self.learning_rate)
        #self.biases = self.biases - np.multiply(self.change_b,self.learning_rate)

    def train(self, images, lables, print_loss=False):
        self.backward(self.loss_derivative(self.forward(images),lables))
        self.update()
        if print_loss: self.print_loss(self.activation[-1],lables)
        
    def print_loss(self, images, lables):
        print('loss = {0}'.format(np.average(self.loss_function(self.predict(images),lables))))
    
    def save(self):
        np.savez(self.file_path,weights=self.weights,biases=self.biases,learning_rate=self.learning_rate)
    
    def load(self):
        with np.load(self.file_path) as data:
            self.weights,self.biases,self.learning_rate = data['weights'],data['biases'],data['learning_rate']

    @staticmethod
    def loss_function(guess, lables):
        return -((1-lables)*np.log(1-guess)+lables*np.log(guess)) # .5*((guess-lables)**2)
    
    @staticmethod
    def loss_derivative(guess, lables):
        return (1-lables)/(1-guess)-(lables/guess) # guess-lables
    
    @staticmethod
    def activation_function(x):
        return 1/(1+np.exp(-x))
    
    @staticmethod
    def activation_derivative(x):
        return NeuralNetwork.activation_function(x)*(1-NeuralNetwork.activation_function(x))
