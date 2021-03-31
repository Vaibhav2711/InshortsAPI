import paramiko
import os
def upload_local_audio_to_remote(outfile,remoteurl):
	ssh =paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(hostname='167.71.225.168',username='root',password='hellohello123')
	sftp=ssh.open_sftp()
	sftp.put(outfile,os.path.join(remoteurl,outfile))
	print("done")
	sftp.close()
	
	
	
