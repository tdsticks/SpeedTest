# -*- coding: utf-8 -*-
import Stickel
import pyspeedtest
import json
import os

__author__ = 'Steve Stickel'
__copyright__ = "Copyright 2016"
__license__ = "GPL"
__maintainer__ = "Steve Stickel"
__email__ = "tdsticks@gmail.com"


class TestSpeed():
    def __init__(self, debug=None):
        self.debug = debug

        self.S = Stickel

        self.log_name = "TestSpeed"

        self.g = self.S.Globals(debug=True)
        self.dateTime = self.S.dateTime.DateTime(debug=False)
        self.fu = self.S.fileUtility.FileUtility(debug=True)

        # Start the logger
        self.l = self.S.logger.Logger(debug=True)
        self.l.create_logger(self.log_name)
        self.l.init_log()

        self.l.log(1, "TestSpeed::__init__")

        # Override the logging
        pyspeedtest.LOG.setLevel(20)

        self.pst = pyspeedtest.SpeedTest(host=None, http_debug=0, runs=10)
        # self.pst = pyspeedtest.SpeedTest()

        get_datetime = self.dateTime.get_fmt_datetime()

        speedTestObj = {}
        speedTestObj["datetime"] = get_datetime
        speedTestObj["download"] = self.test_download_speed()
        speedTestObj["upload"] = self.test_upload_speed()
        speedTestObj["ping"] = str(self.test_ping()) + "Seconds"
        # print "speedTestObj", speedTestObj

        self.speedTestJson = json.dumps(speedTestObj)
        # print "speedTestJson", self.speedTestJson
        self.l.log(1, "speedTestJson:", self.speedTestJson)

        self.write_to_file()

    def test_download_speed(self):
        self.l.log(1, "TestSpeed::test_download_speed")

        return self.pretty_speed(self.pst.download())

    def test_upload_speed(self):
        self.l.log(1, "TestSpeed::test_upload_speed")

        return self.pretty_speed(self.pst.upload())

    def test_ping(self):
        self.l.log(1, "TestSpeed::test_ping")

        self.pst.ping()

        return round(self.pst.ping(), 1)

    def write_to_file(self):
        self.l.log(1, "TestSpeed::write_to_file")

        file_date = self.dateTime.get_fmt_date_for_file()
        file_name = self.log_name + file_date + ".json"
        file_path = self.g.ntwk_path + "data" + self.g.ds + file_name
        # print file_path

        file_data = ""

        # Check to see if the file exists first
        if not os.path.isfile(file_path):
            self.fu.write_file(file_path, "[")
            self.fu.write_file(file_path, self.speedTestJson)
            self.fu.write_file(file_path, "]")
            file_data = self.fu.read_raw_file(file_path)
        else:
            file_data = self.fu.read_raw_file(file_path)
            print "existing file:", file_data

        print "file_data", file_data

        # self.fu.write_file(file_path, self.speedTestJson)

    def pretty_speed(self, speed):
        units = ['bps', 'Kbps', 'Mbps', 'Gbps']
        unit = 0
        while speed >= 1024:
            speed /= 1024
            unit += 1
        return '%0.2f %s' % (speed, units[unit])

if __name__ == '__main__':

    TestSpeed(debug=True)