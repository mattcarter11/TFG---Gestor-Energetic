import pandas as pd
from PySide6.QtWidgets import QTableView, QApplication
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex
import sys, datetime

class QPandasModel(QAbstractTableModel):
    """A model to interface a Qt view with pandas dataframe """

    def __init__(self, dataframe: pd.DataFrame, precision = 3, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._dataframe = dataframe
        self.precision = precision

    def rowCount(self, parent=QModelIndex()) -> int:
        """ Override method from QAbstractTableModel

        Return row count of the pandas DataFrame
        """
        if parent == QModelIndex():
            return len(self._dataframe)

        return 0

    def columnCount(self, parent=QModelIndex()) -> int:
        """Override method from QAbstractTableModel

        Return column count of the pandas DataFrame
        """
        if parent == QModelIndex():
            return len(self._dataframe.columns)
        return 0

    def data(self, index: QModelIndex, role=Qt.ItemDataRole):
        """Override method from QAbstractTableModel

        Return data cell from the pandas DataFrame
        """
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            data = self._dataframe.iloc[index.row(), index.column()]
            if isinstance(data, float):
                if data == 0:
                    return '0'
                return f'{data:.{self.precision}f}'
            if isinstance(data, datetime.datetime):
                return data.strftime('%Y/%d/%m %H:%M:%S')
            return str(data)

        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole):
        """Override method from QAbstractTableModel

        Return dataframe index as vertical header data and columns as horizontal header data.
        """
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._dataframe.columns[section])
            if orientation == Qt.Vertical:
                return str(self._dataframe.index[section])
        return None

class QPandasModelEdit(QPandasModel):

    def setData(self, index: QModelIndex, value, role=Qt.ItemDataRole):
        """Override method from QAbstractTableModel

        Set data cell from the pandas DataFrame
        """
        if role == Qt.EditRole:
            self._dataframe.iloc[index.row(), index.column()] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index):
        """Override method from QAbstractTableModel"""
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

def test(*args):
    print(args)

if __name__ == "__main__":

    app = QApplication(sys.argv)

    df = pd.DataFrame({'a': ['Mary', 'Jim', 'John'],
                   'b': [100, -3, 0.1234],
                   'c': ['a', 'b', 'c']})

    view = QTableView()
    view.resize(800, 500)
    view.horizontalHeader().setStretchLastSection(True)
    view.setAlternatingRowColors(True)
    view.setSelectionBehavior(QTableView.SelectRows)
    view.show()

    model = QPandasModelEdit(df)
    model.dataChanged.connect(test)
    view.setModel(model)

    app.exec()