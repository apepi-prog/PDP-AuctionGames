#!/bin/bash

echo "compilation du pdf en cours"
bibtex 0-memoire
bibtex 0-memoire
pdflatex -shell-escape 0-memoire
bibtex 0-memoire
# without this, we don't have links
pdflatex -shell-escape 0-memoire 
# delete all compiled files
rm 0-memoire.{aux,bbl,blg,lof,log,out,toc}
echo "0-memoire.pdf généré"