import QtQuick 2.0

Image
{
    objectName: "button"
    source: "CopyDog.png"

    function appendPlagiarismInfo(filesList, code)
    {
        plagiarismModel.append( { plagiarismData : filesList, plagiarismCode : code })
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
                mainWindow.openFileBrowser(1)
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
                mainWindow.openFileBrowser(2)
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
            //onClicked: mainWindow.openFileBrowser(3)
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

