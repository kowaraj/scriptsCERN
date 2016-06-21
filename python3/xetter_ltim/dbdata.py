

class DBData():

    def __init__(self, data=None):

        self.data = { self.CLASS : {'name' : self.CLASS, 
                                    'data' : [ {'name' : 'LTIM',   'properties' : ['ExpertSetting', 'LoadEvent']},
                                               {'name' : 'ALLVTU', 'properties' : ['Mode', 'NormalMode']} ]   }
                      self.DEV : {'name' : self.DEV, 
                                  'data' : ['dummyDev1', 'dummyDev2', 'dummyDev3']}
                      self.USR : {'name' : self.USR, 
                                  'data' : ['dummyUser1', 'dummyUser2', 'dummyUser3']}  }

        # Report:
        
        # print("Number of users      : "+ str(len(self.getUsers())))
        # prNames = self.getPropertyNames()
        # print("Number of properties : "+ str(len(prNames)))
        # for n in prNames:
        #     print("Number of parameters : "+ str(len(self.getParameterNames(n))))

            
    def getUserIDs(self):
        return self.userID.values()

    def getUserByID(self, uID):
        for k in self.userID:
            if self.userID[k] == uID:
                return k
        raise RuntimeError("UserID not found: "+ str(uID))

    def getUsers(self):
        return self.data.keys()

    def getPropertyNames(self):
        '''
        Return all the property names (any user)
        '''
        any_user_name = list(self.data)[0]
        return self.data[any_user_name].keys()
    
    def getParameterNames(self, prop):
        '''
        Return names of all the parameter names of the property (any user)
        '''
        any_user_name = list(self.data)[0]
        any_user_prop = self.data[any_user_name][prop]
        return any_user_prop.keys()
            
    def getParameters(self, user, prop):
        '''
        Return parameters dict for the user, the property
        '''
        return self.data[user][prop]

    def getParameterValue(self, user, prop, pa):
        '''
        Return parameters dict for the user, the property
        '''
        return self.data[user][prop][pa]


