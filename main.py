import os
import paho.mqtt.client as mqtt
import tempfile
import sys
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


class MyHandler(FTPHandler):

    def on_connect(self):
        print ("%s:%s connected" , self.remote_ip, self.remote_port)

    def on_disconnect(self):
        # do something when client disconnects
        pass

    def on_login(self, username):
        # do something when user login
        pass

    def on_logout(self, username):
        # do something when user logs out
        pass

    def on_file_sent(self, file):
        # do something when a file has been sent
        
        pass

    def on_file_received(self, file):
        global client
        # do something when a file has been received
        fsize = os.path.getsize(file)
        if fsize > 0:
            print('File received', file, 'with', fsize, 'bytes')
            sys.stdout.flush()
            f = open(file, "rb")
            data = f.read()
            f.close()
            # print(data)
            client.publish(os.environ.get('MQTT_PUBLISH_SUBJECT', "cameras/ftpuser/image"), payload=data, qos=0, retain=False)
            print('published')
        os.remove(file)

    def on_incomplete_file_sent(self, file):
        # do something when a file is partially sent
        pass

    def on_incomplete_file_received(self, file):
        # remove partially uploaded files
        os.remove(file)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    sys.stdout.flush()
    # threading.Thread(target=start_ftp_server).start()

def on_log(client, userdata, level, buf):
    print("MQTT log:", buf)
    sys.stdout.flush()

def on_publish(client, userdata, mid):
    print("Message sent with id", mid)
    sys.stdout.flush()

def main():
    global client 
    mqtt_broker_host = os.environ.get('MQTT_BROKER_HOST', '127.0.0.1')
    mqtt_broker_port = int(os.environ.get('MQTT_BROKER_PORT', '1883'))
    client = mqtt.Client()
    client.on_connect = on_connect
    # client.on_message = on_message
    # client.on_disconnect = on_disconnect
    client.on_log = on_log
    client.on_publish = on_publish

    # print("client.connect")
    client.connect_async(mqtt_broker_host, mqtt_broker_port)
    client.loop_start()

    ftp_server_port = int(os.environ.get('FTP_SERVER_PORT', '2121'))
    ftp_server_passive_ports_min = int(os.environ.get('FTP_SERVER_PASSIVE_PORTS_MIN', '60000'))
    ftp_server_passive_ports_max = int(os.environ.get('FTP_SERVER_PASSIVE_PORTS_MAX', '60100'))
    ftp_server_username = os.environ.get('FTP_SERVER_USERNAME', None)
    ftp_server_password = os.environ.get('FTP_SERVER_PASSWORD', None)
    ftp_server_address = os.environ.get('FTP_SERVER_ADDRESS', '')

    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = DummyAuthorizer()

    if ftp_server_username != None and ftp_server_password != None:
        authorizer.add_user(ftp_server_username, ftp_server_password, '.', perm='w')
    else:
        authorizer.add_anonymous('.', perm='w')

    # Instantiate FTP handler class
    handler = MyHandler
    handler.authorizer = authorizer

    handler.use_sendfile = False

    handler.passive_ports = range(ftp_server_passive_ports_min, ftp_server_passive_ports_max)

    # Instantiate FTP server class and listen on 0.0.0.0:2121
    address = (ftp_server_address, ftp_server_port)
    server = FTPServer(address, handler)

    # set a limit for connections
    server.max_cons = ftp_server_passive_ports_max - ftp_server_passive_ports_min
    server.max_cons_per_ip = 5

    # start ftp server
    server.serve_forever()

if __name__ == '__main__':
    main()