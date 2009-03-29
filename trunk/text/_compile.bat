cslatex diplomka.tex > log.txt
cslatex diplomka.tex > log2.txt
dvips diplomka.dvi
"C:\Program Files (x86)\Adobe\Acrobat 8.0\Acrobat\Acrodist.exe" /N /Q /V C:\Users\root\data\prog\diplomka\svnko\text\diplomka.ps

del *.aux
del kapitoly\*.aux
del prilohy\*.aux
del diplomka.toc