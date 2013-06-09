# $FreeBSD: src/share/skel/dot.profile,v 1.21 2002/07/07 00:00:54 mp Exp $
#
# .profile - Bourne Shell startup script for login shells
#
# see also sh(1), environ(7).
#

# remove /usr/games and /usr/X11R6/bin if you want
PATH=$HOME/.bin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/usr/games:/usr/local/sbin:/usr/X11R6/bin; export PATH

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

alias fs='~/.bin/fs'
alias rp='~/.bin/rp'
alias cword='~/.bin/change_word_in_file.sh'
alias help='~/.bin/help'
alias ctags='~/.bin/ctags'
alias l='ls -alh'
alias ll="ls -alh"
alias te="tail log/sys/error.dat"
alias tl="tail log/debug.log"
alias ecw="vim /home1/ourhome/richard/.bin/cw.sh"
PS1="\[\e]0;\w\a\]\n\[\e[33m\]\w\[\e[0m\]"
#PS1="\w\$ "
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
alias vim="vim -p"
alias lchg="svn di -rPREV:HEAD"
alias conv_achieve="svn up achievement/ && python achieve.py achievement/achievement.xls ../../../wanfa/achievement/main.c"
alias conv_achieve_var="svn up achievement/ && python conv_var.py achievement/成就统计数据表.xls ../../../wanfa/event/utils.c"
alias post-review="post-review --target-groups=server"
export LANG=zh_CN.GBK

#export HOME=/home1/ourhome/richard
export PATH=$HOME/bin:$PATH:/usr/local/bin:/usr/local/sbin

export GIT_EDITOR=vim
export LOGNAME="richardcao"
PYTHONDONTWRITEBYTECODE=x; export PYTHONDONTWRITEBYTECODE;
export SVN_EDITOR=vim
export EDITOR=vim
