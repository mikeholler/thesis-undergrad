#!/bin/bash

articles=$(ls -1 $1)

for article in $articles
do
	path=$1$article
	less $path
	read -p "Delete '$article'? [Y/N]" yn
	if [ "$yn" == "y" ]
	then
		rm -f $path && echo '> Deleted.'
	fi
done



