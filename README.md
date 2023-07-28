# DLMSLogger

Tool that reads data from any DLSM capable smart meter with an infrared reader and writes them to the file system.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install dlmslogger
```

## Usage

```bash
dlms-logger
```

## Configuration

Configuration is done by setting the following env variables:

### DLMS_LOGGER_SERIAL_DEVICE

Set this to /dev/ttyXXX or any other usb device if needed.
Be default we try to auto detect the device.

Default: auto detect

### DLMS_LOGGER_SERIAL_BAUD_RATE

Set the baudrate.

Default: 9600

### DLMS_LOGGER_SERIAL_DATA_BITS

Set serial connection data bits.
 
**Default: 8**

### DLMS_LOGGER_SERIAL_PARITY

Set serial connection parity.

Values: NONE, EVEN, ODD, MARK, SPACE

**Default: NONE**

### DLMS_LOGGER_SERIAL_STOP_BITS 

Set serial connection stop bits.

Values: ONE, TWO, ONE_POINT_FIVE

**Default: ONE**

### DLMS_LOGGER_HDLC_FRAME_SIZE

Set HDLC frame size.

**Default: 128**

### DLMS_LOGGER_HDLC_WINDOW_SIZE

Set HDLC window size

**Default: 1**

### DLMS_LOGGER_AUTHENTICATION 

Set authentication mode. When using mode __Low__ make sure
to set DLMS_LOGGER_SECRET.

Values: None, Low

**Default: None**

### DLMS_LOGGER_SECRET

Set authentication secret

**Default: not set**

### DLMS_LOGGER_CLIENT_ADDRESS 

Set client address.

**Default: 32**

### DLMS_LOGGER_OBJECTS_OUTPUT_FILE

Set the objects output file. This is used to cache the object structure.
Not used to store the values read from the meter.

**Default: dlmsobjects.save**


## License

[GPLv2](https://opensource.org/license/gpl-2-0/)