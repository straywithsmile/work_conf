#/usr/bin/env sh

pwd=$PWD
home=$HOME

ln -sv ${pwd}/bin ${home}/bin
ln -sv ${pwd}/bash_profile ${home}/.bash_profile
ln -sv ${pwd}/start.sh ${home}/start.sh
ln -sv ${pwd}/stop.sh ${home}/stop.sh
ln -sv ${pwd}/vim ${home}/.vim
ln -sv ${pwd}/vimrc ${home}/.vimrc
ln -sv ${pwd}/zprezto ${home}/.zprezto
zsh ./stand_init.zsh

mkdir -p ${home}/tx2env
touch ${home}/tx2env/host.conf
echo "use=unknown" >> ${home}/tx2env/internal_server_info.txt
echo "desc=unknown" >> ${home}/tx2env/internal_server_info.txt
