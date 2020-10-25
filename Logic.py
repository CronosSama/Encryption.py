import hashlib
import base64
from cryptography.fernet import Fernet
from time import sleep
import os

class mainApp():
    def __init__(self,unCleanedFiles=None,typeOfOperation=None,keyCode=None):
        self.keyCode = keyCode
        self.unCleanedFiles = unCleanedFiles
        self.typeOfOperation = typeOfOperation
        self.EDcryptor = None
        self.TargetedFiles = None


        if not self.typeOfOperation==None:
            self.asKey()
            self.Files()

            if self.typeOfOperation =="enc":
                self.Encryptor()
            elif self.typeOfOperation =="dnc":
                self.Decryptor()
        
    
    def asKey(self):
        # keyCode = input('Write The Password : ').encode()
        keyCode = self.keyCode.encode()
        key1 = hashlib.sha3_256(keyCode)
        key_bytes = key1.digest()
        fernet_key = base64.urlsafe_b64encode(key_bytes)

        custom_Encoder = Fernet(fernet_key)
        self.EDcryptor = custom_Encoder

    def Encryptor(self):

        for oneFile in self.TargetedFiles:
            with open(oneFile,'rb+') as newFile:
                file_bytes_normal = newFile.read()
                newFile.seek(0)
                coded = self.EDcryptor.encrypt(file_bytes_normal)
                newFile.write(coded)
                newFile.truncate()


    def Decryptor(self):

        forTheLoop = True
        tryNumber = 0

        while forTheLoop:

            try:
                for oneFile in self.TargetedFiles:
                    with open(oneFile,'rb+') as newFile:

                        file_bytes_encrypted = newFile.read()
                        
                        newFile.seek(0)
                        decoded = self.EDcryptor.decrypt(file_bytes_encrypted)
                        newFile.write(decoded)
                        newFile.truncate()
                        forTheLoop=False

            except:
                print('the password is wrong try Again')
                tryNumber=tryNumber+1
                if tryNumber<=3:
                    print(f'totatl chances you have left is : {3-tryNumber}')
                    self.asKey()
                else:
                    print('You Used All Your Chances !!!')
                    forTheLoop=False
                


    def Files(self):
        # All_Files = os.listdir()
        All_Files = self.unCleanedFiles
        cleanFiles = []
        for oneFile in All_Files:
            if '.py' in oneFile or '.vscode'==oneFile :
                continue
            else:
                cleanFiles.append(oneFile)

        self.TargetedFiles = cleanFiles

        