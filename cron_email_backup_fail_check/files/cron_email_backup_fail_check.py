#!/usr/bin/python
import yaml
import click
import arrow
import datetime
import html2text
import mailparser
import imap_tools
import os, email, imaplib, re, sys, json, base64

from pyzabbix import ZabbixMetric, ZabbixSender

h2t = html2text.HTML2Text()
h2t.ignore_links = True

IMAP_ADDR = os.getenv("IMAP_ADDR")
IMAP_USER = os.getenv("IMAP_USER")
IMAP_PASS = base64.b64decode(os.getenv("IMAP_PASS_B64")).strip().decode('utf8')

ZABBIX_SERVER = os.getenv("ZABBIX_SERVER", "argus.bienert.tech")
ZABBIX_PORT = int(os.getenv("ZABBIX_PORT", "10051"))

HOSTS = yaml.load(open('hosts.yaml', 'rb'), Loader=yaml.FullLoader).get('hosts')
HOST_KEYS = HOSTS.keys()

def check_mail(dateof: arrow.Arrow):
    print(f"date of : {dateof.datetime.date()}")
    criteria = imap_tools.A(date=dateof.datetime.date())
    with imap_tools.MailBox(IMAP_ADDR).login(IMAP_USER, IMAP_PASS) as mailbox:
        for msg in mailbox.fetch(criteria=criteria,
                                 mark_seen=False):
            # import pdb;pdb.set_trace()
            # look over to tuple and try match on host_keys
            if any(to for to in msg.to if to in HOST_KEYS):
                print(f"subject: {msg.subject}, to:{msg.to}, content: {msg.text or h2t.handle(msg.html)}")
                # print(msg.subject, msg.to)
                print("***"*15)
    # import pdb;pdb.set_trace()
    # send_to_zabbix(hostname='hostname1', metrics={})


def send_to_zabbix(hostname: str, metrics: dict):
    """
    hostname = monkey-host-1
    metrics = {
        'test[cpu_usage]': 2,
        'test[system_status]': "OK",
    }
    """
    # Send metrics to zabbix trapper
    packet = []
    for key in metrics:
        packet.append(
            ZabbixMetric(hostname, key, metrics[key]),
        )

    result = ZabbixSender(zabbix_server=ZABBIX_SERVER,
                          zabbix_port=ZABBIX_PORT).send(packet)
    return result

@click.command()
@click.option('--date', '-d', default='today', help='Date today|yesterday|yyyy-dd-mm')
def mail_check(date):
    """
    App to check todays email backup messages and provide zabbix the status data
    """
    if date.lower() == 'today':
        dateof = arrow.utcnow()
    elif date.lower() == 'yesterday':
        dateof = arrow.utcnow().shift(days=-1)
    else:
        dateof = arrow.get(date)

    check_mail(dateof=dateof)


if __name__ == '__main__':
    mail_check()