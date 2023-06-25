from PyQt6 import QtCore, QtWidgets
from PyQt6.QtGui import QScreen
from .main_window import MainWindow
from ..static import (
    GRAPH_DATA,
    LANDING_PAGE_TITLE,
    LANDING_PAGE_WIDTH,
    LANDING_PAGE_HEIGHT,
    PageState,
    VERSIONS,
)


class DropDownListBox(QtWidgets.QComboBox):
    popup_dropdown_window = QtCore.pyqtSignal()

    def showPopup(self):
        self.popup_dropdown_window.emit()
        super(DropDownListBox, self).showPopup()


class LandingPage(QtWidgets.QWidget):
    """
    This is the dropdown menu that appears first on the screen.
    The user is given a list of choices from which she can choose from,
    and when one item is chosen, this window is closed and another window
    with the chosen content pops up.
    """

    def __init__(self):
        super(LandingPage, self).__init__()

        # Set default layout
        self.setWindowTitle(LANDING_PAGE_TITLE)
        self.setGeometry(0, 0, LANDING_PAGE_WIDTH, LANDING_PAGE_HEIGHT)
        self.layout = QtWidgets.QHBoxLayout(
            self)  # Change to QHBoxLayout to place elements side by side

        # Add dropdown list to the window
        self._create_dropdown_list()

        # Add select button to the window
        self._create_select_button()

        # Center the window on the screen
        self._center_window()

    def show(self):
        # Bring window to the front and keep it there
        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        super().show()

    def _center_window(self):
        """Center the window on the screen"""

        screen_geometry = QtWidgets.QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - LANDING_PAGE_WIDTH) // 2
        y = (screen_geometry.height() - LANDING_PAGE_HEIGHT) // 2
        self.move(x, y)

    def _create_dropdown_list(self):
        """Create a clickable dropdown list to this window"""

        dropdown_category = DropDownListBox(self)
        dropdown_list = DropDownListBox(self)
        dropdown_list_version = DropDownListBox(self)

        # Define all choices the users can choose from
        dropdown_category.addItems(sorted(GRAPH_DATA.keys()))
        dropdown_category.setCurrentIndex(0)  # Select the first item by default

        # Add widget to the layout
        self.layout.addWidget(dropdown_category)
        self.layout.addWidget(dropdown_list)
        self.layout.addWidget(dropdown_list_version)
        self.dropdown_category = dropdown_category
        self.dropdown_list = dropdown_list
        self.dropdown_list_version = dropdown_list_version

        # Signal slot connection
        dropdown_category.currentIndexChanged.connect(self._update_listing)
        dropdown_list.currentIndexChanged.connect(self._update_version_dropdown)
        # Trigger the update manually for the first time
        self._update_listing(0)
        self._update_version_dropdown(0)

    def _update_listing(self, index):
        """Update the version dropdown based on the selected item in the first dropdown"""
        selected_category = self.dropdown_category.itemText(index)
        self.dropdown_list.clear()
        self.dropdown_list.addItems(sorted(GRAPH_DATA[selected_category].keys()))

    def _update_version_dropdown(self, index):
        """Update the version dropdown based on the selected item in the second dropdown"""
        if len(self.dropdown_list) == 0:
            return

        selected_animal = self.dropdown_list.itemText(index)
        self.dropdown_list_version.clear()
        self.dropdown_list_version.addItems(VERSIONS[selected_animal])

        if not len(VERSIONS[selected_animal]) == 1:
            self.dropdown_list_version.setEnabled(True)
        else:
            self.dropdown_list_version.setDisabled(True)

    def _create_select_button(self):
        """Create a select button to this window"""
        select_button = QtWidgets.QPushButton("Select", self)

        # Set click event
        select_button.clicked.connect(self._select_button_on_click)

        # Calculate the preferred size of the button
        size_hint = select_button.sizeHint()

        # Set the fixed width based on the preferred size
        select_button.setFixedWidth(size_hint.width())

        # Add widget to the layout
        self.layout.addWidget(select_button)

    def _select_button_on_click(self):
        """
        When user clicks the select button, close this 'menu' window
        and open the desired dashboard
        """

        # Select item and version
        category = self.dropdown_category.currentText()
        page_id = self.dropdown_list.currentText()
        page_version = self.dropdown_list_version.currentText()

        # In case we already opened, close the previous one
        if hasattr(self, "main_window"):
            # TODO what if we keep all canvas and just show and hide them
            PageState.clear()
            self.main_window.close()

        # Create new window and hide this one
        PageState.select_id(category, page_id)
        PageState.select_version(page_version, is_next_version=False)
        self.main_window = MainWindow()
        self.main_window.show()
        self.hide()

    def _simulate_select_first_item(self, text):
        """Simulate selecting a specific item for development purposes"""
        index = self.dropdown_list.findText(text)
        if index >= 0:  # make sure the item was found
            self.dropdown_list.setCurrentIndex(index)
            self._select_button_on_click()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    dropdown_window = LandingPage()
    dropdown_window.show()
    sys.exit(app.exec_())
