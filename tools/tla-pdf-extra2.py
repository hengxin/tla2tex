#!/usr/bin/env python
import sys
import os
import tempfile
import re

def footnotify (line):
  # Make font size footnotesize
  line = line.replace('\\mbox{', '\\mbox{\\footnotesize')

  # Convert all horizontal spacing to footnotesize
  x = line
  z = ''
  while '@s{' in x:
    y = x.split('@s{', 1)
    z += y[0]
    z += '@s{'
    a = y[1].split('}', 1)
    try:
      z += str(round(float(a[0]) * 4.0 / 5.0, 2)) # This is where the size is changed
      z += '}'
      x = a[1]
    except:
      z = ''
      break
  line = z + x

  return line

#TODO: add sys.argv
dirname = '/home/saksham/Desktop/journal/'
fname = 'MultiPaxosCha'
os.system('java tla2tex.TLA ' + dirname + fname + '.tla')
f = fname + '.tex'
tmp=tempfile.mkstemp()
insert_amssymb_if_not_already_present = False
assume_in_line = False

with open(f) as fd1, open(tmp[1],'w') as fd2:
  for line in fd1:
    print(line)
    # Lines of original Latex to skip
    if 'setlength{\\textwidth}' in line or 'setlength{\\textheight}' in line:
      continue

    # Add sty files needed for our Latex additions
    if insert_amssymb_if_not_already_present:
      if 'amssymb' not in line:
        # Add any sty file your latex needs here but the first has to be amssymb
        # because that is what the if-condition is checking
        fd2.write("\\usepackage{amssymb}\n")
        fd2.write("\\usepackage{dsfont}\n\\usepackage{fullpage}\n\\usepackage{xcolor}\n\\usepackage[T1]{fontenc}\n")
        fd2.write("\\usepackage{letltxmacro}\n\\usepackage{scalefnt}\n\\LetLtxMacro{\\oldtextsc}{\\textsc}\n\\renewcommand{\\textsc}[1]{\\oldtextsc{\\scalefont{1.15}#1}}\n")
        fd2.write("\\definecolor{boxshade}{gray}{0.85}\n")
      insert_amssymb_if_not_already_present = False

    if 'documentclass' in line:
      insert_amssymb_if_not_already_present = True

    # Replace \not \exists with \nexists
    # TODO: This wouldn't work if the \not and \exists are in separate lines :(
    line = line.replace('{\\lnot} \E', '{\\nexists}')

    # Replace {} with \emptyset
    line = line.replace('\\{ \\}', '{\\emptyset}')

    # All TLA+ keywords to be colored Purple in Latex
    if 'textsc' in line and 'purple' not in line:
      line = line.replace('textsc','textcolor{purple}{{\\textsc')
      if '%' in line:
        line = line.split('%', 1)[0]
        line += '}}\n'
      else:
        line = line.replace('\n','}}\n')

      if 'case' in line:
        line = line.replace('case ', ' case ')

    # All string constants to be colored blue in Latex
    if 'textsf' in line and 'blue' not in line:
      line = line.replace('textsf','textcolor{blue}{{\\textsf')
      line = line.replace('\n','}}\n')

    # Enable shading in comments by default
    if "setboolean" in line and "shading" in line and "false" in line:
      line = line.replace('false', 'true')

    # Change font size
    line = footnotify(line)

    # Remove extra space in front of `PROVE' keyword
    line = line.replace('{\\PROVE}\\@s{2.0}', '{\\PROVE}')
    if assume_in_line:  # ASSUME in previous line
      if 'PROVE' in line and '\\@x{' not in line:
        line = line.replace('{\\PROVE}', '{\\PROVE}\\@s{-4.1}')
    if 'ASSUME' in line: assume_in_line = True
    else: assume_in_line = False

    fd2.write(line)

os.rename(tmp[1], f)
os.system('pdflatex ' + fname + '.tex')
