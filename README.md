# Data-Structures-Notifier
A script to check the RPI Data Structures website for lab and homework postings. It sends email updates to subscribed students when assignments are released.

Writen in Python, the script interfaces with Gmail to send notifications and manage subscription settings.

Commands: sent via the subject line of an email to data.structures.notifier@gmail.com
"subscribe": add to mailing list
"unsubscribe: remove from mailing list
"test": sends a test message during the next cycle

Usage:
-Run "main.py" from the command line with two arguments:
  1. Number of cycles before terminating the program
  2. Length of the delay between each cycle (in seconds)

-There should be an account_config.txt file with the username for the email account on the first line and the password on the second line. 

-Each possible message needs to have a message template text file with the subject on the first line and the message on subsequent lines.
