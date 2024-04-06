import sys
import os

from bookkeeper.view import model_to_view
from PySide6.QtWidgets import QApplication
if os.path.isfile('lovely.db'):
    os.remove('lovely.db')

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.sqlite_repository import SQLiteRepository
import bookkeeper.repository.database_create

cat_repo = SQLiteRepository('lovely.db', Category)
exp_repo = SQLiteRepository('lovely.db', Expense)

app = QApplication([])
win1 = model_to_view.MainWindow()
win1.cat_repo = cat_repo
win1.exp_repo = exp_repo
win1.show()


sys.exit(app.exec())