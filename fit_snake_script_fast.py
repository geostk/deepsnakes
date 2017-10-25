import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from skimage.filters import gaussian
import scipy
#from skimage.segmentation import active_contour
import snake_inference_fast as snake
import time


# Test scipy version, since active contour is only possible
# with recent scipy version

split_version = scipy.__version__.split('.')
if not(split_version[-1].isdigit()): # Remove dev string if present
        split_version.pop()
scipy_version = list(map(int, split_version))
new_scipy = scipy_version[0] > 0 or \
            (scipy_version[0] == 0 and scipy_version[1] >= 14)

filename = 'square_energy.png'
img = io.imread(filename)
img = img[:,:,0]
img = np.float32(img)/255
filename = 'square_corners.png'
img_beta = io.imread(filename)
img_beta = img_beta[:,:,0]
beta = np.float32(img_beta)*0.01
filename = 'square_alpha.png'
img_alpha = io.imread(filename)
img_alpha = img_alpha[:,:,0]
kappa = (0.02 - np.float32(img_alpha)*0.0001)*1
alpha = np.float32(img_alpha)*0.0001


Du = np.gradient(gaussian(img,4),axis=0)*500
Dv = np.gradient(gaussian(img,4),axis=1)*500


L = 60
s = np.linspace(0, 2*np.pi, L, endpoint=False)
init_u = 128 + 80*np.cos(s)
init_v = 128 + 80*np.sin(s)
init_u = init_u.reshape([L,1])
init_v = init_v.reshape([L,1])

u = init_u
v = init_v
du = np.zeros(u.shape)
dv = np.zeros(v.shape)
gamma  = 1
max_px_move = 1
delta_s = 1
maxiter = 300


tic = time.time()
u, v, du, dv, snake_hist = \
    snake.active_contour_step(maxiter, Du, Dv, du, dv, u, v,
    alpha, beta, kappa,
    gamma, max_px_move, delta_s)
print('%.2f' % (time.time() - tic) + ' s snake')

fig0, (ax) = plt.subplots(ncols=1)
plt.gray()
im = ax.imshow(img)
for i in range(0,len(snake_hist)):
    ax.plot(snake_hist[i][:, 1], snake_hist[i][:, 0], '-', color=[1-i / len(snake_hist), 1-i / len(snake_hist), i / len(snake_hist)], lw=1)
ax.plot(v, u, '--k', lw=3)
plt.colorbar(im, ax=ax)
fig0.suptitle('Image, GT (red) and converged snake (black)', fontsize=20)
plt.show()

#ax.set_xticks([]), ax.set_yticks([])
#ax.axis([0, img.shape[1], img.shape[0], 0])