" Vim syntax file
" Language:        easy todo
" Maintainer:    xbeta (http://blog.sina.com.cn/m/xbeta)
" Changelog:    v1.0(061218)
" Install:
"    1) Copy this file into your $VIM/syntax directory.
"    2) Add this line to filetype.vim:
"       au BufNewFile,BufRead *.etd setf easytodo
" Usage:
"    1)
"	缩进决定折叠层级。建议：第几周顶格；日期缩进1个tab；todo项目缩进2个tab。
"    2)
"	todo项目前的数字表示状态，决定颜色。建议：0表示完成；1表示todo；2表示紧急todo。
"    3)
"	用Ctrl-A和Ctrl-X来对状态数字加减1。如按键无效，很可能是启用了mswin风格映射。

" For version 5.x: Clear all syntax items
" For version 6.x: Quit when a syntax file was already loaded

set fdc=4
set lsp=5
syn match zweek ".*week.*"
syn match ztd0 "^\t\t0 \S.*"
syn match ztd1 "^\t\t1 \S.*"
syn match ztd2 "^\t\t2 \S.*"
syn match done "OK"
syn keyword Comment	OK
syn keyword Repeat      OKing
syn keyword Float       Later
syn keyword Underlined  underline
syn keyword NonText	nontext
syn keyword Constant	constant NotOK

hi ztd0 guifg=darkgray
hi ztd1 guifg=yellow
hi ztd2 guifg=red gui=bold
hi zweek  guibg=darkgray

abb <buffer> week week______________________________________________________
"上一句为输入week后，自动在后面加上N个下划级，这样比较醒目
set fdm=expr
set foldexpr=Myindent(v:lnum)
func! Myindent(lnum)
  let s:a=strlen(matchstr(getline(v:lnum), '^\t\+'))
  if s:a == 0
    return '>1'
  elseif s:a == 1
    return '>2'
  else
    return '='
  endif
endf
