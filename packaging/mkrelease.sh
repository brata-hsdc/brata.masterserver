#!/bin/bash
#
#  Create the relese archive needed to deploy on a remote host 
#
#

usage() {
   echo "mkrelease"
   exit 1;
}



rm -f m.zip
pushd ../workspace/m
zip  -r ../../packaging/m.zip * .ht*
popd



