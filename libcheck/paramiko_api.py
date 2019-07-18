#/usr/bin/python
#coding=utf-8

import paramiko

class mySSH:
    def __init__(self,hostip,username):
        self.hostip = hostip
        #self.port = port
        self.username = username
        #self.password = password
        self.obj = None
        self.objsftp = None


    # connect to client and open sftp
    def connect_with_sftp(self):
        try:
            self.obj = paramiko.SSHClient()
            self.obj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # self.obj.connect(self.hostip,self.port,self.username,self.password)
            self.obj.connect(hostname=self.hostip, username=self.username)
            self.objsftp = self.obj.open_sftp()
        except Exception, e:
            return (False, str(e))
        else:
            return (True, 'OK')

    # connect to client only
    def connect(self):
        try:
            self.obj = paramiko.SSHClient()
            self.obj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # self.obj.connect(self.hostip,self.port,self.username,self.password)
            self.obj.connect(hostname=self.hostip, username=self.username)
        except Exception,e:
            return (False,str(e))
        else:
            return (True,'OK')

    # run command on remote
    def run_cmd(self,cmd):
        stdin,stdout,stderr = self.obj.exec_command(cmd)
        return stdout

    # run multi-command on remote
    def run_cmdlist(self,cmdlist):
        self.resultList = []
        for cmd in cmdlist:
            stdin,stdout,stderr = self.obj.exec_command(cmd)
            self.resultList.append(stdout)
        return self.resultList

    # get remote file via sftp
    def get(self,remotepath,localpath):
        try:
            self.objsftp.get(remotepath,localpath)
        except Exception,e:
            return (False,str(e))
        else:
            return (True,'OK')

    # put file to remote via sftp
    def put(self,localpath,remotepath):
        try:
            self.objsftp.put(localpath,remotepath)
        except Exception,e:
            return (False,str(e))
        else:
            return (True,'OK')

    '''
    def getTarPackage(self,path):
        list = self.objsftp.listdir(path)
        for packageName in list:
            stdin,stdout,stderr  = self.obj.exec_command("cd " + path +";"
                                                         + "tar -zvcf /tmp/" + packageName
                                                         + ".tar.gz " + packageName)
            stdout.read()
            self.objsftp.get("/tmp/" + packageName + ".tar.gz","/tmp/" + packageName + ".tar.gz")
            self.objsftp.remove("/tmp/" + packageName + ".tar.gz")
            print "get package from " + packageName + " ok......"
    '''

    # close ssh
    def close(self):
        if self.objsftp is not None:
            self.objsftp.close()
        if self.obj is not None:
            self.obj.close()