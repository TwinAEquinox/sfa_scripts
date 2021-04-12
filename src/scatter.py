import logging

from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import pymel.core as pmc
from pymel.core.system import Path

log = logging.getLogger(__name__)


def maya_main_window():
    """Return the maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class ScatterUI(QtWidgets.QDialog):

    def __init__(self):
        super(ScatterUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Scatter Tool")
        self.setFixedWidth(600)
        self.setFixedHeight(850)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.scat_ui()
        self.connections()
        self.scatterobject = ScatterObject()

    def scat_ui(self):
        self.title_lbl = QtWidgets.QLabel("Scatter Tool")
        self.title_lbl.setStyleSheet("font: bold 20px")
        layout = self.layouts()
        layout.addWidget(self.title_lbl)
        layout.addLayout(self.scatter_field_lay)
        layout.addLayout(self.xrot_rand_lay)
        layout.addLayout(self.yrot_rand_lay)
        layout.addLayout(self.zrot_rand_lay)
        layout.addLayout(self.xscale_rand_lay)
        layout.addLayout(self.yscale_rand_lay)
        layout.addLayout(self.zscale_rand_lay)
        layout.addLayout(self.bottom_button_rand_lay)
        return layout

    def layouts(self):
        main_lay = QtWidgets.QVBoxLayout()
        self.ui_start()
        self.xrot_rand_lay.setRowMinimumHeight(0, 20)
        self.xrot_rand_lay.setRowMinimumHeight(1, 20)
        self.yrot_rand_lay.setRowMinimumHeight(0, 20)
        self.zrot_rand_lay.setRowMinimumHeight(0, 20)
        self.xscale_rand_lay.setRowMinimumHeight(0, 40)
        self.yscale_rand_lay.setRowMinimumHeight(0, 20)
        self.zscale_rand_lay.setRowMinimumHeight(0, 20)
        self.bottom_button_rand_lay.setRowMinimumHeight(0, 20)
        self.setLayout(main_lay)
        return main_lay

    def ui_start(self):
        self.scatter_field_lay = self.scatter_field_ui()
        self.xrot_rand_lay = self.xrot_ui()
        self.yrot_rand_lay = self.yrot_ui()
        self.zrot_rand_lay = self.zrot_ui()
        self.xscale_rand_lay = self.xscale_ui()
        self.yscale_rand_lay = self.yscale_ui()
        self.zscale_rand_lay = self.zscale_ui()
        self.bottom_button_rand_lay = self.scatter_button()

    def scatter_field_ui(self):
        layout = self.scatter_titles()
        self.scatter_obj = QtWidgets.QLineEdit()
        self.scatter_obj_pb = QtWidgets.QPushButton("Select")
        self.scatter_obj_pb.setFixedWidth(50)
        self.scatter_targ = QtWidgets.QLineEdit()
        self.scatter_targ_pb = QtWidgets.QPushButton("Select")
        self.scatter_targ_pb.setFixedWidth(50)
        layout.addWidget(self.scatter_obj, 3, 0)
        layout.addWidget(self.scatter_obj_pb, 1, 2)
        layout.addWidget(self.scatter_targ, 3, 3)
        layout.addWidget(self.scatter_targ_pb, 1, 4)
        return layout

    def xrot_ui(self):
        layout = QtWidgets.QGridLayout()
        self.x_min_lbl = QtWidgets.QLabel("X Rotation Min")
        self.x_max_lbl = QtWidgets.QLabel("X Rotation Max")
        self.xrot_spinbox()
        layout.addWidget(self.x_min_lbl, 7, 0)
        layout.addWidget(self.xrot_min, 8, 0)
        layout.addWidget(self.x_max_lbl, 9, 0)
        layout.addWidget(self.xrot_max, 10, 0)
        return layout

    def yrot_ui(self):
        layout = QtWidgets.QGridLayout()
        self.y_min_lbl = QtWidgets.QLabel("Y Rotation Min")
        self.y_max_lbl = QtWidgets.QLabel("Y Rotation Max")
        self.yrot_spinbox()
        layout.addWidget(self.y_min_lbl, 9, 0)
        layout.addWidget(self.yrot_min, 10, 0)
        layout.addWidget(self.y_max_lbl, 11, 0)
        layout.addWidget(self.yrot_max, 12, 0)
        return layout

    def zrot_ui(self):
        layout = QtWidgets.QGridLayout()
        self.z_min_lbl = QtWidgets.QLabel("Z Rotation Min")
        self.z_max_lbl = QtWidgets.QLabel("Z Rotation Max")
        self.zrot_spinbox()
        layout.addWidget(self.z_min_lbl, 11, 0)
        layout.addWidget(self.zrot_min, 12, 0)
        layout.addWidget(self.z_max_lbl, 13, 0)
        layout.addWidget(self.zrot_max, 14, 0)
        return layout

    def xrot_spinbox(self):
        self.xrot_min = QtWidgets.QSpinBox()
        self.xrot_min.setMinimum(0)
        self.xrot_min.setMaximum(360)
        self.xrot_min.setMinimumWidth(100)
        self.xrot_min.setSingleStep(10)
        self.xrot_max = QtWidgets.QSpinBox()
        self.xrot_max.setMinimum(0)
        self.xrot_max.setMaximum(360)
        self.xrot_max.setValue(360)
        self.xrot_max.setMinimumWidth(100)
        self.xrot_max.setSingleStep(10)

    def yrot_spinbox(self):
        self.yrot_min = QtWidgets.QSpinBox()
        self.yrot_min.setMinimum(0)
        self.yrot_min.setMaximum(360)
        self.yrot_min.setMinimumWidth(100)
        self.yrot_min.setSingleStep(10)
        self.yrot_max = QtWidgets.QSpinBox()
        self.yrot_max.setMinimum(0)
        self.yrot_max.setMaximum(360)
        self.yrot_max.setValue(360)
        self.yrot_max.setMinimumWidth(100)
        self.yrot_max.setSingleStep(10)

    def zrot_spinbox(self):
        self.zrot_min = QtWidgets.QSpinBox()
        self.zrot_min.setMinimum(0)
        self.zrot_min.setMaximum(360)
        self.zrot_min.setMinimumWidth(100)
        self.zrot_min.setSingleStep(10)
        self.zrot_max = QtWidgets.QSpinBox()
        self.zrot_max.setMinimum(0)
        self.zrot_max.setMaximum(360)
        self.zrot_max.setValue(360)
        self.zrot_max.setMinimumWidth(100)
        self.zrot_max.setSingleStep(10)