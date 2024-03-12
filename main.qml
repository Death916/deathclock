// main.qml
import QtQuick
import QtQuick.Controls

ApplicationWindow {
    visible: true
    width: 800
    height: 480
    title: "Clockz"
    property string currTime: "00:00:00"
    property string onTouchPressed: "Left area not pressed"
    
    
    Rectangle {
        anchors.fill: parent

        Image {
            anchors.fill: parent
            source: "/home/death916/code/python/pyside/images/background.png"
            fillMode: Image.PreserveAspectCrop
        }

        // Left touch area
        MouseArea {
            id : scoreArea
            anchors.left: parent.left
            width: 70
            height: parent.height // Full height

            // Header text inside the MouseArea
            Text {
                anchors.top: parent.top
                width: parent.width
                height: 30
                text: "Scores"
                font.pixelSize: 20
                color: "white"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }

            onClicked: {
                console.log("Left area pressed!")
                onTouchPressed = "Left area pressed"
            }
        }

        // Colored rectangle to indicate the active area
        Rectangle {
            anchors.left: parent.left
            width: 70
            height: parent.height - newsArea.height // Full height
            color: Qt.rgba(0, 0, 1, 0.3) // Slightly opaque blue
        }

        // Display the message on the screen
        Text {
            anchors.centerIn: parent
            text: onTouchPressed
            font.pixelSize: 20
            color: "white"
        }

        // Weather box
        Rectangle {
            width: parent.width * 1 / 3 // 1/3 of the parent width
            height: parent.height * 1 / 3 // 1/3 of the parent height
            color: Qt.rgba(0, 0, 1, 0.5) // Semi-transparent blue
            anchors.centerIn: parent

            // Text "Weather" at the top
            Text {
                anchors.top: parent.top
                width: parent.width * 1 / 3
                height: 30
                text: "Weather"
                font.pixelSize: 20
                color: "white"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }

            

            Image {
                anchors.fill: parent
                source: weatherMapPath
            //fillMode: Image.fill            // Fill the entire area // Uncomment this line to fill the entire area
            }

            // Additional weather content can be added here
        }

        // Clock container
        Rectangle {
            x: 300
            y: 1
            width: time.implicitWidth + 20 // Adjusted width based on the text size
            height: time.implicitHeight + 20 // Adjusted height based on the text size
            border.color: "gray"
            color: "transparent"

            Text {
                id: time
                text: currTime
                font.pixelSize: 20
                color: "black"
                horizontalAlignment: Text.AlignHCenter
            }
        }

        //bottom news scroll area
        Rectangle {
            id: newsArea
            width: parent.width
            height: parent.height * 1 / 6
            color: Qt.rgba(0, 0, 1, 0.5) // Semi-transparent blue
            anchors.bottom: parent.bottom
            anchors.left: parent.left

            // Text "News" at the top
            Text {
                id: newsHeader
                anchors.top: parent.top
                width: parent.width
                height: 30
                text: "News"
                font.pixelSize: 20
                color: "white"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }

            Text {
                
                id: newsText
                text: news
                font.pixelSize: 15
                color: "white"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                x: parent.width
                anchors.top: newsHeader.bottom

                SequentialAnimation on x {
                    loops: Animation.Infinite
                    running: true

                    PropertyAnimation {
                        from: parent.width
                        to: -newsText.width
                        duration: 2000000 // 10 seconds (in milliseconds)
                    }
                }
            }

            Timer {
                id: newsTimer
                interval: 300005// 10 minutes
                running: true
                repeat: true
                onTriggered: {
                    newsText.text = news // Update the news text
                }
            }
        }

        // ... Additional UI elements as needed ...
    }
}
