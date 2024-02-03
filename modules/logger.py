# NOTE: This module has no implementation on the robotRio, 
# so dont have it in your robot code (use for logging output on your personal computer)
import logging

class Logger:
    def __init__(self, filename):    
        logging.basicConfig(filename=filename, 
                            filemode='a', 
                            format='%(message)s',
                            level=logging.DEBUG)
        
        # Write a header so people know where their log output starts and ends
        logging.info('--- Start of Output ---\n')

    def write(self, message):
        # Check message for:
            # DEBUG -> logging.debug()
            # ERROR -> logging.warning()
            # SUCCESS -> logging.info()

        if 'DEBUG:' in message:
            logging.debug(message)

        elif 'ERROR:' in message:
            logging.warning(message)

        elif 'SUCCESS:' in message:
            logging.info(message)

        else:
            print(f'''Logger could not find a logging level in the provided message:\n\t--> {message}''')