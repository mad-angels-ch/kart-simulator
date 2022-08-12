import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Page {
    ColumnLayout {
        anchors.centerIn: parent

        Button {
            Layout.alignment: Qt.AlignHCenter
            text: qsTr("New solo game")
        }

        Button {
            Layout.alignment: Qt.AlignHCenter
            text: qsTr("New multiplayers game")
        }

        Button {
            Layout.alignment: Qt.AlignHCenter
            text: qsTr("Join a multiplayers game")
        }

        Button {
            Layout.alignment: Qt.AlignHCenter
            text: qsTr("Main menu")
            onClicked: stack.pop(null)
        }
    }
}