#!/bin/sh

MUV=pymuv


runtest() {
    infile="test_$1_in.muv"
    outfile="test_$1_out.muf"
    cmpfile="test_$1_cmp.muf"

    incldir=$(dirname $(pwd))/incls
    $MUV -I $incldir -o $outfile $infile
    if [[ -e $cmpfile ]] ; then
        echo "Checking test $1"
        diff -c -b -B -w $cmpfile $outfile
    else
        echo "Installing first run results for test $1"
        mv $outfile $cmpfile
    fi
}

if [[ $# > 0 ]] ; then
    for n in $@ ; do
        runtest $n
    done
    exit
fi

for f in test_*_in.muv ; do
    n=$(basename $f _in.muv | sed 's/^test_//')
    runtest $n
done

