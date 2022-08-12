import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Page {
    title: qsTr("Settings")

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 10
        spacing: 10

        GroupBox {
            Layout.fillWidth: true
            Layout.fillHeight: true
            title: qsTr("Cart")

            ListView {
                id: cartsView
                anchors.fill: parent
                orientation: ListView.Horizontal
                spacing: 10
                model: ["Best cart", "Worst cart", "Other cart"]
                delegate: RadioDelegate {
                    id: musicDelegate
                    text: modelData
                }
            }
        }

        GroupBox {
            Layout.fillWidth: true
            Layout.fillHeight: true
            title: qsTr("Music")
            
            ListView {
                id: musicsView
                anchors.fill: parent
                orientation: ListView.Horizontal
                spacing: 10
                model: ["Best song", "Worst song", "Other song"]
                delegate: RadioDelegate {
                    id: musicDelegate
                    text: modelData
                }
            }
        }

        GroupBox {
            Layout.fillWidth: true
            title: qsTr("My account")

            Button {
                text: qsTr("Log out")
            }
        }

        Button {
            Layout.alignment: Qt.AlignHCenter
            text: qsTr("Main menu")
            onClicked: stack.pop(null)
        }
    }
}