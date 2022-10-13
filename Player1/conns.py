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
        self.encap = "*"
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
                        #STATUS__
                        if data:
                            self.FM.write_file("SOCKET_DATA/IN_BOUND.txt", data,"*", "w")
                            print("STILL_CONNECTED")


                        #MAIN_GAME_DATA
                        if "MATCH" in data:
                            self.FM.write_file("SOCKET_DATA/SERVER.txt", data,"*", "w")
                            print("SAVING MATCH")
                        if "MOVE" in data:
                            self.FM.write_file("SOCKET_DATA/MOVE.txt", data,"*", "w")
                            print("SAVING MOVE")
                        if "DECK" in data:
                            self.FM.write_file("SOCKET_DATA/DECK.txt", data,"*", "w")
                            print("SAVING DECK")

                        #OPP_DATA
                        if "OOP_PROFILE" in data:
                            self.FM.write_file("SOCKET_DATA/OppData.txt", data, "*","w")
                            print("GOT_OPP_DETAILS")

                        #PROFILE_{LOGIN/REGISTER}
                        if "MY_PROFILE" in data:
                            self.FM.write_file("SOCKET_DATA/Profile.txt", data,"*", "w")

                        if "LOGIN" in data or "PLEASE_REGISTER" in data:
                            print("LOGIN_RET:DATA:: ", str(data))
                            u_data = data.split("%")
                            print("MY_PROFILE_LOADING", str(u_data[0]))
                            print("MY_PROFILE_LOADING", str(u_data[1]))
                            self.FM.write_file("SOCKET_DATA/Profile.txt", str(u_data[1]),"*", "w")
                            self.FM.write_file("SOCKET_DATA/IN_BOUND.txt", data,"*", "w")
                        if "LOGIN_FAIL" in data:
                            self.FM.write_file("SOCKET_DATA/Profile.txt", "","*", "w")
                            self.FM.write_file("SOCKET_DATA/IN_BOUND.txt", data,"*", "w")
                        data_len = 0

            except Exception as e:
                print("[SOCKET CLOSED]")
                print(str(e)) 
                self.sock.close()
                sys.exit(1)


    def lst_to_str(self, lst):
        try:
            str_ = ""
            for _ in lst:
                str_ += str(_)+"*"
            return str_
        except Exception as e:
            print("LST_TO_STR:ERROR:", str(e))


    def send_msg(self):
        print("[SEND_MSG]:[RUNNING]")
        #READ ALL DATA FROM FILES>>
        path = "SOCKET_DATA/OUT_BOUND.txt"



        try:
            self.init_data = str(self.FM.read_file(path, "*"))
            print("INIT_DATA:: ", self.init_data)
        except:
            print("conns.py::send_msg():: ERROR??")

        try:
            while True:
                #STD_COMMS_DATA

                ndata = self.FM.read_file(path, "*")
                data = self.lst_to_str(ndata)

                if self.init_data != data and len(data) > 1:
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
                


        except Exception as e:
            print("SENDING_ERROR::", str(e))


