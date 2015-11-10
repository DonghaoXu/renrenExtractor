# coding: utf-8
import urllib2, urllib, re, bs4, json
import Logging

Logging.Logging.flag = True
class renren:
  def __init__(self, cookie):
    self.headers = {'cookie': cookie}
    self.__userId = self.userId()

  def userId(self):
    idPattern = re.compile(r'\Wid=([0-9]+);')
    ids = idPattern.findall(cookie)
    if len(ids) < 1:
      Logging.Logging.error(u'The cookie doesn''t contain user ID.')
      return None
    else:
      Logging.Logging.info(u'>>> Logged user ID: ' + ids[0])
      return ids[0]

  def fetchStatus(self, userId=None, page=1):
    # Collect status of the given id
    # If id is none, id = the logged id, self.__id
    if userId is None:
      userId = self.__userId
    if userId is None:
      return
    Logging.Logging.info(u'>>> Fetching target: ' + str(userId) + '/Status')
    # Fetch the status url with the requested page
    Logging.Logging.info(str(userId) + u'/Status>>> Fetching page ' + str(page) + u'...')
    queryData = {
      'userId': userId,
      'curpage': page - 1
    }
    url = 'http://status.renren.com/GetSomeomeDoingList.do?' + urllib.urlencode(queryData)
    statusResponse = self.fetchURL(url).read()
    # Parse & Save data
    # statusJson is a list of status
    statusJson = json.loads(statusResponse)['doingArray']
    if len(statusJson) < 1:
      Logging.Logging.error(str(userId) + u'/Status>>> Incorrect user ID or page number! Fetching STOPPED!')
      return
    status = []
    conversation = []
    for stat in statusJson:
      # status info
      status.append({
        'userId': userId,
        'userName': stat['name'],
        'statusId': int(stat['id']),
        'statusDate': stat['dtime'],
        'isPrivate': False,
        'statusContent': stat['content'],
      })
      # conversation info by status ID
      queryData = {
        'limit': 20,
        'desc': 'true',
        'offset': 0,
        'replaceUBBLarge': 'true',
        'type': 'status',
        'entryId': int(stat['id']),
        'entryOwnerId': str(userId)
      }
      url = 'http://comment.renren.com/comment/xoa2?' + urllib.urlencode(queryData)
      commentResponse = self.fetchURL(url).read()
      # commentJson is a list of comments json objects
      commentJson = json.loads(commentResponse)['comments']
      for comment in commentJson:
        conversation.append({
          'statusId': int(stat['id']),
          'authorId': comment['authorId'],
          'authorName': comment['authorName'],
          'commentId': comment['commentId'],
          'isWhisper': comment['isWhisper'],
          'commentDate': comment['time'],
          'like': comment['like']['count'],
          'commentContent': comment['content']
        })
    Logging.Logging.success(str(userId) + u'>>> Fetching status DONE!')
    return {
      'status': status,
      'comment': conversation
    }

  def fetchURL(self, url, data=None, headers=None):
    if headers is None:
      headers = self.headers
    req = urllib2.Request(url, data = data, headers = headers)
    response = urllib2.urlopen(req)
    return response

  def statusOutput(self, statusDict, dir):
    if dir is None:
      dir = 'Status_NotGivenThenALoooooooooooooongName.txt'
    try:
      fh = open(dir, 'a')
      for stat in statusDict['status']:
        pass
    except:
      return




    

if __name__ == '__main__':
  cookie = raw_input('Enter your cookie: ')
  rr = renren(cookie)
  dd = rr.fetchStatus(page=10)
  print dd['comment'][0]



