#!/bin/bash
# author: @whattheslime
if [ "$#" != 2 ]; then
	echo "Usage: $0 <plugin-slug> <version-number>"
	exit
fi

slug=$1
version=$2

wget https://downloads.wordpress.org/plugin/$slug.$version.zip -O $slug.$version.zip
