@echo off
echo Configurando o MarySmoke Recibos...
echo.

:: Cria um script powershell temporário para gerar o atalho de forma segura
set PSScript=%temp%\create_shortcut.ps1
echo $WshShell = New-Object -comObject WScript.Shell > "%PSScript%"
echo $DesktopPath = [Environment]::GetFolderPath('Desktop') >> "%PSScript%"
echo $Shortcut = $WshShell.CreateShortcut("$DesktopPath\MarySmoke Recibos.lnk") >> "%PSScript%"
echo $Shortcut.TargetPath = "pythonw.exe" >> "%PSScript%"
echo $Shortcut.Arguments = "interface.py" >> "%PSScript%"
echo $Shortcut.WorkingDirectory = "%~dp0" >> "%PSScript%"
echo $Shortcut.IconLocation = "shell32.dll,22" >> "%PSScript%"
echo $Shortcut.Save() >> "%PSScript%"

:: Executa o script gerado
powershell -ExecutionPolicy Bypass -NoProfile -File "%PSScript%"

:: Apaga o arquivo temporário
del "%PSScript%"

echo.
echo Pronto! O atalho 'MarySmoke Recibos' foi criado na sua Area de Trabalho.
echo Voce ja pode fechar esta janela.
echo.
pause
