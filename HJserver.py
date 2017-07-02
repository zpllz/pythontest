import sys, socket
import os
import base64

host = '127.0.0.1'
port = 51234
respond = '''
HTTP/1.1 200 OK
Content-Type: %s
Content-Length: %d

'''

badrespond = '''
HTTP/1.1 200 OK
Content-Type: %s
Content-Length: 0

'''


text = 'text/html'
img = ''


ssd = open('property.xml')
ssp = ssd.read()
ssd.close()
ssp = map(lambda x:x.strip(), ssp.split('\n'))



error404 = '''
HTTP/1.1 404 Not Found

'''


DEFAULTFILE = 'example.htm'#'index.html'


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(10)


print 'Server is running on port %d; press ctrl-C to stop' % port
i = 0
while True:
    print 'Waiting...'
    clientsock, clientaddr = s.accept()
    i = i+1
    print '<%d> times connected!' % i
    print '>> ClientSock:', clientsock#, ', Name:', clientsock.getpeername()
    print '>> ClientAddress:', clientaddr
    
    while True:
        line = clientsock.recv(2048)
        if line=='':
            break


        print '{'
        print line
        print '}'
        if 'GET' in line:
            end = line.index('HTTP')-1
            if '?' in line:
                end = min(end, line.index('?'))
            fname = line[4 : end]       
            print '>>want file', fname
            if fname=='/':# or fname=='/index.html':
                print '>> want default index.html' 
                fd = open(DEFAULTFILE)
                opfile = fd.read()
                #print opfile
                clientsock.sendall(respond % (text, len(opfile)) + opfile)
                fd.close()
            else:
                print '>>searching!'
                cpath = os.getcwd()
                try:
                    fd = open(cpath+fname)
                except: # not exist
                    print '<<No such file!'
                    clientsock.sendall(error404)
                    clientsock.sendall(badrespond % text)
                    
                    
                else:   # exist
                    print '>> cpath:', cpath
                    print '>> fname', fname
                    retval = ''
                    
                    sdx = fname.index('.')+1
                    l = list(fname)
                    l.reverse()
                    sdx = max(sdx, len(l)-l.index('.'))

                    extname = fname[sdx:]
                    print '>> extname', extname
                    for rule in ssp:
                        if rule[1:rule.index('=')] == extname:
                            retval = rule[rule.index('=')+1:]      
                            break
                    print '#############>> match:', retval
                    if retval!='':
                        # here is a test
                        if extname=='png' or extname=='jpg':
                            opfile = base64.b64encode(fd.read())
                            print '>>ready, to be sent'
                            #############
                            clientsock.sendall(respond % (retval, len(opfile)) + opfile)
                            #############
                            
                            clientsock.sendall(badrespond % text)
                            print '>>file sent out'
                        else:
                        # here is a test
                            opfile = fd.read()
                            print '>>ready, to be sent'
                            ####
                            
                            #clientsock.sendall()
                            ###
                            clientsock.sendall(respond % (retval, len(opfile)) + opfile)

                            clientsock.sendall(badrespond % text)

                            print '>>file sent out'
                    else:
                        print '<<No such extension name!'
                        clientsock.sendall(error404)
                        clientsock.sendall(badrespond % text)
                  
                
    clientsock.close()
    print '<%d> connection done' % i










