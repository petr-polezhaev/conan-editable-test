#!/bin/bash

source `dirname $0`/conan_init.sh

test $# -lt 1 && exit 1

path=$1
temp_dir=$rootdir/.temp/$path

mkdir -p $temp_dir

run_conan editable add --output-folder $temp_dir $rootdir/$path `basename $path`/1.0@temp/test

if ! test -e $temp_dir/.source; then
    run_conan source $rootdir/$path
    touch $temp_dir/.source
fi

if ! test -e $temp_dir/.build; then
    run_conan build --output-folder $temp_dir $rootdir/$path
    touch $temp_dir/.build
fi

rm -f $temp_dir/.build $temp_dir/.source
