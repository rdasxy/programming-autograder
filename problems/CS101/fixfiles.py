# fix IO files 

import os 
Home = os.getcwd()
SubdirList = os.listdir(Home)
for Sub in SubdirList:
    if os.path.isdir(Sub):
        os.chdir(Sub)
        FileList = os.listdir(os.getcwd())
        for f in FileList: 
            if f.startswith('input'): 
                OutName = f.replace('in', 'out')
                InName = f
                ProgName = 'solution.py'
                CmdLine = 'python %s <%s >%s 2>%s' % (ProgName, InName, OutName, 'err.txt')
                os.system(CmdLine)
                ErrMsg = open('err.txt').read()
                if len(ErrMsg) > 2:
                    print Sub, "Error"
                    continue
                #print InName, '>>>', OutName 
        print Sub, 'OK'
        os.chdir(Home)
            