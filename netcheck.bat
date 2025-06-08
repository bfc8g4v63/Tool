@echo off
color 0A
echo ========================================
echo   區網連線快速檢測工具（By Nelson）
echo ========================================
echo.

:: 顯示網路卡基本資訊
echo [1] 顯示本機 IP 設定：
ipconfig
echo.
pause

:: 檢查是否有拿到閘道（Default Gateway）
echo [2] 嘗試 ping 預設閘道（192.168.50.1）...
ping 192.168.50.1 -n 4
echo.
pause

:: 嘗試 ping 公網 DNS（Google）
echo [3] 嘗試 ping Google 公共 DNS（8.8.8.8）...
ping 8.8.8.8 -n 4
echo.
pause

:: 嘗試 DNS 解析測試
echo [4] 嘗試 ping 網域（www.google.com）以測試 DNS...
ping www.google.com -n 4
echo.
pause

echo 測試完成，請根據上面結果檢查問題來源。
pause
