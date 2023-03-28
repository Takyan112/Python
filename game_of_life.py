import tkinter as tk
import numpy as np

WIDTH = 480
HEIGHT = 360

def _photo_image(image: np.ndarray):
    height, width = image.shape[:2]
    data = 'P5 {0} {1} 255 '.format(width,height).encode() + image.astype(np.uint8).tobytes()
    return tk.PhotoImage(width=width, height=height, data=data, format='PPM')

root = tk.Tk()
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

grid = np.random.rand(HEIGHT, WIDTH) < 0.1
look_up = np.stack((np.mgrid[-1:HEIGHT-1,0:WIDTH], # Top
                    np.mgrid[-HEIGHT+1:HEIGHT-HEIGHT+1,0:WIDTH], # Bottom
                    np.mgrid[0:HEIGHT,-1:WIDTH-1], # Left
                    np.mgrid[0:HEIGHT,-WIDTH+1:WIDTH-WIDTH+1], # Right
                    np.mgrid[-1:HEIGHT-1,-1:WIDTH-1], # Top-left
                    np.mgrid[-1:HEIGHT-1,-WIDTH+1:WIDTH-WIDTH+1], # Top-right
                    np.mgrid[-HEIGHT+1:HEIGHT-HEIGHT+1,-1:WIDTH-1], # Bottom-left
                    np.mgrid[-HEIGHT+1:HEIGHT-HEIGHT+1,-WIDTH+1:WIDTH-WIDTH+1], # Bottom-right
                    ),axis=1)
# look_up.shape == (2,8,HEIGHT,WIDTH)

def task():
    global grid, look_up, stop
    if ~stop:
        neighbours = np.sum(grid[look_up[0],look_up[1]],axis=0)
        grid = np.logical_or((neighbours==3),np.logical_and(grid,(neighbours==2)))
        # new cell when neighbours == 3, keep alive when neighbours == 2~3
    img = _photo_image(grid*255)
    canvas.create_image(0, 0, anchor=tk.NW, image=img)
    root.update()
    root.after(0,task)    

def mouse(event,paint,size):
    global grid
    area = np.mgrid[-size:size,-size:size].T+[event.y, event.x]
    area = area.clip(0,[HEIGHT-1,WIDTH-1]).T
    grid[area[0],area[1]] = paint

def start_stop(event):
    global stop
    stop = ~stop    

root.bind("<space>", start_stop)
root.bind("<B1-Motion>", lambda event : mouse(event, paint=True, size=4))
root.bind("<B3-Motion>", lambda event : mouse(event, paint=False, size=16))

stop = False
root.after(0,task)
root.mainloop()
