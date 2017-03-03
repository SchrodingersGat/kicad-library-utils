@ECHO OFF

for /d %%i in (*.pretty) do (
    echo %%i
    copy .travis.yml %%i
    cd %%i
    git pull
    git add .travis.yml
    del library-check.sh
    git add library-check.sh
    git commit -m "Fixed travis CI scripts (moved .sh file to KLC repo)"
    git push
    cd ..
    PAUSE
)