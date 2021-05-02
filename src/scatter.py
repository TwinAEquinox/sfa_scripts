import logging
import random

from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds

log = logging.getLogger(__name__)


def maya_main_window():
    """Return the maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class ScatterUI(QtWidgets.QDialog):
    """Scatter Tool UI Class"""

    def __init__(self):
        super(ScatterUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Scatter Tool")
        self.setFixedWidth(700)
        self.setFixedHeight(900)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.scat_ui()
        self.connections()
        self.scatterobject = ScatterObject()

    def scat_ui(self):
        self.title = QtWidgets.QLabel("Scatter Tool")
        self.title.setStyleSheet("font: bold 25px")
        layout = self.layouts()
        layout.addWidget(self.title)
        layout.addLayout(self.scatter_lay)
        layout.addLayout(self.align_to_normals_lay)
        layout.addLayout(self.xrot_rand_lay)
        layout.addLayout(self.yrot_rand_lay)
        layout.addLayout(self.zrot_rand_lay)
        layout.addLayout(self.xscale_rand_lay)
        layout.addLayout(self.yscale_rand_lay)
        layout.addLayout(self.zscale_rand_lay)
        layout.addLayout(self.selected_vert_perc_rand_lay)
        layout.addStretch()
        layout.addLayout(self.bottom_button_rand_lay)
        return layout

    def layouts(self):
        main_lay = QtWidgets.QVBoxLayout()
        self.ui_start()
        self.xrot_rand_lay.setRowMinimumHeight(0, 20)
        self.xrot_rand_lay.setRowMinimumHeight(0, 20)
        self.yrot_rand_lay.setRowMinimumHeight(0, 20)
        self.zrot_rand_lay.setRowMinimumHeight(0, 20)
        self.xscale_rand_lay.setRowMinimumHeight(0, 40)
        self.yscale_rand_lay.setRowMinimumHeight(0, 20)
        self.zscale_rand_lay.setRowMinimumHeight(0, 20)
        self.bottom_button_rand_lay.setRowMinimumHeight(0, 20)
        self.selected_vert_perc_rand_lay.setRowMinimumHeight(0, 20)
        self.setLayout(main_lay)
        return main_lay

    def ui_start(self):
        self.scatter_lay = self._scat_field_ui()
        self.align_to_normals_lay = self._align_to_normals_ui()
        self.xrot_rand_lay = self._xrot_ui()
        self.yrot_rand_lay = self._yrot_ui()
        self.zrot_rand_lay = self._zrot_ui()
        self.xscale_rand_lay = self._xscale_ui()
        self.yscale_rand_lay = self._yscale_ui()
        self.zscale_rand_lay = self._zscale_ui()
        self.selected_vert_perc_rand_lay = \
            self._vert_percent_offset_ui()
        self.bottom_button_rand_lay = self._scat_button_ui()

    def connections(self):
        """Connects Signals and Slots"""
        self.scatter_btn.clicked.connect(self._scat_click)
        self.scatter_obj_pb.clicked.connect(self._source_object_click)
        self.scatter_targ_pb.clicked.connect(self._dest_object_click)
        self.align_to_normals.clicked.connect(self._align_to_normals_click)

    @QtCore.Slot()
    def _source_object_click(self):
        self._select_source_object()

    @QtCore.Slot()
    def _dest_object_click(self):
        self._select_dest_object()

    @QtCore.Slot()
    def _align_to_normals_click(self):
        self._align_to_normals_check()

    @QtCore.Slot()
    def _scat_click(self):
        self._user_input_values()
        self.scatterobject.scat_align_check()

    def _scat_field_ui(self):
        layout = self._object_titles()
        self.scatter_obj = QtWidgets.QLineEdit()
        self.scatter_obj_pb = QtWidgets.QPushButton("Select Object")
        self.scatter_obj_pb.setFixedWidth(100)
        self.scatter_targ = QtWidgets.QLineEdit()
        self.scatter_targ_pb = QtWidgets.QPushButton("Select Object")
        self.scatter_targ_pb.setFixedWidth(100)
        layout.addWidget(self.scatter_obj, 1, 0)
        layout.addWidget(self.scatter_obj_pb, 0, 2)
        layout.addWidget(self.scatter_targ, 1, 3)
        layout.addWidget(self.scatter_targ_pb, 0, 4)
        return layout

    def _align_to_normals_ui(self):
        layout = QtWidgets.QGridLayout()
        self.align_to_normals = QtWidgets.QCheckBox("Align to Surface Normals")
        layout.addWidget(self.align_to_normals, 2, 0)
        return layout

    def _align_to_normals_check(self):
        if self.align_to_normals.isChecked():
            self.scatterobject.scatter_choice = 1
        else:
            self.scatterobject.scatter_choice = 0

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

    def xscale_ui(self):
        layout = QtWidgets.QGridLayout()
        self.scale_xmin_lbl = QtWidgets.QLabel("Scale X Min")
        self.scale_xmax_lbl = QtWidgets.QLabel("Scale X Max")
        self.xscale_spinbox()
        layout.addWidget(self.scale_xmin_lbl, 1, 0)
        layout.addWidget(self.scale_xmin, 2, 0)
        layout.addWidget(self.scale_xmax_lbl, 3, 0)
        layout.addWidget(self.scale_xmax, 4, 0)
        return layout

    def yscale_ui(self):
        layout = QtWidgets.QGridLayout()
        self.scale_ymin_lbl = QtWidgets.QLabel("Scale Y Min")
        self.scale_ymax_lbl = QtWidgets.QLabel("Scale Y Max")
        self.yscale_spinbox()
        layout.addWidget(self.scale_ymin_lbl, 3, 0)
        layout.addWidget(self.scale_ymin, 4, 0)
        layout.addWidget(self.scale_ymax_lbl, 5, 0)
        layout.addWidget(self.scale_ymax, 6, 0)
        return layout

    def zscale_ui(self):
        layout = QtWidgets.QGridLayout()
        self.scale_zmin_lbl = QtWidgets.QLabel("Scale Z Min")
        self.scale_zmax_lbl = QtWidgets.QLabel("Scale Z Max")
        self.zscale_spinbox()
        layout.addWidget(self.scale_zmin_lbl, 5, 0)
        layout.addWidget(self.scale_zmin, 6, 0)
        layout.addWidget(self.scale_zmax_lbl, 7, 0)
        layout.addWidget(self.scale_zmax, 8, 0)
        return layout

    def xscale_spinbox(self):
        self.scale_xmin = QtWidgets.QDoubleSpinBox()
        self.scale_xmin.setMinimum(0.1)
        self.scale_xmin.setValue(1.0)
        self.scale_xmin.setMaximum(10)
        self.scale_xmin.setMinimumWidth(100)
        self.scale_xmin.setSingleStep(.1)
        self.scale_xmax = QtWidgets.QDoubleSpinBox()
        self.scale_xmax.setMinimum(0.1)
        self.scale_xmax.setValue(1.0)
        self.scale_xmax.setMaximum(10)
        self.scale_xmax.setMinimumWidth(100)
        self.scale_xmax.setSingleStep(.1)

    def yscale_spinbox(self):
        self.scale_ymin = QtWidgets.QDoubleSpinBox()
        self.scale_ymin.setMinimum(0.1)
        self.scale_ymin.setValue(1.0)
        self.scale_ymin.setMaximum(10)
        self.scale_ymin.setMinimumWidth(100)
        self.scale_ymin.setSingleStep(.1)
        self.scale_ymax = QtWidgets.QDoubleSpinBox()
        self.scale_ymax.setMinimum(0.1)
        self.scale_ymax.setValue(1.0)
        self.scale_ymax.setMaximum(10)
        self.scale_ymax.setMinimumWidth(100)
        self.scale_ymax.setSingleStep(.1)

    def zscale_spinbox(self):
        self.scale_zmin = QtWidgets.QDoubleSpinBox()
        self.scale_zmin.setMinimum(0.1)
        self.scale_zmin.setValue(1.0)
        self.scale_zmin.setMaximum(10)
        self.scale_zmin.setMinimumWidth(100)
        self.scale_zmin.setSingleStep(.1)
        self.scale_zmax = QtWidgets.QDoubleSpinBox()
        self.scale_zmax.setMinimum(0.1)
        self.scale_zmax.setValue(1.0)
        self.scale_zmax.setMaximum(10)
        self.scale_zmax.setMinimumWidth(100)
        self.scale_zmax.setSingleStep(.1)

    def _create_selected_vert_percentage_ui(self):
        layout = QtWidgets.QGridLayout()
        self.selected_vert_lbl = QtWidgets.QLabel("Scatter Percentage")
        self._set_selected_vert_percentage_spinbox()
        layout.addWidget(self.selected_vert_lbl, 14, 0)
        layout.addWidget(self.selected_vert_perc, 15, 0)
        return layout

    def _set_selected_vert_percentage_spinbox(self):
        self.selected_vert_perc = QtWidgets.QSpinBox()
        self.selected_vert_perc.setMinimum(0)
        self.selected_vert_perc.setMaximum(100)
        self.selected_vert_perc.setValue(100)
        self.selected_vert_perc.setMinimumWidth(100)
        self.selected_vert_perc.setSingleStep(5)

    def scatter_button(self):
        layout = QtWidgets.QGridLayout()
        self.scatter_btn = QtWidgets.QPushButton("Scatter")
        layout.addWidget(self.scatter_btn, 30, 1)
        return layout

    def scatter_titles(self):
        self.scatter_targ_lbl = QtWidgets.QLabel("Source Object")
        self.scatter_obj_lbl = QtWidgets.QLabel("Destination Object")
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.scatter_targ_lbl, 2, 0)
        layout.addWidget(self.scatter_obj_lbl, 2, 3)
        return layout

    def scatter_input(self):
        self.scatterobject.scatter_x_min = self.xrot_min.value()
        self.scatterobject.scatter_x_max = self.xrot_max.value()
        self.scatterobject.scatter_y_min = self.yrot_min.value()
        self.scatterobject.scatter_y_max = self.yrot_max.value()
        self.scatterobject.scatter_z_min = self.zrot_min.value()
        self.scatterobject.scatter_z_max = self.zrot_max.value()
        self.scatterobject.scatter_scale_xmin = self.scale_xmin.value()
        self.scatterobject.scatter_scale_xmax = self.scale_xmax.value()
        self.scatterobject.scatter_scale_ymin = self.scale_ymin.value()
        self.scatterobject.scatter_scale_ymax = self.scale_ymax.value()
        self.scatterobject.scatter_scale_zmin = self.scale_zmin.value()
        self.scatterobject.scatter_scale_zmax = self.scale_zmax.value()
        self.scatterobject.scatter_object()
        self.scatterobject.scatter_percentage = self.selected_vert_perc.value()

    def lock_source_object(self):
        self.scatterobject.select_source_object()
        self.scatter_obj.setText(self.scatterobject.current_object_def)

    def lock_destination_object(self):
        self.scatterobject.select_destination_object()
        self.scatter_targ.setText(str(self.scatterobject.current_target_def))


class ScatterObject(object):

    def __init__(self):
        self.scatter_x_min = 0
        self.scatter_x_max = 0
        self.scatter_y_min = 0
        self.scatter_y_max = 0
        self.scatter_z_min = 0
        self.scatter_z_max = 0
        self.scatter_scale_xmin = 0
        self.scatter_scale_xmax = 0
        self.scatter_scale_ymin = 0
        self.scatter_scale_ymax = 0
        self.scatter_scale_zmin = 0
        self.scatter_scale_zmax = 0
        self.scatter_obj_def = None
        self.current_object_def = None
        self.scatter_target_def = None
        self.current_target_def = None

    def scatter_object(self):
        if cmds.objectType(self.current_object_def) == "transform":
            for target in self.scatter_target_def:
                self.scatterObject = cmds.instance(self.current_object_def,
                                                   name=self.current_object_def
                                                   + "_instance#")
                x_point, y_point, z_point = cmds.pointPosition(target)
                cmds.move(x_point, y_point, z_point, self.scatterObject)
                self.randomize()

    def randomize(self):
        xRot = random.uniform(self.scatter_x_min, self.scatter_x_max)
        yRot = random.uniform(self.scatter_y_min, self.scatter_y_max)
        zRot = random.uniform(self.scatter_z_min, self.scatter_z_max)
        cmds.rotate(xRot, yRot, zRot, self.scatterObject)
        scaleFactorX = random.uniform(self.scatter_scale_xmin,
                                      self.scatter_scale_xmax)
        scaleFactorY = random.uniform(self.scatter_scale_ymin,
                                      self.scatter_scale_ymax)
        scaleFactorZ = random.uniform(self.scatter_scale_zmin,
                                      self.scatter_scale_zmax)
        cmds.scale(scaleFactorX, scaleFactorY, scaleFactorZ,
                   self.scatterObject)

    def select_destination_object(self):
        self.scatter_target_def = cmds.ls(os=True, fl=True)
        for obj in self.scatter_target_def:
            if 'vtx[' not in obj:
                self.scatter_target_def.remove(obj)
        self.current_target_def = self.scatter_target_def


    def select_source_object(self):
        self.scatter_obj_def = cmds.ls(os=True, o=True)
        if len(self.scatter_obj_def) > 0:
            self.current_object_def = self.scatter_obj_def[-1]
