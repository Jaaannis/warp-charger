#!/bin/sh

# Simple auto-deploy from github
# This is called on docs.warp-charger.com with cron
cd /var/www/git/warp-charger/docs.warp-charger.com/
/usr/bin/git pull origin master
/usr/local/bin/npm run build
