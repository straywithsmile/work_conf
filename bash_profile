# $FreeBSD: src/share/skel/dot.profile,v 1.21 2002/07/07 00:00:54 mp Exp $
#
# .profile - Bourne Shell startup script for login shells
#
# see also sh(1), environ(7).
#

# remove /usr/games and /usr/X11R6/bin if you want
PATH=/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/usr/games:/usr/local/sbin:/usr/X11R6/bin; export PATH

# Setting TERM is normally done through /etc/ttys.  Do only override
# if you're sure that you'll never log in via telnet or xterm or a
# serial line.
# Use cons25l1 for iso-* fonts
# TERM=cons25; 	export TERM

BLOCKSIZE=K;	export BLOCKSIZE
EDITOR=vim;   	export EDITOR
PAGER=less;  	export PAGER

# set ENV to a file invoked each time sh is started for interactive use.
ENV=$HOME/.shrc; export ENV

[ -x /usr/games/fortune ] && /usr/games/fortune freebsd-tips

alias l='ls'
alias ll="ls -alh"
alias te="tail log/sys/error.dat"
alias tl="tail log/debug.log"
alias t="tmux"
alias tt="tmux attach -t"
#PS1="\[\e]0;\w\a\]\n\[\e[33m\]\w\[\e[0m\]"
PS1="\w "
#PS1="`whoami`@`hostname | sed 's/\..*//'`"
case `id -u` in
        0) PS1="${PS1}# ";;
        *) PS1="${PS1}$ ";;
esac
export PS1
#export PS1="\w\$ "
alias ls="ls -G"
alias vo="vim -R"
alias todo="vim /home/richard/.todo.etd"
alias vi="vim"
alias lchg="svn di -rPREV:HEAD"
alias mergelast="svn merge -rPREV:HEAD --ignore-ancestry"
alias post-review="post-review --target-groups=xy2_server"
export LANG=zh_CN.GBK

export GOROOT=$HOME/go
export PATH=$GOROOT/bin:$HOME/bin:$PATH

export GIT_EDITOR=vim
export PYTHONDONTWRITEBYTECODE=x
export SVN_EDITOR=vim
export EDITOR=vim

export GOROOT=$HOME/go
export GOBIN=$GOROOT/bin
export PATH=$PATH:$GOBIN
export GOPATH=$HOME/go_src

#gpg-agent --daemon --enable-ssh-support --write-env-file "${HOME}/.gpg-agent-info"

#if [ -f "${HOME}/.gpg-agent-info" ]; then
#	. "${HOME}/.gpg-agent-info"
#	export GPG_AGENT_INFO
#	export SSH_AUTH_SOCK
#	export SSH_AGENT_PID
#fi
#
#GPG_TTY=$(tty)
#export GPG_TTY
