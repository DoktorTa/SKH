import sys
import webbrowser

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QMessageBox, QDesktopWidget, QAction, qApp,\
    QMainWindow, QTextEdit, QFileDialog, QLabel, QVBoxLayout, QTabWidget
from PyQt5.QtGui import QIcon, QFont

from MyTab import MyTabWidget



class Hex_view(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Этот статический метод устанавливает шрифт, используемый для показа всплывающих подсказок.
        # Мы используем шрифт 10px SansSerif.
        QToolTip.setFont(QFont('SansSerif', 10))

        # Чтобы создать подсказку, мы вызываем метод setTooltip(). Мы можем использовать HTML форматирование текста.
        self.setToolTip('This is a <b>QWidget</b> widget')

        # Мы создаём виджет кнопки и устанавливаем всплывающую подсказку для неё.
        #btn = QPushButton('Button', self)
        #btn.setToolTip('This is a <b>QPushButton</b> widget')
        # Меняем размер у кнопки, перемещаем её в окно. Метод sizeHint() даёт рекомендуемый размер для кнопки.
        #btn.resize(btn.sizeHint())
        #btn.move(70, 70)
        # self.widget_on_win()

        self.test()

        self.menu_bar_init()

        self.resize(1080, 720)
        self.center()
        self.setWindowTitle('Tooltips')
        self.show()

    def test(self):
        self.tab_widget = MyTabWidget(self)
        self.setCentralWidget(self.tab_widget)

    def file_serch(self):
        file_name = QFileDialog.getOpenFileName(self, "Open files", "/home/jana")
        # Функция открытия файла необходимо сообственно открытие файла.

    # Любые события должны быть созданы и зарегестрированны в меню бар.
    def menu_bar_init(self):
        exit_action = QAction('&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.close)

        open_file_action = QAction('&Open', self)
        open_file_action.setShortcut('Ctrl+O')
        open_file_action.setStatusTip('Open new file')
        open_file_action.triggered.connect(self.file_serch)
        # self.statusBar()
        help_action = QAction('&Git progect', self)
        help_action.setShortcut('Ctrl+H')
        help_action.setStatusTip('Open git this progect')
        help_action.triggered.connect(lambda: webbrowser.open('https://github.com/DoktorTa/SKH'))

        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(open_file_action)
        file_menu.addAction(exit_action)

        help_menu = menu_bar.addMenu('&Help')
        help_menu.addAction(help_action)

    # Диологовое окно перед выходом.
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Exit', "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # Центрирование окна приложения, стоит убрать, ибо зачем?
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Hex_view()
    sys.exit(app.exec_())
