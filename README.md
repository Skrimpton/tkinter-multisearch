# tkinter-multisearch
Very simple tool to create search-urls for bookmarked goups of websites, and open them in new tabs.

## NB - edit lines 24/25
On windohs you probably have to manually edit the .pyw-file and input the full path to your webbrowser executable.

Name of the executable was enough on linux, probably cause they usually get auto-added to path on install.

Current value is for linux, and included windows-path is the standard path of install for firefox  


### Tested on: 
* windows 10
* linux: Manjaro - KDE plasma 5.27


### Dependencies
* python 3
* tkinter
* webbrowser module
* a json file
* an icon file, i'm just realizing. Any .png or .ico will do. <br>But the filename has to be: ```icon```

Replace included icon.ico ( windows ) or icon.png ( linux ) with your own, if you're paranoid.
