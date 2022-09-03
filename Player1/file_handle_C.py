

import os

from pathlib import Path



class File_man():
    def __init__(self, **kwargs):
        #super().__init__(**kwargs)
        pass
    
    
    def read_file(self, file_name):
        
        #f_check = File_man.check_file(file_name)
        if file_name:
            try:
                #print(f'[filename]: {file_name}')
                with open(file_name, "r") as rf:
                    data = rf.readlines()
                    rf.close()
                    #print("NEW FILE_DATA", str(data))
                    return data
            except Exception as e:
                print(e)
                

    
    def write_file(self, file_name, data, rwm):
        text = ""
        #print(f'data to write {data}')
        fc = self.check_file(file_name)
        
        if fc == True:
            try:
                if type(data) == list:
                    for _ in data:
                        text += str(_)+"@"
                elif type(data) == str:
                    text += str(data) + str('@')
            except Exception as e:
                print(e)

            #print(f'TEXT_TO_WRITE: \n {text}')      
            with open(file_name, rwm) as wf:
                wf.write(text)
                wf.close()
            return
        else:
            fc = self.check_file(file_name)
            print(fc)

    def encrypt_file(self):
        pass
    

    def check_file(self, file_name):
        path_to_file = file_name
        path = Path(path_to_file)

        if path.is_file():
            
            #user_auth
            #DO A STRING COMPARE TO SEE IF THE PASSWORD MATCHES
            # #####!*!*!*!*!*!
            
            file_data = self.read_file(file_name)
            #print(f'[file exists] : {file_name}')
            #print(f'[FILE_DATA]   : {file_data}')
            return True
        else:
            #print(f'[file]: {path_to_file} !does_not_exist!\n \nWELCOME_NEW_PLAYER\n')
            os.system('touch ' + file_name)
            return False

    



