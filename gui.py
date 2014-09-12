#!/usr/bin/python3

from gi.repository import Gtk, Gdk, Gio, GdkPixbuf

class SlideWidget(Gtk.EventBox):

	def __init__(self, filename):
		super(Gtk.EventBox, self).__init__()
		self.image = Gtk.Image.new_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file(filename))
		self.add(self.image)
		self.active=True

		self.connect("button_press_event", lambda widget, event: self.toggleActive(event))

	def toggleActive(self,event):
		if event.type != Gdk.EventType.BUTTON_PRESS or event.button != 1:
			return
		self.active = not self.active
		self.image.set_opacity(1.0 if self.active else 0.1)



class MainWindow(Gtk.Window):

	def __init__(self):	
		super(Gtk.Window, self).__init__()

		#Window Header Bar
		headerBar = Gtk.HeaderBar()
		headerBar.props.show_close_button = True
		headerBar.props.title = "SvgSlides"
		self.set_titlebar(headerBar)


		button = Gtk.Button(label="Create PDF!")
		headerBar.pack_end(button)


		#Window Content
		self.scrollArea = Gtk.ScrolledWindow()		
		self.slides = Gtk.VBox()
		self.slides.set_spacing(16)
		for i in range(4):
			self.slides.add(SlideWidget("presentation.png"))

		self.scrollArea.set_size_request(900,800)
		self.scrollArea.add(self.slides)
		self.add(self.scrollArea)


	def on_slide_clicked(self, widget, event):
		
		image = widget.get_children()[0]
		if(image.get_opacity() == 1.0 ): image.set_opacity(0.2) 
		else: image.set_opacity(1.0);

	def on_button_clicked(self, widget):
		print("eier")

win = MainWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()