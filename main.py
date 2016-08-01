import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import SequenceAlignment


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Bioinformatics Toolkit v0.01")

        # set window properties
        self.set_default_size(700, 550)
        self.set_border_width(10)

        # set up tabs
        self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        # set up header bar

        header_bar = Gtk.HeaderBar()
        header_bar.set_show_close_button(True)  # So the user can access the "close" button
        header_bar.props.title = "Bioinformatics Toolkit v0.01"
        self.set_titlebar(header_bar)

        # Home page
        self.page1 = Gtk.Box()
        self.page1.set_border_width(10)
        # self.page1.add(Gtk.Label("Stuff in main area."))
        self.notebook.append_page(self.page1, Gtk.Label("Main"))

        # Grid containing buttons for different modules
        self.grid = Gtk.Grid()
        self.page1.add(self.grid)

        # Add button to go to Alignment tab
        alignmentButton = Gtk.Button()
        alignmentImage = Gtk.Image()
        alignmentLabel = Gtk.Label()
        alignmentLabel.set_markup("<big> Sequence Alignment </big>")
        alignmentImage.set_from_file("Pictures/Icons/Alignment.png")
        alignmentButton.set_image(alignmentImage)

        # Add to grid such that button is right below label
        self.grid.attach(alignmentLabel, 0, 1, 1, 1)
        self.grid.attach(alignmentButton, 0, 2, 1, 3)

        # Add callback method to button
        alignmentButton.connect("clicked", self.alignment_clicked)
        '''new_tab = Gtk.Box()
        new_tab.set_border_width(10)
        grid = Gtk.Grid()
        new_tab.add(grid)'''

        # Add tab for sequence alignment

        alignment_page = SequenceAlignment.AlignmentPage(self)
        self.notebook.append_page(alignment_page, Gtk.Label("Sequence Alignment"))

    def makeButton(self, labelText, imageLoc, labelCoords, imageCoords, pageNum):
        button = Gtk.Button()
        image = Gtk.Image()
        label = Gtk.Label()
        label.set_markup("<big> " + labelText + "</big>")
        image.set_from_file(imageLoc)
        button.set_image(image)
        self.grid.attach(label, labelCoords[0], labelCoords[1], labelCoords[2], labelCoords[3])
        self.grid.attach(image, imageCoords[0], imageCoords[1], imageCoords[2], imageCoords[3])

    def button_clicked(self, widget, pageNumber):
        print("go to " + widget.get_properties("label")[0])

    def alignment_clicked(self, widget):
        print("go to alignment tab")
        '''new_tab = Gtk.Box()
        new_tab.set_border_width(10)
        grid = Gtk.Grid()
        new_tab.add(grid)
        self.notebook.append_page(new_tab, Gtk.Label("Sequence Alignment"))'''
        self.notebook.set_current_page(1)


window = MainWindow()
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()
