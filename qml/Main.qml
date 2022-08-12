import QtQuick
import QtQuick.Controls

import "Pages"

ApplicationWindow {
    id: app
    title: qsTr("Kart Simulator")
    visible: true
    // visibility: ApplicationWindow.FullScreen
    visibility: ApplicationWindow.Maximized

    StackView {
        id: stack
        initialItem: mainMenuPage
        anchors.fill: parent
    }

    Component {
        id: mainMenuPage

        MainMenuPage {}
    }
}