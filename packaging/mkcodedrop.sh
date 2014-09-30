#!/bin/bash
#
#  Create the tar ball for a code drop 
# A code drop has everything to replicate the source code 
#
#

usage() {
   echo "mkcodedrop <version> <release>"
   exit 1;
}

#
#  helper to do the taring
#  tarit c|r tarname
#
tarit( ) {
opt=$1
tarname=$2
shift
shift

tar --exclude .git  --exclude "*.tar" --exclude "*~*" --exclude "_*" \
    --exclude .metadata --exclude Debug --exclude Release \
    -${opt} -vf ${tarname} $1
}

#
#  Make a directory without the contents
#
tarmkdir() {
tar --append --no-recursion -f $1 $2
}

VERSION=$1
RELEASE=$2
PACKAGE=masterserver

if [ x"$VERSION" == x ] ; then
  usage;
  exit 1 ;
fi

if [ x"$RELEASE" == x ] ; then
  usage;
  exit 1 ;
fi

RPMPATH=${PWD}/../_RPM

if [ ! -e $RPMPATH ] ; then
   echo "you must create $RPMPATH";
   exit 1;
fi

#
#  build file names from the parts
#
VERNAME=${PACKAGE}-${VERSION}-${RELEASE}
TARNAME=${RPMPATH}/${VERNAME}-codedrop.tar
SAVETARNAME=$TARNAME

rm -f $TARNAME.*

pushd ..
tarit c ${TARNAME} workspace
tarit r ${TARNAME} Doc
tarit r ${TARNAME} packaging
tarmkdir  ${TARNAME} _RPM
#tarmkdir  ${TARNAME} _doxygen

popd
gzip $TARNAME



