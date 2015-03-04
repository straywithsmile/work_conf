#/usr/bin/env sh

pwd=$PWD
home=$HOME
env_dir=${home}/work_conf

ln -sv ${env_dir}/bin ${home}/bin
ln -sv ${env_dir}/bash_profile ${home}/.bash_profile
ln -sv ${env_dir}/start.sh ${home}/start.sh
ln -sv ${env_dir}/stop.sh ${home}/stop.sh
ln -sv ${env_dir}/vim ${home}/.vim
ln -sv ${env_dir}/vimrc ${home}/.vimrc
ln -sv ${env_dir}/zprezto ${home}/.zprezto
ln -sv ${env_dir}/autojump ${home}/.autojump 
ln -sv ${env_dir}/tmux.conf ${home}/.tmux.conf
ln -sv ${env_dir}/teamocil ${home}/.teamocil

zsh ./stand_init.zsh

mkdir -p ${home}/tx2env
touch ${home}/tx2env/host.conf
echo "use=unknown" >> ${home}/tx2env/internal_server_info.txt
echo "desc=unknown" >> ${home}/tx2env/internal_server_info.txt
