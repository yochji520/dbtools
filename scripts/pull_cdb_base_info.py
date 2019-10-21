#-*- coding: utf-8 -*-

import sys;
reload(sys);
sys.setdefaultencoding("utf8")



# 腾讯云认证KEY
SECRET_ID = "AKIDHgqkNQpl35LOCkv7xXrGQL0PaV9XhKL5"
SECRET_Key = "gEWYBZOyJQIuIm23pLblmaU91iAVcTA6"

class InstanceInfo:
    """
    @:description : 拉取腾讯云实例信息列表,并生成execl文件
    @:author : jack.you
    @:time :2019-10-15
    @:parameter
    """
    def __init__(self):
        pass

    InstanceId = None
    InstanceName = None
    Vip = None
    RoGroups = {}
    EngineVersion = None
    Cpu = None

    #初始化日志
    def init_log(self,):
        import os,datetime
        try:
            if not os.path.exists("Log"):
                os.mkdir("Log")
            nowtime = datetime.datetime.now()
            self.log_file = open(
                "Log/MergeLog_%d%d%d_%d%d%d.txt" %
                (nowtime.year, nowtime.month, nowtime.day, nowtime.hour, nowtime.minute, nowtime.second), "wb")
        except Exception as e:
            print e
            return -1
        return 0

    #基本信息输出
    def note_log(self,msg):
        import datetime,platform
        nowtime = datetime.datetime.now()
        os = platform.system()
        if os == "Windows":
            s = msg.decode('utf-8')
            print "%s %s" % (nowtime, s)
        elif os == "Linux":
            print "\033[1;34;40m%s %s\033[0m" % (nowtime, msg)
        self.init_log()

    #错误日志
    def error_log(self,msg):
        import datetime,platform
        nowtime = datetime.datetime.now()
        os = platform.system()
        if os == "Windows":
            s = msg.decode('utf-8')
            print "%s %s" % (nowtime, s)
        elif os == "Linux":
            print "\033[1;34;40m%s %s\033[0m" % (nowtime, msg)
        self.write_log('%s %s\n' % (nowtime, msg))

    #写入日志
    def write_log(self,msg):
        try:
            if self.log_file:
                self.log_file.write(msg)
                self.log_file.flush()
        except Exception as e:
            print e
            return -1
        return 0
