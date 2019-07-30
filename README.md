# FTP2MQTT

This service acts as FTP server. A surveillance camera can use this FTP server. Each image that is sent from a camera is then published to a MQTT broker.

## Options

| Option        | Default Value  | Description  |
| ------------- |:-------------:| -----:|
| MQTT_BROKER_HOST | 127.0.0.1 | MQTT broker address |
| MQTT_BROKER_PORT      | 1883      |   MQTT broker port |
| MQTT_PUBLISH_SUBJECT | cameras/ftpuser/image | Subject the image is published to |
| FTP_SERVER_PORT | 2121      |    FTP server port |
| FTP_SERVER_PASSIVE_PORTS_MIN | 60000      |    FTP server passive ports min value |
| FTP_SERVER_PASSIVE_PORTS_MAX | 60100      |    FTP server passive ports max value |
| FTP_SERVER_USERNAME | Not set | FTP server username |
| FTP_SERVER_PASSWORD | Not set | FTP server password |

If both FTP_SERVER_USERNAME and FTP_SERVER_PASSWORD are set the FTP server accepts only connection with these credentials. Otherwise the server accepts anonymous connections.

Options can be set by using environment variables.

## Build

```
docker build . -t ftpd
```

## Run

```
docker run --rm -p 2121:2121 -p 60000-60099:60000-60099 -e MQTT_BROKER_HOST=mymqttbroker ftpd
```
You must expose at least the listening port for the FTP server and the passive ports range. 
