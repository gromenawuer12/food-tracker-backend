#!/bin/sh
rm -f package.zip
pip3 install -r requirements.txt --target ./package
cd package
zip -r ../package.zip * -x '*__pycache__*'
cd ../src
zip -r ../package.zip * -x '*__pycache__*'
cd ..
rm -rf package