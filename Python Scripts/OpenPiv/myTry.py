# importing all necessary libraries
from openpiv import tools, pyprocess, validation, filters, scaling

import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline

import imageio
import importlib_resources
import pathlib

# read images

path = importlib_resources.files('openpiv')

#each image represents a frame
frame_a  = tools.imread( path / '/home/pi/Final-year-project/Python Scripts/OpenPiv/2-1.bmp' )
frame_b  = tools.imread( path / '/home/pi/Final-year-project/Python Scripts/OpenPiv/2-2.bmp' )

fig,ax = plt.subplots(1,2,figsize=(12,10))
ax[0].imshow(frame_a,cmap=plt.cm.gray);
ax[1].imshow(frame_b,cmap=plt.cm.gray);


# Processing

winsize = 32 # pixels, interrogation window size in frame A
searchsize = 38  # pixels, search area size in frame B
overlap = 17 # pixels, 50% overlap
dt = 0.02 # sec, time interval between the two frames

u0, v0, sig2noise = pyprocess.extended_search_area_piv(
    frame_a.astype(np.int32),
    frame_b.astype(np.int32),
    window_size=winsize,
    overlap=overlap,
    dt=dt,
    search_area_size=searchsize,
    sig2noise_method='peak2peak',
)


#find the center of each interogation window
x, y = pyprocess.get_coordinates(
    image_size=frame_a.shape,
    search_area_size=searchsize,
    overlap=overlap,
)
print("Processing done")

#Post processing - plot vectors

invalid_mask = validation.sig2noise_val(u0, v0, sig2noise, threshold=1.05)


u2, v2 = filters.replace_outliers(
    u0, v0,
    invalid_mask,
    method='localmean',
    max_iter=3,
    kernel_size=3,
)

# convert x,y to mm
# convert u,v to mm/sec

x, y, u3, v3 = scaling.uniform(
    x, y, u2, v2,
    scaling_factor = 96.52,  # 96.52 pixels/millimeter
)

# 0,0 shall be bottom left, positive rotation rate is counterclockwise
x, y, u3, v3 = tools.transform_coordinates(x, y, u3, v3)

# Results
# Ensure that all variables are arrays
x = np.asarray(x)
y = np.asarray(y)
u3 = np.asarray(u3)
v3 = np.asarray(v3)
invalid_mask = np.asarray(invalid_mask)

# Concatenate x, y, u3, and v3 into a single array
data = np.column_stack((x.flatten(), y.flatten(), u3.flatten(), v3.flatten()))

# Save the concatenated data array along with invalid_mask to a text file
np.savetxt('exp1_001.txt', np.column_stack((data, invalid_mask.flatten())))

fig, ax = plt.subplots(figsize=(8, 8))
tools.display_vector_field(
    pathlib.Path('exp1_001.txt'),
    ax=ax, scaling_factor=96.52,
    scale=50,  # scale defines here the arrow length
    width=0.0035,  # width is the thickness of the arrow
    on_img=True  # overlay on the image
)
 
