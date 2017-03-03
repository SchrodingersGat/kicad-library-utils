@ECHO OFF

for /d %%i in (*.pretty) do (
    echo %%i
    copy .travis.yml %%i
    copy library-check.sh %%i
    cd %%i
    git add .travis.yml
    git add library-check.sh
    git commit -m "Added travis CI scripts"
    git push
    cd ..
)