from PIL import Image
import matplotlib.pyplot as plot
from matplotlib.widgets import Slider
import time
import numpy as np

height = 1000
width = 1000
x_bound = (-2, 2)
y_bound = (-2, 2)

def julia(n, m, itermax, xmin, xmax, ymin, ymax, c):
    ix, iy = np.mgrid[0:n, 0:m]
    x = np.linspace(xmin, xmax, n)[ix]
    y = np.linspace(ymin, ymax, m)[iy]
    z = x+complex(0,1)*y
    del x, y
    img = np.zeros(z.shape, dtype=int)
    ix.shape = n*m
    iy.shape = n*m
    z.shape = n*m
    for i in range(itermax):
        if not len(z):
            break
        z = np.square(z) + c
        rem = z.real ** 2 + z.imag ** 2 > 4.0
        img[ix[rem], iy[rem]] = i+1
        rem = ~rem
        z = z[rem]
        ix, iy = ix[rem], iy[rem]
    return img

def mandel(n, m, itermax, xmin, xmax, ymin, ymax):
    ix, iy = np.mgrid[0:n, 0:m]
    x = np.linspace(xmin, xmax, n)[ix]
    y = np.linspace(ymin, ymax, m)[iy]
    c = x+complex(0,1)*y
    del x, y
    img = np.zeros(c.shape, dtype=int)
    ix.shape = n*m
    iy.shape = n*m
    c.shape = n*m
    z = np.copy(c)
    for i in range(itermax):
        if not len(z):
            break
        z = np.square(z) + c
        rem = z.real ** 2 + z.imag ** 2 > 4.0
        img[ix[rem], iy[rem]] = i+1
        rem = ~rem
        z = z[rem]
        ix, iy = ix[rem], iy[rem]
        c = c[rem]
    return img

def transform_color(val):
    if val < 0:
        return (0, 0, 0)
    return tuple(map(int, (val * 255, 0, 255 - val * 255)))

def get_julia_img(julia_data, c):
    sTime = time.time()
    I = julia(julia_data[0], julia_data[1], julia_data[2], julia_data[3],
                                   julia_data[4], julia_data[5], julia_data[6], c)
    print("Time: {}".format(time.time() - sTime))
    I[I==0] = 101
    return I

def create_update(img, real_slide, imag_slide, julia_data):
    def _update(val):
        real = real_slide.val
        imag = imag_slide.val
        img.set_data(get_julia_img(julia_data, real + 1j * imag))
        plot.draw()
    return _update

if __name__ == "__main__":
    fig, ax = plot.subplots()
    julia_data = [width, height, 100, x_bound[0], x_bound[1], y_bound[0], y_bound[1]]
    I = get_julia_img(julia_data, 0)
    img = plot.imshow(I.T)
    plot.subplots_adjust(left=0.25, bottom=0.25)
    axreal = plot.axes([0.25, 0.15, 0.65, 0.03])
    aximag = plot.axes([0.25, 0.1, 0.65, 0.03])
    sreal = Slider(axreal, 'Real', -2, 2, valinit=0)
    simag = Slider(aximag, 'Imag', -2, 2, valinit=0)
    sreal.on_changed(create_update(img, sreal, simag, julia_data))
    simag.on_changed(create_update(img, sreal, simag, julia_data))
    plot.show()

