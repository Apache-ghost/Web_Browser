import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QToolBar,
    QLineEdit,
    QAction,
    QVBoxLayout,
    QWidget,
    QTabWidget,
    QSizePolicy,
    QCompleter,
    QColorDialog,
)
from PyQt5.QtWebEngineWidgets import QWebEngineView


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.setDocumentMode(True)
        self.tabs.setMovable(True)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.tabs)
        self.central_widget.setLayout(self.layout)

        self.add_new_tab()

        # Navigation Bar
        navbar = QToolBar()
        self.addToolBar(navbar)

        # Back Button
        back_btn = QAction(QIcon("icons/back.png"), "Back", self)
        back_btn.triggered.connect(lambda: self.current_tab().back())
        navbar.addAction(back_btn)

        # Forward Button
        forward_btn = QAction(QIcon("icons/forward.png"), "Forward", self)
        forward_btn.triggered.connect(lambda: self.current_tab().forward())
        navbar.addAction(forward_btn)

        # Reload Button
        reload_btn = QAction(QIcon("icons/reload.png"), "Reload", self)
        reload_btn.triggered.connect(lambda: self.current_tab().reload())
        navbar.addAction(reload_btn)

        # Home Button
        home_btn = QAction(QIcon("icons/home.png"), "Home", self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        # New Tab Button
        new_tab_btn = QAction(QIcon("icons/new_tab.png"), "New Tab", self)
        new_tab_btn.triggered.connect(self.add_new_tab)
        navbar.addAction(new_tab_btn)

        # Address Bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        completer = QCompleter(["http://", "https://"])
        self.url_bar.setCompleter(completer)
        navbar.addWidget(self.url_bar)

        # Search Engine Dropdown
        search_engine = QCompleter(["https://www.google.com/search?q={}", "https://www.bing.com/search?q={}"])
        self.url_bar.setCompleter(search_engine)

        # Set up initial window properties
        self.setWindowTitle("Python Browser")
        self.setGeometry(100, 100, 1024, 768)
        self.show()

    def current_tab(self):
        return self.tabs.currentWidget()

    def add_new_tab(self, url=None):
        browser = QWebEngineView()
        browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        if url:
            browser.setUrl(QUrl(url))

        tab_index = self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentIndex(tab_index)

        # Update address bar and title when the page changes
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))
        browser.loadFinished.connect(lambda _, browser=browser: self.update_title(browser))

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            self.close()

    def navigate_home(self):
        self.current_tab().setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):
        q = QUrl(self.url_bar.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.current_tab().setUrl(q)

    def update_title(self, browser):
        title = browser.page().title()
        index = self.tabs.indexOf(browser)
        self.tabs.setTabText(index, title)

    def update_urlbar(self, q, browser=None):
        if browser != self.current_tab():
            return

        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)

    def mousePressEvent(self, event):
        if event.button() == 4:  # Middle mouse button
            self.add_new_tab()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    sys.exit(app.exec_())
