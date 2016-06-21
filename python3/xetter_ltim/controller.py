from pyjapc import PyJapc
import json

class Settings():

    DEV = 'Devices'
    USR = 'Users'
    PROP = 'Properties'
    CLA = 'Class'

    DBDATA_FILENAME = 'db.json'
    SPSUSERS_FILENAME = 'sps_users_description.txt'

class DBData(dict):

    def __init__(self, data=None):
        # self.data = { Settings.CLA : {'LTIM'   : {Settings.PROP : ['ExpertSetting', 'LoadEvent'],
        #                                             Settings.DEV  : ['dummyLTIMDev1', 'dummyLTIMDev2', 'dummyLTIMDev3'] }, 
        #                                 'ALLVTU' : {Settings.PROP : ['Mode', 'NormalMode'], 
        #                                             Settings.DEV  : ['dummyALLVTUDev1', 'dummyALLVTUDev2'] }             }, 
        #               Settings.USR : [['1', 'dummyUser1', 'dummy user 1'], [...... 'dummyUser2', 'dummyUser3']  }
        
        # with open('temp.txt', 'w') as fd:
        #     fd.write(json.dumps(self.data))
        #     fd.close()
            

        # empty dict
        self.data = {}
        # load classes from db.json
        with open(Settings.DBDATA_FILENAME, 'r') as fd:
            self.data[Settings.CLA] = json.loads(fd.read())
        # load users from sps_users.txt
        # with open(Settings.SPSUSERS_FILENAME, 'r') as fd:
        #     sps_users_list = [line.rstrip('\n') for line in fd.readlines()]
        #     self.data[Settings.USR] = sps_users_list
        with open(Settings.SPSUSERS_FILENAME, 'r') as fd:
            sps_users_list2d = [line.split(None, 2) for line in fd.readlines()]
            self.data[Settings.USR] = sps_users_list2d
        print ('Loaded data: ' + str(self.data))
        
        dict.__init__(self, self.data)


class AcqData(dict):

    def __init__(self):
        dict.__init__(self, {})

    def addData(self, dev, user, prop, data):
        print('AcqData::addData: dev = '+dev)

        if dev in self:
            devData = self[dev]
        else:
            devData = {}

        if user in devData:
            userData = devData[user]
        else:
            userData = {}

        userData[prop] = data
        devData[user] = userData
        self[dev] = devData

    def getParameterNames(self, dev, prop):
        any_user_name = list(self[dev])[0]
        return list(self[dev][any_user_name][prop])
            
    def getParameterValue(self, dev, user, prop, pa):
        p = self[dev][user][prop]
        return p[pa]

    def getUserIDs(self, dev):
        users = list(self[dev])
        ids = [ Controller._data_getIDByUser(user) for user in users]
        print ('ids = '+str(ids))
        return ids



class Controller():

    dbdata = DBData()

    def __init__(self):

        self.pj = PyJapc(selector='will be set later', incaAcceleratorName="SPS", noSet=False)

        self.data = self.dbdata
        self.query = {Settings.CLA : 'LTIM', 
                      Settings.PROP : 'ExpertSetting', 
                      Settings.DEV : ['RFAGSPS1-0-1', 'RFAGSPS1-0-2'], 
                      Settings.USR : ['LHC1', 'LHC2', 'LHC3'] }

        self._acqData = None #_acqdata_fake_doAcquire()

    # @property
    # def acqData(self):
    #     print ('acqdata type = '+str(type(self._acqData)))
    #     return self._acqData

                    
    def acquireData(self):
        self._acqdata_doAcquire()

    def _acqdata_doAcquire(self):
        data = AcqData()

        dev = self._query_getDevice()

        for user in self._query_getUsers():
            print ('user = '+user)
            prop = self._query_getProperty()
            pdata = self.__acquireProp(dev, user, prop)
            data.addData(dev, user, prop, pdata)
                
        for u in data[dev].keys():
            print('DONE: ' +str(data[dev][u]))
        self._acqData = data

    # def _fake__acquireProp(self, aDev, aUser, aProp):
    #     prop_data  = {'ena' : False, 'delay' : 777, 'something else' : 'else'   }
    #     # 'SFTPRO2' :         { 'ExpertSetting' : {'ena' : True,  'delay' : 666, 'something else' : 'else'   },
    #     #                       'LoadEvent'     : {'loadEvent' : 'SIX.F1KFO'} },
    #     return prop_data

    def __acquireProp(self, aDev, aUser, aProp):
        '''
        Do the pyjapc call to the hardware to read the data
        '''
        prop_str = aDev + '/' + aProp
        print('pj: '+ prop_str + ' @' + aUser)
        self.pj.setSelector('SPS.USER.'+aUser)
        prop_val = self.pj.getParam(prop_str)
        print('pj: '+str(prop_val))
        #prop_data  = {'ena' : False, 'delay' : 777, 'something else' : 'else'   }

        # 'SFTPRO2' :         { 'ExpertSetting' : {'ena' : True,  'delay' : 666, 'something else' : 'else'   },
        #                       'LoadEvent'     : {'loadEvent' : 'SIX.F1KFO'} },
        return prop_val


    def _acqdata_getParameterNames(self, dev, prop):
        print('dev = '+str(dev))
        if not self._acqData:
            return ['no data']
        return self._acqData.getParameterNames(dev, prop)
            
    def _acqdata_getParameterValue(self, dev, user, prop, pa):
        if not self._acqData:
            return 'no data'
        return self._acqData.getParameterValue(dev, user, prop, pa)

    def _acqdata_getUserIDs(self, dev):
        if not self._acqData:
            return []
        return sorted(self._acqData.getUserIDs(dev))

    # DBData by default, can also be called on AcqData 

    def _data_getClasses(self, data=None):
        if not data: 
            data = self.data
        return data[Settings.CLA].keys()
        
    def _data_getDevices(self, aClass, data=None):
        if not data: 
            data = self.data
        return data[Settings.CLA][aClass][Settings.DEV]

    def _data_getUsers(self, data=None):
        if not data: 
            data = self.data
        return data[Settings.USR]

    def _data_getUserNames(self, data=None):
        if not data: 
            data = self.data
        return [u[1] for u in self._data_getUsers(data)]

    def _data_getUserIDs(self, data=None):
        if not data: 
            data = self.data
        return [u[0] for u in self._data_getUsers(data)]

    def _data_getUserByID(self, uID):
        for u in self._getUsers(self.data):
            if u[0] == uID:
                return u[1]
        raise RuntimeError("UserID not found: "+ str(uID))

    @staticmethod
    def _data_getUserByID(uID):
        for u in Controller.dbdata[Settings.USR]:
            if u[0] == uID:
                return u[1]
        raise RuntimeError("UserID not found: "+ str(uID))
    
    @staticmethod
    def _data_getIDByUser(user):
        for u in Controller.dbdata[Settings.USR]:
            if u[1] == user:
                return u[0]
        raise RuntimeError("User not found: "+ user)

    def __data_loadFile(self):
        pass
        # fd = open(self.DB_FILENAME, 'r')
        # self.data = json.loads(fd.read())

    def __data_saveFile(self):
        pass
        # import shutil
        # import time
        # ts = str(time.strftime('%y%m%d_%H%M%S', time.localtime(time.time())))
        # shutil.move(Settings.DB_FILENAME, Settings.DB_FILENAME+'.bak_'+ts)
        # with open(Settings.DB_FILENAME, 'w') as fd:
        #     fd.write(json.dumps(self.data))
        #     fd.close()

    def getData(self, dataType, cla="LTIM"):
        print('getData = '+dataType)
        if dataType == Settings.DEV:
            return self.data[Settings.CLA][cla][Settings.DEV]
        elif dataType == Settings.CLA:
            return list(self.data[Settings.CLA])
        elif dataType == Settings.USR:
            return [ x[1] for x in self.data[Settings.USR]] # return the names only
        elif dataType == Settings.PROP:
            return self.data[Settings.CLA][cla][Settings.PROP]
        else:
            raise RuntimeError("Unknown dataType requested: "+dataType)

    def update(self, dataType, val):
        print('update = '+dataType)
        cla = self._query_getClass()
        if dataType == Settings.DEV:
            d = self.data[Settings.CLA][cla][Settings.DEV]
        elif dataType == Settings.CLA:
            d = self.data[Settings.CLA]
        elif dataType == Settings.USR:
            raise RuntimeError("User list cannot be changed")
        elif dataType == Settings.PROP:
            d = self.data[Settings.CLA][cla][Settings.PROP]
        else:
            raise RuntimeError("Unknown dataType requested to update: "+dataType)

        if val in d:
            d.remove(val)
        else:
            d.append(val)

    def getQuery(self):
        return self.query

    def _query_getUsers(self):
        return self.query[Settings.USR]

    def _query_getDevice(self):
        ' Takes the first devices only'
        d = self.query[Settings.DEV]
        if isinstance(d, list):
            return d[0]
        elif isinstance(d, str):
            return d
        else:
            raise RuntimeError('unknown type')
    
    def _query_getProperty(self):
        return self.query[Settings.PROP]

    def _query_getClass(self):
        return self.query[Settings.CLA]

    def updateQuery(self, field, val):
        print('updateQuery = '+field+' : '+str(val))
        self.query[field] = val
        self.infoFrame.infoFrameCallback()


    def addCallbackInfoFrame(self, infoFrame):
        self.infoFrame = infoFrame


