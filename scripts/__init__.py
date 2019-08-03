import logging
import sys
import os


logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s \
    %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


sys.path.append(os.path.abspath('.'))
