import time
import datetime
import serial
import requests
import json
import os

class SIM900:
    server_url = "https://smser.benax.rw/services/nesa/api.php"
    def __init__(self, port, baudrate, timeout):
        self.mPort = port
        self.mPBaudrate = baudrate
        self.mTimeout = timeout
        self.mConn = None

    def connect(self):
        try:
            self.mConn = serial.Serial(port=self.mPort, baudrate=self.mPBaudrate, timeout=self.mTimeout)
            return True
        except Exception as e:
            print(str(e))
            return False

    def sendSMS(self, phoneNumber, msg):
        try:
            self.mConn.write('AT+CMGF=1\r'.encode())
            time.sleep(1)

            cmd = 'AT+CMGS="{}"\r'.format(phoneNumber)
            self.mConn.write(cmd.encode())
            time.sleep(1)

            cmd = '{}\r'.format(msg)
            self.mConn.write(cmd.encode())
            time.sleep(1)

            self.mConn.write(bytes([26])) #26bits or 1x1A to mean CTRL+Z
            time.sleep(1)

            return True
        except Exception as e:
            print(str(e))
            return False

    def receiveSMS(self):
        #os.system("clear")
        self.mConn.write(b'AT+CMGDA="DEL ALL"\r\n')
        time.sleep(3)
        msg = self.mConn.read(self.mConn.inWaiting())
        print("Listening for incoming SMS...")
        print("\n*******************************************\n") 
        while True:
            msg = self.mConn.read(self.mConn.inWaiting())
            if msg != b"":  
                try:
                    self.mConn.write(b'AT+CMGR=1\r\n')
                    time.sleep(3)
                    msg = self.mConn.read(self.mConn.inWaiting())
                    
                    # Extracting sender and message from SMS content
                    decoded_msg = msg.decode('utf-8', 'ignore').split("\r\n")
                    content = decoded_msg[1].split(",")            
                    
                    time_received = "20"+(content[3]+" "+content[4]).replace("\"", "").strip().split("+")[0].replace("/","-")
                    sender = content[1].replace("\"", "").strip()
                    message = decoded_msg[2].strip()

                    print("Time:", time_received)
                    print("Sender:", sender)
                    print("Message:", message)
                    self.mConn.read(self.mConn.inWaiting()) 

                except:
                    my_msg = msg.decode('utf-8', 'ignore').strip()
                    if my_msg !="OK" and my_msg !="" and "+CMTI: \"SM\",1" not in my_msg:
                        print(my_msg)
                    self.reset()
                    continue
                
                msg = b''  # Convert the empty string to bytes
                time.sleep(3)
                self.mConn.write(b'AT+CMGDA="DEL ALL"\r\n')
                time.sleep(3)
                print("\n*******************************************\n")           
            time.sleep(5)

    def parseResponse(self):
        #os.system("clear")
        print("Listening for downloaded messages...")
        print("\n*******************************************\n")
        while True:
            response = requests.get(self.server_url)
            if response.status_code == 200:
                try:
                    data = json.loads(response.text)
                    prev_recipient=""
                    prev_msg=""
                    for item in data["topLevel"]:
                        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        recipient = item["recipient"]
                        msg = item["message"]
                        if recipient != "null" and recipient != prev_recipient and msg != prev_msg:
                            self.sendSMS(recipient, msg)
                            time.sleep(1)
                            f=open("/home/pi/smserPiProject/sim900/report.txt","a")
                            f.write("Time: "+timestamp+"\n")
                            f.write("Sent to: "+recipient+"\n")
                            f.write("Message: "+msg+"\n")
                            f.write("\n*******************************************\n")
                            f.close()
                            print("Time:", timestamp)
                            print("To:", recipient)
                            print("Message:", msg)
                            prev_recipient = recipient
                            prev_msg = msg
                            print("\n*******************************************\n")
                            time.sleep(1)
                except (json.JSONDecodeError, KeyError) as e:
                    print("Error parsing response: " + str(e))
            else:
                print("Error retrieving data from server. Status code:", response.status_code)    
                   
            time.sleep(1)
        
    def makeCall(self,phoneNumber):
        try:
            print ("Set call mode")
            self. mConn.write("AT+CMGF=0\r".encode())
            time.sleep(1)
            print ("Start call")

            cmd = "ATD{};\r".format(phoneNumber)
            self.mConn.write(cmd.encode())
            time.sleep(30)
            print ("End call")
        except Exception as e:
            print(str(e))
            return False
        
    def disconnect(self):
        try:
            if self.mConn is not None:
                self.mConn.close()
            return True
        except Exception as e:
            print(str(e))
            return False

    def flush(self):
        try:
            if self.mConn is not None:
                self.mConn.reset_input_buffer()
                self.mConn.reset_output_buffer()
            return True
        except Exception as e:
            print(str(e))
            return False

    def reset(self):
        self.mConn.write(b'AT\r\n')
        time.sleep(0.5)
        self.mConn.write(b"\r\n")
        time.sleep(0.5)
        self.mConn.write(b'ATE0\r\n')  # Disable the Echo
        time.sleep(0.5)
        self.mConn.write(b'AT+CMGF=1\r\n')  # Select Message format as Text mode
        time.sleep(0.5)
    

