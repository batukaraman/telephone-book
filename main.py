import sqlite3
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
import sys


class Main(QWidget):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        self.initUI()
        self.DataBaseCreate()
        self.DataBaseGeneralGet()

    def initUI(self):
        # Başlangıç Ayarları
        self.setFixedSize(400, 550)
        self.setWindowIcon(QtGui.QIcon("assets/icon.ico"))
        self.setWindowTitle("Rehber")

        # Düzenleyiciler
        self.GeneralVerticalLayout = QVBoxLayout()
        self.PageButtonsHorizontalLayout = QHBoxLayout()
        self.AltButtonsHorizontalLayout = QHBoxLayout()

        # Arama
        self.SearchLineEdit = QLineEdit()
        self.SearchLineEdit.setObjectName("search")
        self.SearchLineEdit.setPlaceholderText("Kişi, numara ara...")
        self.GeneralVerticalLayout.addWidget(self.SearchLineEdit)

        # Sayfa Butonları
        self.PersonsPushButton = QPushButton("Kişiler")
        self.PersonsPushButton.clicked.connect(self.PersonsIsHidden)
        self.PageButtonsHorizontalLayout.addWidget(self.PersonsPushButton)
        self.FavoritesPushButton = QPushButton("Favoriler")
        self.FavoritesPushButton.clicked.connect(self.FavIsHidden)
        self.PageButtonsHorizontalLayout.addWidget(self.FavoritesPushButton)
        self.GeneralVerticalLayout.addLayout(self.PageButtonsHorizontalLayout)

        # Kişileri Gösterme Ekranı
        self.PersonsScreenTable = QTableWidget()
        self.PersonsScreenTable.horizontalHeader().setDefaultSectionSize(400)
        self.PersonsScreenTable.verticalHeader().setVisible(False)
        self.PersonsScreenTable.horizontalHeader().setVisible(False)
        self.PersonsScreenTable.setShowGrid(False)
        self.PersonsScreenTable.setFocusPolicy(QtCore.Qt.NoFocus)
        self.PersonsScreenTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.AddPersonScreenPushButton = QPushButton("Kişi Ekle")
        self.AddPersonScreenPushButton.clicked.connect(self.AddScreenIsHidden)
        self.AltButtonsHorizontalLayout.addWidget(self.AddPersonScreenPushButton)

        # Favorileri Gösterme Ekranı
        self.FavScreenTable = QTableWidget()
        self.FavScreenTable.setHidden(True)
        self.FavScreenTable.horizontalHeader().setDefaultSectionSize(400)
        self.FavScreenTable.verticalHeader().setVisible(False)
        self.FavScreenTable.horizontalHeader().setVisible(False)
        self.FavScreenTable.setShowGrid(False)
        self.FavScreenTable.setFocusPolicy(QtCore.Qt.NoFocus)
        self.FavScreenTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Kişi Ekleme Ekranı
        self.AddPersonScreenFormLayout = QFormLayout()
        self.AddPersonScreenGroupBox = QGroupBox()
        self.AddPersonScreenGroupBox.setHidden(True)
        self.AddPersonScreenGroupBox.setLayout(self.AddPersonScreenFormLayout)
        self.NameLineEdit = QLineEdit()
        self.NameLineEdit.setPlaceholderText("Ad")
        self.NumberTypeComboBox = QComboBox()
        self.NumberTypeComboBox.addItems(["Cep", "İş", "Ev"])
        self.NumberLineEdit = QLineEdit()
        self.NumberLineEdit.setPlaceholderText("Telefon Numaras")
        self.MailLineEdit = QLineEdit()
        self.MailLineEdit.setPlaceholderText("E-Posta")
        self.FavCheckBox = QCheckBox("Favorilere Ekle")

        self.AddPersonScreenFormLayout.addRow(self.NameLineEdit)
        self.AddPersonScreenFormLayout.addRow(self.NumberTypeComboBox, self.NumberLineEdit)
        self.AddPersonScreenFormLayout.addRow(self.MailLineEdit)
        self.AddPersonScreenFormLayout.addRow(self.FavCheckBox)

        self.AddPersonPushButton = QPushButton("Ekle")
        self.AddPersonPushButton.setHidden(True)
        self.AddPersonPushButton.clicked.connect(self.DataBaseInsert)
        self.AltButtonsHorizontalLayout.addWidget(self.AddPersonPushButton)

        # Kişi Düzenleme Ekranı
        self.EditPersonScreenFormLayout = QFormLayout()
        self.EditPersonScreenGroupBox = QGroupBox()
        self.EditPersonScreenGroupBox.setHidden(True)
        self.EditPersonScreenGroupBox.setLayout(self.EditPersonScreenFormLayout)

        self.EditNameLineEdit = QLineEdit()
        self.EditNameLineEdit.setPlaceholderText("Ad")
        self.EditNumberTypeComboBox = QComboBox()
        self.EditNumberTypeComboBox.addItems(["Cep", "İş", "Ev"])
        self.EditNumberLineEdit = QLineEdit()
        self.EditNumberLineEdit.setPlaceholderText("Telefon Numarası")
        self.EditMailLineEdit = QLineEdit()
        self.EditMailLineEdit.setPlaceholderText("E-Posta")
        self.EditFavCheckBox = QCheckBox("Favorilere Ekle")

        self.EditPersonScreenFormLayout.addRow(self.EditNameLineEdit)
        self.EditPersonScreenFormLayout.addRow(self.EditNumberTypeComboBox, self.EditNumberLineEdit)
        self.EditPersonScreenFormLayout.addRow(self.EditMailLineEdit)
        self.EditPersonScreenFormLayout.addRow(self.EditFavCheckBox)

        self.EditScreenPushButton = QPushButton("Düzenle")
        self.EditScreenPushButton.clicked.connect(self.PersonsEditIsHidden)
        self.AltButtonsHorizontalLayout.addWidget(self.EditScreenPushButton)

        self.PersonUpdatePushButton = QPushButton("Kaydet")
        self.PersonUpdatePushButton.setHidden(True)
        self.PersonUpdatePushButton.clicked.connect(self.DataBaseUpdate)
        self.AltButtonsHorizontalLayout.addWidget(self.PersonUpdatePushButton)

        self.PersonDeletePushButton = QPushButton("Sil")
        self.PersonDeletePushButton.setHidden(True)
        self.PersonDeletePushButton.clicked.connect(self.DataBaseDelete)
        self.AltButtonsHorizontalLayout.addWidget(self.PersonDeletePushButton)

        # Atamalar
        self.GeneralVerticalLayout.addWidget(self.PersonsScreenTable)
        self.GeneralVerticalLayout.addWidget(self.AddPersonScreenGroupBox)
        self.GeneralVerticalLayout.addWidget(self.FavScreenTable)
        self.GeneralVerticalLayout.addWidget(self.EditPersonScreenGroupBox)
        self.GeneralVerticalLayout.addLayout(self.AltButtonsHorizontalLayout)
        self.setLayout(self.GeneralVerticalLayout)
        self.show()

    def DataBaseCreate(self):
        self.db = sqlite3.connect("Directory.sqlite")
        self.ptr = self.db.cursor()
        self.ptr.execute("CREATE TABLE IF NOT EXISTS directory (ID, Name, NumberType, Number, Mail, Fav)")
        self.ptr.close()
        self.db.commit()
        self.db.close()

    def DataBaseGeneralGet(self):
        self.db = sqlite3.connect("Directory.sqlite")
        self.ptr = self.db.cursor()

        if self.PersonsScreenTable.isHidden():
            self.ptr.execute(
                "SELECT * FROM directory WHERE Name LIKE '%%%s%%%%' AND Fav=1 OR Number LIKE '%%%s%%%%' AND Fav=1" % (
                self.SearchLineEdit.text().lower(), self.SearchLineEdit.text().lower()))

            rows = self.ptr.fetchall()
            self.FavScreenTable.setRowCount(len(rows))
            self.FavScreenTable.setColumnCount(1)

            for row in rows:
                if self.SearchLineEdit.text() in row[1] or self.SearchLineEdit.text() in row[3]:
                    inx = rows.index(row)
                    self.FavScreenTable.setItem(inx, 0, QTableWidgetItem(str(row[1]).capitalize() + " | " + row[3]))

        else:
            self.ptr.execute("SELECT * FROM directory WHERE Name LIKE '%%%s%%%%' OR Number LIKE '%%%s%%%%'" % (self.SearchLineEdit.text().lower(), self.SearchLineEdit.text().lower()))
            rows = self.ptr.fetchall()
            self.PersonsScreenTable.setRowCount(len(rows))
            self.PersonsScreenTable.setColumnCount(1)

            for row in rows:
                if self.SearchLineEdit.text() in row[1] or self.SearchLineEdit.text() in row[3]:
                    inx = rows.index(row)
                    self.PersonsScreenTable.setItem(inx, 0, QTableWidgetItem(str(row[1]).capitalize() + " | " + row[3]))

        self.ptr.close()
        self.db.commit()
        self.db.close()

        QtCore.QTimer.singleShot(100, self.DataBaseGeneralGet)

    def DataBaseInsert(self):
        self.Name = self.NameLineEdit.text().lower()
        self.NumberType = self.NumberTypeComboBox.currentText().lower()
        self.Number = self.NumberLineEdit.text().lower()
        self.Mail = self.MailLineEdit.text().lower()
        self.Fav = self.FavCheckBox.isChecked()

        if not self.NameLineEdit.text() or not self.NumberLineEdit.text():
            QMessageBox.about(self, "Eksik Var", "Gerekli alanlar boş olmamalı!")
            self.NameLineEdit.setText("")
            self.NumberLineEdit.setText("")
            self.MailLineEdit.setText("")
        else:
            self.db = sqlite3.connect("Directory.sqlite")
            self.ptr = self.db.cursor()

            self.ptr.execute("INSERT INTO directory VALUES (?, ?, ?, ?, ?, ?)",
                             (None, self.Name, self.NumberType, self.Number, self.Mail, self.Fav))
            self.ptr.close()
            self.db.commit()
            self.db.close()

            self.NameLineEdit.setText("")
            self.NumberLineEdit.setText("")
            self.MailLineEdit.setText("")

            QMessageBox.about(self, "", "Kişi Eklendi.")

        self.AddPersonScreenGroupBox.setHidden(True)
        self.AddPersonPushButton.setHidden(True)
        self.PersonsScreenTable.setHidden(False)
        self.AddPersonScreenPushButton.setHidden(False)
        self.EditScreenPushButton.setHidden(False)

    def DataBaseDelete(self):
        self.db = sqlite3.connect("Directory.sqlite")
        self.ptr = self.db.cursor()

        self.ptr.execute("SELECT * FROM directory")
        res = self.ptr.fetchall()
        for row in enumerate(res):
            if row[0] == self.PersonsScreenTable.currentRow():
                self.ptr.execute("DELETE FROM directory WHERE ID=?", (row[1][0],))

        self.ptr.close()
        self.db.commit()
        self.db.close()

        self.PersonsIsHidden()

    def DataBaseUpdate(self):
        self.db = sqlite3.connect("Directory.sqlite")
        self.ptr = self.db.cursor()

        self.ptr.execute("SELECT * FROM directory")
        res = self.ptr.fetchall()
        for row in enumerate(res):
            if row[0] == self.PersonsScreenTable.currentRow():
                self.ptr.execute("UPDATE directory SET Name=? WHERE ID=?",
                                 (self.EditNameLineEdit.text().lower(), row[1][0],))
                self.ptr.execute("UPDATE directory SET NumberType=? WHERE ID=?",
                                 (self.EditNumberTypeComboBox.currentText().lower(), row[1][0],))
                self.ptr.execute("UPDATE directory SET Number=? WHERE ID=?",
                                 (self.EditNumberLineEdit.text().lower(), row[1][0],))
                self.ptr.execute("UPDATE directory SET Mail=? WHERE ID=?",
                                 (self.EditMailLineEdit.text().lower(), row[1][0],))
                self.ptr.execute("UPDATE directory SET Fav=? WHERE ID=?",
                                 (self.EditFavCheckBox.isChecked(), row[1][0],))

        self.ptr.close()
        self.db.commit()
        self.db.close()
        self.PersonsIsHidden()

    def PersonsIsHidden(self):
        self.PersonsScreenTable.setHidden(False)

        self.FavScreenTable.setHidden(True)

        self.AddPersonScreenPushButton.setHidden(False)
        self.AddPersonPushButton.setHidden(True)
        self.AddPersonScreenGroupBox.setHidden(True)

        self.EditScreenPushButton.setHidden(False)
        self.EditPersonScreenGroupBox.setHidden(True)

        self.PersonDeletePushButton.setHidden(True)
        self.PersonUpdatePushButton.setHidden(True)

    def FavIsHidden(self):
        self.PersonsScreenTable.setHidden(True)

        self.FavScreenTable.setHidden(False)

        self.AddPersonScreenPushButton.setHidden(True)
        self.AddPersonPushButton.setHidden(True)
        self.AddPersonScreenGroupBox.setHidden(True)

        self.EditScreenPushButton.setHidden(True)
        self.EditPersonScreenGroupBox.setHidden(True)

        self.PersonDeletePushButton.setHidden(True)
        self.PersonUpdatePushButton.setHidden(True)

    def AddScreenIsHidden(self):
        self.PersonsScreenTable.setHidden(True)

        self.FavScreenTable.setHidden(True)

        self.AddPersonScreenPushButton.setHidden(True)
        self.AddPersonPushButton.setHidden(False)
        self.AddPersonScreenGroupBox.setHidden(False)

        self.EditScreenPushButton.setHidden(True)
        self.EditPersonScreenGroupBox.setHidden(True)

        self.PersonDeletePushButton.setHidden(True)
        self.PersonUpdatePushButton.setHidden(True)

    def PersonsEditIsHidden(self):
        self.PersonsScreenTable.setHidden(True)

        self.FavScreenTable.setHidden(True)

        self.AddPersonScreenPushButton.setHidden(True)
        self.AddPersonPushButton.setHidden(True)
        self.AddPersonScreenGroupBox.setHidden(True)

        self.EditScreenPushButton.setHidden(True)
        self.EditPersonScreenGroupBox.setHidden(False)

        self.db = sqlite3.connect("Directory.sqlite")
        self.ptr = self.db.cursor()

        self.ptr.execute("SELECT * FROM directory")
        res = self.ptr.fetchall()
        for row in enumerate(res):
            if row[0] == self.PersonsScreenTable.currentRow():
                self.EditNameLineEdit.setText(row[1][1])
                self.EditNumberLineEdit.setText(row[1][3])
                self.EditMailLineEdit.setText(row[1][4])
                self.EditFavCheckBox.setChecked(row[1][5])

        self.ptr.close()
        self.db.commit()
        self.db.close()

        self.PersonDeletePushButton.setHidden(False)
        self.PersonUpdatePushButton.setHidden(False)


if __name__ == '__main__':
    App = QApplication(sys.argv)
    App.setStyleSheet(open('./style/style.css').read())
    ex = Main()
    sys.exit(App.exec_())
