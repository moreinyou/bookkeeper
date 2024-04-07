from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QHeaderView,
    QTableWidgetItem,
    QLineEdit,
    QGridLayout,
    QComboBox,
    QPushButton,
    QDialog,
    QDialogButtonBox,
    QMessageBox
)

from datetime import datetime, time
from PySide6.QtGui import QIntValidator
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
from bookkeeper.utils import read_tree,listT2list, get_cat_name_pk


class TextInputDialog(QDialog):
    def __init__(self, parent=None):
        super(TextInputDialog, self).__init__(parent)

        self.setWindowTitle('Введите название категории')
        self.layout = QVBoxLayout(self)
        self.text_input = QLineEdit(self)
        self.layout.addWidget(self.text_input)

        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        self.layout.addWidget(btn_box)

    def get_text(self):
        return self.text_input.text()

# class Oshibka(QMessageBox):
#     def __init__(self):
#         super().__init__()
#
#         self.setWindowTitle('Сообщение об ошибке!')
#         self.layout = QVBoxLayout(self)
#         self.layout.addWidget(QLabel('Некорректный формат даты'))


class MainWindow(QMainWindow):
    def __init__(self, ):
        super().__init__()
        self.setWindowTitle("Личная бухгалтерия")
        self.resize(700, 650)

        self.exp_repo = None
        self.cat_repo = None
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout(self.central_widget)

        with open(r'D:\PycharmProjects\практика\app\bookkeeper\style.qss', 'r') as f:
            self.setStyleSheet(f.read())
    #def table1(self):
        self.layout.addWidget(QLabel('Последние расходы'))
        self.table_widget = QTableWidget(50, 5)
        self.table_widget.setColumnHidden(4,True)
        self.table_widget.setHorizontalHeaderLabels("Сумма, Категория, Дата покупки, Комментарий".split(','))
        self.table_widget.cellChanged.connect(self.cell_changed)
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        self.layout.addWidget(self.table_widget, 0, 0, 1, 2)


    #def table2(self):
        self.layout.addWidget(QLabel("Бюджет"))
        self.table_widget2 = QTableWidget(3, 3)
        self.table_widget2.setHorizontalHeaderLabels("Период Сумма Бюджет".split())
        header2 = self.table_widget2.horizontalHeader()
        header2.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header2.setSectionResizeMode(1, QHeaderView.Stretch)
        header2.setSectionResizeMode(2, QHeaderView.Stretch)
        self.layout.addWidget(self.table_widget2, 1, 0, 1, 2)

    # def input_stroka(self):
        self.layout.addWidget(QLabel('Сумма'), 2, 0)
        self.line_edit = QLineEdit(placeholderText="0")
        self.int_validator = QIntValidator()
        self.line_edit.setValidator(self.int_validator)
        self.layout.addWidget(self.line_edit, 3, 0)

        self.layout.addWidget(QLabel('Дата покупки: (ГГГГ-ММ-ДД)'), 2, 1)
        self.line_edit3 = QLineEdit(placeholderText="Поумолчанию сегодняшняя дата")
        self.layout.addWidget(self.line_edit3, 3, 1)

        self.layout.addWidget(QLabel('Комментарий'), 4, 0)
        self.line_edit2 = QLineEdit(placeholderText="Не обязательно...")
        self.layout.addWidget(self.line_edit2, 5, 0, 1, 2)

    #def ui(self):
        self.label = QLabel('Выберете категорию')
        self.layout.addWidget(self.label, 6, 0)
        self.combo_box = QComboBox()
        self.layout.addWidget(self.combo_box, 7, 0, 1, 3)
        self.setLayout(self.layout)

    #def btns(self):
        self.btn_add = QPushButton("Добавить в рассходы")
        self.btn_add.clicked.connect(self.add_exp)
        self.layout.addWidget(self.btn_add, 8, 0)

        self.btn_exp_remove = QPushButton("Удалить из расходов")
        self.btn_exp_remove.clicked.connect(self.remove_exp)
        self.layout.addWidget(self.btn_exp_remove, 8, 1)

        self.btn_cat = QPushButton("Добавить новую категорию")
        self.btn_cat.clicked.connect(self.add_cat)
        self.layout.addWidget(self.btn_cat, 9, 0)

        self.btn_cat_remove = QPushButton("Удалить категорию из списка")
        self.btn_cat_remove.clicked.connect(self.remove_cat)
        self.layout.addWidget(self.btn_cat_remove, 9, 1)

        self.add_budget = QPushButton("Установить бюджет")
        self.add_budget.clicked.connect(self.add_bud)
        self.layout.addWidget(self.add_budget, 10, 0, 1, 3)

    def remove_cat(self):
        if self.combo_box.currentText() != '':
            category_pk = int(self.combo_box.currentText().split('.')[0])
            obj = self.cat_repo.get(category_pk)
            raskh_obj = self.exp_repo.get_all({'category': obj.pk})
            self.cat_repo.delete(obj)
            for raskhod in raskh_obj:
                self.exp_repo.delete(raskhod)
            self.update_cat_list()
            self.update_table()

    def add_bud(self):
        pass

    def cell_changed(self, row, column):
        if self.table_widget.currentRow() >= 0:
            obj_data = [self.table_widget.item(self.table_widget.currentRow(),column).text() \
                        for column in range(self.table_widget.columnCount())]
            if self.cat_repo.get_all({'name': obj_data[1]}) != [] and \
                   obj_data[0].isdigit():
                obj_data[1] = self.cat_repo.get_all({'name': obj_data[1]})[0].pk
                obj_data[4] = int(obj_data[4])
                obj = Expense(*obj_data)
                self.exp_repo.update(obj)
            self.update_table()



    def remove_exp(self):
        category_pk_column = 4
        if self.table_widget.currentRow() >= 0:
            pk = self.table_widget.item(self.table_widget.currentRow(),category_pk_column).text()
            self.exp_repo.delete(self.exp_repo.get(int(pk)))
            self.update_table()



    def add_exp(self,exp_repo):
        if self.combo_box.currentText() != '' and self.line_edit.text() != '':
            amount = int(self.line_edit.text())
            comment = self.line_edit2.text()
            if self.line_edit3.text() !='':
                try:
                    date = datetime.strptime(self.line_edit3.text(),'%Y-%m-%d').date()
                    if self.combo_box.currentText() != '':
                        category_pk = int(self.combo_box.currentText().split('.')[0])
                        self.exp_repo.add(Expense(amount, category_pk,date, comment=comment))
                        self.update_table()
                except (ValueError):
                    QMessageBox.critical(self, "ValueError", "Некорректный формат даты", QMessageBox.Ok)
            else:
                if self.combo_box.currentText() != '':
                    category_pk = int(self.combo_box.currentText().split('.')[0])
                    self.exp_repo.add(Expense(amount, category_pk, comment = comment))
                    self.update_table()
            self.line_edit3.clear()
            self.line_edit.clear()

    def add_cat(self):
        text_dialog = TextInputDialog(self)
        result = text_dialog.exec_()
        if result == QDialog.Accepted:
            entered_text = text_dialog.get_text()
            self.cat_repo.add(Category(name = entered_text))
            self.update_cat_list()

    def add_all_cat(self,cat_names_list: list[str]):
        self.combo_box.addItems(cat_names_list)

    def update_cat_list(self):
        self.combo_box.clear()
        if self.cat_repo.get_all() != []:
            self.combo_box.addItems(['. '.join([cat_n[2],cat_n[0]]) for cat_n in listT2list(self.cat_repo.get_all())])

    def update_table(self):
        self.table_widget.clearContents()
        if self.exp_repo.get_all() != []:
            data = listT2list(self.exp_repo.get_all())
            data = get_cat_name_pk(data, self.cat_repo)
            self.set_data(self.table_widget,data)

    def set_data(self, table_widget, data: list[list[str]]):
        self.table_widget.setRowCount(len(data))
        for i, row in enumerate(data):
            for j, x in enumerate(row):
             self.table_widget.setItem(i, j, QTableWidgetItem(str(x)))



def date_withouttime():
    current_day = datetime.date(datetime.combine(datetime.now(), time.min))
    return current_day