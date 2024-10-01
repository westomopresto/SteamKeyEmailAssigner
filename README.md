This is a project with 2 python scripts.

The first one main.py does the following:

1) Grabs emails out of patreon.csv from the second column (Assumed)
2) For eache email, it assigns a SteamKey out of steam_keys.txt (a key per line)
3) After doing this, it edits the steam_key.txt file with emails for each claimed key
4) It also writes out a paired_data.csv with that same information for the next step.

The second script is sendemails.py , and does the following:

1) For each Row in the paired_data.csv, it will make an email message.
2) This email message contains the Steam Key that email was assigned.
3) Everytime an email is successfully sent, it is recorded in "Completed Emails.text"
4) The email account that is used is inside this python script and needs to be edited.
5) The password for that email account is read from a separate .txt file named "emailpassword_secret.txt"
6) Please do not upload emailpassword_secret.txt to github with your actual password for the email.
