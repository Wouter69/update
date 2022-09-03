#CONNECTION__
import socket
from socket import error as sock_error
import sys
import threading
from file_handle_C import File_man

#CONNECTION CLASSES
class connections():
    def __init__(self, **kwargs):
        self.val = ""
        self.FM = File_man()
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as e:
            print('CONNECTION_INIT[ERROR]:: ', str(e))
        self.host = '127.0.0.1'
        self.port = 8085
        self.encap = "@"
        try:
            self.sock.connect((self.host, self.port))
            print("\n[CONNECTED]\n")
        except Exception as e:
            print('SOCK_ERROR:: ', str(e))
            sys.exit(1)

    def get_msg(self):
        print("[GET_MSG]:[RUNNING]")
        self.E = threading.Event()
        while True:
            data = ""
            try:
                data_len = int(self.sock.recv(64).decode())
                if not data_len:
                    self.E.wait()
                print("MSG_LEN: ", str(data_len))
                if int(data_len) > 0:
                    data = str(self.sock.recv(data_len).decode())

                    if data:
                        print("DATA RECVED:: ", str(data))
                        if "MATCH" in data:
                            self.FM.write_file("SOCKET_DATA/SERVER.txt", data, "w")
                            print("SAVING MATCH")
                        if "MOVE" in data:
                            self.FM.write_file("SOCKET_DATA/MOVE.txt", data, "w")
                            print("SAVING MOVE")
                        if "DECK" in data:
                            self.FM.write_file("SOCKET_DATA/DECK.txt", data, "w")
                            print("SAVING DECK")
                        if "OOP_PROFILE" in data:
                            self.FM.write_file("SOCKET_DATA/OppData.txt", data, "w")
                            print("GOT_OPP_DETAILS")
                        if "LOGIN" in data or "NEW" in data:
                            print("WRITING ", str(data), "TO LOGIN.txt")
                            self.FM.write_file("SOCKET_DATA/LOGIN.txt", data, "w")
                        data_len = 0

            except Exception as e:
                print("[SOCKET CLOSED]")
                print(str(e)) 
                self.sock.close()
                sys.exit(1)
    
    
    def send_msg(self):
        print("[SEND_MSG]:[RUNNING]")
        #READ ALL DATA FROM FILES>>
        path = "SOCKET_DATA/GAME.txt"
        path2 = "SOCKET_DATA/Player.txt"
        try:
            self.init_data = str(self.FM.read_file(path))
            self.init_pl = str(self.FM.read_file(path2))
            print("INIT_DATA:: ", self.init_data)
            print("PLAYER_DATA: ", str(self.init_pl))
        except:
            print("conns.py::send_msg():: ERROR??")

        try:
            while True:
                #MAIN_GAME_DATA
                data = str(self.FM.read_file(path))
                #CLEAN UP DATA
                #.split etc 
                if self.init_data != data and len(data) >= 6 and data != "['@']":
                    msg_len = len(data)
                    send_len = str(msg_len).encode()
                    send_len += b' ' * (64 - len(send_len))
                    print(f'[SENDING]:: {send_len}')
                    print(f'[SENDING]:: {data}')
                    try:
                        self.sock.send(send_len)
                        self.sock.send(data.encode())
                        print("SENT:", str(data))
                        self.init_data = data
                    except Exception as e:
                        print("FUCKUP::SEND_MSG::", str(e))
                        sys.exit(1)
                

                #PLAYER_DATA
                data2 = str(self.FM.read_file(path2))
                if self.init_pl != data2 and data2 != "['@']" and len(data2)>2:
                    msg_len2 = len(data2)
                    send_len2 = str(msg_len2).encode()
                    send_len2 += b' ' * (64 - len(send_len2))
                    print(f'[SENDING]:: {send_len2}')
                    print(f'[SENDING]:: {data2}')
                    try:
                        self.sock.send(send_len2)
                        self.sock.send(data2.encode())
                        print("SENT:", str(data2))
                        self.init_pl = data2
                    except Exception as e:
                        print("FUCKUP::SEND_MSG::", str(e))
                        sys.exit(1)

        except Exception as e:
            print("SENDING_ERROR::", str(e))


