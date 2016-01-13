import sys

from netzob.all import *


session = PCAPImporter.readFile(sys.argv[1]).values()

symbol = Symbol(messages=session)

class ProtoHdr(object):
    proto_id_field = Field(name='Protocol ID', domain=Raw(nbBytes=1))
    hp_cnt_addr_off_field = Field(name='Hop Count or Address Offset', domain=(BitArray(nbBits=5)))
    hdr_len_field = Field(name='Header Length', domain=BitArray(nbBits=3))
    priority_field = Field(name='Priority', domain=BitArray(nbBits=2))
    signal_rtr_field = Field(name='Signal Router', domain=BitArray(nbBits=1))
    addr_type_field = Field(name='Address Type', domain=BitArray(nbBits=1))
    block_len_field = Field(name='Block Length', domain=BitArray(nbBits=4))
    svc_id_field = Field(name='Service ID', domain=Raw(nbBytes=1))
    msg_id_field = Field(name='Message ID', domain=Raw(nbBytes=1))
    sndr_addr_len_field = Field(name='Sender Address Length', domain=BitArray(nbBits=4))
    rcvr_addr_len_field = Field(name='Receiver Address Length', domain=BitArray(nbBits=4))
    #TODO
    #rcvr_addr
    #sndr_addr
    #padding
    #higher layer data
