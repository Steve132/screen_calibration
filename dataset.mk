img_luts := $(patsubst %.jpg,%.lutsparse,$(wildcard *.jpg))

all: all.lutsp

%.lutsparse: %.jpg
	../../readcalibrate.py $< > $@

all.lutsp: $(img_luts)
	cat $(img_luts) > all.lutsp
