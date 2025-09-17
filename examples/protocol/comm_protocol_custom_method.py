from maix import protocol
from maix import app
from maix.err import Err


APP_CMD_ECHO = 0x01


# init communicate method
def send(data:bytes):
    pass

def read():
    return b''


# APP_ID = "my_app1"
# app.set_app_id(APP_ID) # Just for test!!! temporary sets app id, DO NOT use it when release(pack) APP.

p = protocol.Protocol(buff_size = 1024)

while not app.need_exit():
    send_data = None
    data = read()
    msg = p.decode(data)
    if msg and msg.is_req: # find message and is request
        if msg.cmd == APP_CMD_ECHO:
            resp_msg = "echo from app {}".format(app.app_id())
            send_data = msg.encode_resp_ok(resp_msg.encode())
        elif msg.cmd == protocol.CMD.CMD_SET_REPORT:
            send_data = msg.encode_resp_err(Err.ERR_NOT_IMPL, "this cmd not support auto upload".encode())
    if send_data:
        send(send_data)

