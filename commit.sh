#!/bin/bash
cd src

echo "Root permissions are required to easily remove some __pycache__ folders"
sudo pyclean .

git add -A
git commit -m $@
git push origin

cd ..