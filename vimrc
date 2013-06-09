" An example for a vimrc file.
"
" Maintainer:	Bram Moolenaar <Bram@vim.org>
" Last change:	2002 Sep 19
"
" To use it, copy it to
"     for Unix and OS/2:  ~/.vimrc
"	      for Amiga:  s:.vimrc
"  for MS-DOS and Win32:  $VIM\_vimrc
"	    for OpenVMS:  sys$login:.vimrc

" When started as "evim", evim.vim will already have done these settings.
if v:progname =~? "evim"
  finish
endif

" Use Vim settings, rather then Vi settings (much better!).
" This must be first, because it changes other options as a side effect.
set nocompatible
" set nu

" allow backspacing over everything in insert mode
set backspace=indent,eol,start

set nobackup
"if has("vms")
"  set nobackup		" do not keep a backup file, use versions instead
"else
"  set backup		" keep a backup file
"endif
set history=50		" keep 50 lines of command line history
set ruler		" show the cursor position all the time
"set showcmd		" display incomplete commands
set incsearch		" do incremental searching

" For Win32 GUI: remove 't' flag from 'guioptions': no tearoff menu entries
" let &guioptions = substitute(&guioptions, "t", "", "g")

" Don't use Ex mode, use Q for formatting
map Q gq

" This is an alternative that also works in block mode, but the deleted
" text is lost and it only works for putting the current register.
"vnoremap p "_dp

" Switch syntax highlighting on, when the terminal has colors
" Also switch on highlighting the last used search pattern.
if &t_Co > 2 || has("gui_running")
  syntax on
  set hlsearch
endif

" Only do this part when compiled with support for autocommands.
if has("autocmd")

  " Enable file type detection.
  " Use the default filetype settings, so that mail gets 'tw' set to 72,
  " 'cindent' is on in C files, etc.
  " Also load indent files, to automatically do language-dependent indenting.
  filetype plugin indent on

  " Put these in an autocmd group, so that we can delete them easily.
  augroup vimrcEx
  au!

  " For all text files set 'textwidth' to 78 characters.
  autocmd FileType text setlocal textwidth=78

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

"set statusline=%F%m%r%h%w\ [FORMAT=%{&ff}]\ [TYPE=%Y]\ [ASCII=\%03.3b]\ [HEX=\%02.2B]\ [POS=%04l,%04v][%p%%]\ [LEN=%L]
 
"set laststatus=2

let Tlist_Show_One_File = 1
let Tlist_Exit_OnlyWindow = 1
"let Tlist_Use_Right_Window = 1

" set mouse=a

"set foldmethod=syntax
"set foldcolumn=3
"set foldlevelstart=3

cnoremap <C-A> <Home>
cnoremap <C-E> <End>
cnoremap <C-K> <C-U>

let &termencoding=&encoding
"set fileencodings=cp936,gbk,utf-8,ucs-bom
map <F4> <Esc>:!"python" %<CR>
map <F5> <Esc>:tabprevious<CR>
map <F6> <Esc>:tabnext<CR>
map <C-J> <Esc>:tabnew .<CR>

" easytodo
au BufNewFile,BufRead *.etd                     setf easytodo

"autocmd FileType python setlocal et sta sw=4 sts=4

hi Underlined guibg=grey22 guifg=#ffa500 gui=underline
"hi Normal guibg=grey90
"hi Cursor guibg=Green guifg=NONE
"hi lCursor guibg=Cyan guifg=NONE
"hi NonText guibg=grey80
"hi Constant gui=NONE guibg=grey95
"hi Special gui=NONE guibg=grey95
hi OrangeColor gui=NONE guibg=#ffa500
"set statusline=%F\ %l\|%L\ %c\ %M
"set statusline=%F%m%r%h/ %r%{CurDir()}%h/ / / Line:/ %l/%L:%c
"let &statusline=%<%f %(%h%m%r %) %-15.15(%l,%c%V%)%P {expand('%:p:h')}
set laststatus=2
set statusline=\ %{HasPaste()}%F%m%r%h\ %w\ \ CWD:\ %r%{CurDir()}%h\ \ \ Line:\ %l/%L:%c

function! CurDir()
	let curdir = substitute(getcwd(), '/Users/amir/', "~/", "g")
	return curdir
endfunction

function! HasPaste()
	if &paste
		return 'PASTE MODE  '
	else
		return ''
	endif
endfunction

set numberwidth=4
set noswapfile
set nu
imap jj <Esc>
"set mouse=a

"map <F2> <Esc>:vimshell bash<CR>

"au BufRead,BufNewFile *.h     setl filetype=lpc
"au BufRead,BufNewFile *.c     setl filetype=lpc

"set tabstop=4
"set shiftwidth=2
"set expandtab
"set noexpandtab

map <C-j> <C-W>j
map <C-k> <C-W>k
map <C-h> <C-W>h
map <C-l> <C-W>l


map <leader>f :FirstExplorerWindow<cr>
map <leader>b :BottomExplorerWindow<cr>
map <F4> :WMToggle<cr>
map <F7> :tp<cr>
map <F8> :tn<cr>
map <F9> :b#<cr> 
map <F10> :nohl<cr> 

au FileType h setl syntax=lpc
au FileType c setl syntax=lpc

set pastetoggle=<F11>
:inoremap { <CR>{<CR>}<ESC>O
