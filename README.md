# send_mail
This script allow to send emails from an email list. This can be useful to send notification to a collection of people.


Usage
-----
The password is set in the running of the script with the echo disable (the typed password will not be visible on the screen).

To run the script, type :
```
$ python3 send_mail.py 
Usage: send_mail.py [--smtp|--ssltls|--starttls] <SMTP_SERVER> <LOGIN> <FROM_EMAIL> <EMAIL_SUBJECT> <EMAIL_BODY_FILE> <DEST_LIST_FILE>
   ex: send_mail.py smtp.domain.com mylogin myemail@mydomain.com "My Subjet" email_body.txt email_list.txt
```
