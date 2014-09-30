#!/bin/bash
#
#  unpack tar ball into target directory
#
#

usage() {
   echo "deploy tarfile targetDir workDir"
   exit 1;
}

tarFile=$1
targetDir=$2
workDir=$3

if [ "$tarFile" == "" -o "$targetDir" == "" -o "$workDir" == "" ] ; then
  usage;
fi

if [ ! -d $targetDir ] ; then
   mkdir $targetDir
fi

if [ ! -d $workDir ] ; then
   mkdir $workDir
   pushd $workDir
   tar -xf ../$tarFile
   popd
fi

mv ${workDir}/workspace/m/* $targetDir
cp ${workDir}/configFiles/$targetDir-.htaccess $targetDir/.htaccess
cp ${workDir}/configFiles/$targetDir-settings_data.php $targetDir/settings_data.php
cp ${workDir}/configFiles/$targetDir-sysconfig_data.php $targetDir/sysconfig_data.php

rm -rf $workDir
