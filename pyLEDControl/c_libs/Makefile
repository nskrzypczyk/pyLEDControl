CC = gcc
CFLAGS = -Wall -shared -fPIC
SRC_DIR = $(realpath $(dir $(lastword $(MAKEFILE_LIST))))
SRC_FILES = $(SRC_DIR)/$(wildcard *.c)
SO_FILES = $(patsubst %.c, %.so, $(SRC_FILES))

RGB_LIB_DISTRIBUTION=$(SRC_DIR)/../../rpi-rgb-led-matrix
RGB_INCDIR=$(RGB_LIB_DISTRIBUTION)/include
RGB_LIBDIR=$(RGB_LIB_DISTRIBUTION)/lib
RGB_LIBRARY_NAME=rgbmatrix
RGB_LIBRARY=$(RGB_LIBDIR)/lib$(RGB_LIBRARY_NAME).a
LDFLAGS+=-L$(RGB_LIBDIR) -l$(RGB_LIBRARY_NAME) -lrt -lm -lpthread

.PHONY: clean

all: $(SO_FILES)

$(RGB_LIBRARY):
	$(MAKE) -C $(RGB_LIBDIR)

%.so: %.c $(RGB_LIBRARY)
	$(CC) $(CFLAGS) $(LDFLAGS) -I$(RGB_INCDIR) -o $@ $<

clean:
	echo $(SO_FILES)
	rm -f $(SO_FILES)