# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from tank.platform.qt import QtCore
for name, cls in QtCore.__dict__.items():
    if isinstance(cls, type): globals()[name] = cls

from tank.platform.qt import QtGui
for name, cls in QtGui.__dict__.items():
    if isinstance(cls, type): globals()[name] = cls


from  . import resources_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(700, 500)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout_2.addWidget(self.buttonBox)

        self.header_label = QLabel(Dialog)
        self.header_label.setObjectName(u"header_label")

        self.verticalLayout_2.addWidget(self.header_label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.task_list_header = QLabel(Dialog)
        self.task_list_header.setObjectName(u"task_list_header")

        self.verticalLayout.addWidget(self.task_list_header)

        self.asset_tree_view = QTreeView(Dialog)
        self.asset_tree_view.setObjectName(u"asset_tree_view")

        self.verticalLayout.addWidget(self.asset_tree_view)

        self.clear_cache_button = QPushButton(Dialog)
        self.clear_cache_button.setObjectName(u"clear_cache_button")

        self.verticalLayout.addWidget(self.clear_cache_button)

        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.asset_tree_header = QLabel(Dialog)
        self.asset_tree_header.setObjectName(u"asset_tree_header")

        self.verticalLayout_3.addWidget(self.asset_tree_header)

        self.task_list_view = QListView(Dialog)
        self.task_list_view.setObjectName(u"task_list_view")

        self.verticalLayout_3.addWidget(self.task_list_view)

        self.dynamic_sort_checkbox = QCheckBox(Dialog)
        self.dynamic_sort_checkbox.setObjectName(u"dynamic_sort_checkbox")

        self.verticalLayout_3.addWidget(self.dynamic_sort_checkbox)

        self.refresh_button = QPushButton(Dialog)
        self.refresh_button.setObjectName(u"refresh_button")

        self.verticalLayout_3.addWidget(self.refresh_button)

        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"The Current Sgtk Environment", None))
        self.header_label.setText(QCoreApplication.translate("Dialog", u"Select any Asset in the tree and see the corresponding Tasks", None))
        self.task_list_header.setText(QCoreApplication.translate("Dialog", u"Asset Tree", None))
        self.clear_cache_button.setText(QCoreApplication.translate("Dialog", u"Clear Cache", None))
        self.asset_tree_header.setText(QCoreApplication.translate("Dialog", u"Associated Tasks", None))
        self.dynamic_sort_checkbox.setText(QCoreApplication.translate("Dialog", u"Click to toggle setDynamicSortFilter", None))
        self.refresh_button.setText(QCoreApplication.translate("Dialog", u"Reload Tasks", None))
    # retranslateUi
