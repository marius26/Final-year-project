import openpiv.tools
import openpiv.pyprocess
import openpiv.scaling

frame_a = openpiv.tools.imread( "exp1_001_a.bmp" )
frame_b = openpiv.tools.imread( "exp1_001_b.bmp" )
u, v, sig2noise = openpiv.process.extended_search_area_piv( frame_a, frame_b, window_size=24,overlap=24)
x, y = openpiv.process.get_coordinates( image_size=frame_a.shape, window_size=24, overlap=12 )
u, v, mask = openpiv.validation.sig2noise_val( u, v, sig2noise, threshold = 1.3 )
u, v = openpiv.filters.replace_outliers( u, v, method="localmean", n_iter=10, kernel_size=2)
x, y, u, v = openpiv.scaling.uniform(x, y, u, v, scaling_factor = 96.52 )
openpiv.tools.save(x, y, u, v, "exp1_001.txt" )