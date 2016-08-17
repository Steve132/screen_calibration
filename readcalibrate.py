#!/usr/bin/env python

from PIL import Image,ImageDraw
import zbar
import sys
import cv2
import numpy as np
import random
import json
import hashlib
from collections import namedtuple


scanner = zbar.ImageScanner()

# configure the reader
scanner.parse_config('enable')
def getbb(location):
	x2, y2 = zip(*location)
	return (min(x2),min(y2)),(max(x2),max(y2))

def yield_barcodes(pil):# obtain image data
	global scanner	
	width, height = pil.size
	raw = pil.tostring()
# wrap image data
	image = zbar.Image(width, height, 'Y800', raw)
	scanner.scan(image)
	for symbol in scanner.results:
		yield symbol
	scanner.recycle(image)

def yield_all_barcodes(pil,num):
	n=0
	draw=ImageDraw.Draw(pil)
	while(n < num):
		found=False
		for bcsym in yield_barcodes(pil):
			yield bcsym
			bb=getbb(bcsym.location)
			found=True
			draw.rectangle(bb, fill=0)
			n+=1
		if(not found):
			break
	del draw
		
class QrCalibrateSymbol(object):
	def __init__(self,bcsym):
		v=int(bcsym.data)
		self.corner=v % 4
		v=v//4
		self.npheight=v % 64
		v=v//64
		self.npwidth=v % 64
		v=v//64
		self.seed=v
		self.location=(bcsym.location[0],bcsym.location[3],bcsym.location[2],bcsym.location[1])

	def get_corner_coords(self,scale=1):
		offsets=[ (0,0), (self.npwidth-4,0),(self.npwidth-4,self.npheight-4),(0,self.npheight-4)]
		locations= [ (0,0),(4,0),(4,4),(0,4) ]
		o=offsets[self.corner]
		return [((o[0]+x)*scale,(o[1]+y)*scale) for x,y in locations]
	def __str__(self):
		return "corner: %r,npsize: %r, seed: %r, location: %r" % (self.corner,(self.npwidth,self.npheight),self.seed,self.location)

###prandomimg

def hexsha2num(hs,bits):
	nbytes=bits//8 + (1 if bits % 8 else 0)
	num=int(hs[0:(nbytes*2)],base=16)
	mask=(1 << bits)-1
	return num & mask

def prand_bits(index,bits,seed):
	input=str(seed)+str(index)
	output=hashlib.sha256(input).hexdigest()
	return hexsha2num(output,bits)

def prand_img_pixel(width,height,x,y,bits,seed):
	pix=[0]*3
	for c in range(3):
		index=x
		index*=height
		index+=y
		index*=3
		index+=c
		pix[c]=prand_bits(index,bits,seed)
	return pix

###prandimg



def get_transformed_image(pil,calibrated_symbols,scale):
	csym=calibrated_symbols[0]
	corner_coords=np.asarray([cc for c in calibrated_symbols for cc in c.get_corner_coords(scale=scale)  ],dtype=np.float32)
	img_coords=np.asarray([ic for c in calibrated_symbols for ic in c.location],dtype=np.float32)
	H,msk=cv2.findHomography(img_coords,corner_coords)
	arrayimg=cv2.warpPerspective(np.array(pil), H, dsize=(csym.npwidth*scale,csym.npheight*scale))
	return Image.fromarray(arrayimg),csym


def deterministic_image(npwidth,npheight,scale,seed):
	dim=Image.new("RGB",(npwidth,npheight))
	dim_sampler=dim.load()
	for x in range(npwidth):
		for y in range(npheight):
			dim_sampler[x,y]=tuple(prand_img_pixel(npwidth,npheight,x,y,8,seed))
	dim=dim.resize((npwidth*scale,npheight*scale),Image.NEAREST)
	return dim

def sample_image_and_deterministic(tpil,npwidth,npheight,scale,seed,scaleend=4,t=0):
	s=scale
	while(s > scaleend):
		tpil.thumbnail((tpil.size[0]//2,tpil.size[1]//2),Image.ANTIALIAS)
		s=s//2
	tpil_sampler=tpil.load() #//faster sampler
	outputs=[]

	for x in range(npwidth):
		for y in range(npheight):
			tc=((x+4) % npwidth,(y+4) % npheight)	#corners
			if(tc[0] >= 8 and tc[1] >= 8):
				lc=(scaleend*x + scaleend//2,scaleend*y + scaleend//2)
				pixel=list(tpil_sampler[lc[0],lc[1]])
				deterministic_pixel=prand_img_pixel(npwidth,npheight,x,y,8,seed)
				outputs.append([t,x,y]+pixel+deterministic_pixel)
	return outputs

def yield_results(fp):
	pimg = Image.open(fp)
	calibrated_symbols=[QrCalibrateSymbol(bsym) for bsym in yield_all_barcodes(pimg.convert('L'),4)]
	tpil,csym=get_transformed_image(pimg,calibrated_symbols,32)
	#tpil.save('tpil.png')
	#dim=deterministic_image(csym.npwidth,csym.npheight,32,seed=csym.seed)
	#dim.save('dpil.png')
	outputs=sample_image_and_deterministic(tpil,csym.npwidth,csym.npheight,32,seed=csym.seed)
	for o in outputs:
		yield o

if __name__=="__main__":
	for f in sys.argv[1:]:
		for o in yield_results(f):
			print('\t'.join([str(oitem) for oitem in o]))


