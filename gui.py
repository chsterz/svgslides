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
		self.image.set_opacity(1.0 if self.active else 0.2)


class MainWindow(Gtk.Window):

	def __init__(self):	
		super(Gtk.Window, self).__init__()

		#center the MainWindow
		self.set_position(Gtk.WindowPosition.CENTER)

		#Window Header Bar
		headerBar = Gtk.HeaderBar()
		headerBar.props.show_close_button = True
		headerBar.props.title = "SvgSlides"
		self.set_titlebar(headerBar)

		chooseFileButton = Gtk.Button(label="Open")
		chooseFileButton.connect("clicked", self.openFileDialog)
		headerBar.pack_start(chooseFileButton)

		createButton = Gtk.Button(label="Create PDF!")
		headerBar.pack_end(createButton)

		#add Droparea to Window first
		self.dropArea = Gtk.EventBox()
		self.dropArea.set_size_request(1024,800)
		self.dropArea.add(Gtk.Image.new_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file("dropMe.png")))
		self.add(self.dropArea)

		#set upd drag and drop
		self.connect('drag-motion', self.on_drag_motion)
		self.connect('drag-drop', self.on_drag_drop)
		self.connect('drag-data-received', self.on_drag_data_received)
		self.drag_dest_set(0, [], 0)

	def on_drag_motion(self, widgt, context, c, y, time):
		Gdk.drag_status(context, Gdk.DragAction.COPY, time)
		return True

	def on_drag_drop(self, widget, context, x, y, time):
		widget.drag_get_data(context, context.list_targets()[-1], time)

	def on_drag_data_received(self, widget, drag_context, x, y, data, info, time):
		files = data.get_text().rstrip('\n').split('\n')
		#drop no more than one file
		if( len(files) != 1 ): return;
		svgFile = files[0]
		#check if file is SVG
		if( svgFile[-4:] != ".svg"): return;
		self.openFile(files[0])

	def openFile(self, filename):
		print("Doing something with " + filename)
		self.showSlides(["presentation.png", "presentation.png", "presentation.png", "presentation.png"])

	def showSlides(self, slideFiles):
		#Window Content
		self.scrollArea = Gtk.ScrolledWindow()
		self.slides = Gtk.VBox()
		self.slides.set_spacing(16)
		for filename in slideFiles:
			self.slides.add(SlideWidget(filename))
		
		self.scrollArea.add(self.slides)
		self.remove(self.get_children()[0])
		self.add(self.scrollArea)
		self.scrollArea.show_all()
		print (self.dropArea.get_children()[0])

	def openFileDialog(self, widget):
		dialog = Gtk.FileChooserDialog("Please choose a file", self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

		svgFilter = Gtk.FileFilter()
		svgFilter.add_pattern("*.svg")
		svgFilter.set_name("Scalable Vector Graphics (*.svg)")
		dialog.add_filter(svgFilter)
		
		response = dialog.run()
		if response == Gtk.ResponseType.OK: self.openFile(dialog.get_filename());
		elif response == Gtk.ResponseType.CANCEL: print("Cancel clicked");

		dialog.destroy()

win = MainWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()