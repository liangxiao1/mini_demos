import rpyc

conn = rpyc.connect("192.168.50.12", 9002)
with open("/home/xiliang/clones/xiliang/mypro/pi/pics/ca.jpg", "rb") as fd:
    contents = fd.read()
conn.root.write(contents)
print(conn.root.resnet50("test.jpg"))