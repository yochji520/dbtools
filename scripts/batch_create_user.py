#-*- coding: utf-8 -*-

import sys;
reload(sys);
sys.setdefaultencoding("utf8")
import time
import logging
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.cloudaudit.v20190319 import cloudaudit_client, models
from tencentcloud.cdb.v20170320 import cdb_client, models
import yaml,os


"""
class LogtoLog(object):
    def __init__(self, logger=None):
        #指定保存日志的文件路径，日志级别，以及调用文件将日志存入到指定的文件中
        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.INFO)
        # 创建一个handler，用于写入日志文件
        self.log_time = time.strftime("%Y_%m_%d_")
        self.log_path = "./"
        self.log_name = self.log_path + self.log_time + 'running.log'

        fh = logging.FileHandler(self.log_name, 'a', encoding='utf-8')
        fh.setLevel(logging.INFO)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # 定义handler的输出格式
        formatter = logging.Formatter('[%(asctime)s] %(filename)s-->%(funcName)s line:%(lineno)d [%(levelname)s]%(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

        # 关闭打开的文件
        fh.close()
        ch.close()

    def getlog(self):
        return self.logger
"""


class UserManager(object):
    """腾讯云账号管理"""
    """
    @:param user
    """
    def __init__(self,**userinfo):
        self.user = userinfo['user']
        self.host = userinfo['host']
        self.passwd = userinfo['passwd']
        self.instance_id = userinfo['instance_id']

    #连接认证
    def client_auth(self, secret_id=None,secret_key=None):
        try:
            cred = credential.Credential(secret_id, secret_key)
            httpProfile = HttpProfile()
            httpProfile.endpoint = "cdb.tencentcloudapi.com"
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = cdb_client.CdbClient(cred, "ap-guangzhou", clientProfile)
            return client
        except TencentCloudSDKException as err:
            print err
            logging.info(err)

    #创建cdb用户
    def create_user(self):
        description = "DBA管理账号"
        client = UserManager().client_auth(self.secret_id,self.secret_key)
        try:
            req = models.CreateAccountsRequest()
            params = {"InstanceId":self.instance_id,"Accounts":[{"User":self.user,"Host":self.host}],\
                      "Password":self.passwd,"Description":description}
            req.from_json_string(params)
            resp = client.CreateAccounts(req)
            print(resp.to_json_string())
            logging.info(resp.to_json_string())
        except TencentCloudSDKException as err:
            print(err)
            logging.info("创建用户失败" + err)

    #删除用户
    def delete_user(self):
        try:
            client = UserManager().client_auth(self.secret_id, self.secret_key)
            req = models.DeleteAccountsRequest()
            params = {"InstanceId":self.instance_id,"Accounts":[{"User":self.user, "Host":self.host}]}
            req.from_json_string(params)
            resp = client.DeleteAccounts(req)
            print(resp.to_json_string())
            logging.info(resp.to_json_string())
        except TencentCloudSDKException as err:
            print(err)
            logging.info("删除用户失败:" +  err)

    #赋予用户权限
    def give_power(self):
        try:
            client = UserManager().client_auth(self.secret_id, self.secret_key)
            req = models.ModifyAccountPrivilegesRequest()
            params = {"InstanceId":self.instance_id,"Accounts":[{"User":self.user,"Host":self.host}],' \
                     '"GlobalPrivileges":["SELECT","INSERT","UPDATE","DELETE","CREATE",' \
                     ' "PROCESS", "DROP","REFERENCES","INDEX","ALTER","SHOW DATABASES",' \
                     '"CREATE TEMPORARY TABLES","LOCK TABLES","EXECUTE","CREATE VIEW",' \
                     '"SHOW VIEW","CREATE ROUTINE","ALTER ROUTINE","EVENT","TRIGGER"]}
            req.from_json_string(params)
            resp = client.ModifyAccountPrivileges(req)
            print(resp.to_json_string())
            logging.info(resp.to_json_string())
        except TencentCloudSDKException as err:
            print(err)
            logging.info("赋予用户权限失败:" + err)


def pull_all_instanceid():
    """
    拉取所有实例信息
    @:return instanceid_list 返回CDB实例ID列表，
    """
    try:
        # 生成认证对象
        client = UserManager().client_auth(secret_id,secret_key)
        req = models.DescribeDBInstancesRequest()
        # 传入参数,返回实例信息数量，返回信息默认20，最大值2000,
        params = '{"Limit":200}'
        req.from_json_string(params)
        resp = client.DescribeDBInstances(req)
        instanceid_list = []
        for ins_list in resp.Items:
            instance_list.append(str(ins_list.InstanceId))
        return instanceid_list
    except TencentCloudSDKException as err:
        print(err)

if __name__ == '__main__':
    secret_id = "AKIDHgqkNQpl35LOCkv7xXrGQL0PaV9XhKL5"
    secret_key = "gEWYBZOyJQIuIm23pLblmaU91iAVcTA6"
    instance_list = pull_all_instanceid(secret_id,secret_key)
    conf_path = os.path.dirname(os.path.relpath("usermanager.yaml"))
    print conf_path
    #for instance in instance_list:
    #    pass
