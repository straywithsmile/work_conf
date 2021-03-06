#/usr/bin/env sh

HERE=$PWD

ln -sv ${HERE}/bin ${HOME}/.bin
ln -sv ${HERE}/bash_profile ${HOME}/.bash_profile
ln -sv ${HERE}/vimrc ${HOME}/.vimrc
ln -sv ${HERE}/autojump ${HOME}/.autojump 
ln -sv ${HERE}/tmux.conf ${HOME}/.tmux.conf

curl -fLo ~/.vim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
