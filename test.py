import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QLineEdit, QAction, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://www.google.com"))

        self.setCentralWidget(self.browser)

        # Navigation Bar
        navbar = QToolBar()
        self.addToolBar(navbar)

        # Back Button
        back_btn = QAction('Back', self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        # Forward Button
        forward_btn = QAction('Forward', self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        # Reload Button
        reload_btn = QAction('Reload', self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        # Address Bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        navbar.addWidget(self.url_bar)

        # Home Button
        home_btn = QAction('Home', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(navbar)
        layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        # Set up initial window properties
        self.setWindowTitle("Python Browser")
        self.showMaximized()

    def navigate_home(self):
        self.browser.setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):
        q = QUrl(self.url_bar.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.browser.setUrl(q)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    sys.exit(app.exec_())