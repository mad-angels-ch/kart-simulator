import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Page {
    title: qsTr("Login")

    GridLayout {
        columns: 2
        anchors.centerIn: parent

        Label {
            text: qsTr("Username")
        }

        TextField {
            id: usernameField
        }

        Label {
            text: qsTr("Password")
        }

        TextField {
            id: passwordField
            echoMode: TextField.Password
        }

        Button {
            text: qsTr("Cancel")
            onClicked: stack.pop()
        }

        Button {
            text: qsTr("Log in")
        }

        Button {
            Layout.columnSpan: 2
            text: qsTr("Create account")
        }
    }
}