# Update.ID
Update.ID is a program that checks if it's currently updated or not and, if it needs updating, updates itself, restarts itself, and runs again. Wow!

Instead of opting to build a webserver that hosts some files, Update.ID currently uses the extremely high-tech solution of checking another GitHub repository for potential updates. Wow! Honestly, git is the new Go.

## Features
To utilize modern security concepts, Update.ID ensures no attackers can provide malicious updates by generating a unique MD5 hash of updater.py in config.json on the server-side. Unless an attacker modifies config.json, updater.py will only accept updates that match the MD5 hash provided by the remote config.json.

## Installation
Clone this repo
Boot up the virtual env
```bash
source .env/bin/activate
```
Run updater.py
```bash
python3 updater.py
``` 

## Pushing an update
To use my revolutionary alternative to a server, aka GitHub, see https://github.com/NoahFiner/groove-remote.

On a serious note, if you'd like to I would be more than happy to write some actual back-end code for serving up files. I categorized an architecture of just a few GET requests to be unnecessary to write.

## Assumptions
There were a few assumptions I had to make
1) Our program is extremely simple and consists of only one file without any modules.
2) Attackers do not have access to config.json on our GitHub "webserver".
3) GitHub is a valid replacement for a web server.
4) A sysadmin has the patience to use a hacky method for pushing updates.

## Solutions
1) Put all of the files (including in directories and subdirectories) of our program in a queue and update all of them one-by-one by popping. End by rewriting to updater.py itself then restart it. This would involve much more complicated back-end and therefore a non-GitHub server.
2) Make sure hackers can't access GitHub accounts, preferably see #3.
3) Create a simple server that has a few endpoints returning config.json as actual json, the text of updater.py, and maybe more files. Include documentation for a sysadmin to upload updated files and update a config.json or specified endpoints.
4) See #3.

## More improvements/notes
1) Use YAML instead of JSON if the back-end is written in Flask. If it's written in JS or Go, we should stick with JSON.
I use https://blog.petrzemek.net/2014/03/23/restarting-a-python-script-within-itself/ to restart updater.py