#/usr/bin/env sh

pwd=$PWD
home=$HOME

ln -sv ${pwd}/bin ${home}/bin
ln -sv ${pwd}/bash_profile ${home}/.bash_profile
ln -sv ${pwd}/start.sh ${home}/start.sh
ln -sv ${pwd}/stop.sh ${home}/stop.sh
ln -sv ${pwd}/vim ${home}/.vim
ln -sv ${pwd}/vimrc ${home}/.vimrc
