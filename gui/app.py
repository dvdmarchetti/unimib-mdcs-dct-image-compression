import sys


import numpy as np
from PyQt5 import uic
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from scipy.fftpack import dctn, idctn


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        uic.loadUi('ui/application.ui', self)

        self.connectSignals()
        self.show()

    def connectSignals(self):
        # Bind openFile push button signals
        self.openFile.clicked.connect(self.ask_image)

        # Bind scaleImage checkbox signals
        self.scaleImage.stateChanged.connect(self.updateImageScaling)

        # Bind F slider signals
        self.fSlider.valueChanged.connect(self.updateFLabel)
        self.fSlider.valueChanged.connect(self.updateMaxDValue)

        # Bind d slider signals
        self.dSlider.valueChanged.connect(self.updateDLabel)

        # Bind applyButton signals
        self.applyButton.clicked.connect(self.compress_image)

    def ask_image(self):
        inputImage = QFileDialog.getOpenFileName(self, 'Open file...', '.', 'Bitmap files (*.bmp)')

        if inputImage[0]:
            pixmap = QPixmap(inputImage[0])

            if not pixmap.toImage().isGrayscale():
                errorBox = QMessageBox()
                errorBox.setWindowTitle("Unsupported file Type")
                errorBox.setText("The input file must be a greyscale bitmap")
                errorBox.setIcon(QMessageBox.Critical)

                errorBox.exec_()
                return

            # Remove text placeholders and display image
            self.originalImage.setText('')
            self.compressedImage.setText('')
            self.originalImage.setPixmap(pixmap)
            self.compressedImage.setPixmap(None)

            limit = min(pixmap.width(), pixmap.height())
            self.fSlider.setMaximum(limit)
            self.fSlider.setEnabled(True)
            self.fSlider.setTickInterval(limit / 10)

    def compress_image(self):
        source = self.originalImage.pixmap.toImage()
        width, height = [source.width(), source.height()]

        # bits() -> deep copy // constBits() -> references
        values = source.constBits()
        values.setsize(height * width * 4)

        pixels = np.frombuffer(values, np.uint8).reshape((height, width, 4)).copy()
        pixels = pixels[:, :, 0].astype(np.float)

        F = self.fSlider.value()
        d = self.dSlider.value()

        height_blocks_count = int(height / F)
        width_blocks_count = int(width / F)

        for r in range(height_blocks_count):
            for c in range(width_blocks_count):
                block = dctn(pixels[r*F : (r+1)*F, c*F : (c+1)*F], norm='ortho')

                for k in range(F):
                    for l in range(F):
                        if k + l >= d:
                            block[k,l] = 0

                pixels[r*F : (r+1)*F, c*F : (c+1)*F] = idctn(block, norm='ortho')

        pixels = pixels.clip(0, 255).round().astype(np.uint8)

        target = QImage(bytes(pixels), pixels.shape[1], pixels.shape[0], int(pixels.nbytes/height), QImage.Format_Grayscale8)
        self.compressedImage.setPixmap(QPixmap.fromImage(target))

    def updateImageScaling(self):
        for target in [self.originalImage, self.compressedImage]:
            target.setShouldScale(self.scaleImage.isChecked())

    def updateFLabel(self):
        self.fValue.setText(str(self.fSlider.value()))

    def updateDLabel(self):
        self.dValue.setText(str(self.dSlider.value()))

    def updateMaxDValue(self):
        if self.fSlider.value() == 1:
            self.dSlider.setValue(0)
            self.dSlider.setEnabled(False)
            return

        limit = 2*self.fSlider.value() - 2

        self.dSlider.setMaximum(limit)
        self.dSlider.setTickInterval(limit / 10)
        self.dSlider.setEnabled(True)

app = QApplication(sys.argv)
window = App()
sys.exit(app.exec_())
