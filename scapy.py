import sys
import time

from scapy.all import *
import struct


class AProto(Packet):
    name='A Protocol'
    fields_desc = [
        XByteField('proto_id', 0),
        BitField('hop_cnt_addr_off', 0, 5),
        BitField('hdr_len', 0, 3),
        BitEnumField('priority', 0, 2, {
            0: 'low',
            1: 'normal',
            2: 'high',
            3: 'emergency'
        }),
        BitEnumField('signal_rtr', 0, 1, {0: 'no_err', 1: 'err'}),
        BitEnumField('addr_type', 0, 1, {0: 'direct', 1: 'relative'}),
        BitField('block_len', 0, 4),
        XByteField('svc_id', 0),
        XByteField('msg_id', 0),
        BitFieldLenField('sndr_addr_len', 0, 4, length_of='sndr_addr'),
        BitFieldLenField('rcvr_addr_len', 0, 4, length_of='rcvr_addr'),
        ConditionalField(
            StrLenField('unk', None, length_from=lambda pkt: pkt.hdr_len*2-6),
            lambda pkt: pkt.hdr_len != 3
        ),
        StrLenField('rcvr_addr', None, length_from=lambda pkt: pkt.rcvr_addr_len*2),
        StrLenField('sndr_addr', None, length_from=lambda pkt: pkt.sndr_addr_len*2),
        StrLenField(
            'hdr_pad',
            '',
            length_from=lambda pkt: 4 - (((pkt.hdr_len * 2) % 4) if ((pkt.hdr_len * 2) % 4) else 4)
        )
    ]
bind_layers(UDP, AProto, dport=1740)

class AMsg(Packet):
    name = 'A Message'
    fields_desc = [
        Field('unk-before_crc', '', fmt='4s'),
        XIntField('LE_CRC32', None),
        XIntField('nonce', None),
        Field('unk-remaining', '', fmt='8s')
    ]
bind_layers(AProto, AMsg, svc_id=0x40)


def handle_aproto(pkt):
    print pkt[AProto].show2()
    if pkt.svc_id == 0x40:
        payload = str(pkt.lastlayer())
        print 'LE CRC-32: 0x{}'.format(
            struct.pack('<i', crc32(payload[:4] + '\x00'*4 + payload[8:])).encode('hex')
        )


def a_proto_cb(pkt):
    if pkt[UDP].dport == 1740:
        print
        print 'time: {}'.format(time.asctime())
        print pkt.summary()
        handle_aproto(pkt)
    else:
        print 'Cannot handle packet with UDP destination port "{}"!'.format(pkt[UDP].dport)


def main():
    if len(sys.argv) == 1:
        pcap_file = None
    elif len(sys.argv) == 2:
        pcap_file = sys.argv[1]
    else:
        print 'Wrong number of args!'
        sys.exit(1)

    sniff(
        offline=pcap_file,
        prn=a_proto_cb,
        lfilter=lambda pkt: pkt.haslayer(UDP) and pkt[UDP].dport in [1740],
        iface='eth1'
    )


if __name__ == '__main__':
    main()
