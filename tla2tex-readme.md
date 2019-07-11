# tla2tex 解决方案

## 简要说明
编写 tex 文件 test.tex, 该文件使用 `\usepackage{tlatex}`, 并使用环境变量 `tla`, `pcal` 如 `\begin{tla} \end{tla}` 代码块.
直接在块中写 tla 代码. 然后运行命令:
```bash
java -cp tla2tools.jar tla2tex.TeX test.tex
```
生成的 test.tex 文件中对 `\begin{tla} \end{tla}` 进行了处理, 可生成具有 tla 格式的 paper.

## 详细说明
在 [tlaplus - Google Groups](https://groups.google.com/forum/#!forum/tlaplus) 检索了 tex 相关问题, 发现相关问题有但并不多.
在一个关于 [TLATeX](https://groups.google.com/forum/#!searchin/tlaplus/tex%7Csort:date/tlaplus/MsWuYgY1E0c/HFY5DrrzCQAJ)
问题中发现之前的想法, 即将 tla 生成 latex 代码并插入到 paper 中的方式并不正确. 开发者也不会搞这么麻烦的东西让大家用.

首先, 下载 [tla2tools.jar](https://tla.msr-inria.inria.fr/tlatoolbox/dist/tla2tools.jar) 工具. 之前使用的该工具的 `TLA` 类,
这个类接受参数是一个 tla 文件, 要求 tla 文件是完整的模块. 应该使用 `TeX` 类. 这个类接受的参数是一个 tex 文件, 并对输入文件使用了 tla
的部分进行解析, 生成对应的 tex 代码. 下面的是一个完整的 latex 输入文件:
```latex
\documentclass{article}
\usepackage{graphicx}
\usepackage{tlatex}
\usepackage{color}
\definecolor{boxshade}{gray}{.85}
\setboolean{shading}{true}

\begin{document}
	
	\title{Introduction to \LaTeX{}}
	\author{Author's Name}
	
	\maketitle
	
	\begin{abstract}
		The abstract text goes here.
	\end{abstract}
	
	\section{Introduction}
	Here is the text of your introduction.
	
	\begin{equation}
	\label{simple_equation}
	\alpha = \sqrt{ \beta }
	\end{equation}
	
	\subsection{Subsection Heading Here}
	Write your subsection text here.
	\begin{tla}
(***************************************************************************)
(* Greatest common divisor of m and n                                      *)
(***************************************************************************)
GCD(m, n) == SetMax(DivisorsOf(m) \cap DivisorsOf(n))
	\end{tla}
	
	\section{Conclusion}
	Write your conclusion here.
	
\end{document}

```

这个文件几个值得注意的地方是:
1. `\usepackage{tlatex}` 使用了 tlatex 包, 它要求 tlatex.sty 文件在包含目录内. (tla2tools.jar 压缩包的 tla2tex/tlatex.sty)
2. `\usepackage{color} \definecolor{boxshade}{gray}{.85} \setboolean{shading}{true}` 这三行设置注释有阴影效果, 是可选的. 
Mr. Lamport 认为第二行设置阴影值为 .85 效果最好.
3. `\begin{tla} \end{tla}`这个代码块中直接写了 tla 代码, 如果直接编译的话发现这些代码不会被显示在 pdf 中. 这是一种 `TeX` 类
需要处理的环境变量. 除此之外环境变量还有 `pcal`, 里面写 pluscal 代码.

下面调用 tla2tools.jar 工具对输入文件进行处理:
```bash
java -cp tla2tools.jar tla2tex.TeX test.tex
```

此时, test.tex 文件内容在 `\end{tla}` 后面增加了一部分内容 `\begin{tlatex} \end{tlatex}`:
```
\documentclass{article}
\usepackage{graphicx}
\usepackage{tlatex}
\usepackage{color}
\definecolor{boxshade}{gray}{.85}
\setboolean{shading}{true}

\begin{document}
	
	\title{Introduction to \LaTeX{}} \author{Author's Name}
	
	\maketitle
	
	\begin{abstract}
		The abstract text goes here.
	\end{abstract}
	
	\section{Introduction}
	Here is the text of your introduction.
	
	\begin{equation}
	\label{simple_equation}
	\alpha = \sqrt{ \beta }
	\end{equation}
	
	\subsection{Subsection Heading Here}
	Write your subsection text here.
	\begin{tla}
(***************************************************************************)
(* Greatest common divisor of m and n                                      *)
(***************************************************************************)
GCD(m, n) == SetMax(DivisorsOf(m) \cap DivisorsOf(n))
	\end{tla}
\begin{tlatex}
\begin{lcom}{0}%
\begin{cpar}{0}{F}{F}{0}{0}{}%
 Greatest common divisor of m and n                                      
\end{cpar}%
\end{lcom}%
 \@x{ GCD ( m ,\, n ) \.{\defeq} SetMax ( DivisorsOf ( m ) \.{\cap} DivisorsOf
 ( n ) )}%
\end{tlatex}
	
	\section{Conclusion}
	Write your conclusion here.
	
\end{document}
```
用这个生成的tex文件生成pdf就可以变成想要的样子了. 没有其他需要处理的细节.

帮助说可以指定 `-out` 参数让它产生一个新的名字而不是覆盖原来的. 我发现程序会报错, 在最后的重命名阶段报错. 但实际上已经执行成功了. 如:
```bash
java -cp tla2tools.jar tla2tex.TeX -out out test.tex
```
会生成一个叫 out.new 的文件, 需要手动改为 out.tex

可以考虑把 tla2tools.jar 文件放在 java 的 classpath 中, 这样就不用在命令行中写 `-cp tla2tools.jar` 了.

关于详细的生成说明和步骤见:
```bash
java -cp tla2tools.jar tla2tex.TeX -info
```
这个命令其实打印了 tla2tools.jar 压缩包内的 tla2tex/texinfo.txt 文件.


---
Ruize Tang

2018-12-27 21:08:22
