import json


class DBDict:

    K_PROP    = 'property'
    K_PARAM   = 'parameter'
    K_DEV_SRC = 'device' #
    K_USR_SRC = 'user' #
    K_DEV_DST = 'device_dst'
    K_USR_DST = 'user_dst'

    '''
    dict = {'devices' : [
                     { 'name'         : 'VTUFrevAllawake1', 
                       'class'        : 'ALLVTULHC', 
                       'fec'          : 'cfv-ba3-allawake3', 
                       'pers-data'    : 'du-name.class-name', 
                       'copy-in-file' : 'filename'...'
                     }
                     ...
                    ]
        'classes' : [
                     {'name' : 'ALLVTULHC', 'properties' : ['Mode', 'Status', ..], ...
                     ...
                    ]

    '''

    DB_FILENAME = 'db.json'

    def __init__(self):
        pass
        # with open(self.DB_FILENAME, 'r') as fd:
        #     self.data = json.loads(fd.read())
        
        # with open('sps_users.txt', 'r') as fd:
        #     for l in fd.readlines():
        #         self.data[self.K_USR_SRC].append(l.rstrip(' ').rstrip('\n'))
        # self.__saveDB()
            
#        print(self.data[self.K_USR_SRC])

        
    def __saveDB(self):
        import shutil
        shutil.move(self.DB_FILENAME, self.DB_FILENAME+'.bak')
        with open(self.DB_FILENAME, 'w') as fd:
            fd.write(json.dumps(self.data))
            fd.close()
        
    def updateDB(self, name):
        if name in self.data[self.K_DEV_SRC]:
            self.data[self.K_DEV_SRC].remove(name)
        else:
            self.data[self.K_DEV_SRC].append(name)
        self.__saveDB()
