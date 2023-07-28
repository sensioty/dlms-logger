import click
import os
import traceback
import dlmslogger.reader.GXDLMSReader as gxreader
from gurux_serial import GXSerial
from gurux_dlms.secure.GXDLMSSecureClient import GXDLMSSecureClient
from gurux_common.enums import TraceLevel
from gurux_common.io import Parity, StopBits, BaudRate
from gurux_dlms.enums import Authentication, ObjectType
from gurux_dlms.objects import GXDLMSObjectCollection
from gurux_dlms import GXDLMSException, GXDLMSExceptionResponse, GXDLMSConfirmedServiceError


class DLMSLogger:
    def __init__(self):
        self.media = GXSerial(None)
        self.trace = TraceLevel.INFO
        self.invocationCounter = None
        self.client = GXDLMSSecureClient(False)  # Use short naming
        self.outputFile = os.getenv(
            "DLMS_LOGGER_OUTPUT_FILE", "dlmsobjects.save")

    def initializeConfiguration(self):

        # Serial settings
        self.media.port = self.getUSBDevice()

        self.media.baudRate = int(
            os.getenv('DLMS_LOGGER_SERIAL_BAUD_RATE', BaudRate.BAUD_RATE_9600))
        self.media.dataBits = int(os.getenv('DLMS_LOGGER_SERIAL_DATA_BITS', 8))
        self.media.parity = Parity[os.getenv(
            'DLMS_LOGGER_SERIAL_PARITY', 'NONE').upper()]
        self.media.stopBits = StopBits[os.getenv('DLMS_LOGGER_SERIAL_STOP_BITS', 'ONE').upper()]

        # Windows Size
        self.client.hdlcSettings.windowSizeRX = self.client.hdlcSettings.windowSizeTX = int(
            os.getenv('DLMS_LOGGER_HDLC_WINDOW_SIZE', '1'))

        # Max Info Size
        self.client.hdlcSettings.maxInfoRX = self.client.hdlcSettings.maxInfoTX = int(
            os.getenv('DLMS_LOGGER_HDLC_FRAME_SIZE', '128'))

        # Authentication mode
        self.client.authentication = self.getAutentication()
        if self.client.authentication == Authentication.LOW:
            pw = os.getenv('DLMS_LOGGER_SECRET')

            if pw:
                self.client.password = pw
            else:
                raise ValueError("Missing DLMS_LOGGER_SECRET.")

        # Client address
        self.client.clientAddress = int(
            os.getenv('DLMS_LOGGER_CLIENT_ADDRESS', '32'))

    def getUSBDevice(self):
        devices = GXSerial.getPortNames()

        for device_name in devices:
            if 'usb' in device_name.lower():
                return device_name

        raise Exception("No usb device found.")

    def getAutentication(self):
        authentication = os.getenv('DLMS_LOGGER_AUTHENTICATION', 'None')

        try:
            if authentication == "None":
                return Authentication.NONE
            elif authentication == "Low":
                return Authentication.LOW
        except Exception:
            raise ValueError(
                f"Invalid authentication option '{authentication}'. (None, Low)")

    def read_data(self):
        try:
            reader = gxreader.GXDLMSReader(self.client, self.media,
                                           self.trace, self.invocationCounter)
            self.media.open()
            read = False
            reader.initializeConnection()
            if self.outputFile and os.path.exists(self.outputFile):
                try:
                    c = GXDLMSObjectCollection.load(self.outputFile)
                    self.client.objects.extend(c)
                    if self.client.objects:
                        read = True
                except Exception:
                    read = False
            if not read:
                reader.getAssociationView()

            # TODO: Use configured values to read and store to file
            objectId = "1.1.10.8.0.255"
            attributeIndex = 2
            obj = self.client.objects.findByLN(ObjectType.REGISTER, objectId)
            if obj is None:
                raise Exception("Unknown logical name:" + objectId)

            val = reader.read(obj, attributeIndex)
            print(val)
            reader.showValue(attributeIndex, val)

            if self.outputFile:
                self.client.objects.save(self.outputFile)

        except (ValueError, GXDLMSException, GXDLMSExceptionResponse, GXDLMSConfirmedServiceError) as ex:
            print(ex)
        except (KeyboardInterrupt, SystemExit, Exception) as ex:
            traceback.print_exc()
            if self.media:
                self.media.close()
            reader = None
        finally:
            if reader:
                try:
                    reader.close()
                except Exception:
                    traceback.print_exc()


@click.command()
def cli():
    logger = DLMSLogger()
    logger.initializeConfiguration()
    logger.read_data()


if __name__ == '__main__':
    cli()
