#!/usr/bin/python
# -*- coding:Utf-8 -*-

import gtk
import os
import sys

import webkit
import gobject

class Browser:
    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def open_list(self):
        self.urls = open("urls", "r").readlines()
        if len(self.urls) == 0:
            print "List empty, fill list before launching"
            sys.exit(0)
        print len(self.urls), self.urls

    def __init__(self):
        gobject.threads_init()
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_resizable(True)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.connect("key-press-event", self.keyboard_cb)

        self.open_list()

        self.position = 0

        #webkit.WebView allows us to embed a webkit browser
        #it takes care of going backwards/fowards/reloading
        #it even handles flash
        self.web_view = webkit.WebView()
        self.web_view.open(self.urls[0][:-1])

        #entry bar for typing in and display URLs, when they type in a site
        #and hit enter the on_active function is called
        self.url_bar = gtk.Entry()
        self.url_bar.connect("activate", self.on_active)

        self.bar = gtk.Label()
        self.bar.set_single_line_mode(True)
        self.bar.set_text(self.urls[0][:-1] + "               " + "%i/%i" % (self.position + 1, len(self.urls)))

        #anytime a site is loaded the update_buttons will be called
        self.web_view.connect("load_committed", self.update_buttons)

        scroll_window = gtk.ScrolledWindow(None, None)
        scroll_window.add(self.web_view)


        vbox = gtk.VBox(False, 0)
        vbox.pack_start(self.bar, False, True, 0)
        vbox.add(scroll_window)

        self.window.add(vbox)
        self.window.show_all()

    def on_active(self, widge, data=None):
        '''When the user enters an address in the bar, we check to make
           sure they added the http://, if not we add it for them.  Once
           the url is correct, we just ask webkit to open that site.'''
        url = self.url_bar.get_text()
        try:
            url.index("://")
        except:
            url = "http://"+url
        self.url_bar.set_text(url)
        self.web_view.open(url)

    def go_back(self, widget, data=None):
        '''Webkit will remember the links and this will allow us to go
           backwards.'''
        self.web_view.go_back()

    def go_forward(self, widget, data=None):
        '''Webkit will remember the links and this will allow us to go
           forwards.'''
        self.web_view.go_forward()

    def refresh(self, widget, data=None):
        '''Simple makes webkit reload the current back.'''
        self.web_view.reload()

    def update_buttons(self, widget, data=None):
        '''Gets the current url entry and puts that into the url bar.
           It then checks to see if we can go back, if we can it makes the
           back button clickable.  Then it does the same for the foward
           button.'''
        self.url_bar.set_text( widget.get_main_frame().get_uri() )

    def main(self):
        gtk.main()

    def keyboard_cb(self, widget, event, data=None):
        #print "event:", event
        keyname = gtk.gdk.keyval_name(event.keyval)
        print keyname
        if keyname == "Escape" or keyname == "q":
            print "call deleting"
            self.destroy(widget)
        elif keyname == "space" or keyname == "n":
            print "next"
            self.next()
        elif keyname == "r" or keyname == "R":
            print "reload"
            self.refresh("widget")
        elif keyname == "b" or keyname == "p" or keyname == "Backspace":
            print "previous"
            self.previous()
        elif keyname == "s":
            print "saving"
            self.save()
        elif keyname == "S":
            print "saving"
            self.save()
            print "destroying"
            self.destroy("widget")
        elif keyname == "y":
            print "copy to clipboard"
            if os.system('echo -n "%s" | xclip -i' % self.web_view.get_main_frame().get_uri()):
                print "#fail"
        elif keyname == "f":
            print "go to firefox"
            if os.system("firefox %s" % self.web_view.get_main_frame().get_uri()):
                print "#fail"

    def save(self):
        urls = open("urls", "w")
        for i in self.urls[self.position + 1:]:
            urls.write(i)

    def next(self):
        print "was:", self.position
        if self.position < len(self.urls) - 1:
            print "go forwarf", self.position + 1
            self.position += 1
            print "loading:", self.urls[self.position][:-1]
            self.web_view.open(self.urls[self.position][:-1])
            self.bar.set_text(self.urls[self.position][:-1] + "               " + "%i/%i" % (self.position + 1, len(self.urls)))
        elif self.position == len(self.urls) - 1:
            print "show finish", self.position + 1
            data = '<html><head><title>Hello</title></head><body><center><h1>Finish</h1><h3>One more step forward and the browser will quit and empty the list</h3></center></body></html>'
            self.web_view.load_string(data, 'text/html', "utf-8", "about")
            self.position += 1

        else:
            print "end → saving → destroy"
            self.save()
            self.destroy("widget")

    def previous(self):
        print "was:", self.position
        if self.position > 0:
            print "go back", self.position - 1
            self.position -= 1
            self.web_view.open(self.urls[self.position][:-1])
            self.bar.set_text(self.urls[self.position][:-1] + "               " + "%i/%i" % (self.position + 1, len(self.urls)))
        elif self.position == 0:
            self.position -= 1
            print "show begin"
            data = '<html><head><title>Hello</title></head><body><center><h1>Begin</h1></center></body></html>'
            self.web_view.load_string(data, 'text/html', "utf-8", "about")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        open("/home/psycojoker/code/python/ulr/urls", "a").write(sys.argv[1] + "\n")
    else:
        browser = Browser()
        browser.main()

