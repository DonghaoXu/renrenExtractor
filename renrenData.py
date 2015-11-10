# coding: utf8



class user:
  def __init__(self, userDict):
    self.userId = userDict['userId']
    self.userName = userDict['userName']
    self.education = userDict['education']
    self.favoriteStuff = userDict['favoriteStuff']
    self.sex = userDict['sex']
    self.dateBirth = userDict['dateBirth']
    self.hometown = userDict['hometown']
    self.friendList = userDict['friendList']

  def makeFriend(anna, zelo):
    if anna not in zelo.friendList:
      zelo.friendList.append(anna)
    if zelo not in anna.friendList:
      anna.friendList.append(zelo)



class talk:
  def __init__(self, talkDict):
    self.statusId = talkDict['statusId']
    self.author = talkDict['authorId']
