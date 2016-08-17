
OUT=paulisboots_main.js
SRC=paulisboots_main.pyj paulisboots_render.pyj paulisboots_game.pyj qusimple.pyj

all: ${OUT}

#%.js: %.pyj
#	rapydscript $< -o $@ -p 

#qu.js: qu.jso ${LINK}
##	cat ${LINK} qu.jso > qu.js


paulisboots_main.js: ${SRC}
	rapydscript paulisboots_main.pyj -o paulisboots_main.js -p

%.run: %.js
	node $<

clean:
	rm -rf ${OUT}
	rm -rf qu.jso
	
