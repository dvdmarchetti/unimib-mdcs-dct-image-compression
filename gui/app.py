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
        self.scaleImage.stateChanged.connect(self.fx_UpdateImageScaling(source=self.scaleImage, targets=[self.originalImage, self.compressedImage]))

        # Bind F slider signals
        self.fSlider.valueChanged.connect(self.fx_UpdateLabel(source=self.fSlider, target=self.fValue))
        self.fSlider.valueChanged.connect(self.fx_UpdateMaxDValue(source=self.fSlider, target=self.dSlider))

        # Bind d slider signals
        self.dSlider.valueChanged.connect(self.fx_UpdateLabel(source=self.dSlider, target=self.dValue))

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
        pixels = pixels[:, :, 0]

        F = self.fSlider.value()
        d = self.dSlider.value()

        height_blocks_count = int(height / F)
        width_blocks_count = int(width / F)

        for r in range(height_blocks_count):
            for c in range(width_blocks_count):
                block = pixels[r*F : (r+1)*F, c*F : (c+1)*F]
                block = dctn(block, norm='ortho')

                for k in range(F):
                    for l in range(F):
                        if k + l >= d:
                            block[k,l] = 0

                pixels[r*F : (r+1)*F, c*F : (c+1)*F] = idctn(block, norm='ortho')

        for r in range(height_blocks_count*F):
            for c in range(width_blocks_count*F):
                if pixels[r,c] > 255:
                    pixels[r,c] = 255
                elif pixels[r,c] < 0:
                    pixels[r,c] = 0

        target = QImage(bytes(pixels), pixels.shape[1], pixels.shape[0], int(pixels.nbytes/height), QImage.Format_Grayscale8)
        self.compressedImage.setPixmap(QPixmap.fromImage(target))

    def fx_UpdateImageScaling(self, source=None, targets=[]):
        return lambda: [target.setShouldScale(source.isChecked()) for target in targets]

    def fx_UpdateLabel(self, source=None, target=None):
        return lambda: target.setText(str(source.value()))

    def fx_UpdateMaxDValue(self, source=None, target=None):
        return lambda: (
            source.value() == 1 and target.setValue(0),
            source.value() > 1 and target.setMaximum(2*source.value() - 2),
            source.value() > 1 and target.setTickInterval((2*source.value() - 2) / 10),
            target.setEnabled(True if source.value() > 1 else False)
        )


app = QApplication(sys.argv)
window = App()
sys.exit(app.exec_())
