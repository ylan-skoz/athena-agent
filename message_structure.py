class MESSAGE_STRUCTURE:
    ID = "id"

    class TYPE:
        NAME = "type"

        PING = "ping"
        TELEMETRY = "telemetry"
        COMMAND = "command"
        NOTIFICATION = "notification"
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
