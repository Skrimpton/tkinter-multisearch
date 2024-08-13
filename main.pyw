#!/bin/env python3
import webbrowser
import time
import platform

import os
import json

import tkinter as tk
from tkinter import (   font as tkf,
                        ttk
)



class MainWindow:

    def __init__(self):

        # -----------------------------------------------------------------------------------------
        # SET PRIVATE BROWSER  GOTTA INPUT MANUALLY FOR NOW:
        # https://github.com/python/cpython/issues/105983
        # -----------------------------------------------------------------------------------------
        self.PRIVATEBROWSER = "firefox -private-window %s"
        #self.PRIVATEBROWSER = "C:/Program Files/Mozilla Firefox/firefox.exe -private-window %s"
        # -----------------------------------------------------------------------------------------
        self.OS             = platform.system()

        self.root           = tk.Tk()
        self.widgets        = {}

        self.current_index  = 0
        self.scrolltimer = None
        self.scrolling  = False


    def build(self):
        root            = self.root
        widgets         = self.widgets
        self.root.config(background='black')

        self.current_list = self.links['video']

        dark_theme = {
            ".": {
                "configure": {
                    "background": "#2d2d2d",  # Dark grey background
                    "foreground": "white",    # White text
                }
            },
            "TLabel": {
                "configure": {
                    "foreground": "white",    # White text
                }
            },
            "TEntry": {
                "configure": {
                    "background": "#2d2d2d",  # Dark grey background
                    "foreground": "white",    # White text
                    "fieldbackground" : "#4d4d4d",
                    "insertcolor": "white",
                    "bordercolor" : "black",
                    "lightcolor" : "#4d4d4d",
                    "darkcolor" : "black",
                }
            },
                "TCheckbutton": {
                "configure": {
                    "foreground": "white",    # White text
                    "indicatorbackground" : "white",
                    "indicatorforeground" : "black",
                }
            },
            "TCombobox": {
                "configure": {
                    "background": "#2d2d2d",  # Dark grey background
                    "foreground": "white",    # White text
                    "fieldbackground" : "#4d4d4d",
                    "insertcolor": "white",
                    "bordercolor" : "black",
                    "lightcolor" : "#4d4d4d",
                    "darkcolor" : "black",
                    "arrowcolor" : "white"
                },
            },
        }

        root.title("Multisearch 0.2")
        root.minsize(410,40)
        root.geometry("440x40")

        if self.OS == "Windows":
            root.iconbitmap("icon.ico")
        elif self.OS == "Linux":
            working_dir = os.getcwd()
            icon = os.path.join(working_dir,'icon.png')
            mycon =  tk.PhotoImage(file=icon)
            root.iconphoto(True, mycon)


        root.attributes('-topmost', True)
        root.option_add("*TCombobox*Listbox*Background", "black")
        root.option_add("*TCombobox*Listbox*Foreground", "white")

        style = ttk.Style()
        style.theme_create('dark', parent="clam", settings=dark_theme)
        style.theme_use('dark')


        comboframe = ttk.Frame(root)
        combovar = tk.StringVar(root, "1")
        self.check_var = tk.BooleanVar(value=True)

        # Dictionary to create multiple buttons


        # Loop is used to create multiple combobuttons
        # rather than creating each button separately
        helv = tkf.Font( family = "Helvetica",
                                 size = 20,)


        # --------------------------------------- CHECK - BEGIN

        check = ttk.Checkbutton(comboframe
                                ,variable=self.check_var)


        check.pack              (side = 'left'
                                 ,fill='both'
                                 ,padx=2
                                 ,ipady = 5
        );
        # --------------------------------------- CHECK - END
        # --------------------------------------- LABEL - BEGIN
        label = ttk.Label        (comboframe
                                  ,text='video'
                                  ,anchor='center'
                                  ,font=helv
        );
        label.bind('<Button-1>',lambda e: self.check_var.set(not self.check_var.get()))

        label.pack              (side = 'left'
                                 ,expand=True
                                 ,fill='both'
                                 ,ipady = 5
        );

        # --------------------------------------- LABEL - END
        # --------------------------------------- COMBO - BEGIN

        combo = ttk.Combobox    (comboframe
                                 ,text = "NRK"
                                 ,textvariable = combovar
                                 ,font=helv
                                 ,justify='center'
        );


        combo.bind              ('<<ComboboxSelected>>'
                                 ,self.onComboSelectedChanged
        );
        combo.bind              ('<Return>'
                                 ,self.onReturnCombo
        );
        if self.PRIVATEBROWSER != "":
            combo.pack              (side = 'left'
                                    ,fill='both'
                                    ,expand=True
                                    ,ipady = 5
            );
        tmp = [];
        for link in self.links:
            tmp.append(link)

        combo['values'] = tmp
        del(tmp)

        # --------------------------------------- COMBO - END

        # --------------------------------------- ENTRY - BEGIN

#        entry             = tk.Entry        ( root )
#
#        entry             .bind             ( '<Return>'
#                                              ,self.onReturnEntry
#        );
#        entry             .pack             ( fill='x'
#                                              ,padx=2
#                                              ,expand=True
#        );

        # --------------------------------------- ENTRY - END

#        widgets['entry'] = entry
        widgets['combo'] = combo
        widgets['label'] = label
        widgets['check'] = check

        if self.OS == "Windows":
            widgets['combo'].bind("<MouseWheel>", self.onMouseWheel,  add='+')
            widgets['label'].bind("<MouseWheel>", self.onMouseWheel,  add='+')
            widgets['check'].bind("<MouseWheel>", self.onMouseWheel,  add='+')
        elif self.OS == "Linux":
            widgets['combo'].bind("<Button-4>", self.onMouseWheel,  add='+')
            widgets['combo'].bind("<Button-5>", self.onMouseWheel,  add='+')
            widgets['label'].bind("<Button-4>", self.onMouseWheel,  add='+')
            widgets['label'].bind("<Button-5>", self.onMouseWheel,  add='+')
            widgets['check'].bind("<Button-4>", self.onMouseWheel,  add='+')
            widgets['check'].bind("<Button-5>", self.onMouseWheel,  add='+')
        comboframe.pack         (fill='both'
                                ,expand=True)

    # --------------------------------------- !! END OF build() !!
    def onMouseWheel(self,e):
        combo = self.widgets['combo']
        nix = self.current_index
        new_index_flag = False
        if self.scrolling is False:
            if self.OS == 'Windows':

                if e.delta > 0: # up
                    if nix > 0:
                        new_index_flag = True
                        combo.current(nix - 1)
                else:
                    if nix < (len(combo['values']) -1):
                        new_index_flag = True
                        combo.current(nix + 1)

            if self.OS == 'Linux':
                if e.num == 4: # up?
                    if nix > 0:
                        new_index_flag = True
                        combo.current(nix - 1)
                else:
                    if nix < (len(combo['values']) -1):
                        new_index_flag = True
                        combo.current(nix + 1)

            if new_index_flag == True:
                sel                 = self.links[combo.get()]
                new_txt             = combo.get()
                lbl                 = self.widgets['label']
                lbl['text']         = new_txt
                self.current_list   = sel
                self.current_index  =combo.current()
                combo.delete        (0, 'end') # --------------- CLEAR ENTRY

            self.scrollfix()

    def scrollfix(self):
        if self.scrolltimer is None:
            self.scrolltimer = self.root.after(80,self.scrolldone)
            self.scrolling = True

    def scrolldone(self):
        self.scrolltimer = None
        self.scrolling = False
        self.widgets['combo'].focus_set()

    def onComboSelectedChanged(self,e=None):

        combo               = e.widget
        if self.scrolling is False:
            sel                 = self.links[combo.get()]
            new_txt             = combo.get()
            lbl                 = self.widgets['label']
            lbl['text']         = new_txt
            self.current_list   = sel
            self.current_index  =combo.current()
        combo.delete        (0, 'end') # --------------- CLEAR ENTRY
        combo.focus_set()


    def onReturnCombo(self,e=None):

        if self.check_var.get() == True and self.PRIVATEBROWSER != "":
            browser = webbrowser.get(
                self.PRIVATEBROWSER
            )
        time.sleep(0.1)
        search = self.widgets['combo'].get().replace(" ","%20")

        for link in self.current_list:
            link = f"{link}" % search
            if self.check_var.get() == True and self.PRIVATEBROWSER != "":

                browser.open(link
                             ,autoraise=True
                );
            else:
                webbrowser.open(link
                                ,autoraise=True
                );
            time.sleep(0.5)

    def mainloop(self):
        root        = self.root
        root        .after                  (1,
                                             lambda:\
                                             self.widgets['combo'].focus_set()
        );
        root        .mainloop      ()


working_dir = os.getcwd()

json_file = os.path.join(working_dir,'bookmarks.json')
try:
    with open(json_file) as json_data:
        data    = json.load(json_data)
except:

    data        = {
            'video'         :[
                'https://odysee.com/$/search?q=%s'
                ,'https://archive.org/details/movies?tab=collection&query=%s'
                ,'https://www.youtube.com/results?search_query=%s'
            ],

            'pictures'         :[
                'https://www.deviantart.com/search?q=%s'
                ,'https://duckduckgo.com/?t=ffab&q=%s&t=ffab&iar=images&iax=images&ia=images'
            ],
    }



app = MainWindow()
app.links=data
app.build()
app.mainloop()
