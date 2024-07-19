class MESSAGE_STRUCTURE:
    DEVICE_ID = "device_id"
    ID = "id"

    class TYPE:
        NAME = "type"

        DATA = 'data'

        PING = "ping"
        TELEMETRY = "telemetry"
        COMMAND = "command"
        NOTIFICATION = "notification"
        NOTIFICATION_RESPONSE = "notification_response"
        ACKNOWLEDGE = "acklowledge"


    class TELEMETRY:
        
        class STATUS:
            KEY = "status"

            RECEIVED = "RECEIVED"
            FAILED = "failed"
            

    class ACKNOWLEDGE:

        class STATUS:
            
            NAME = "status" 

            RECEIVED = "received"
            FAILED = "failed"
