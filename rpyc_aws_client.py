import rpyc

conn = rpyc.connect("127.0.0.1", 9002)
print(conn.root.vm_state("i-01acb38a37ba99ae8","us-west-2"))
