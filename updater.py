from importlib import reload
import json
import requests
import hashlib

class Updater:

    # Get the most recent commit, the local config, and the remote config.
    # Save those to Updater.
    def __init__(self):
        # We need to start by getting the most recent commit sha
        # since just accessing the file through githubusercontent.com
        # will cache it at a specific URL permanently.
        r = requests.get("https://api.github.com/repos/NoahFiner/groove-remote/git/refs/heads/master")
        response = json.loads(r.text)
        self.commit = response["object"]["sha"]

        # Read from our local config
        with open('config.json', 'r') as f:
            self.local_config = json.load(f)

        # Read from the remote config
        r = requests.get("https://raw.githubusercontent.com/NoahFiner/groove-remote/{0}/config.json".format(self.commit))
        self.remote_config = json.loads(r.text)

    # Checks if there is there a difference between the remote and local
    # config. If there is, then ask the user if they want to update or not.
    #
    # Returns true if we should run the current version of the program
    # and false if we should update it. 
    def should_run_current_version(self):
        if self.local_config["version"] != self.remote_config["version"]:
            response = input("""

There is currently an update available (version {version}).
Notes about this new version: {notes}

You are currently at version {version_old}.
Would you like to update? (y/n):""".format(
                        version=self.remote_config["version"],
                        notes=self.remote_config["notes"],
                        version_old=self.local_config["version"]))
                
            return response != "y"
        else:
            print("Up to date!")
            return True

    # Updates the module 
    def update(self):
        # Fetch the updated groove_program.py from GitHub
        print("Fetching version "+self.remote_config["version"]+"...", end='')
        r = requests.get("https://raw.githubusercontent.com/NoahFiner/groove-remote/{0}/updater.py".format(self.commit))
        print("done!")

        # Write that to the current groove_program.py and reload it
        print("Updating to "+self.remote_config["version"]+"...", end='')
        file = open(__file__, "w")
        file.write(r.text)
        file.close()

        # Update the current config.json
        file = open("config.json", "w")
        file.write(json.dumps(self.remote_config))
        file.close()
        print("done!")

        print("Checking MD5 hash with config...", end='')
        if(self.get_md5(__file__)
                                        == self.remote_config["hash"]):
            print("verified!")

            print("Restarting the updater...\n\n")
            
            # Restart the program
            import os
            import sys
            os.execv(sys.executable, ['python', __file__])
            # os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
        else:
            print("UNVERIFIED!")
            print("Please use generate_update.py to generate a valid hash")
            print("Exiting...")

    # Helper function for getting an MD5 hash of a file and determining
    # authenticity of an update
    def get_md5(self, filename):
        md5 = hashlib.md5()
        file = open(filename, "r")
        while True:
            data = file.read(32)
            if not data:
                break
            md5.update(data.encode("utf-8"))
        return md5.hexdigest()


def special_function():
    print("Hello from version 1.0!")

if __name__ == "__main__":
    updater = Updater()

    if(updater.should_run_current_version()):
        print("Running with version {0}".format(
                                            updater.local_config["version"]))
        
        special_function()
    else:
        updater.update()