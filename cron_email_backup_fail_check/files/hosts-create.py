#!/usr/bin/python
import click
import datetime
import os

from pyzabbix.api import ZabbixAPI

ZABBIX_SERVER = os.getenv("ZABBIX_SERVER", "argus.bienert.tech")
ZABBIX_PORT = int(os.getenv("ZABBIX_PORT", "10051"))

ZABBIX_USER='sa-cron_email_backup_fail_check'
ZABBIX_PASS='nwWUUscHg2dsc&'

def sync_hosts():
    hosts = (

    )
    # Create ZabbixAPI class instance
    with ZabbixAPI(url=f"https://{ZABBIX_SERVER}/", user=ZABBIX_USER, password=ZABBIX_PASS) as zapi:
        # Get all monitored hosts
        import pdb;pdb.set_trace()
        result1 = zapi.host.get(monitored_hosts=1, output='extend')
        print(result1)

@click.command()
def hosts_sync():
    """
    sync_hosts
    """
    sync_hosts()


if __name__ == '__main__':
    hosts_sync()