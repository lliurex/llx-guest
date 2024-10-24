import org.kde.plasma.core as PlasmaCore
import org.kde.kirigami as Kirigami
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import org.kde.plasma.components as PC

Rectangle{
    color:"transparent"
    Text{ 
        text:i18nd("llx-guest-gui","Guest User")
        font.family: "Quattrocento Sans Bold"
        font.pointSize: 16
    }

    GridLayout{
        id:generalLayout
        rows:2
        flow: GridLayout.TopToBottom
        rowSpacing:10
        Layout.fillWidth: true
        anchors.left:parent.left

        Kirigami.InlineMessage {
            id: messageLabel
            visible:llxGuestBridge.showSettingsMessage[0]
            text:getMessageText(llxGuestBridge.showSettingsMessage[1])
            type:getMessageType(llxGuestBridge.showSettingsMessage[2])
            Layout.minimumWidth:490
            Layout.maximumWidth:490
            Layout.topMargin: 40
        }

        GridLayout{
            id: optionsGrid
            rows: 1
            flow: GridLayout.TopToBottom
            rowSpacing:5
            Layout.topMargin: messageLabel.visible?0:50

            PC.CheckBox {
                id:guestUserCb
                text:i18nd("llx-guest-gui","Enable a guest user account in SDDM (Login Display Manager)")
                checked:llxGuestBridge.isGuestUserEnabled
                font.pointSize: 10
                focusPolicy: Qt.NoFocus
                Keys.onReturnPressed: guestUserCb.toggled()
                Keys.onEnterPressed: guestUserCb.toggled()
                onToggled:{
                   llxGuestBridge.manageChanges(checked)
                }

                Layout.alignment:Qt.AlignLeft
                Layout.bottomMargin:15
            }
        }
    }
    RowLayout{
        id:btnBox
        anchors.bottom: parent.bottom
        anchors.right:parent.right
        anchors.bottomMargin:15
        anchors.rightMargin:10
        spacing:10

        PC.Button {
            id:applyBtn
            visible:true
            focus:true
            display:AbstractButton.TextBesideIcon
            icon.name:"dialog-ok"
            text:i18nd("llx-guest-gui","Apply")
            Layout.preferredHeight:40
            enabled:llxGuestBridge.settingsChanged
            Keys.onReturnPressed: applyBtn.clicked()
            Keys.onEnterPressed: applyBtn.clicked()
            onClicked:{
                applyChanges()
                closeTimer.stop()
                llxGuestBridge.applyChanges()
            }
        }
        PC.Button {
            id:cancelBtn
            visible:true
            focus:true
            display:AbstractButton.TextBesideIcon
            icon.name:"dialog-cancel"
            text:i18nd("llx-guest-gui","Cancel")
            Layout.preferredHeight: 40
            enabled:llxGuestBridge.settingsChanged
            Keys.onReturnPressed: cancelBtn.clicked()
            Keys.onEnterPressed: cancelBtn.clicked()
            onClicked:{
                discardChanges()
                closeTimer.stop()
                llxGuestBridge.cancelChanges()
            }
        }
    } 

    ChangesDialog{
        id:cdcChangesDialog
        dialogTitle:"Llx Guest"+" - "+i18nd("llx-guest-gui","Settings")
        dialogVisible:llxGuestBridge.showChangesDialog
        dialogMsg:i18nd("llx-guest-gui","The are pending changes to apply.\nDo you want apply the changes or discard them?")

        Connections{
            target:cdcChangesDialog
            function onDialogApplyClicked(){
                applyChanges()
                
            }
            function onDiscardDialogClicked(){
                discardChanges()
            }
            function onCancelDialogClicked(){
                closeTimer.stop()
                llxGuestBridge.manageSettingsDialog("Cancel")
            }

        }
    }
    CustomPopup{
        id:synchronizePopup
     }

    Timer{
        id:delayTimer
    }

    function delay(delayTime,cb){
        delayTimer.interval=delayTime;
        delayTimer.repeat=true;
        delayTimer.triggered.connect(cb);
        delayTimer.start()
    }

    Timer{
        id:waitTimer
    }

    function wait(delayTime,cb){
        waitTimer.interval=delayTime;
        waitTimer.repeat=true;
        waitTimer.triggered.connect(cb);
        waitTimer.start()
    }


    function getMessageText(code){

        var msg="";
        switch (code){
            case 0:
                msg=i18nd("llx-guest-gui","Guest user added sucessfully");
                break;
            case 1:
                msg=i18nd("llx-guest-gui","Guest user deleted sucessfully");
                break;
            case 2:
                msg=i18nd("llx-guest-gui","Guest user already enabled")
                break;
            case 3:
                msg=i18nd("llx-guest-gui","Guest user already disabled")
                break;
            case -1:
                msg=i18nd("llx-guest-gui","There has been a problem creating guest user");
                break;
            case -2:
                msg=i18nd("llx-guest-gui","There has been a problem deleting guest use");
                break;
            default:
                break;
        }
        return msg;

    }

    function getMessageType(type){

        switch (type){
            case "Info":
                return Kirigami.MessageType.Information
            case "Success":
                return Kirigami.MessageType.Positive
            case "Error":
                return Kirigami.MessageType.Error
        }

    } 

    function applyChanges(){
        synchronizePopup.open()
        synchronizePopup.popupMessage=i18nd("llx-guest-gui", "Please wait until the process is finished")
        delayTimer.stop()
        delay(500, function() {
            if (llxGuestBridge.closePopUp){
                synchronizePopup.close(),
                delayTimer.stop()
            }
        })
    } 

    function discardChanges(){
        synchronizePopup.open()
        synchronizePopup.popupMessage=i18nd("llx-guest-gui", "Restoring previous values. Wait a moment...")
        delayTimer.stop()
        delay(1000, function() {
            if (llxGuestBridge.closePopUp){
                synchronizePopup.close(),
                delayTimer.stop()

            }
        })
    }  
} 
