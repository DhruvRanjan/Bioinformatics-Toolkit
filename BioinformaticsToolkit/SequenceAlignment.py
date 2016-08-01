# Makes tab for Sequence Alignment

import gi
import Scripts.GlobalAlignment as GlobalAlignment
import Scripts.LocalAlignment as LocalAlignment
import Scripts.FittingAlignment as FittingAlignment
import Scripts.OverlapAlignment as OverlapAlignment
import Scripts.AffineGapAlignment as AffineGapAlignment
import RSeqGraphs2

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class AlignmentPage(Gtk.Box):
    def __init__(self, main_app_window):
        # Set up page
        self.main_app_window = main_app_window
        self.file_name = ""
        self.scoreDict = ""
        Gtk.Box.__init__(self)
        self.set_border_width(10)
        self.set_orientation(Gtk.Orientation.VERTICAL)
        alignment_grid = Gtk.Grid()

        # Set up buttons
        self.global_alignment_button = Gtk.ToggleButton(label="Global Alignment")
        self.local_alignment_button = Gtk.ToggleButton(label="Local Alignment")
        self.fitting_alignment_button = Gtk.ToggleButton(label="Fitting Alignment")
        self.overlap_alignment_button = Gtk.ToggleButton(label="Overlap Alignment")
        self.affine_gap_alignment_button = Gtk.ToggleButton(label="Affine Gap Alignment")
        self.add(alignment_grid)

        # Add buttons to grid
        alignment_grid.attach(self.global_alignment_button, 0, 1, 1, 1)
        alignment_grid.attach_next_to(self.local_alignment_button, self.global_alignment_button, Gtk.PositionType.RIGHT,
                                      1, 1)
        alignment_grid.attach_next_to(self.fitting_alignment_button, self.local_alignment_button,
                                      Gtk.PositionType.RIGHT, 1, 1)
        alignment_grid.attach_next_to(self.overlap_alignment_button, self.fitting_alignment_button,
                                      Gtk.PositionType.RIGHT, 1, 1)
        alignment_grid.attach_next_to(self.affine_gap_alignment_button, self.overlap_alignment_button,
                                      Gtk.PositionType.RIGHT, 1,
                                      1)

        # Set callback handlers for each button
        self.global_alignment_button.connect("toggled", self.handle_toggle)
        self.local_alignment_button.connect("toggled", self.handle_toggle)
        self.fitting_alignment_button.connect("toggled", self.handle_toggle)
        self.overlap_alignment_button.connect("toggled", self.handle_toggle)
        self.affine_gap_alignment_button.connect("toggled", self.handle_toggle)

        # Add file choosing button

        file_choose_button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        file_choose_button = Gtk.Button("Choose File")
        file_choose_button_box.pack_start(file_choose_button, True, True, 0)
        file_choose_button.connect("clicked", self.file_chooser_clicked)
        alignment_grid.attach_next_to(file_choose_button_box, self.global_alignment_button, Gtk.PositionType.BOTTOM, 5,
                                      1)

        # Add label for displaying the name of the chosen file

        self.file_name_label = Gtk.Label("")
        file_choose_button_box.pack_start(self.file_name_label, True, False, 0)

        # Add Frame for selecting scoring matrix
        alignment_frame = Gtk.Frame()
        alignment_frame.set_label("Choose Scoring Matrix")
        alignment_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        alignment_grid.attach_next_to(alignment_frame, file_choose_button_box, Gtk.PositionType.BOTTOM, 1, 2)
        alignment_frame.add(alignment_box)

        # Add Radio buttons for scoring matrices

        self.blosum62_button = Gtk.RadioButton.new_with_label_from_widget(None, label="Blosum62")
        self.blosum45_button = Gtk.RadioButton.new_with_label_from_widget(self.blosum62_button, label="Blosum45")
        self.blosum90_button = Gtk.RadioButton.new_with_label_from_widget(self.blosum62_button, label="Blosum90")

        self.pam250_button = Gtk.RadioButton.new_with_label_from_widget(self.blosum62_button, label="Pam250")
        self.pam30_button = Gtk.RadioButton.new_with_label_from_widget(self.blosum62_button, label="Pam30")
        self.pam70_button = Gtk.RadioButton.new_with_label_from_widget(self.blosum62_button, label="Pam70")

        alignment_box.pack_start(self.blosum62_button, True, True, 5)
        alignment_box.pack_start(self.blosum45_button, True, True, 5)
        alignment_box.pack_start(self.blosum90_button, True, True, 5)
        alignment_box.pack_start(Gtk.HSeparator(), False, False, 0)
        alignment_box.pack_start(self.pam250_button, True, True, 5)
        alignment_box.pack_start(self.pam30_button, True, True, 5)
        alignment_box.pack_start(self.pam70_button, True, True, 5)

        # Add frame and text boxes to hold the input DNA sequences

        seq_frame = Gtk.Frame()
        seq_frame.set_label("DNA Sequences")
        seq_frame.set_label_align(0.5, 1.0)
        seq_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=30)
        self.seq1_text = Gtk.Entry()
        self.seq2_text = Gtk.Entry()
        self.seq1_text.set_max_length(65536)
        self.seq2_text.set_max_length(65536)
        seq_box.pack_start(self.seq1_text, True, True, 5)
        seq_box.pack_start(self.seq2_text, True, True, 5)
        seq_frame.add(seq_box)
        alignment_grid.attach_next_to(seq_frame, alignment_frame, Gtk.PositionType.RIGHT, 5, 1)

        # Add button to start alignment

        align_button = Gtk.Button(label="Align Sequences")
        align_button.connect("clicked", self.align_button_clicked)
        alignment_grid.attach_next_to(align_button, seq_frame, Gtk.PositionType.BOTTOM, 1, 1)

        # Add Results frame

        results_frame = Gtk.Frame()
        results_frame.set_label("Results")
        results_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        results_frame.add(results_box)
        # alignment_grid.attach_next_to(results_frame, alignment_frame, Gtk.PositionType.BOTTOM, 1, 1)
        self.pack_start(results_frame, True, True, 5)

        # Add text box to hold the alignment score
        # Add text boxes to hold the sequence alignments

        self.score_text = Gtk.Entry()
        self.align1_text = Gtk.Entry()
        self.align2_text = Gtk.Entry()
        self.align1_text.set_max_length(65536)
        self.align2_text.set_max_length(65536)

        score_label = Gtk.Label("Alignment Score")
        align1_label = Gtk.Label("Sequence 1 Alignment")
        align2_label = Gtk.Label("Sequence 2 Alignment")

        score_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=55)
        seq1_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        seq2_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)

        score_box.pack_start(score_label, False, True, 5)
        score_box.pack_start(self.score_text, False, True, 5)
        seq1_box.pack_start(align1_label, False, True, 5)
        seq1_box.pack_start(self.align1_text, True, True, 5)
        seq2_box.pack_start(align2_label, False, True, 5)
        seq2_box.pack_start(self.align2_text, True, True, 5)

        results_box.pack_start(score_box, True, True, 5)
        results_box.pack_start(seq1_box, True, True, 5)
        results_box.pack_start(seq2_box, True, True, 5)

        # Add button to generate graphs using R (for current selection)

        graph_button = Gtk.Button(label="Generate Score Graph")
        graph_button.connect("clicked", self.make_graph_button_clicked)
        alignment_grid.attach_next_to(graph_button, align_button, Gtk.PositionType.RIGHT, 1, 1)

        # Add button to generate graphs using R for current selection and all matrices

        graph_button_matrices = Gtk.Button(label="Generate Matrix Graph")
        graph_button_matrices.connect("clicked", self.make_graph_button_matrices_clicked)
        alignment_grid.attach_next_to(graph_button_matrices, graph_button, Gtk.PositionType.RIGHT,1,1)

    def make_graph_button_matrices_clicked(self,widget):

        RSeqGraphs2.plotMatrixScores(int(self.score_text.get_text()), self.align1_text.get_text(),
                                  self.align2_text.get_text())

    def make_graph_button_clicked(self, widget):

        RSeqGraphs2.plotSeqScores(int(self.score_text.get_text()), self.align1_text.get_text(),
                                  self.align2_text.get_text(), self.scoreDict)

    def align_button_clicked(self, widget):

        # determine selected matrix
        matrix_buttons = self.blosum62_button.get_group()
        selected_matrix = ""
        for matrix in matrix_buttons:
            if matrix.get_active():
                selected_matrix = matrix.get_properties("label")[0]
        print selected_matrix
        # determine selected alignment method
        if self.global_alignment_button.get_active():
            score, seq1, seq2, scoreDict = GlobalAlignment.globalAlignmentWrapper(self.file_name, selected_matrix)
        elif self.local_alignment_button.get_active():
            score, seq1, seq2, scoreDict = LocalAlignment.localAlignmentWrapper(self.file_name, selected_matrix)
        elif self.fitting_alignment_button.get_active():
            score, seq1, seq2 = FittingAlignment.fittingAlignmentWrapper(self.file_name)
        elif self.overlap_alignment_button.get_active():
            score, seq1, seq2 = OverlapAlignment.overlapAlignmentWrapper(self.file_name)
        elif self.affine_gap_alignment_button.get_active():
            score, seq1, seq2, scoreDict = AffineGapAlignment.affineGapAlignmentWrapper(self.file_name, selected_matrix)
        self.score_text.set_text(str(score))
        self.align1_text.set_text(seq1)
        self.align2_text.set_text(seq2)
        self.scoreDict = scoreDict

    def file_chooser_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Select a file", self.main_app_window, Gtk.FileChooserAction.OPEN,
                                       ("Cancel", Gtk.ResponseType.CANCEL,
                                        "Open", Gtk.ResponseType.OK))

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.file_name = dialog.get_filename()
            self.file_name_label.set_label(self.file_name)
            print("You Clicked the Open button")
            print("File selected: " + dialog.get_filename())
            self.display_seqs(self.file_name)
        elif response == Gtk.ResponseType.CANCEL:
            print("You clicked cancel")
        dialog.destroy()

    def display_seqs(self, fileName):

        contents = open(fileName).readlines()
        seq1 = contents[0].strip()
        seq2 = contents[1].strip()
        print seq1
        print seq2
        self.seq1_text.set_text(seq1)
        self.seq2_text.set_text(seq2)

    def handle_toggle(self, widget):

        button_name = widget.get_properties("label")[0]
        print button_name
        if button_name == "Global Alignment" and widget.get_active() == True:
            self.local_alignment_button.set_active(False)
            self.fitting_alignment_button.set_active(False)
            self.overlap_alignment_button.set_active(False)
            self.affine_gap_alignment_button.set_active(False)
        elif button_name == "Local Alignment" and widget.get_active() == True:
            self.global_alignment_button.set_active(False)
            self.fitting_alignment_button.set_active(False)
            self.overlap_alignment_button.set_active(False)
            self.affine_gap_alignment_button.set_active(False)
        elif button_name == "Fitting Alignment" and widget.get_active() == True:
            self.local_alignment_button.set_active(False)
            self.global_alignment_button.set_active(False)
            self.overlap_alignment_button.set_active(False)
            self.affine_gap_alignment_button.set_active(False)
        elif button_name == "Overlap Alignment" and widget.get_active() == True:
            self.local_alignment_button.set_active(False)
            self.fitting_alignment_button.set_active(False)
            self.global_alignment_button.set_active(False)
            self.affine_gap_alignment_button.set_active(False)
        elif button_name == "Affine Gap Alignment" and widget.get_active() == True:
            self.local_alignment_button.set_active(False)
            self.fitting_alignment_button.set_active(False)
            self.overlap_alignment_button.set_active(False)
            self.global_alignment_button.set_active(False)
