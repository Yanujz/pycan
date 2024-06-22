# Copyright 2024 Yanujz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
class UDSSubFunction:
    def __init__(self, id, name, comment):
        self._id = id
        self._name = name
        self._comment = comment

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def comment(self):
        return self._comment


class UDSNegativeResponseCode:
    def __init__(self, id, mnemonic, name, comment):
        self._id = id
        self._mnemonic = mnemonic
        self._name = name
        self._comment = comment

    @property
    def id(self):
        return self._id

    @property
    def mnemonic(self):
        return self._mnemonic

    @property
    def name(self):
        return self._name

    @property
    def comment(self):
        return self._comment


class UDSServiceInfo:
    def __init__(self, sid, mnemonic, name, comment, subfunctions=None):
        self._sid = sid
        self._mnemonic = mnemonic
        self._name = name
        self._comment = comment
        self._subfunctions = {
                    sub_func.id: sub_func for sub_func in subfunctions} if subfunctions else {}
        
    @property
    def sid(self):
        return self._sid

    @property
    def mnemonic(self):
        return self._mnemonic

    @property
    def name(self):
        return self._name

    @property
    def comment(self):
        return self._comment

    @property
    def subfunctions(self):
        return list(self._subfunctions.values())


class UDSUtility:
    SID_INFO = {
        0x10: UDSServiceInfo(0x10, "DSC", "DiagnosticSessionControl", "DiagnosticSessionControl service is used to change diagnostic sessions in the server(s). In each diagnostic session, a different set of diagnostic services (and/or functionalities) is enabled in the server. The server shall always be in exactly one diagnostic session.",
                             [UDSSubFunction(0x01, "DefaultSession", "Default Session"), UDSSubFunction(0x02, "ProgrammingSession", "Programming Session"), UDSSubFunction(0x03, "ExtendedSession", "Extended Session"), UDSSubFunction(0x04, "SystemSafetyDiagnosticSession", "System Safety Diagnostic Session")]),
        0x11: UDSServiceInfo(0x11, "ER", "ECUReset", "ECUReset service is used by the client to request a server reset.",
                             [UDSSubFunction(0x00, "HardReset", "Perform a hard reset"), UDSSubFunction(0x01, "KeyOffOn", "Perform a key off/on reset"),
                              UDSSubFunction(0x02, "SoftReset", "Perform a soft reset"), UDSSubFunction(0x03, "EnableRapidPowerShutDown", "Enable rapid power shut down")]),
        0x14: UDSServiceInfo(0x14, "CDI", "ClearDiagnosticInformation", "ClearDiagnosticInformation service is used by the client to clear all diagnostic information (DTC and related data) in one or multiple servers' memory."),
        0x19: UDSServiceInfo(0x19, "RDTCI", "ReadDTCInformation", "ReadDTCInformation service allows the client to read from any server or group of servers within a vehicle, current information about all Diagnostic Trouble Codes. This could be the status of reported Diagnostic Trouble Code (DTC), the number of currently active DTCs, or any other information returned by supported ReadDTCInformation SubFunctions."),
        0x22: UDSServiceInfo(0x22, "RDBI", "ReadDataByIdentifier", "ReadDataByIdentifier service allows the client to request data record values from the server identified by one or more DataIdentifiers (DIDs)."),
        0x23: UDSServiceInfo(0x23, "RMB", "ReadMemoryByAddress", "ReadMemoryByAddress service allows the client to request server's memory data stored under the provided memory address."),
        0x24: UDSServiceInfo(0x24, "RSDI", "ReadScalingDataByIdentifier", "ReadScalingDataByIdentifier service allows the client to request from the server a scaling data record identified by a DataIdentifier (DID). The scaling data contains information such as data record type (e.g., ASCII, signed float), formula and its coefficients used for value calculation, units, etc."),
        0x27: UDSServiceInfo(0x27, "SA", "SecurityAccess", "SecurityAccess service allows the client to unlock functions/services with restricted access."),
        0x28: UDSServiceInfo(0x28, "CC", "CommunicationControl", "CommunicationControl service allows the client to switch on/off the transmission and/or the reception of certain messages on a server(s)."),
        0x29: UDSServiceInfo(0x29, "AU", "Authentication", "Authentication service provides a means for the client to prove its identity, allowing it to access data and/or diagnostic services, which have restricted access for, for example security, emissions, or safety reasons."),
        0x2A: UDSServiceInfo(0x2A, "RDBPI", "ReadDataByPeriodicIdentifier", "ReadDataByPeriodicIdentifier service allows the client to request the periodic transmission of data record values from the server identified by one or more periodicDataIdentifiers."),
        0x2C: UDSServiceInfo(0x2C, "DDDI", "DynamicallyDefineDataIdentifier", "DynamicallyDefineDataIdentifier service allows the client to dynamically define in a server a DataIdentifier (DID) that can be read via the ReadDataByIdentifier_ service at a later time."),
        0x2E: UDSServiceInfo(0x2E, "WDBI", "WriteDataByIdentifier", "WriteDataByIdentifier service allows the client to write information into the server at an internal location specified by the provided DataIdentifier (DID)."),
        0x2F: UDSServiceInfo(0x2F, "IOCBID", "InputOutputControlByIdentifier", "InputOutputControlByIdentifier service allows the client to substitute a value for an input signal, internal server function and/or force control to a value for an output (actuator) of an electronic system."),
        0x31: UDSServiceInfo(0x31, "RC", "RoutineControl",
                             "RoutineControl service allows the client to execute a defined sequence of steps to obtain any relevant result. There is a lot of flexibility with this service, but typical usage may include functionality such as erasing memory, resetting or learning adaptive data, running a self-test, overriding the normal server control strategy.",
                             [UDSSubFunction(0x01, "StartRoutine", "Start routine"), UDSSubFunction(0x02, "StopRoutine", "Start routine"), UDSSubFunction(0x03, "ResultRoutine", "Routine result")]),
        0x34: UDSServiceInfo(0x34, "RD", "RequestDownload", "RequestDownload service allows the client to initiate a data transfer from the client to the server (download)."),
        0x35: UDSServiceInfo(0x35, "RU", "RequestUpload", "RequestUpload service allows the client to initiate a data transfer from the server to the client (upload)."),
        0x36: UDSServiceInfo(0x36, "TD", "TransferData", "TransferData service is used by the client to transfer data either from the client to the server (download) or from the server to the client (upload)."),
        0x37: UDSServiceInfo(0x37, "RTE", "RequestTransferExit", "RequestTransferExit service is used by the client to terminate a data transfer between the client and server."),
        0x38: UDSServiceInfo(0x38, "RFT", "RequestFileTransfer", "RequestFileTransfer service allows the client to initiate a file data transfer either from the server to the client (upload) or from the server to the client (upload)."),
        0x3D: UDSServiceInfo(0x3D, "WMB", "WriteMemoryByAddress", "WriteMemoryByAddress service allows the client to write information into the server's memory data under the provided memory address."),
        0x3E: UDSServiceInfo(0x3E, "TP", "TesterPresent", "TesterPresent service is used by the client to indicate to a server(s) that the client is still connected to a vehicle and certain diagnostic services and/or communication that have been previously activated are to remain active."),
        0x84: UDSServiceInfo(0x84, "SDT", "SecuredDataTransmission", "SecuredDataTransmission service is applicable if a client intends to use diagnostic services defined in this document in a secured mode. It may also be used to transmit external data, which conform to some other application protocol, in a secured mode between a client and a server. A secured mode in this context means that the data transmitted is protected by cryptographic methods."),
        0x85: UDSServiceInfo(0x85, "CDTCS", "ControlDTCSetting", "ControlDTCSetting service allows the client to stop or resume the updating of DTC status bits in the server(s) memory."),
        0x86: UDSServiceInfo(0x86, "ROE", "ResponseOnEvent", "ResponseOnEvent service allows the client to request from the server to start or stop transmission of responses on a specified event."),
        0x87: UDSServiceInfo(0x87, "LC", "LinkControl", "LinkControl service allows the client to control the communication between the client and the server(s) in order to gain bus bandwidth for diagnostic purposes (e.g., programming)."),
    }

    @staticmethod
    def is_valid_sid(sid):
        """
        Check if a Service Identifier (SID) is valid.
        """
        return sid in UDSUtility.SID_INFO

    @staticmethod
    def get_sid(sid):
        """
        Get the information (comment) associated with a Service Identifier (SID).
        """
        return UDSUtility.SID_INFO.get(sid, UDSServiceInfo(0xFF, "Unknown SID", "Unknown SID"))

    @staticmethod
    def get_sub_function(sid, sub_func_id):
        """
        Get the information (comment) associated with a Sub-Function Identifier (SubFuncID) for a given Service Identifier (SID).
        """
        service_info = UDSUtility.SID_INFO.get(sid)
        if service_info:
            return service_info._subfunctions.get(sub_func_id, UDSSubFunction(0xFF, "Unknown SubFunc", "Unknown SubFunc"))
        else:
            return UDSSubFunction(0xFF, "Unknown SubFunc", "Unknown SubFunc")

    NRC_INFO = {
        0x10: UDSNegativeResponseCode(0x10, "GR", "GeneralReject", "The requested action has been rejected by the server."),
        0x11: UDSNegativeResponseCode(0x11, "SNS", "ServiceNotSupported", "The requested action will not be taken because the server does not support the requested service."),
        0x12: UDSNegativeResponseCode(0x12, "SFNS", "SubFunctionNotSupported", "The requested action will not be taken because the server does not support the service-specific parameters of the request message."),
        0x13: UDSNegativeResponseCode(0x13, "IMLIFE", "IncorrectMessageLengthOrInvalidFormat", "The requested action will not be taken because the length of the received request message does not match the prescribed length for the specified service or the format of the parameters do not match the prescribed format for the specified service."),
        0x14: UDSNegativeResponseCode(0x14, "RTL", "ResponseTooLong", "The response to be generated exceeds the maximum number of bytes available by the underlying network layer."),
        0x21: UDSNegativeResponseCode(0x21, "BR", "BusyRepeatRequest", "The server is temporarily too busy to perform the requested operation."),
        0x22: UDSNegativeResponseCode(0x22, "CNC", "ConditionsNotCorrect", "The requested action will not be taken because the server prerequisite conditions are not met."),
        0x24: UDSNegativeResponseCode(0x24, "RSE", "RequestSequenceError", "The requested action will not be taken because the server expects a different sequence of request messages or message as sent by the client."),
        0x25: UDSNegativeResponseCode(0x25, "NRSC", "NoResponseFromSubnetComponent", "The server has received the request but the requested action could not be performed by the server as a subnet component necessary to supply the requested information did not respond within the specified time."),
        0x26: UDSNegativeResponseCode(0x26, "FPE", "FailurePreventsExecutionOfRequestedAction", "The requested action will not be taken because a failure condition, identified by a DTC, has occurred and that this failure condition prevents the server from performing the requested action."),
        0x31: UDSNegativeResponseCode(0x31, "ROR", "RequestOutOfRange", "The requested action will not be taken because the server has detected that the request message contains a parameter which attempts to substitute a value beyond its range of authority."),
        0x33: UDSNegativeResponseCode(0x33, "SAD", "SecurityAccessDenied", "The requested action will not be taken because the server's security strategy has not been satisfied by the client."),
        0x34: UDSNegativeResponseCode(0x34, "AR", "AuthenticationRequired", "The requested service will not be taken because the client has insufficient rights based on its Authentication state."),
        0x35: UDSNegativeResponseCode(0x35, "IK", "InvalidKey", "The server has not given security access because the key sent by the client did not match with the key in the server's memory."),
        0x36: UDSNegativeResponseCode(0x36, "ENTAO", "ExceedNumberOfAttempts", "The requested action will not be taken because the client has unsuccessfully attempted to gain security access more times than the server's security strategy will allow."),
        0x37: UDSNegativeResponseCode(0x37, "RTDNE", "RequiredTimeDelayNotExpired", "The requested action will not be taken because the client's latest attempt to gain security access was initiated before the server's required timeout period had elapsed."),
        0x38: UDSNegativeResponseCode(0x38, "SDTR", "SecureDataTransmissionRequired", "The requested service will not be taken because the requested action is required to be sent using a secured communication channel."),
        0x39: UDSNegativeResponseCode(0x39, "SDTNA", "SecureDataTransmissionNotAllowed", "This message was received using the SecuredDataTransmission service, but the requested action is not allowed to be sent using the SecuredDataTransmission service."),
        0x3A: UDSNegativeResponseCode(0x3A, "SDVF", "SecureDataVerificationFailed", "The message failed in the security sub-layer."),
        0x50: UDSNegativeResponseCode(0x50, "CVF-ITP", "CertificateVerificationFailed_InvalidTimePeriod", "Date and time of the server does not match the validity period of the Certificate."),
        0x51: UDSNegativeResponseCode(0x51, "CVF-IS", "CertificateVerificationFailed_InvalidSignature", "Signature of the Certificate could not be verified."),
        0x52: UDSNegativeResponseCode(0x52, "CVF-ICT", "CertificateVerificationFailed_InvalidChainOfTrust", "The Certificate could not be verified against stored information about the issuing authority."),
        0x53: UDSNegativeResponseCode(0x53, "CVF-ITY", "CertificateVerificationFailed_InvalidType", "The Certificate does not match the current requested use case."),
        0x54: UDSNegativeResponseCode(0x54, "CVF-IF", "CertificateVerificationFailed_InvalidFormat", "The Certificate could not be evaluated because the format requirement has not been met."),
        0x55: UDSNegativeResponseCode(0x55, "CVF-IC", "CertificateVerificationFailed_InvalidContent", "The Certificate could not be verified because the content does not match."),
        0x56: UDSNegativeResponseCode(0x56, "CVF-IS", "CertificateVerificationFailed_InvalidScope", "The scope of the Certificate does not match the contents of the server."),
        0x57: UDSNegativeResponseCode(0x57, "CVF-IC", "CertificateVerificationFailed_InvalidCertificate", "The Certificate received from the client is invalid because the server has revoked access for some reason."),
        0x58: UDSNegativeResponseCode(0x58, "OVF", "OwnershipVerificationFailed", "Delivered Ownership does not match the provided challenge or could not be verified with the own private key."),
        0x59: UDSNegativeResponseCode(0x59, "CCF", "ChallengeCalculationFailed", "The challenge could not be calculated on the server side."),
        0x5A: UDSNegativeResponseCode(0x5A, "SARF", "SettingAccessRightsFailed", "The server could not set the access rights."),
        0x5B: UDSNegativeResponseCode(0x5B, "SKCOF", "SessionKeyCreationOrDerivationFailed", "The server could not create or derive a session key."),
        0x5C: UDSNegativeResponseCode(0x5C, "CDUF", "ConfigurationDataUsageFailed", "The server could not work with the provided configuration data."),
        0x5D: UDSNegativeResponseCode(0x5D, "DAF", "DeAuthenticationFailed", "DeAuthentication was not successful, server could still be unprotected."),
        0x70: UDSNegativeResponseCode(0x70, "UDNA", "UploadDownloadNotAccepted", "An attempt to upload/download to a server's memory cannot be accomplished due to some fault conditions."),
        0x71: UDSNegativeResponseCode(0x71, "TDS", "TransferDataSuspended", "A data transfer operation was halted due to some fault. The active transferData sequence shall be aborted."),
        0x72: UDSNegativeResponseCode(0x72, "GPF", "GeneralProgrammingFailure", "The server detected an error when erasing or programming a memory location in the permanent memory device (e.g. Flash Memory)."),
        0x73: UDSNegativeResponseCode(0x73, "WBSC", "WrongBlockSequenceCounter", "The server detected an error in the sequence of blockSequenceCounter values."),
        0x78: UDSNegativeResponseCode(0x78, "RCRRP", "RequestCorrectlyReceived_ResponsePending", "The request message was received correctly, and that all parameters in the request message were valid, but the action to be performed is not yet completed, and the server is not yet ready to receive another request."),
        0x7E: UDSNegativeResponseCode(0x7E, "SFNSIAS", "SubFunctionNotSupportedInActiveSession", "The requested action will not be taken because the server does not support the requested SubFunction in the currently active session."),
        0x7F: UDSNegativeResponseCode(0x7F, "SNSIAS", "ServiceNotSupportedInActiveSession", "The requested action will not be taken because the server does not support the requested service in the currently active session."),
        0x81: UDSNegativeResponseCode(0x81, "RTH", "RpmTooHigh", "The requested action will not be taken because the server prerequisite condition for RPM is not met."),
        0x82: UDSNegativeResponseCode(0x82, "RTL", "RpmTooLow", "The requested action will not be taken because the server prerequisite condition for RPM is not met."),
        0x83: UDSNegativeResponseCode(0x83, "EIR", "EngineIsRunning", "Required for those actuator tests which cannot be actuated while the engine is running."),
        0x84: UDSNegativeResponseCode(0x84, "EINR", "EngineIsNotRunning", "Required for those actuator tests which cannot be actuated unless the engine is running."),
        0x85: UDSNegativeResponseCode(0x85, "ERTL", "EngineRunTimeTooLow", "The requested action will not be taken because the server prerequisite condition for engine run time is not met."),
        0x86: UDSNegativeResponseCode(0x86, "TTH", "TemperatureTooHigh", "The requested action will not be taken because the server prerequisite condition for temperature is not met."),
        0x87: UDSNegativeResponseCode(0x87, "TTL", "TemperatureTooLow", "The requested action will not be taken because the server prerequisite condition for temperature is not met."),
        0x88: UDSNegativeResponseCode(0x88, "VSTH", "VehicleSpeedTooHigh", "The requested action will not be taken because the server prerequisite condition for vehicle speed is not met."),
        0x89: UDSNegativeResponseCode(0x89, "VSTL", "VehicleSpeedTooLow", "The requested action will not be taken because the server prerequisite condition for vehicle speed is not met."),
        0x8A: UDSNegativeResponseCode(0x8A, "TPTLH", "ThrottleOrPedalTooHigh", "The requested action will not be taken because the server prerequisite condition for throttle/pedal position is not met."),
        0x8B: UDSNegativeResponseCode(0x8B, "TPTLL", "ThrottleOrPedalTooLow", "The requested action will not be taken because the server prerequisite condition for throttle/pedal position is not met."),
        0x8C: UDSNegativeResponseCode(0x8C, "TRNIN", "TransmissionRangeNotInNeutral", "The requested action will not be taken because the server prerequisite condition for being in neutral is not met."),
        0x8D: UDSNegativeResponseCode(0x8D, "TRNIG", "TransmissionRangeNotInGear", "The requested action will not be taken because the server prerequisite condition for being in gear is not met."),
        0x8F: UDSNegativeResponseCode(0x8F, "BSOSNC", "BrakeSwitchOrSwitchesNotClosed", "For safety reasons, this is required for certain tests before it begins, and shall be maintained for the entire duration of the test."),
        0x90: UDSNegativeResponseCode(0x90, "SLNIP", "ShifterLeverNotInPark", "For safety reasons, this is required for certain tests before it begins, and shall be maintained for the entire duration of the test."),
        0x91: UDSNegativeResponseCode(0x91, "TCCL", "TorqueConvertClutchLocked", "The requested action will not be taken because the server prerequisite condition for torque converter clutch is not met."),
        0x92: UDSNegativeResponseCode(0x92, "VTH", "VoltageTooHigh", "The requested action will not be taken because the server prerequisite condition for voltage at the primary pin of the server (ECU) is too high."),
        0x93: UDSNegativeResponseCode(0x93, "VTL", "VoltageTooLow", "The requested action will not be taken because the server prerequisite condition for voltage at the primary pin of the server (ECU) is too low."),
        0x94: UDSNegativeResponseCode(0x94, "RTNA", "ResourceTemporarilyNotAvailable", "The requested action will not be taken because the server's normal operating mode is temporarily inhibited, e.g., because it is busy or temporarily out of service. The client may repeat the request, but it should be tried less often in the future."),
    }

    @staticmethod
    def is_valid_nrc(id):
        """
        Check if a Negative Response Code (NRC) is valid.
        """
        return id in UDSUtility.NRC_INFO

    @staticmethod
    def get_nrc(id):
        """
        Get the information (comment) associated with a Negative Response Code (NRC).
        """
        return UDSUtility.NRC_INFO.get(id, UDSNegativeResponseCode(0xFF, "Unknown NRC", "Unknown NRC"))


def main():
    print(UDSUtility.get_sub_function(0x11, 0x00).comment)


if __name__ == '__main__':
    main()
