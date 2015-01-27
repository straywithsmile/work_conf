syn on
set ruler
set showcmd
set smartindent
set nocp
set helplang=cn
set mouse=a
set scrolloff=3
set background=dark
set incsearch
set ambiwidth=double
set hlsearch
"set foldmethod=syntax
"set foldcolumn=4
"set foldlevelstart=3
set termencoding=cp936
set enc=cp936
"set magic
filetype indent plugin on
"runtime ftplugin/man.vim
map <C-X><C-X> :!ctags -R --C++-kinds=+p --fields=+iaS --extra=+q .<CR>

set pastetoggle=<F11>
set nu

au BufRead,BufNewFile *.c       if (getcwd() =~ 'logic' && &ft == 'c') | set ft=lpc | let lpc_pre_v22=1 | endif
au BufRead,BufNewFile *.h       if (getcwd() =~ 'logic' && &ft == 'h') | set ft=lpc | let lpc_pre_v22=1 | endif
au BufRead,BufNewFile *.go      set ft=go
set backspace=indent,eol,start

""&lt;ESC&gt;i:inoremap ( ()&lt;ESC&gt;i
""&lt;ESC&gt;i:inoremap ) &lt;c-r&gt;=ClosePair(')')&lt;CR&gt;
""&lt;ESC&gt;i:inoremap { {&lt;CR&gt;}&lt;ESC&gt;O
""&lt;ESC&gt;i:inoremap } &lt;c-r&gt;=ClosePair('}')&lt;CR&gt;
""&lt;ESC&gt;i:inoremap [ []&lt;ESC&gt;i
""&lt;ESC&gt;i:inoremap ] &lt;c-r&gt;=ClosePair(']')&lt;CR&gt;
""&lt;ESC&gt;i:inoremap " ""&lt;ESC&gt;i
""&lt;ESC&gt;i:inoremap ' ''&lt;ESC&gt;i
""&lt;ESC&gt;ifunction! ClosePair(char)
""&lt;ESC&gt;i	if getline('.')[col('.') - 1] == a:char
""&lt;ESC&gt;i		return "\<Right>"
""&lt;ESC&gt;i	else
""&lt;ESC&gt;i		return a:char
""&lt;ESC&gt;i	endif
""&lt;ESC&gt;iendfunction

":inoremap ( ()<ESC>i
":inoremap ) <c-r>=ClosePair(')')<CR>
":inoremap { {<CR><Left>}<ESC>O
":inoremap } <c-r>=ClosePair('}')<CR>
":inoremap [ []<ESC>i
":inoremap ] <c-r>=ClosePair(']')<CR>
":inoremap < <><ESC>i
":inoremap > <c-r>=ClosePair('>')<CR>
":inoremap " ""<ESC>i
":inoremap ' ''<ESC>i
"key :inoremap { <CR>{<CR>}<ESC>O

function! FillRound()
	let line = getline(".")
	let previous_char = l:line[col(".")-1]

	"if index(["("], l:previous_char) != -1
	if previous_char == '('
		execute "normal! a\{});\<Esc>\<Left>\<Left>i"
	else
		execute "normal! a\<CR>{\<CR>}\<Esc>O"
	end
endfunction 

inoremap { <ESC>:call FillRound()<CR>a

"function ClosePair(char)
"	if getline('.')[col('.') - 1] == a:char
"		return "\<Right>"
"	else
"		return a:char
"	endif
"endfunction
"au BufReadPost * if line("'\"") > 0|if line("'\"") <= line("$")|exe("norm '\"")|else|exe "norm $"|endif|endif

"inoremap <C-h> <Left>
inoremap <C-l> <Right>
:imap jj <Esc>

" 状态栏
set laststatus=2      " 总是显示状态栏
highlight StatusLine cterm=bold ctermfg=yellow ctermbg=blue
" 获取当前路径，将$HOME转化为~
function! CurDir()
    let curdir = substitute(getcwd(), $HOME, "~", "g")
    return curdir
endfunction
set statusline=[%n]\ %f%m%r%h\ \|\ \ pwd:\ %{CurDir()}\ \ \|%=\|\ %l,%c\ %p%%\ \|\ ascii=%b,hex=%b%{((&fenc==\"\")?\"\":\"\ \|\ \".&fenc)}\ \|\ %{$USER}\ @\ %{hostname()}\

" Only do this part when compiled with support for autocommands.
if has("autocmd")

  " Enable file type detection.
  " Use the default filetype settings, so that mail gets 'tw' set to 72,
  " 'cindent' is on in C files, etc.
  " Also load indent files, to automatically do language-dependent indenting.
  "filetype plugin indent on

  " Put these in an autocmd group, so that we can delete them easily.
  augroup vimrcEx
  au!

  " For all text files set 'textwidth' to 78 characters.
  "autocmd FileType text setlocal textwidth=78

  " When editing a file, always jump to the last known cursor position.
  " Don't do it when the position is invalid or when inside an event handler
  " (happens when dropping a file on gvim).
  autocmd BufReadPost *
    \ if line("'\"") > 0 && line("'\"") <= line("$") |
    \   exe "normal g`\"" |
    \ endif

  augroup END

else

  set autoindent		" always set autoindenting on

endif " has("autocmd")
set autoindent		" always set autoindenting on
