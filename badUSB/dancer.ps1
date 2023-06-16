# surf to Google Drive
Start-Process "chrome.exe" "https://drive.google.com"
Start-Sleep -Milliseconds 200

# open directory
Start-Process "explorer.exe" "$env:USERPROFILE\Documents\dance"
Start-Sleep -Milliseconds 200

# set volume to 70%
Start-Process powershell "-NoProfile -ExecutionPolicy Bypass -Command `"& { Set-Volume 70 }`""
Start-Sleep -Milliseconds 200

function Set-Volume {
    Param(
        [Parameter(Mandatory=$true)]
        [ValidateRange(0, 100)]
        [Int]$volume
    )

    $keyPresses = [Math]::Ceiling($volume / 2)
    $obj = New-Object -ComObject WScript.Shell
    1..50 | ForEach-Object {
        $obj.SendKeys([char]174)
    }
    for ($i = 0; $i -lt $keyPresses; $i++) {
        $obj.SendKeys([char]175)
    }
}

Set-Volume 70
