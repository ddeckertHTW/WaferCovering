import datetime

def logMessage(message):
    timestamp = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]  # Truncate microseconds to milliseconds
    print(f'{timestamp} - {message}')

def getLogMessageString(message, startTimestamp = None):
    timestamp = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]  # Truncate microseconds to milliseconds
    testvar = datetime.datetime.now() - startTimestamp if startTimestamp is not None else None
    return({'message': message,
            'timeSinceStart': (datetime.datetime.now() - startTimestamp) if startTimestamp else None, 
            'timestamp': timestamp,  
            })
