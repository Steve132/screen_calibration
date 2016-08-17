import numpy

def densify_channel(values,indices,outdims,iterations):
	#values as fp32
	#indices as indices
	#indices to linearized_indices (outdims)
	#H=5x5x5 or 3x3x3 gaussian or box
	#dense=zeros()
	for i in range(iterations):
		dense[linearized_indices]=values
		dense=convolve(dense,H)
	return dense
	
