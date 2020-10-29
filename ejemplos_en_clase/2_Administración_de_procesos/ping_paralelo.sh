#!/bin/sh

# Redes en las cuales buscar direcciones vivas (separadas por espacio,
# dentro de una sola cadena
NETS='192.168.1. '


for NET in $NETS
do
    for HOST in $(seq 1 254)
    do
	if ping -c 1 ${NET}${HOST} >/dev/null 2>&1
	then
	    echo ${NET}${HOST} está vivo

	fi &
    done &
done | sort
