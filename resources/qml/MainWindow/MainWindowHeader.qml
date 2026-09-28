// Copyright (c) 2021 Ultimaker B.V.
// Cura is released under the terms of the LGPLv3 or higher.

import QtQuick 2.7
import QtQuick.Controls 2.4

import UM 1.5 as UM
import Cura 1.0 as Cura

import "../Account"
import "../ApplicationSwitcher"

Rectangle
{
    id: base
    color: UM.Theme.getColor("main_window_header_background")

    Column {
        anchors.fill: parent
        anchors.margins: UM.Theme.getSize("default_margin").width
        spacing: 20

        Column {
            spacing: 15
            anchors.horizontalCenter: parent.horizontalCenter
            
            Image
            {
                id: logo
                source: "../../images/cura-icon-dark.png"
                width: 100
                height: 100
                fillMode: Image.PreserveAspectFit
                anchors.horizontalCenter: parent.horizontalCenter
            }
            
            UM.Label {
                text: "ProSlicer"
                color: UM.Theme.getColor("text")
                font: UM.Theme.getFont("large_bold")
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }

        ButtonGroup
        {
            buttons: stagesListContainer.children
        }

        Column
        {
            id: stagesListContainer
            spacing: Math.round(UM.Theme.getSize("default_margin").width / 2)
            width: parent.width

            // The main window header is dynamically filled with all available stages
            Repeater
            {
                id: stagesHeader
                model: UM.StageModel { }

                delegate: Button
                {
                    id: stageSelectorButton
                    text: model.name.toUpperCase()
                    checkable: true
                    checked: UM.Controller.activeStage !== null && model.id == UM.Controller.activeStage.stageId
                    
                    width: parent.width
                    height: Math.round(UM.Theme.getSize("main_window_header").height)
                    property string stageId: model.id
                    hoverEnabled: true

                    background: Rectangle
                    {
                        radius: UM.Theme.getSize("action_button_radius").width
                        color: stageSelectorButton.checked ? UM.Theme.getColor("main_window_header_button_background_active") : (stageSelectorButton.hovered ? UM.Theme.getColor("main_window_header_button_background_hovered") : "transparent")
                    }

                    contentItem: UM.Label
                    {
                        id: buttonLabel
                        text: stageSelectorButton.text
                        anchors.centerIn: stageSelectorButton
                        font: UM.Theme.getFont("medium")
                        color: stageSelectorButton.checked ? UM.Theme.getColor("main_window_header_button_text_active") : (stageSelectorButton.hovered ? UM.Theme.getColor("main_window_header_button_text_hovered") : UM.Theme.getColor("main_window_header_button_text_inactive"))
                    }

                    MouseArea
                    {
                        anchors.fill: parent
                        onClicked: UM.Controller.setActiveStage(model.id)
                    }
                }
            }
        }
        

        Item {
            width: 1
            height: 10 // spacer
        }

        Cura.MachineSelector
        {
            id: machineSelection
            headerCornerSide: Cura.RoundedRectangle.Direction.All
            width: parent.width
            height: UM.Theme.getSize("stage_menu").height

            machineManager: Cura.MachineManager
            onSelectPrinter: function(machine)
            {
                toggleContent();
                Cura.MachineManager.setActiveMachine(machine.id);
            }
            machineListModel: Cura.MachineListModel {}
            buttons: [
                Cura.SecondaryButton
                {
                    id: managePrinterButton
                    leftPadding: UM.Theme.getSize("default_margin").width
                    rightPadding: UM.Theme.getSize("default_margin").width
                    text: catalog.i18nc("@button", "Manage printers")
                    width: parent.width
                    onClicked:
                    {
                        machineSelection.toggleContent()
                        Cura.Actions.configureMachines.trigger()
                    }
                }
            ]
        }

        Cura.ConfigurationMenu
        {
            id: printerSetup
            width: parent.width
            height: UM.Theme.getSize("stage_menu").height
        }

        Cura.PrintSetupSelector
        {
            id: printSetupSelectorItem
            width: parent.width
            height: UM.Theme.getSize("stage_menu").height
            headerCornerSide: Cura.RoundedRectangle.Direction.All
        }

        Item {
            width: 1
            height: 10 // spacer
        }


        Button
        {
            id: marketplaceButton
            text: catalog.i18nc("@action:button", "Marketplace")
            height: Math.round(UM.Theme.getSize("main_window_header").height)
            width: parent.width
            onClicked: Cura.Actions.browsePackages.trigger()
            hoverEnabled: true

            background: Rectangle
            {
                id: marketplaceButtonBorder
                radius: UM.Theme.getSize("action_button_radius").width
                color: "transparent"
                border.width: UM.Theme.getSize("default_lining").width
                border.color: UM.Theme.getColor("primary_text")

                Rectangle
                {
                    id: marketplaceButtonFill
                    anchors.fill: parent
                    radius: parent.radius
                    color: UM.Theme.getColor("primary_text")
                    opacity: marketplaceButton.hovered ? 0.2 : 0
                    Behavior on opacity { NumberAnimation { duration: 100 } }
                }
            }

            contentItem: UM.Label
            {
                id: label
                text: marketplaceButton.text
                color: UM.Theme.getColor("primary_text")
                anchors.centerIn: parent
            }

            Cura.NotificationIcon
            {
                id: marketplaceNotificationIcon
                anchors
                {
                    top: parent.top
                    right: parent.right
                    rightMargin: (-0.5 * width) | 0
                    topMargin: (-0.5 * height) | 0
                }
                visible: CuraApplication.getPackageManager().packagesWithUpdate.length > 0
                labelText:
                {
                    const itemCount = CuraApplication.getPackageManager().packagesWithUpdate.length
                    return itemCount > 9 ? "9+" : itemCount
                }
            }
        }

        ApplicationSwitcher
        {
            id: applicationSwitcher
            anchors.horizontalCenter: parent.horizontalCenter
        }

        AccountWidget
        {
            id: accountWidget
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }
}
