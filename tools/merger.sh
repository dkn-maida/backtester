#! /bin/sh

sec=$(basename $1)
echo "security is $sec" 
cd $1
cat *csv | awk '!a[$0]++' > $sec.csv