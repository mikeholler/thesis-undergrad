#!/bin/bash

articles=$(ls -1 $1)

for article in $articles
do
	path=$1$article
	egrep -v "^(Cite error:.*|..:.*)$" $path > "$path.tmp"
	mv "$path.tmp" $path
done



