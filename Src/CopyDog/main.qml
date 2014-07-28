import QtQuick 2.0

Image
{
    source: "CopyDog.png"

    function appendPlagiarismInfo(filesList, code)
    {
        plagiarismModel.append( { plagiarismData : filesList, plagiarismCode : code })
    }

    Rectangle
    {
        id : exportButton
        width : 150
        height: width /4
        opacity: screen2.opacity
        z: screen2.z + 1

        anchors { top : parent.top; right: parent.right ; topMargin : 10 ; rightMargin : 10 }

        Text
        {
            id: exportButtonText
            text: qsTr("Export and Exit")
            anchors.centerIn: parent
            font.pixelSize:18
        }

        MouseArea
        {
            id: exportMouse
            anchors.fill: parent
            onClicked:
            {
                exportButtonText.text = "Exporting.."
                exportMouse.enabled = false
                mainWindow.exportPlagiarismInformation()
            }
        }
    }

    Item
    {
        anchors { left: parent.left ; bottom: parent.bottom }
        width: parent.width * .3
        height: parent.height * .3

        MouseArea
        {
            anchors.fill: parent
            onClicked:
            {
                mainWindow.openFileBrowser(languageSelection.selected, parseInt(sliderBarText.text), 0)
                screen2.opacity = 1
                screen2.z = 10
            }
        }
    }

    Item
    {
        anchors { right: parent.right ; bottom: parent.bottom }
        width: parent.width * .3
        height: parent.height * .3

        MouseArea
        {
            anchors.fill: parent
            onClicked:
            {
                mainWindow.openFileBrowser(languageSelection.selected, parseInt(sliderBarText.text), 1)
                screen2.opacity = 1
                screen2.z = 10
            }
        }
    }

    Item
    {
        anchors { right: parent.right ; bottom: parent.bottom; rightMargin: parent.width / 3; }
        width: parent.width * .3
        height: parent.height * .3

        MouseArea
        {
            anchors.fill: parent
            //onClicked: mainWindow.openFileBrowser(languageSelection.selected)
        }
    }

    Column
    {
        id: languageSelection
        x: 35
        y: 150
        spacing : 60
        property int selected : 0

        Repeater
        {
            model: 3
            Image
            {
                source: languageSelection.selected == index ? "radioChecked.png" :  "radioUnchecked.png"
                smooth: true
                scale: .85


                Text
                {
                    x: 35
                    y: 8
                    color: "#dd462a"
                    text: if( 0 == index ) "Python"
                          else if ( 1 == index) "C++"
                          else if ( 2 == index) "C"
                    font.pixelSize: 16
                }

                MouseArea
                {
                    anchors.fill: parent
                    onClicked: languageSelection.selected = index
                }
            }
        }
    }

    Text
    {
        text: "     Select\n  Language"
        color: "#dd462a"
        font.pixelSize: 16
        anchors{ top : languageSelection.bottom ; topMargin: 35; horizontalCenter: languageSelection.horizontalCenter }
    }


    Rectangle
    {
        id: bar
        width: 5
        height: parent.height * .50
        radius: 15
        color: "#d7d0b4"
        anchors { right: parent.right; top: parent.top ; topMargin: parent.height * .10 ; rightMargin: parent.width * .10  }

        Image
        {
            x: - width * .45
            y: bar.height - height / 2 - 28
            source: "slider.png"

            Text
            {
                id: sliderBarText
                text: parseInt((( 1000 - ((parent.y + 2) * 3000) / 913 ) + 10)*1000/1010) + 1
                color: "white"
                anchors.centerIn: parent
            }

            MouseArea
            {
                id: dragMouse
                anchors.fill: parent
                drag.target: parent
                drag.axis: Drag.YAxis
                drag.minimumY: -2
                drag.maximumY: bar.height - parent.height / 2
            }
        }

        Text
        {
            x: -40
            y: 340
            color: "#dd462a"
            text: "Characters\n  to Match"
            font.pixelSize: 16
        }
    }

    Rectangle
    {
        id: screen2
        anchors.fill: parent
        color: "darkgrey"
        opacity: 0
        z : -10

        ListView
        {
                anchors.fill: parent
                model: plagiarismModel
                delegate:

                Column
                {
                    width: parent.width

                    Text
                    {
                        text : "Files with plagiarism\n" + plagiarismData
                        width: parent.width
                        wrapMode: Text.WordWrap
                        elide: Text.ElideLeft
                        font.family: "courier"
                        font.bold: true
                    }

                    Text
                    {
                        text :  "\n" + plagiarismCode + "\n\n\n"
                        width: parent.width
                        elide: Text.ElideLeft
                        font.family: "courier"
                    }
                }

                focus: true
        }

        ListModel
        {
            id: plagiarismModel

//            ListElement
//            {
//                    plagiarismCode: "while n > 0 :\n	print n \n 	a = 10 \n 	b = 30 \n 	c = a + b"
//                    plagiarismData: "1 34 4 21 34 4 21 34 4 21 34 4 21 34 4 21 34 4 21 34 4 21 34 4 21 34 4 21 34 4 21 34 4 21 34 4 21 34 4 21 34 4 21 34 4 21 34 4 21"
//            }

//            ListElement
//            {
//                    plagiarismData: "1 34 4 21 34 4 21 34 4 21 34 4 21 34 4 21 34 4 21 34 4 21 34 4 21 34 4 21 34 4 21 34 4 21 34 4 21 34 4 21 34 4 21 34 4 21 34 4 21"
//                    plagiarismCode: "while n > 0 :\n	print n \n 	a = 10 \n 	b = 30 \n 	c = a + b"
//            }

//            ListElement
//            {
//                    plagiarismData: "4 21"
//                    plagiarismCode: "while n > 0 :\n	print n \n 	a = 10 \n 	b = 30 \n 	c = a + b"
//            }
        }
    }
}

