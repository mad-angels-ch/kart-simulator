import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Page {
    title: qsTr("Main menu")

    ColumnLayout {
        anchors.centerIn: parent
        
        Button {
            Layout.alignment: Qt.AlignHCenter
            text: qsTr("Play")
            onClicked: stack.push(playMenuPage)
        }

        Button {
            Layout.alignment: Qt.AlignHCenter
            text: qsTr("Scores")
        }

        Button {
            Layout.alignment: Qt.AlignHCenter
            text: qsTr("Settings")
            onClicked: stack.push(settingsPage)
        }

        Button {
            Layout.alignment: Qt.AlignHCenter
            text: qsTr("Quit")
            onClicked: {
                app.close()
            }
        }
    }

    Component {
        id: playMenuPage

        PlayMenuPage {}
    }

    Component {
        id: settingsPage

        SettingsPage {}
    }
}