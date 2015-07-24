#!/c/dev/tools/Python27/python

import os
import sys
import html2text
import argparse

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('input')
    return p.parse_args()


def fenceCode(html):

  codes = {'java':'java','coldfusion':'cfm','cfml':'cfm','vb':'vb','javascript':'js','jscript':'js','css':'css','csharp':'cs','cs':'cs','html':'html'}

  for o, n in codes.iteritems():
    html = html.replace("<pre class=\"" + o + "\" name=\"code\">", "```" + n + "\n")
    html = html.replace("<pre name=\"code\" class=\"" + o + "\">", "```" + n)
    html = html.replace("</pre>","```" + "\n")
  return html


def convertFile(infile):
  print "processing file: " + infile
  outfile = infile.replace(".html",".markdown")

  with open(infile) as fd:
    html = fd.read()
    # grap front matter
    start = html.find('---')
    end = html.find('---', start+3)
    fm = html[start:end+3]


    html = html[end+3:]

    html = fenceCode(html)



    parser = html2text.HTML2Text()
    parser.MARK_CODE = True
    parser.USE_AUTOMATIC_LINKS = True

    text = fm + "\n" + parser.handle(html)


  with open(outfile,"w") as fd:
    fd.write(text)


def main():
  for i in os.listdir(os.getcwd()):
    if(i.endswith(".html")):
      convertFile(i)
      continue
    else:
      continue


if __name__ == '__main__':
  main()