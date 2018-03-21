#!/bin/sh

# -s = dont echo input
read -s savepass
#echo $test

#val=`cat test | gpg --quiet`
#echo $val

#echo "hello" | gpg --symmetric --armor --cipher-algo AES256


echo $savepass | openssl enc -aes-256-cbc -a -salt
# echo $savepass | openssl aes-256-cbc -a -salt -d
