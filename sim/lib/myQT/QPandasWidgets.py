import pandas as pd
from PySide6.QtWidgets import QTableView, QApplication, QHeaderView, QStyleOptionHeader, QStyle
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex, QRect, QSize
import sys, datetime

stylesheet = '''
QHeaderView::section {
	background-color: rgb(205, 205, 205);
    border: 0px transparent;
	font-weight: bold;
}

QTableView::item {
	border-top: 0px transparent;
	border-bottom: 0px transparent;
}

QTableView:item:selected {
	background-color: #007ac9; 
	color: #FFFFFF;
}

QHeaderView {
    qproperty-defaultAlignment: AlignHCenter AlignVCenter;
}
'''

class WrapHeader(QHeaderView):
    def sectionSizeFromContents(self, logicalIndex):
        # get the size returned by the default implementation
        size = super().sectionSizeFromContents(logicalIndex)
        if self.model():
            if size.width() > self.sectionSize(logicalIndex):
                text = self.model().headerData(logicalIndex, 
                    self.orientation(), Qt.DisplayRole)
                if not text:
                    return size
                # in case the display role is numeric (for example, when header 
                # labels are not defined yet), convert it to a string; 
                text = str(text)

                option = QStyleOptionHeader()
                self.initStyleOption(option)
                alignment = self.model().headerData(logicalIndex, 
                    self.orientation(), Qt.TextAlignmentRole)
                if alignment is None:
                    alignment = option.textAlignment

                # get the default style margin for header text and create a 
                # possible rectangle using the current section size, then use
                # QFontMetrics to get the required rectangle for the wrapped text
                margin = self.style().pixelMetric(
                    QStyle.PM_HeaderMargin, option, self)
                maxWidth = self.sectionSize(logicalIndex) - margin * 2
                rect = option.fontMetrics.boundingRect(
                    QRect(0, 0, maxWidth, 10000), 
                    alignment | Qt.TextWordWrap, 
                    text)

                # add vertical margins to the resulting height
                height = rect.height() + margin * 2
                if height >= size.height():
                    # if the height is bigger than the one provided by the base
                    # implementation, return a new size based on the text rect
                    return QSize(rect.width(), height)
        return size

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
        
        elif role == Qt.TextAlignmentRole:
            return int(Qt.AlignCenter)

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

        elif role == Qt.TextAlignmentRole:
            return int(Qt.AlignCenter | Qt.TextWordWrap)

        return None

class QPandasModelEdit(QPandasModel):

    def setData(self, index: QModelIndex, value, role=Qt.ItemDataRole):
        """Override method from QAbstractTableModel

        Set data cell from the pandas DataFrame
        """
        if role == Qt.EditRole:
            try:  
                if isinstance(value, str):
                    value = float(value.replace(',', '.'))
                self._dataframe.iloc[index.row(), index.column()] = value
                self.dataChanged.emit(index, index)
                return True
            except: 
                pass
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
                   'c': ['a', 'b', 'c'],
                   'test test test test test': ['test test test test test', '', '']})

    view = QTableView()
    view.resize(400, 500)
    view.setHorizontalHeader(WrapHeader(Qt.Horizontal, view))
    view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    view.setAlternatingRowColors(True)
    view.setSelectionBehavior(QTableView.SelectRows)
    view.show()
    view.setStyleSheet(stylesheet)

    model = QPandasModelEdit(df)
    model.dataChanged.connect(test)
    view.setModel(model)

    app.exec()