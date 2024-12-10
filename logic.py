from PyQt6.QtWidgets import *
from gui import *
import os
import  csv

if not os.path.exists("voterID.txt"):
    with open("voterID.txt", "w") as file:
        pass

class Logic(QMainWindow, Ui_MainWindow):
    """
    Logic class that handles the voting application.
    voteButton: QPushButton connected to trigger the vote method.
    warningLabel: QLabel used to display warnings or success messages.
    """
    def __init__(self) -> None:
        """
        Initialize the voting application.
        Sets up ui, hides the warning label initially.
        """
        super().__init__()
        self.setupUi(self)
        self.voteButton.clicked.connect(lambda: self.vote())
        self.warningLabel.setVisible(False)
        self.vote_counts = {"Jordan": 0, "Lebron": 0}
        self.load_votes()
        self.update_vote_counts()

    def load_votes(self) -> None:
        """
        Loads votes from the file and updates vote counts.
        """
        try:
            with open("voterID.txt", "r") as fileCheck:
                for line in fileCheck:
                    _, candidate = line.strip().split(",")
                    if candidate in self.vote_counts:
                        self.vote_counts[candidate] += 1
        except FileNotFoundError:
            pass

    def update_vote_counts(self) -> None:
        """
        Updates the vote count labels on the GUI.
        """
        self.jordanCount.setText(str(self.vote_counts["Jordan"]))
        self.lebronCount.setText(str(self.vote_counts["Lebron"]))
    def vote(self) -> None:
        """
        voting button logic, checks if ID is valid, checks whether voter has already voted,
        records vote for the candidate
        Displays messages for invalid input, duplicate voting, or normal voting.
        """
        try:
            idField: int = int(self.idField.text())
            voter_found: bool = False
            with open("voterID.txt", "r+") as file:
                voters: list[str] = file.readlines()
                for line in voters:
                    voter_id: str = line.strip().split(",")[0]
                    if str(idField) == voter_id:
                        voter_found = True
                        break
                if voter_found:
                    self.warningLabel.setVisible(True)
                    self.warningLabel.setText("Already Voted")
                    self.warningLabel.setStyleSheet("color: red;")
                else:
                    candidate: str | None = None
                    if self.jordanRadio.isChecked():
                        candidate = "Jordan"
                    elif self.lebronRadio.isChecked():
                        candidate = "Lebron"
                    if candidate:
                        file.write(f"{idField},{candidate}\n")
                        self.vote_counts[candidate] += 1
                        self.update_vote_counts()
                        self.warningLabel.setVisible(True)
                        self.warningLabel.setText(f"Vote cast for {candidate}")
                        self.warningLabel.setStyleSheet("color: green;")
                        self.update_vote_counts()
                    else:
                        self.warningLabel.setVisible(True)
                        self.warningLabel.setText("Please select a candidate")
                        self.warningLabel.setStyleSheet("color: orange;")

        except ValueError:
            # Handle non-integer inputs
            self.warningLabel.setVisible(True)
            self.warningLabel.setText("Identifier must be numbers only")
            self.warningLabel.setStyleSheet("color: red;")
