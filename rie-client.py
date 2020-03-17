import bernhard

c = bernhard.Client(host='localhost', port=5555)
#(bernhard is a dependency you will need to include)
data = {
    'host': 'myhost.foobar.com',
    'service': 'test',
    'tags': ["running"],
    'metric': 1.23,
}
c.send(data)