@echo off
echo ========================================
echo    Re-pushing Git Tag to Remote
echo ========================================
echo.

cd /d "%~dp0"

echo Deleting remote tag...
git push origin :refs/tags/v0.2.0-chat-enhancement

echo.
echo Pushing tag again...
git push origin v0.2.0-chat-enhancement

echo.
echo ========================================
echo ✅ Tag re-pushed successfully!
echo ========================================
echo.
echo Now go to GitHub and create the release:
echo https://github.com/yunquleonliu/PyMD/releases/new
echo.
pause
