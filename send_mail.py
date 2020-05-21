#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
import getpass
import time
import urllib

SMTP_SERVER = 'smtp.mydomain.com'  # <-- NEED TO BE CONFIGURED

if len(sys.argv) is not 6:
        print('Usage: %s <LOGIN> <FROM_EMAIL> <EMAIL_SUBJECT> <EMAIL_BODY_FILE> <DEST_LIST_FILE>' % sys.argv[0])
        print('   ex: %s mylogin myemail@mydomain.com "My Subjet" email_body.txt email_list.txt' % sys.argv[0])
        quit(1)

(login, from_email, email_subject, email_body_file, dest_list_file) = sys.argv[1:]

password = getpass.getpass()

email_body_fd = open(email_body_file)
email_body = email_body_fd.read().replace('\n', '<br />')
email_body_fd.close()

dst_fd = open(dest_list_file)
for to_email in dst_fd.readlines():
        to_email = to_email.strip()
        if len(to_email) == 0:
                continue
        print('Sending email to %s ...' % to_email)
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = email_subject
        pad = ' ' * (16 - (len(to_email)%16))
        msg.attach(MIMEText(email_body, 'html', 'utf-8'))
        mailserver = smtplib.SMTP_SSL(SMTP_SERVER, 465)
        mailserver.ehlo()
        mailserver.login(login, password)
        try:
                mailserver.sendmail(from_email, to_email, msg.as_string())
        except smtplib.SMTPRecipientsRefused:
                print('ERROR: unable to send email to "%s" !' % to_email)
        mailserver.quit()
        time.sleep(5)
