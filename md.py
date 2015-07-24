#!/c/dev/tools/Python27/python

import os
import sys
import html2text
import argparse

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('input')
    return p.parse_args()


def fixPointyBrackets(html):
  html = html.replace("&gt;",">")
  html = html.replace("&lt;","<")
  return html

def fenceCode(html):

  codes = {'java':'java','coldfusion':'cfm','cfml':'cfm','vb':'vb','javascript':'js','jscript':'js','css':'css','csharp':'cs','cs':'cs','html':'html','sql':'sql','php':'php'}

  for o, n in codes.iteritems():
    html = html.replace("<pre class=\"" + o + "\" name=\"code\">", "\n```" + n + "\n")
    html = html.replace("<pre name=\"code\" class=\"" + o + "\">", "\n```\n" + n)
  html = html.replace("</pre>","\n```" + "\n")
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
    parser.USE_AUTOMATIC_LINKS = True
    parser.RE_UNESCAPE = True

    text = fm + "\n" + parser.handle(html)

    text = fixPointyBrackets(text)

  with open(infile,"w") as fd:
    fd.write(text)

  os.rename(infile,outfile)



def main():
  for i in os.listdir(os.getcwd()):
    if(i.endswith(".html")):
      convertFile(i)
      continue
    else:
      continue


if __name__ == '__main__':
  main()