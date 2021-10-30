import time
from settings import login, connection
from custom_ami import CustomAMIClient

from action import SimpleAction
from event import EventListener

RunEventListener = True
SIPListPeers = []
ami_white_list = []

def Event_Listener_PJSIP_SIP(event,**kwargs):
    global RunEventListener
    global SIPListPeers
    if event.name == 'ContactStatusDetail':
        URIPORT = event.keys['URI'].split('@')[1]
        URI = URIPORT.split(':')[0]
        print event.keys['EndpointName'], ':', URI, ':', event.keys['UserAgent']
    if event.name == 'ContactStatusDetailComplete':
        RunEventListener = False
    if event.name == 'PeerStatus':
        SIPListPeers.append(event.keys['Peer'].split('/')[1])
    if event.name == 'SIPpeerstatusComplete':
        RunEventListener = False

try:
    client = CustomAMIClient(**connection)
    future = client.login(**login)
    if future.response.is_error():
        raise Exception(str(future.response))
    action_off = SimpleAction('Events', Eventmask='off',)
    future = client.send_action(action_off)
    if future.response.is_error():
        raise Exception(str(future.response))
    action_status_chan_sip = SimpleAction('ModuleCheck', Module='chan_sip.so')
    future = client.send_action(action_status_chan_sip)
    if not future.response.is_error():
        ami_white_list = ['PeerStatus', 'SIPpeerstatusComplete']
        action_status_chan_sip = SimpleAction('ModuleCheck', Module='chan_pjsip.so')
        future = client.send_action(action_status_chan_sip)
        if not future.response.is_error():
            ami_white_list.extend(['ContactStatusDetail','ContactStatusDetailComplete'])
            client.add_event_listener(EventListener(on_event=Event_Listener_PJSIP_SIP, white_list=ami_white_list))
            action_getPJSIP = SimpleAction('PJSIPShowRegistrationInboundContactStatuses',)
            future = client.send_action(action_getPJSIP)
            if future.response.is_error():
                raise Exception(str(future.response))
            while RunEventListener:
                time.sleep(1)
            RunEventListener = True
            action_getSIPPeersStatus = SimpleAction('SIPpeerstatus',)
            future = client.send_action(action_getSIPPeersStatus)
            if future.response.is_error():
                raise Exception(str(future.response))
            while RunEventListener:
                time.sleep(1)
            for PeerName in SIPListPeers:
                action_getSIPPeerStatus = SimpleAction('SIPshowpeer', Peer=PeerName)
                PeerStatus = client.send_action(action_getSIPPeerStatus)
                if PeerStatus.response.is_error():
                    continue
                else:
                    ipaddres = PeerStatus.response.keys['Address-IP'] if PeerStatus.response.keys['Address-IP'] != '(null)' else '0.0.0.0'
                    useragent = PeerStatus.response.keys['SIP-Useragent'] if PeerStatus.response.keys['SIP-Useragent'] != '' else 'no'
                    print('\"%s\";\"%s\";\"%s\"' % (PeerName, ipaddres, useragent))
            response = client.logoff()
        else:
            client.add_event_listener(EventListener(on_event=Event_Listener_PJSIP_SIP, white_list=ami_white_list))
            action_getSIPPeersStatus = SimpleAction('SIPpeerstatus',)
            future = client.send_action(action_getSIPPeersStatus)
            while RunEventListener:
                time.sleep(1)
            for PeerName in SIPListPeers:
                action_getSIPPeerStatus = SimpleAction('SIPshowpeer', Peer=PeerName)
                PeerStatus = client.send_action(action_getSIPPeerStatus)
                if PeerStatus.response.is_error():
                    continue
                else:
                    ipaddres = PeerStatus.response.keys['Address-IP'] if PeerStatus.response.keys['Address-IP'] != '(null)' else '0.0.0.0'
                    useragent = PeerStatus.response.keys['SIP-Useragent'] if PeerStatus.response.keys['SIP-Useragent'] != '' else 'no'
                    print('\"%s\";\"%s\";\"%s\"' % (PeerName, ipaddres, useragent))
            response = client.logoff()
    else:
        action_status_chan_sip = SimpleAction('ModuleCheck', Module='chan_pjsip.so')
        future = client.send_action(action_status_chan_sip)
        if not future.response.is_error():
            ami_white_list.extend(['ContactStatusDetail', 'ContactStatusDetailComplete'])
            client.add_event_listener(EventListener(on_event=Event_Listener_PJSIP_SIP, white_list=ami_white_list))
            action_getPJSIP = SimpleAction('PJSIPShowRegistrationInboundContactStatuses',)
            future = client.send_action(action_getPJSIP)
            if future.response.is_error():
                raise Exception(str(future.response))
            while RunEventListener:
                time.sleep(1)
            response = client.logoff()
        else:
            response = client.logoff()
except (KeyboardInterrupt, SystemExit):
    response = client.logoff()
