# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import sgtk

from sgtk.platform.qt import QtCore, QtGui
from .ui.dialog import Ui_Dialog

shotgun_model = sgtk.platform.import_framework(
    "tk-framework-shotgunutils", "shotgun_model"
)
SimpleShotgunModel = shotgun_model.SimpleShotgunModel


# standard toolkit logger
logger = sgtk.platform.get_logger(__name__)


def show_dialog(app_instance):
    """
    Shows the main dialog window.
    """
    # in order to handle UIs seamlessly, each toolkit engine has methods for launching
    # different types of windows. By using these methods, your windows will be correctly
    # decorated and handled in a consistent fashion by the system.

    # we pass the dialog class to this method and leave the actual construction
    # to be carried out by toolkit.
    app_instance.engine.show_dialog("Test App", app_instance, AppDialog)


class AlphaProxyModel(QtGui.QSortFilterProxyModel):
    """
    Proxy model to sort ShotgunModel items alphanumerically
    """
    def lessThan(self, left, right):
        """
        Overrides the base class method to sort the model by content.

        Args:
            left (QModelIndex): The left index.
            right (QModelIndex): The right index.

        Returns:
            bool: True if the left index is less than the right index, False otherwise.
        """
        source_model = self.sourceModel()
        lvalue = source_model.itemFromIndex(left).data(QtCore.Qt.DisplayRole)
        rvalue = source_model.itemFromIndex(right).data(QtCore.Qt.DisplayRole)
        return lvalue < rvalue


class UniqueNameProxyModel(AlphaProxyModel):
    """
    Proxy model to filter out duplicate content
    """
    def filterAcceptsRow(self, source_row, source_parent):
        """
        Overrides the base class method to filter out duplicate content.

        Args:
            source_row (int): The row number in the source model.
            source_parent (QModelIndex): The parent index in the source model.
        """
        try:
            source_model = self.sourceModel()
            content_index = source_model.index(source_row, 0, source_parent)
            content = source_model.data(content_index, QtCore.Qt.DisplayRole)

            # Check if the content is already in the view
            for row in range(self.rowCount()):
                index = self.index(row, 0)
                existing_content = self.data(index, QtCore.Qt.DisplayRole)
                if content == existing_content:
                    return False
            return super(UniqueNameProxyModel, self).filterAcceptsRow(source_row, source_parent)
        except Exception as e:
            logger.error(
                f"An error occurred while filtering content: {e}", exc_info=True
            )
            return False


class AppDialog(QtGui.QWidget):
    """
    Main application dialog window
    """

    def __init__(self):
        """
        Constructor
        """
        super(AppDialog, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        logger.info("Launching Test App...")
        self._app = sgtk.platform.current_bundle()

        self.ui.asset_tree_view.setIndentation(16)
        self.ui.asset_tree_view.setUniformRowHeights(True)
        self.ui.asset_tree_view.setSortingEnabled(True)
        self.ui.asset_tree_view.sortByColumn(0, QtCore.Qt.AscendingOrder)

        # ------------------------------
        # Entity model
        # ------------------------------
        self._entity_model = shotgun_model.ShotgunEntityModel(
            "Asset",  # entity type
            [["project", "is", self._app.context.project]],  # filters
            ["project.Project.name", "sg_asset_type", "code"],  # hierarchy
            ["description", "id", "project", "sg_asset_type"],  # fields
            self,
        )
        self._entity_model.async_refresh()
        self._entity_proxy_model = QtGui.QSortFilterProxyModel(self)
        self._entity_proxy_model.setDynamicSortFilter(True)
        self._entity_proxy_model.setSourceModel(self._entity_model)
        self.ui.asset_tree_view.setModel(self._entity_proxy_model)
        # selections
        self.ui.asset_tree_view.selectionModel().selectionChanged.connect(
            self.handle_asset_selection
        )

        # ------------------------------
        # Tasks model
        # ------------------------------
        self._entity_tasks_model = shotgun_model.ShotgunModel(self)
        self._entity_tasks_model.data_refreshed.connect(self.on_task_data_refreshed)
        self._entity_tasks_proxy_model = UniqueNameProxyModel(self)
        self._entity_tasks_proxy_model.setDynamicSortFilter(True)
        self._entity_tasks_proxy_model.setSourceModel(self._entity_tasks_model)
        self.ui.task_list_view.setModel(self._entity_tasks_proxy_model)

        #
        # Buttons and checkboxes
        #
        self.ui.refresh_button.clicked.connect(self.load_task_data)
        self.ui.clear_cache_button.clicked.connect(self._entity_tasks_model.hard_refresh)
        self.ui.dynamic_sort_checkbox.setChecked(self._entity_tasks_proxy_model.dynamicSortFilter())
        self.ui.dynamic_sort_checkbox.stateChanged.connect(
            self.on_dynamic_sort_changed
        )

    def destroy(self):
        """
        Destroy the model as required by the API.
        """
        try:
            self._entity_model.destroy()
            self._entity_tasks_model.destroy()
        except Exception as e:
            # log exception
            pass

    def handle_asset_selection(self, selected, deselected):
        """
        Handle when an asset is selected in the tree view.

        Args:
            selected (QItemSelection): The selected items.
            deselected (QItemSelection): The deselected items.
        """
        try:
            indexes = selected.indexes()
            if not indexes:
                return
            # get the selected entity
            index = indexes[0]
            entity = self._entity_proxy_model.data(
                index, shotgun_model.ShotgunEntityModel.SG_DATA_ROLE
            )
            # update the active entity
            self.active_entity = entity
            self.load_task_data()
        except Exception as e:
            logger.error(f"*** Error selecting source task: {e}")

    def load_task_data(self):
        # self._entity_tasks_proxy_model.invalidate()
        self._entity_tasks_model._load_data(
            "Task",
            fields=["content", "sg_task_token", "step.Step.short_name"],
            filters=[
                ["entity", "is", self.active_entity],
            ],
            hierarchy=["content"],
            # We could set the order here, but it's not the "correct" way to sort the model.
            # and we may have more complex sorting requirements in the future.
            # order=[{"field_name": "content", "direction": "asc"}],
        )
        self._entity_tasks_model._refresh_data()

    def on_task_data_refreshed(self):
        self._entity_tasks_proxy_model.sort(0, QtCore.Qt.AscendingOrder)

    def clear_cache(self):
        self._entity_tasks_model.clear()
        self._entity_tasks_model._refresh_data()

    def on_dynamic_sort_changed(self, state):
        logger.debug(f"*** _entity_tasks_proxy_model setDynamicSortFilter: {state}")
        self._entity_tasks_proxy_model.setDynamicSortFilter(state)
        self._entity_tasks_model._refresh_data()
