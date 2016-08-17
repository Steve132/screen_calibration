import random
import hashlib

def hexsha2num(hs,bits):
	nbytes=bits//8 + (1 if bits % 8 else 0)
	num=int(hs[0:(nbytes*2)],base=16)
	mask=(1 << bits)-1
	return num & mask
def prand_bits(index,bits,seed):
	input=str(seed)+str(index)
	output=hashlib.sha256(input).hexdigest()
	return hexsha2num(output,bits)
	
seed=1
random.seed(seed)
vals=5;

for i in range(vals):
	print(prand_bits(i,5,seed))