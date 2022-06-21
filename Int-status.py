from schedule import every, repeat, run_pending
import time
# For Twilio
import os
from twilio.rest import Client
# For Genie/Pyats
from genie.conf import Genie
from genie.utils import Dq
from genie.testbed import load
import requests
import json

# Your Account SID from twilio.com/console
account_sid = "Removed" #removed for privacy
# Your Auth Token from twilio.com/console
auth_token  = "Removed" #removed for privacy

client = Client(account_sid, auth_token)

_baseline = ['GigabitEthernet0/0', 'GigabitEthernet0/2', 'Loopback0', 'Loopback100']

@repeat(every(1).minutes)
def _pyats_show_interface():
    global _admin_up
    global _baseline
    global _text
    _testbed = load('/Repositories/1-Ansible Code/testbed.yml') 
    _device = _testbed.devices['R1']
    _device.connect()
    _ints = _device.parse('show interfaces')
    _admin_up = _ints.q.contains_key_value('oper_status', 'up').get_values('[0]')
    print(_admin_up)
    print(_baseline)
    _out = set(_baseline) - set(_admin_up)
    print(_out)
    _text = str(_out)


_pyats_show_interface()
while(_admin_up == _baseline ):
    run_pending()
    time.sleep(1)
else:
    message = client.messages.create(
        to="removed", #removed for privacy
        from_="removed",#removed for privacy
        body=_text + " down!")
    print(message.sid)


################## need to check and validate everything above to make code neat!!!!!! and test with multiple ints down

