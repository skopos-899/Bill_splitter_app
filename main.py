import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, 
    QHBoxLayout, QScrollArea, QFrame, QFormLayout, QMessageBox 
)
from PyQt6.QtCore import Qt

class RentSplitCalculator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Rent Split Calculator")
        self.setGeometry(100, 100, 500, 600)
        self.setMinimumSize(300, 600)  # Minimum size for smaller screens
        self.setMaximumSize(400, 700)

        # Layouts
        main_layout = QVBoxLayout()

        # Number of roommates
        num_roommates_layout = QHBoxLayout()
        num_roommates_label = QLabel("No. of Roommates:")
        self.num_roommates_input = QLineEdit()
        self.num_roommates_input.setText("2")  # Default value
        self.num_roommates_input.setPlaceholderText("Enter number of roommates")  # Updated placeholder
        self.num_roommates_input.returnPressed.connect(self.create_roommate_entries)
        num_roommates_layout.addWidget(num_roommates_label)
        num_roommates_layout.addWidget(self.num_roommates_input)
        
        # Scrollable roommate entries
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.roommate_container = QWidget()
        self.roommate_layout = QVBoxLayout(self.roommate_container)
        self.scroll_area.setWidget(self.roommate_container)

        # Room Rent
        room_rent_layout = QHBoxLayout()
        room_rent_label = QLabel("Total Room Rent:")
        self.room_rent_input = QLineEdit()
        self.room_rent_input.setText("900")  # Default value
        self.room_rent_input.returnPressed.connect(self.calculate_rent_split)
        room_rent_layout.addWidget(room_rent_label)
        room_rent_layout.addWidget(self.room_rent_input)

        # Buttons
        button_layout = QHBoxLayout()  # Change back to QHBoxLayout for side-by-side layout
        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.setMinimumHeight(40)  # Increase button height for touch
        self.calculate_button.clicked.connect(self.calculate_rent_split)

        self.clear_button = QPushButton("Clear")
        self.clear_button.setMinimumHeight(40)  # Increase button height for touch
        self.clear_button.clicked.connect(self.clear_inputs)

        button_layout.addWidget(self.calculate_button)
        button_layout.addWidget(self.clear_button)


        # Result display
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)

        # Add everything to main layout
        main_layout.addLayout(num_roommates_layout)
        main_layout.addWidget(self.scroll_area)
        main_layout.addLayout(room_rent_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(QLabel("Rent Split Results:"))
        main_layout.addWidget(self.result_display)

        self.setLayout(main_layout)

        self.setStyleSheet("""
    QWidget {
        background-color: #1C1C1C;  /* Dark gray background */
        color: #D8DEE9;              /* Light text color */
        font-size: 14px;
    }
    QLabel {
        font-weight: bold;
        color: #E0E4E9;              /* Lighter label color for better contrast */
    }
    QLineEdit {
        background-color: #2A2A2A;   /* Darker input field background */
        color: #D8DEE9;               /* Light text in input fields */
        border: 1px solid #3B3B3B;   /* Darker border color */
        padding: 5px;
        border-radius: 5px;
        min-width: 150px;  /* Minimum width for input fields */
    }
    QPushButton {
        background-color: #5E81AC;   /* Keep the button color */
        color: white;
        border-radius: 5px;
        padding: 8px;
        min-width: 80px;  /* Minimum width for buttons */
    }
    QPushButton:hover {
        background-color: #81A1C1;    /* Hover effect */
    }
    QTextEdit {
        background-color: #2A2A2A;    /* Keep the result display background darker */
        color: #D8DEE9;                /* Light text in result display */
        border: 1px solid #3B3B3B;    /* Darker border for result display */
        padding: 5px;
        border-radius: 5px;
    }
""")

        # Initialize roommate entries
        self.roommate_name_inputs = []
        self.expense_inputs = []
        self.create_roommate_entries()

    def create_roommate_entries(self):
        try:
            num_roommates = int(self.num_roommates_input.text())

            if num_roommates < 2:
                QMessageBox.critical(self, "Error", "Number of roommates must be at least 2.")
                return
            elif num_roommates > 10:
                QMessageBox.critical(self, "Error", "Number of roommates must be less than 10.")
                return

            # Clear previous entries
            for i in reversed(range(self.roommate_layout.count())):
                self.roommate_layout.itemAt(i).widget().deleteLater()

            self.roommate_name_inputs = []
            self.expense_inputs = []

            for i in range(num_roommates):
                form_layout = QFormLayout()

                # Roommate Name
                name_input = QLineEdit()
                name_input.setPlaceholderText(f"Roommate {i + 1} Name")  # Set placeholder
                self.roommate_name_inputs.append(name_input)

                # Expense
                expense_input = QLineEdit()
                expense_input.setPlaceholderText(f"Goods Expense {i + 1}")  # Set placeholder
                self.expense_inputs.append(expense_input)

                # Bind Enter key navigation
                name_input.returnPressed.connect(lambda i=i: self.focus_next(i, "name"))
                expense_input.returnPressed.connect(lambda i=i: self.focus_next(i, "expense"))

                # Add to layout
                frame = QFrame()
                frame.setLayout(form_layout)
                form_layout.addRow(name_input)  # Add input to form layout
                form_layout.addRow(expense_input)  # Add input to form layout
                self.roommate_layout.addWidget(frame)

            self.roommate_name_inputs[0].setFocus()

        except ValueError:
            QMessageBox.critical(self, "Error", "Please enter a valid number of roommates.")

    def focus_next(self, index, entry_type):
        if entry_type == "name":
            name = self.roommate_name_inputs[index].text().strip()
            if not name:
                QMessageBox.critical(self, "Error", f"Please enter a name for Roommate {index + 1}.")
                self.roommate_name_inputs[index].setFocus()
                return
            elif not all(part.isalpha() for part in name.split()):
                QMessageBox.critical(self, "Error", f"Please enter a valid name for Roommate {index + 1}.")
                self.roommate_name_inputs[index].setFocus()
                return
            self.expense_inputs[index].setFocus()
        elif entry_type == "expense":
            expense_value = self.expense_inputs[index].text().strip()
            if not expense_value:
                QMessageBox.critical(self, "Error", f"Please enter an expense for Goods Expenses {index + 1}.")
                self.expense_inputs[index].setFocus()
                return
            try:
                expense_float = float(expense_value)
                if expense_float < 0:
                    raise ValueError("Negative value")
            except ValueError:
                QMessageBox.critical(self, "Error", f"Please enter a valid positive number for Goods Expenses {index + 1}.")
                self.expense_inputs[index].setFocus()
                return

            if index < len(self.expense_inputs) - 1:
                self.roommate_name_inputs[index + 1].setFocus()
            else:
                self.room_rent_input.setFocus()

    def calculate_rent_split(self):
        try:
            total_rent = float(self.room_rent_input.text())
            num_roommates = len(self.roommate_name_inputs)
            expenses = [float(expense.text() or 0) for expense in self.expense_inputs]

            total_expenses = sum(expenses)
            average_expense = total_expenses / num_roommates
            room_rent_share = total_rent / num_roommates

            results = []
            for i in range(num_roommates):
                name = self.roommate_name_inputs[i].text() or f"Roommate {i + 1}"
                difference = average_expense - expenses[i]

                if expenses[i] > average_expense:
                    amount_due = room_rent_share - (expenses[i] - average_expense)
                else:
                    amount_due = room_rent_share + (average_expense - expenses[i])

                results.append(f"{name}: Rs {amount_due:.2f}")

            self.result_display.clear()
            self.result_display.setPlainText("\n".join(results))

        except ValueError:
            QMessageBox.critical(self, "Error", "Please enter a valid total rent.")

    def clear_inputs(self):
        self.num_roommates_input.setText("2")
        self.room_rent_input.setText("900")
        self.result_display.clear()

        for name_input in self.roommate_name_inputs:
            name_input.clear()
        for expense_input in self.expense_inputs:
            expense_input.clear()

        self.num_roommates_input.setFocus()
        self.create_roommate_entries()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RentSplitCalculator()
    window.show()
    sys.exit(app.exec())
