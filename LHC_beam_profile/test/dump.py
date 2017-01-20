import numpy as np
import pylab as plt
import h5py as hp


# Loading the profile
filename = r'./prof.h5'
h5file = hp.File(filename, 'r') 
profile = np.array(h5file["/Profile/profile"], dtype = np.double)
samplerate = float(h5file["/Profile/samplerate"][0])
recordlength = int(h5file["/Profile/record_length"][0])
h5file.close()



h5file = hp.File(r'tf.h5', 'r') 
freq_array_f64 = np.array(h5file["/TransferFunction/freq"])
TF_array_c128 = np.array(h5file["/TransferFunction/TF"])
h5file.close()

TF_real_f64 = TF_array_c128.real
TF_imag_f64 = TF_array_c128.imag



f = hp.File("dump.h5",'w')
f.require_group('dump')

g = f['dump']

g.create_dataset('profile_f32', shape = profile.shape, dtype = 'f')
g['profile_f32'][:,:] = profile

g.create_dataset('tf_real_f64', shape = TF_real_f64.shape, dtype = 'd')
g['tf_real_f64'][:] = TF_real_f64
g.create_dataset('tf_imag_f64', shape = TF_imag_f64.shape, dtype = 'f')
g['tf_imag_f64'][:] = TF_imag_f64.astype(dtype='f')


f.close()
                     
