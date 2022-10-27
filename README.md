# tla2tex
TLA+ code to TeX code

## How to do that?

- Put your `tla` code in between `\begin{tla}` and `\end{tla}` in file 
like [`tla2tex-example-tla.tex`](https://github.com/hengxin/tla2tex/blob/master/tla2tex-example-tla.tex).
  - Ignore the code in between `\begin{\tlatex}` and `\end{\tlatex}` now.
- Run `java -cp tla2tools.jar tla2tex.TeX tla2tex-example-tla.tex`
  - This will automatically generate that code in between `\begin{\tlatex}` and `\end{\tlatex}`.
  - ***Important Note:*** 
  You'd better run `java -cp` under the directory of `tlatex-example-tla.tex`. 
  Otherwise, you may get a `renaming` error and information indicating that 
  some `.new` file was generated in a different directory.
  - `-cp tla2tools.jar`: 
  make sure that `tla2tools.jar` is in your path; 
  use `your-path-to-tla2tools.jar` when necessary.
- Compile [`tlatex-example-tla.tex`](https://github.com/hengxin/tla2tex/blob/master/tla2tex-example-tla.tex) 
to produce the [pdf version](https://github.com/hengxin/tla2tex/blob/master/tla2tex-example-tla.pdf) 
which can be inserted into your LaTeX document as usual.
  - Make sure that [`tlatex.sty`](https://github.com/hengxin/tla2tex/blob/master/tlatex.sty) is in your path.

For detailed info, see [tla2tex-readme.md](https://github.com/hengxin/tla2tex/blob/master/tla2tex-readme.md).
