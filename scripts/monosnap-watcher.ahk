#Requires AutoHotkey v2.0
#SingleInstance Force

watchFolder := EnvGet("MONOSNAP_DIR")

; Store the latest file creation timestamp
global lastTimestamp := A_Now

; Check for new files every 500ms
SetTimer(CheckForNewFiles, 500)

A_IconTip := "Monosnap Watcher"

CheckForNewFiles() {
    global lastTimestamp, watchFolder

    loop files watchFolder "\*.*" {
        if (A_LoopFileTimeCreated > lastTimestamp) {
            lastTimestamp := A_LoopFileTimeCreated
            A_Clipboard := A_LoopFileFullPath
            TrayTip("Path copied", A_LoopFileFullPath, 1)
        }
    }
}
