import neuralnetwork as nn
import numpy as np

x = np.atleast_3d([[1.,0.,0.],
                   [0.,1.,0.],
                   [0.,0.,1.]])

net = nn.NeuralNetwork((3,1,3), file_path='netnetnet.npz',learning_rate=0.1)

for num in range(1000):
    net.train(x,x,True)
    if num != 1000-1: print("\x1b[F\x1b[K", end="")

print(str(x) + "\x1b[10F\x1b[10G" + str(np.around(net.predict(x),2)).replace("\n", "\x1b[E\x1b[10G"))