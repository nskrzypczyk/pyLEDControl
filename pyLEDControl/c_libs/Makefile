CC = gcc
CFLAGS = -Wall -shared -fPIC
SRC_DIR = $(realpath $(dir $(lastword $(MAKEFILE_LIST))))
SRC_FILES = $(SRC_DIR)/$(wildcard *.c)
SO_FILES = $(patsubst %.c, %.so, $(SRC_FILES))

.PHONY: clean

all: $(SO_FILES)

%.so: %.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	echo $(SO_FILES)
	rm -f $(SO_FILES)