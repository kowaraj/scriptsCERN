from pyjapc import PyJapc
import json

import tkinter
from tkinter import *
from tkinter import messagebox



class Settings():

    DEV = 'Devices'
    USR = 'Users'
    PROP = 'Properties'
    CLA = 'Class'

    #DBDATA_FILENAME = 'db_IonBA3LTIM.json'
    #DBDATA_FILENAME = 'db_Lab864LTIM.json'
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

        self.setquery = {'Parameter' : '',
                         'Value' : '', 
                         'Type' : ''}

        self._acqData = None #_acqdata_fake_doAcquire()
        self._xframes = []


    def addXFrame(self, f):
        self._xframes.append(f)

    # @property
    # def acqData(self):
    #     print ('acqdata type = '+str(type(self._acqData)))
    #     return self._acqData

                    
    def acquireData(self):
        self._acqdata_doAcquire()

    def _acqdata_doAcquire(self):
        data = AcqData()

        for dev in self._query_getDevices():

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

    def getClassSelected(self):
        return self._query_getClass()

    def getData(self, dataType):
        
        cla=self.getClassSelected()
        print('clas = '+str(cla))

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

        elif dataType == Settings.CLA: # special case for classes (as it's a dict, not a list)
            d = self.data[Settings.CLA]
            if val in d:
                del d[val]
            else:
                d[val] = {Settings.DEV : ["dummyDev0"], Settings.PROP : ["dummyProp0"]}

            self.__saveDB()
            return 

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

        self.__saveDB()


    def __saveDB(self):
        import shutil
        shutil.move(Settings.DBDATA_FILENAME, Settings.DBDATA_FILENAME+'.bak')
        with open(Settings.DBDATA_FILENAME, 'w') as fd:
            fd.write(json.dumps(self.data[Settings.CLA]))
            fd.close()

                                                                
    def getQuery(self):
        return self.query

    def _query_getUsers(self):
        return self.query[Settings.USR]

    def _query_getDevices(self):
        ' Takes the first devices only'
        d = self.query[Settings.DEV]
        if not isinstance(d, list):
            raise RuntimeError('unknown type')
        return d

    
    def _query_getProperty(self):
        return self.query[Settings.PROP]

    def _query_getClass(self):
        return self.query[Settings.CLA]

    def updateQuery(self, field, val):
        print('updateQuery = '+field+' : '+str(val))
        self.query[field] = val
        self.infoFrame.infoFrameCallback()

        if field == Settings.CLA:
            self.updateXFrameDevices()
            self.updateXFrameProperties()
            

    def updateXFrameDevices(self):
        for f in self._xframes:
            if f._name == Settings.DEV:
                f.update()

    def updateXFrameProperties(self):
        for f in self._xframes:
            if f._name == Settings.PROP:
                f.update()

        

    def addCallbackInfoFrame(self, infoFrame):
        self.infoFrame = infoFrame
    def addCallbackSetFrame(self, setFrame):
        self.setFrame = setFrame

    def _setquery_changed(self):
        self.setFrame.setFrameCallback()

    def _setquery_setParameter(self, name, val):
        self.setquery['Parameter'] = name
        self.setquery['Value'] = val
        self._setquery_changed()


    def getSetQuery(self):
        return self.setquery

    # def _setquery_setParameterName(self, name):
    #     self.setquery['Parameter'] = name
    #     self.setFrame._tvLabelSetVal = name
    #     print('done')
    def _setquery_setParameterValue(self, value):
        self.setquery['Value'] = value
        self._setquery_changed()

    def _setquery_setParameterType(self, vtype):
        self.setquery['Type'] = vtype
        self._setquery_changed()

    def _driveHardware(self):
        print('Writing...\n param: '+ str(self.setquery['Parameter']) + '\n' + 'value: '+ str(self.setquery['Value']))
        print('read-query:\n param: '+ str(self.query))

        param = self.setquery['Parameter']
        val = self.setquery['Value']
        vtype = self.setquery['Type']

        devs_ = str(self._query_getDevices())
        user_ = str(self._query_getUsers())
        prop_ = str(self._query_getProperty())
        warning_msg = "Devices:\n"+devs_  \
                       +"\nUsers:\n"+user_  \
                       +"\nProperty:\n"+prop_ \
                       +"\nParameter:\n"+param \
                       +"\nValue = "+str(val) \
                       +"\nType = "+str(vtype)

        if not tkinter.messagebox.askyesno("Set?", warning_msg):
            return

        # Do it...
        for dev in self._query_getDevices():
            for user in self._query_getUsers():
                print ('user = '+user)
                prop = self._query_getProperty()
                self.__setParameter(dev, user, prop, param, val, vtype)

    def __setParameter(self, aDev, aUser, aProp, aParam, val, vtype='int'):
        '''
        Do the pyjapc call to the hardware to _write_ the data
        '''
        prop_str = aDev + '/' + aProp
        #print('pj: read: '+ prop_str + ' @' + aUser)
        self.pj.setSelector('SPS.USER.'+aUser)
        prop_data = self.pj.getParam(prop_str)
        
        # prop_types = self.pj.getParamInfo(prop_str)
        # print('types = '+str(prop_types))

        new_prop_data = self.__replaceParamValueInProperty(prop_data, aParam, val, vtype)

        #input('sure?')
        self.pj.setSelector('SPS.USER.'+aUser)
        prop_val = self.pj.setParam(prop_str, new_prop_data)
        print('done.')
        

    def __replaceParamValueInProperty(self, prop_data, param, val, vtype='int'):
        # print('pj: read: '+str(prop_data))
        # print('pj: read: '+str(type(prop_data)))
        # print('pj: read: param = '+str(param))
        # print('pj: read: param = '+str(val))
        # print('pj: read: param = '+str(type(val)))
        if vtype == '':
            converted_val = int(val)
        elif vtype == 'int':
            converted_val = int(val)
        elif vtype == 'float':
            converted_val = float(val)
        elif vtype == 'bool':
            converted_val = bool(val)
        elif vtype == 'str':
            converted_val = str(val)
        else:
            raise RuntimeError("Only [int,float,bool,str] types allowed")

        prop_data[param] = converted_val
        # print('pj: read: '+str(prop_data))
        return prop_data
        



