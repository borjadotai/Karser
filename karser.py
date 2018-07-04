import argparse
import os
import datetime
 
# Setting up parser option to control how we wanna run the script and se the file we want to use
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", dest="myFilenameVariable",
                    help="After writting -f, call the file that you want to format", metavar="FILE")
parser.add_argument("-e", "--extended",
                        action="store_true", dest="verbose",
                        default=False,
                        help="If you run -e at the end of your command you'll be able to see our logs and check if there was errors and were.")
args = parser.parse_args()

# Opening and reading file. Whole text stored as a string in content. Parsed after that by chunks (entries / notes) using '==========' in entries.
fullContent = open(args.myFilenameVariable, 'r').read()
content = fullContent.split('==========')

# Function that separates the full content into chunks per book. Returns an array of iteration numbers that defines the sections per books and a list of their titles.
def separator(entries):
  different = [] # It will have the structure [126, 256, 356, 460] where the numbers are iteration numbers for each book.
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
  return different, books

# Initialising succesful and errors arrays. They will contain all the final information as logs. Successful will have all the parsed information and errors will contain the ones that broke for future revision.
succesful = []
errors = []

# Create a Notes directory and put everything inside
if not os.path.exists('Notes'):
  os.makedirs('Notes')

# PARSING PROCESS
def printer(entries, name):
  txt = name.rstrip().lstrip() + '.txt'
  pdf = name.rstrip().lstrip() + '.pdf'
  f = open(txt, "w")
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
      f.write('Title: ' + title.lstrip() + '\n')
      iteration.append(title)
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

      f.write('Page: ' + page.lstrip() + '\n')
      f.write('Location: ' + location.lstrip() + '\n')
      f.write('Date: ' + date.lstrip() + '\n')
      f.write('Text: ' + text.lstrip() + '\n')
      f.write('\n')
      f.write('==========' + '\n')
      f.write('\n')

      iteration.append(location)
      iteration.append(date)
      iteration.append(text)
      succesful.append(iteration)
      
    except:
      content = entries[i]
      errors.append([i, content])
      pass

  # Closes the txt file, turns it into a pdf and then deletes de previously created txt
  f.close()
  os.system('python txt2pdf.py -o ' + pdf + ' ' + txt)
  os.system('rm ' + txt)
  new = ''.join('Notes/' + pdf)
  os.rename(pdf, new)
    
# RUNNER (WHERE THE MAGIC GETS CALLED). We call the function separator with our full content separated only by '========' and we get the list of iteration numbers and book titles.
diffs, books = separator(content)

# Then we parse and create pdfs for each book.
for i in range(0, len(diffs)):
  if i == 0:
    printer(content[0:diffs[0]], books[0])
  else:
    printer(content[diffs[i-1]+1:diffs[i]], books[i])

# If verbose was chosen, print out successful and if there were errors print them and create a log file
if (args.verbose):
  if not errors:
    print 'Succesfully added:', len(succesful)
    print 'No errors found.'
  else:
    now = datetime.datetime.now()
    log = "Notes/errors_{0}.txt".format(now.strftime("%Y-%m-%d"))
    f = open(log, "w")
    f.write(''.join(str(e) for e in errors))
    f.close()
    print 'Succesfully added:', len(succesful)
    print 'Woops, there were:', len(errors), 'errors. You can see the logfile', log