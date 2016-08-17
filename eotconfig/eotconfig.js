var width = 1280;
var height= 720;
var game;



window.onload=function()
{
game = new Phaser.Game(width,height, Phaser.AUTO, 'phaser-example', { preload: preload, create: create, update: update, render: render },false,false);
}

function preload() {

}
function screen_size_to_pattern_size(swidth,sheight,qrheight,poffsetx,poffsety)
{
	innerwidth=swidth-poffsetx*2;
	innerheight=sheight-poffsety*2;
	var pwidth=qrheight/4;
	var npheight=innerheight/pwidth;
	var npwidth=innerwidth/pwidth;
	return {'pwidth':pwidth,'npheight':npheight,'npwidth':npwidth};
}

var poffsetx=64;
var poffsety=72;
var qrsize=128;
var psize=screen_size_to_pattern_size(width,height,qrsize,poffsetx,poffsety);
var npheight=psize['npheight'];
var npwidth=psize['npwidth'];
var pwidth=psize['pwidth'];
var bgwidth=npwidth;
var bgheight=npheight;

function makeqrval(seed,npwidth,npheight,corner)
{
	var value=seed;
	value*=64;
	value+=npwidth;
	value*=64;
	value+=npheight;
	value*=4;
	value+=corner;
	return value;
}
function qrpattern(seed,qrheight,npwidth,npheight,corner)
{
	var v=makeqrval(seed,npwidth,npheight,corner);
	var qr = new QRious({value:v.toString(),level:'H',size: qrheight});
	return qr.toDataURL();
}
function add_image_pattern(qrbd,dataurl)
{
	var dataURI=dataurl;
	var data = new Image();
	data.src = dataURI;
	//game.cache.removeImage(nam);
	//game.cache.addImage(nam, dataURI, data);
	data.onload=function () { qrbd.copy(data); };
}

var bgdata;
var qrbdata=[];

function update_bgdata_texture(img)
{
	for(var x=0;x<img.length;x++)
	{
		for(var y=0;y<img[x].length;y++)
		{
			var p=img[x][y];
			for(var c=0;c<3;c++)
			{
				bgdata.setPixel32(x,y,p[0],p[1],p[2],255.0,false);
			}
		}
	}
	var p=img[0][0];
	bgdata.setPixel32(x,y,p[0],p[1],p[2],255.0,true);
}

function update_new(seed)
{
	var delaytime=500;

	for(var i=0;i<4;i++)
	{
		add_image_pattern(qrbdata[i],qrpattern(seed,qrsize,npwidth,npheight,i));
	}

	var PIMG=prand_img(bgwidth,bgheight,8,seed);
	update_bgdata_texture(PIMG);
}

function nrandomimage()
{
	var seed=Math.floor(Math.random()*(1 << 25));
	update_new(seed);
	console.log(seed.toString());
}

function create() {

	var seed=3;
	var delaytime=500;

	bgdata=new Phaser.BitmapData(game,'bgdata',bgwidth,bgheight);
	bgdata.addToWorld(poffsetx,poffsety,0,0,pwidth,pwidth);
	console.log([bgwidth,bgheight]);
	
	for(var i=0;i<4;i++)
	{
		qrbdata.push(new Phaser.BitmapData(game,'qrbdata'+i.toString(),qrsize,qrsize));
	}
	qrbdata[0].addToWorld(poffsetx,poffsety);
	qrbdata[1].addToWorld(width-poffsetx-qrsize,poffsety);
	qrbdata[2].addToWorld(width-poffsetx-qrsize,height-poffsety-qrsize);
	qrbdata[3].addToWorld(poffsetx,height-poffsety-qrsize);
	
	update_new(3);

	game.stage.backgroundColor = '#4d4d4d';
	game.time.events.loop(delaytime, nrandomimage ,this);

	// Stretch to fill
	//game.scale.fullScreenScaleMode = Phaser.ScaleManager.EXACT_FIT;

	// Keep original size
	// game.scale.fullScreenScaleMode = Phaser.ScaleManager.NO_SCALE;

	// Maintain aspect ratio
	game.scale.fullScreenScaleMode = Phaser.ScaleManager.SHOW_ALL;
	game.input.onDown.add(gofull, this);
}

function gofull() {

	if (game.scale.isFullScreen)
	{
		game.scale.stopFullScreen();
	}
	else
	{
		game.scale.startFullScreen(false);
	}

}

function update() {
	
}

function render () {

	bgdata.render();
	// game.debug.text('Click / Tap to go fullscreen', 270, 16);
	// game.debug.text('Click / Tap to go fullscreen', 0, 16);

	//game.debug.inputInfo(32, 32);
	// game.debug.pointer(game.input.activePointer);

}
