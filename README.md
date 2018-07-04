![kaser_logo](https://i.imgur.com/Yqw7hNM.png)
## The Ultimate Kindle Note & Highlight Parser 🚀

### What is it?
When you take notes or higlight things on kindle, all those actions get stored in a file called clippings.txt that you have access to. Getting that file is a great way of going through the most important parts of the books you've read (this is only necesary if you didn't purchase the books on amazon itself, if you did, you can handle everything through their app). 

The problem is that clippings.txt is a massive disgusting file that you don't wanna go through. What can you do then?

Karser is a simple python script that lets you turn your clippings.txt file from your kindle into beautiful organised PDFs for each book you've read and highlited! 🤖

### Usage

Karser is really easy to use! Since it's just a small python script, you just have to run it passing it the necessary arguments as flags, so let's go through that!

1. Clone this repo 
2. Get inside the folder
3. Move your file into the folder
4. Run the script! 💖

```sh
git clone git@github.com:P3rzival/Karser.git
cd Karser
mv ~/my_files/clippings.txt ~/Downloads/Karser
python karser.py -f clippings.txt 
```
As simple as that! You just gotta call karser script and pass it the .txt file you want to parse after the -f flag. 

If you want to get a extended verbose version to see if there were any errors in the process and if so, get a log of them, you can add the flag -e at the end to do so.
```sh
python karser.py -f filename.txt -e
```
As promised, Karser is really easy to use! 💡

### Why did you do this?
I've always been an eager reader that devours novels and lately I've started reading non fiction where I've wanted to highligth and take notes of interesting things. When I realised that I had no way of nicely exporting those highlights or notes I figured I had to create something myself.

I've also always been atracted to python's simplicity and potential but I never actually dived into it so I thought that since I had to write a simple script, this would probably be a good moment to try! So now, my first ever python script is released!

Because of my novelty and the fact that I wrote everything in one day, the quality of the code is probably not the best so if you see anything that can be improved or fixed (there are some small issues atm, you can see them in the issues of the repo and try to work on them!) please do so and make a PR! 🙀

I hope this helps people organising their notes and highlights in a better way so that from now on, that clippings file is actually useful! It has definitely helped me learning python and I've already passed all my notes to nice PDFs that I can through to get the best points of read books! 💖

PS: I hope people also like the pun with amazon's and karser's logo 🤣

### It wasn't all me
Even though I fully wrote the script, part of the functionality of it has to do with converting .txt files into .pdf and in order to do that I used a script created by [@baruchel](https://github.com/baruchel) called [txt2pdf](https://github.com/baruchel/txt2pdf). Really simple and nice script that just does the job, so shotout to him and if you need to turn txt into pdf, deffinitely give it a go! 🏗️
