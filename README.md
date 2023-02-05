# PDFcomposer

A script that allows you to freely interleave and concatenate the pages (single pages or page ranges) 
of many PDFs into a new single PDF file. It can also be used to extract a subset of pages from a single 
PDF file.

## how to run
```
python path/to/PDFcomposer.py
--fin <name1@path/to/file1.pdf> [<name2@path/to/file2.pdf> ... <nameN@path/to/fileN.pdf>] 
--fout path/to/output_file.pdf
--struct [name1,(pageA,pageB)]-[name2,pageC]-[name3,(pageD,pageE)]-[name2,(pageF,pageG)]
[--overwrite False]
```

## Arguments
<code>fin</code>: 
List of input file paths with their corresponding names. 
The names are used to easily identify the files from which you want to extract the pages that will make up the new PDF.

<code>fout</code>: 
Path where the produced PDF file is saved.

<code>struct</code>: 
The desired structure of the new PDF file.
Pages are extracted from the input files in the order in which the blocks are specified.

<code>overwrite</code>: 
Specify this argument and set it to True if you want to allow the generated output file to overwrite an existing file 
found in the same output path.

## Example
```
python PDFcomposer.py \
--fin \
red@C:.examples/red.pdf 
blue@C:./examples/blue.pdf \
green@C:./examples/green.pdf \
--fout ./examples/mix_test.pdf \
--struct [red,1]-[green,(5,6)]-[blue,9]-[red,(1,2,3)]-[blue,(6,7)] \
--overwrite True
```

![example](example.png)
