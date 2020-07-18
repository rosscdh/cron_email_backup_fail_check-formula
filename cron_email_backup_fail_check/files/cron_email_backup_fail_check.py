#!/usr/bin/python

import email, imaplib, re, sys, json, base64, os

USER_EMAIL = os.getenv("USER_EMAIL")
USER_PASS_B64 = os.getenv("USER_PASS_B64")
IMAP_ADDR = os.getenv("IMAP_ADDR")
IMAP_USER = os.getenv("IMAP_USER")
IMAP_PASS_B64 = os.getenv("IMAP_PASS_B64")
IMAP_CONN = os.getenv("IMAP_CONN")
ZABBIX_ALERT_EMAIL = os.getenv("ZABBIX_ALERT_EMAIL")
SUBJECT_REGEXP = os.getenv("SUBJECT_REGEXP", "Snap:\s*(.+?)\s+failed")


# connect to mailbox,switch to "SNAP" folder and search for emails with "failed"
# in subject
user = USER_EMAIL
pwd = base64.b64decode(USER_PASS_B64)
conn = imaplib.IMAP4_SSL(IMAP_ADDR)
conn.login(IMAP_USER, IMAP_PASS_B64)
conn.select(IMAP_CONN)

# resp, items = conn.uid("search",None, 'All')
resp, items = conn.uid("search", None, f'(FROM "{ZABBIX_ALERT_EMAIL}")')


tdata = []
items = items[0].split()

for emailid in items:
    resp, data = conn.uid("fetch", emailid, "(RFC822)")
    if resp == "OK":
        email_body = data[0][1].decode("utf-8")
        mail = email.message_from_string(email_body)
        if mail["Subject"].find("failed") > 0:
            # print mail["Subject"]
            regex1 = f"{SUBJECT_REGEXP}"
            a = re.findall(regex1, mail["Subject"], re.DOTALL)
            if a:
                a = [item.replace("'", "") for item in a]
                a = [item.replace("\r\n", "") for item in a]
                a = [item.replace(" ", "_") for item in a]
                a = [item.replace("|", "_") for item in a]
                a = [item.replace(".", "_") for item in a]
                a = [item.replace("-", "") for item in a]
                a = [item.replace("__", "_") for item in a]
                a = [item.replace("Processor_", "") for item in a]
                seen = set()
                result = []
                for item in a:
                    # remove "_for_" and all after it
                    c = item.split("_for_")[0]
                    # remove digits
                    c = "".join([i for i in c if not i.isdigit()])
                    # limit strings to 36 characters (in order to create zabbix items)
                    s = c[:36]
                    # if string ends with "_",remove it
                    s = re.sub("_$", "", s)
                    # replace "__" with empty space
                    s = c.replace("__", "")
                    s = s[:36]
                    s = re.sub("_$", "", s)
                    if s not in seen:
                        seen.add(s)
                        result.append(s)
                        output = " ".join(result)
                        output.join(result)
                        # create LLD JSON output
                        tdata.append({"{#JOB}": output, "{#NAME}": item})
print(json.dumps({"data": tdata}, indent=4))
