import sys
import os

from bookkeeper.repository import database_create
from bookkeeper.view import model_to_view
from PySide6.QtWidgets import QApplication

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget
from bookkeeper.repository.sqlite_repository import SQLiteRepository
import bookkeeper.repository.database_create

db_dir = 'lovely.db'
if not os.path.isfile(db_dir):
    database_create.create_db(db_dir)
cat_repo = SQLiteRepository(db_dir, Category)
exp_repo = SQLiteRepository(db_dir, Expense)
bud_repo = SQLiteRepository(db_dir, Budget)

app = QApplication([])
win1 = model_to_view.MainWindow()
win1.cat_repo = cat_repo
win1.exp_repo = exp_repo
win1.bud_repo = bud_repo
win1.update_table()
win1.update_bud_table()
win1.update_cat_list()
win1.show()


sys.exit(app.exec())