import datetime
import logging


# ロガーフォーマット
class CustomFormatter(logging.Formatter):
    converter=datetime.datetime.fromtimestamp
    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            s = ct.timestamp()
        return s
        
class DisplayFormatter(logging.Formatter):
    converter=datetime.datetime.fromtimestamp
    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            t = ct.strftime("%Y-%m-%d %H:%M:%S.%f")
            s = "%s.%03d" % (t, record.msecs)
        return s