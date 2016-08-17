
//http://neocotic.com/qrious/
//https://codepen.io/ianmcgregor/pen/qkvcj
//http://fiddle.jshell.net/danthewolfe/6ja1kw32/

function hexsha2num(hs,bits)
{
	var nbytes=Math.ceil(bits/8);
	var nval=parseInt(hs.substr(0,2*nbytes),16);
	var mask=(1 << bits)-1;
	return nval & mask;
}

function prand_bits(index,bits,seed)
{
	var input=seed.toString()+index.toString();
	var output=sha256(input);
	var bits=hexsha2num(output,bits);
	return bits;
}

function prand_img(width,height,bits,seed)
{
	var imgk=[];
	for(var x=0;x<width;x++)
	{
		var col=[];
		for(var y=0;y<height;y++)
		{
			var pix=[];
			for(var c=0;c<3;c++)
			{
				var index=x;
				index*=height;
				index+=y;
				index*=3;
				index+=c;
				pix.push(prand_bits(index,bits,seed));
			}
			col.push(pix);
		}
		imgk.push(col);
	}
	return imgk;
}
