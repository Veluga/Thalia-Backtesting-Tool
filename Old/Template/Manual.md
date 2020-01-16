# Using the Latex template

## Writing

* Different sections must be written in different .tex documents
* E.g. the vision should be contained within a vision.tex file
* Sections can then be imported using \include{sectioname} within main.tex
* Style must be defined globally and overwritten locally

## Citing

* Citations must be inline using \cite{citationname}
* Citations must be contained within a {section}.bib file (where section is the name of the section)
* If a url is used for the source, the bibtex entry must be of type misc (@misc) and contain a howpublished field

## Images

* Images must be placed in the images directory and contain unique names (i.e. the file extension must not serve as
  disambiguation)
