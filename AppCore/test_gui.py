import sys
from PyQt4 import QtGui

app = QtGui.QApplication(sys.argv)

window = QtGui.QWidget()
window.setGeometry(50, 50, 500, 500)
window.setWindowTitle('PyEVA')
window.setWindowIcon(QtGui.QIcon(r'..\lambda.png'))

window.show()
sys.exit(app.exec_())
