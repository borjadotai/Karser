import argparse
from reportlab.pdfgen import canvas
import os
import time
 
#
# Setting up parser option to control how we wanna run the script and se the file we want to use
#
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", dest="myFilenameVariable",
                    help="After writting -f, call the file that you want to format", metavar="FILE")
parser.add_argument("-q", "--quiet",
                        action="store_false", dest="verbose",
                        default=True,
                        help="By default we print out the entries on terminal, if you just want to see the succeses and erros, use -q")
args = parser.parse_args()

#
# Opening and reading file. Whole text stored as a string in content. Parsed after that by chunks (entries / notes) using '==========' in entries.
#
content2 = open(args.myFilenameVariable, 'r').read()
content = content2.split('==========')

def separator(entries):
  different = []
  books = []
  for i in range (0, len(entries)-1):
    try: 
      info = entries[i].splitlines()
      pos = entries[i+1].splitlines()
      sol = info[0] or info[1]
      sol2 = pos[0] or pos[1]
      tit = sol.strip(' ').strip('\xef').strip('\xbb').strip('\xbf')[0:10].replace(' ', '')
      tit2 = sol2.strip(' ').strip('\xef').strip('\xbb').strip('\xbf')[0:10].replace(' ', '')
      if tit != tit2:
        different.append(i)
        books.append(tit)
    except:
      different.append(i)
      books.append(tit)
  # print books
  return different, books

#
# Initialising succesful and errors arrays. They will contain all the final information. Successful will have all the parsed information and errors will contain the ones that broke for future revision.
#
succesful = []
errors = []

#
# PARSING PROCESS
#
def printer(entries, name):
  tit = name.rstrip().lstrip() + '.txt'
  print tit
  pdf = name.rstrip().lstrip() + '.pdf'
  print pdf
  f = open(tit, "w")
  for i in range (0, len(entries)-1):
    try: 
      iteration = []
      info = entries[i].splitlines()
      metadata = info[0:3]
      text = ''.join(info[3:])
      main = metadata[1]
      extra = metadata[2].split('|')
      # Here we deal with entries that don't contain any author
      if '(' in main:
        authorExtra = main.replace(')', '').rsplit('(')
        author = authorExtra[-1]
        title = ''.join(authorExtra[:len(authorExtra)-1])
      else:
        author = 'NOT FOUND'
        title = main
      # if (args.verbose):
      #   print 'Title: ' + title
      f.write('Title: ' + title.lstrip() + '\n')
      iteration.append(title)
      # if (args.verbose):
      #   print 'Author: ' + author
      f.write('Author: ' + author.lstrip() + '\n')
      iteration.append(author)
      # Here we deal with entries that don't contain any page
      if 'page' in extra[0]: 
        page = str(filter(str.isdigit, extra[0]))
        location = extra[1].split('location ')[1]
        date = extra[2].split(', ')[1]
        iteration.append(page)
      else:
        location = extra[0].split('location ')[1]
        date = extra[1].split(', ')[1] 
        page = 'NOT FOUND'
        iteration.append('NOT FOUND')

      # If verbose is on, we print out every parsed entry on terminal
      # if (args.verbose):
      #   print 'Page: ' + page
      #   print 'Location: ' + location
      #   print 'Date: ' + date
      #   print 'Text: ' + text
      #   print('')
      #   print('==========')
      #   print('')

      f.write('Page: ' + page.lstrip() + '\n')
      f.write('Location: ' + location.lstrip() + '\n')
      f.write('Date: ' + date.lstrip() + '\n')
      f.write('Text: ' + text.lstrip() + '\n')
      f.write('\n')
      f.write('==========' + '\n')
      f.write('\n')



      # 
      iteration.append(location)
      iteration.append(date)
      iteration.append(text)
      succesful.append(iteration)
      
    except:
      content = entries[i]
      errors.append([i, content])
      pass

  # print len(succesful)
  # print len(errors)
  f.close()
  os.system('python txt2pdf.py -o ' + pdf + ' ' + tit)

# for i in range (0, len(succesful)-1):
#   if succesful[i][0] == succesful[i+1][0]:
#     if i == 0:
#       name = ''.join(succesful[i][0].rstrip() + '.txt')
#       f = open(name, "w")
#       title = 'Title: ' + succesful[i][0]
#       author = 'Author: ' + succesful[i][1]
#       f.write(title)
#       f.write(author)
#     title = 'Title: ' + succesful[i][0]
#     author = 'Author: ' + succesful[i][1]
#     f.write(title)
#     f.write(author)
#   else:
#     f.close() 
#     name = ''.join(succesful[i+1][0].rstrip() + '.pdf')
#     f = open(name, "w")
#     title = 'Title: ' + succesful[i+1][0]
#     author = 'Author: ' + succesful[i+1][1]
#     f.write(title)
#     f.write(author)
    


diffs, books = separator(content)

for i in range(0, len(diffs)):
  if i == 0:
    printer(content[0:diffs[0]], books[0])
  else:
    printer(content[diffs[i-1]+1:diffs[i]], books[i])