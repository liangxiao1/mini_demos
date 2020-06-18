#!/usr/bin/env python
'''
github : https://github.com/liangxiao1/mini_demos

This demo is a simple rpc server with service provided for check ec2 instance status.

'''
import rpyc
from rpyc.utils.server import ThreadedServer
import boto3
from botocore.exceptions import ClientError

class AWSService(rpyc.Service):
    def exposed_vm_state(self, instanceid, region):
        if instanceid == None:
            return {'Error': "which instanceid do you get?"}
        region = region
        if region == None:
            region = 'us-west-2'
        try:
            ec2 = boto3.resource('ec2', region_name=region)
            instance = ec2.Instance(instanceid)
            instance.reload()
            instance.state
        except ClientError as err:
            return {instanceid: '%s' % err}
        return {'instanceid': instanceid,
               'state': instance.state,
               'IP':instance.public_ip_address}

if __name__ == "__main__":
    server = ThreadedServer(AWSService, port = 9002)
    server.start()