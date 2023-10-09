import numpy as np
from scipy import sparse
from scipy import ndimage
from pylab import *
from scipy.sparse import hstack
from scipy.sparse.linalg import svds
from PIL import Image
import numpy as num


def weights(x, dx=1, orig=0):
    '''
    It computes 'weights' of each pixel
    '''
    x = np.ravel(x)     
    floor_x = np.floor((x - orig) / dx)   #The floor of the scalar x is the largest integer i, such that i <= x (rounded)
    alpha = (x - orig - floor_x * dx) / dx
    return np.hstack((floor_x, floor_x + 1)), np.hstack((1 - alpha, alpha))


def generate_center_coordinates(l_x):
    l_x = float(l_x)
    X, Y = np.mgrid[:l_x, :l_x]
    center = l_x / 2.
    X += 0.5 - center
    Y += 0.5 - center
    return X, Y


def build_system_matrix(l_x, n_dir):
    """
    Compute the tomography design matrix.

    Parameters
    ----------

    l_x : int
        linear size of image array

    n_dir : int
        number of angles at which projections are acquired.

    Returns
    -------
    p : sparse matrix of shape (n_dir l_x, l_x**2)
 
    """
    X, Y = generate_center_coordinates(l_x)  #call the func.
    angles = np.linspace(0, np.pi, int(n_dir), endpoint=False)  # Convert n_dir to an integer
    data_inds, wghts, detector_inds = [], [], []
    data_unravel_indices = np.arange(l_x ** 2)
    data_unravel_indices = np.hstack((data_unravel_indices,
                                      data_unravel_indices))
    for i, angle in enumerate(angles):  #''core, s.page 221 book''#
        Xrot = np.cos(angle) * X - np.sin(angle) * Y    
        inds, w = weights(Xrot, dx=1, orig=X.min())
        mask = np.logical_and(inds >= 0, inds < l_x) #mask : because Iconsider only my case, the rest set to 0 (whereas the program is general)
        wghts += list(w[mask])
        detector_inds += list(inds[mask] + i * l_x)
        data_inds += list(data_unravel_indices[mask])
    system_matrix = sparse.coo_matrix((wghts, (detector_inds, data_inds))) 
    #proj_operatorM= sparse.coo_matrix((weights, (camera_inds, data_inds)),shape=(n_dir*l_x,l_x*l_x,)).todense()
    return system_matrix


def tls(A, b, k):
    """
    A tls (the least square)solution of Ax= b, for sparse A.
    Computes Moore-Penrose pseudoinverse of A.

    Parameters
    ----------

    A : system matrix




    b : projection vector (sinogram)

    k : number of singular values

    Returns
    -------
    v : raveled reconstructed image
    """
    u, s, v= svds(hstack([A, b]), k=l)
    return v[-1, :-1]/ v[-1, -1]

############################################################################################

im=Image.open('image1.jpeg')  # picks the image file from the working directory
width, height = im.size  #determines the dimensions of the image in pixels

if width==height:   # checks, wheather the image is square-shaped , nxn
    print('Image dimension is ',width,'.' ) #if yes, print its size
else:
    print('Image is not square-shaped. Resize the image!')
    sys.exit()  #if the image is not nxn, terminate the script

'''
IMPORT IMAGE
'''

im= im.convert('L')     #convert the image to monochrome
imarray=num.array(im)   #convert the momnochromatic image to 2D array "imarray"

'''Rescale to 0-255 shades of grey  and convert to uint'''
data = (255.0 / imarray.max() * (imarray - imarray.min())).astype(np.uint8)
#name of the image
'''
(Part used only for this programme) :
CALL THE FUNCTIONS : MAIN BODY
'''
l=width   #alocate the dimension of the image into variable "l"

system_matrix = build_system_matrix(l, l/2)
'''computes projected image (sinogram)'''
proj = system_matrix * data.ravel()[:, np.newaxis] #projection vector (data is 2d array but Python makes a vector -with ravel)
'''calls function which solves Ax=B (SVD)'''
reconstructed_ravel = tls(system_matrix, proj, k = l)
'''unravels the reconstructed image projections'''
reconstructed = reconstructed_ravel.reshape(l,l)

###############################################################################################

'''Displays original image vs reconstructed image'''
plt.figure(figsize=(8, 3.3))
plt.subplot(121)
plt.imshow(data, cmap=plt.cm.gray, interpolation='nearest')
plt.axis('off')
plt.title('original image')
plt.subplot(122)
plt.imshow(reconstructed, cmap=plt.cm.gray, interpolation='nearest')
plt.title('reconstructed image')
plt.axis('off')

plt.subplots_adjust(hspace=0.01, wspace=0.01, top=1, bottom=0, left=0,)

plt.savefig("C:\\Users\Bisagny\PycharmProjects\DataScience", dpi=500)

plt.show()

