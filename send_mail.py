#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
import getpass
import time
import urllib
import getopt

def init_starttls(host):
        server = smtplib.SMTP(host, 587)
        server.ehlo()
        server.starttls()
        return server

def init_ssltls(host):
        server = smtplib.SMTP_SSL(host, 465)
        return server

def init_smtp(host):
        server = smtplib.SMTP(host, 25)
        return server

def send_email(smtp_factory, smtp_server, login, password, from_email, email_subject, email_body, emails_dst):
        for to_email in emails_dst:
                print('Sending email to %s ...' % to_email)
                msg = MIMEMultipart()
                msg['From'] = from_email
                msg['To'] = to_email
                msg['Subject'] = email_subject
                pad = ' ' * (16 - (len(to_email)%16))
                msg.attach(MIMEText(email_body, 'html', 'utf-8'))
                mailserver = smtp_factory( smtp_server )
                mailserver.ehlo()
                mailserver.login(login, password)
                try:
                        mailserver.sendmail(from_email, to_email, msg.as_string())
                except smtplib.SMTPRecipientsRefused:
                        print('ERROR: unable to send email to "%s" !' % to_email)
                mailserver.quit()
                time.sleep(5)


if __name__ == '__main__':
        if len(sys.argv) < 7:
                print('Usage: %s [--smtp|--ssltls|--starttls] <SMTP_SERVER> <LOGIN> <FROM_EMAIL> <EMAIL_SUBJECT> <EMAIL_BODY_FILE> <DEST_LIST_FILE>' % sys.argv[0])
                print('   ex: %s smtp.domain.com mylogin myemail@mydomain.com "My Subjet" email_body.txt email_list.txt' % sys.argv[0])
                quit(1)

        smtp_factory = init_ssltls
        (optlist, args) = getopt.getopt(sys.argv[1:], '', ['smtp','ssltls', 'starttls'])
        for (k,v) in optlist:
                if k == '--ssltls':
                        smtp_factory = init_ssltls
                elif k == '--starttls':
                        smtp_factory = init_starttls
                elif k == '--smtp':
                        smtp_factory = init_smtp

        (smtp_server, login, from_email, email_subject, email_body_file, dest_list_file) = args
        password = getpass.getpass()

        email_body_fd = open(email_body_file)
        email_body = email_body_fd.read().replace('\n', '<br />')
        email_body_fd.close()

        with open(dest_list_file) as dst_fd:
                emails_dst = [ to_email.strip() for to_email in dst_fd.readlines() if len(to_email.strip()) > 0 ]

        send_email(smtp_factory, smtp_server, login, password, from_email, email_subject, email_body, emails_dst)
