# Update.ID
Update.ID is a program that checks if it's currently updated or not and, if it needs updating, updates itself, restarts itself, and runs again. Wow!

Additionally, it recursively looks through all directories in the current directory, then checks the server to see if they need updating as well. Yowza!

Instead of opting to build a webserver that hosts some files, Update.ID currently uses the extremely high-tech solution of checking another GitHub repository for potential updates. Wow! Honestly, git is the new Go.

## Features
To utilize modern security concepts, Update.ID ensures no attackers can provide malicious updates by generating a unique MD5 hash of all files (excluding a few) on the server-side. Unless an attacker modifies config.json, updater.py will only accept updates that match the MD5 hash provided by the remote config.json.

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

On a serious note, if you'd like to I would be more than happy to write some actual back-end code for serving up files. I categorized an architecture of just a few GET requests to be unnecessary to write and wanted to mostly focus on this Python script.

## Assumptions
There were a few assumptions I had to make
1) Attackers do not have access to config.json on our GitHub "webserver".
2) GitHub is a valid replacement for a web server.
3) A sysadmin has the patience to use a hacky method for pushing updates.

## Solutions
1) Make sure hackers can't access GitHub accounts, preferably see #2.
2) Create a simple server that has a few endpoints returning config.json as actual json, the text of updater.py, and maybe more files. Include documentation for a sysadmin to upload updated files and update a config.json or specified endpoints.
3) See #2.

## More improvements/notes
1) VERY IMPORTANT! While I was able to figure out how to recursively find every local file and compare that to the upstream, I did not have the time to figure out how to recursively find every file on GitHub using their API. The program currently checks all local files and sees if they need updating from remote sources, and if the remote sources don't exist it deletes those local files. HOWEVER, if a new remote file is created, Update.ID does not know about that file's existance. The only way to add that file is for a user to add it locally.
This issue can be fixed with a more complicated back-end that lists directory contents in a parsable way (such as providing a list of all paths to send GET requests to), however I wanted to focus my time on the Python script instead of implementing a back-end for this feature.
2) I should use YAML instead of JSON if the back-end is written in Flask. If it's written in JS or Go, we should stick with JSON.
3) I use https://blog.petrzemek.net/2014/03/23/restarting-a-python-script-within-itself/ to restart updater.py
