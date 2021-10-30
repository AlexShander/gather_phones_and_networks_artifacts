from asterisk.ami import SimpleAction

from custom_ami import CustomAMIClient
from settings import login, connection

if __name__ == '__main__':
    client = CustomAMIClient(**connection)
    client.login(**login)
    action_off = SimpleAction('Events', Eventmask='off', )
    future = client.send_action(action_off)

    PeersName = ['vip', 'sipnet', 'voipmonitor', '0201', '250', '123IBC123']

    for PeerName in PeersName:
        action_getSIPPeerStatus = SimpleAction('SIPshowpeer', Peer=PeerName)
        PeerStatus = client.send_action(action_getSIPPeerStatus)
        print PeerStatus.response

    response = client.logoff()