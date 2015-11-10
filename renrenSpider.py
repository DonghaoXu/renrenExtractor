# coding: utf-8
import urllib2, urllib, re, bs4, json
import Logging

Logging.Logging.flag = True
badFileName = '_NotGivenThenALoooooooooooooongName'


class renren:
  def __init__(self, cookie):
    self.headers = {'cookie': cookie}
    self.__userId = self.userId()

  def userId(self):
    idPattern = re.compile(r'\Wid=([0-9]+);')
    ids = idPattern.findall(self.headers['cookie'])
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
    userId = str(userId)
    Logging.Logging.info(u'>>> Fetching target: ' + userId + '/Status')
    # Fetch the status url with the requested page
    Logging.Logging.info(userId + u'/Status>>> Fetching page ' + str(page) + u'...')
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
      Logging.Logging.error(userId + u'/Status>>> Incorrect user ID or page number! Fetching STOPPED!')
      return
    status = []
    for stat in statusJson:
      # Retrieve each comment under the status
      queryData = {
        'limit': 20,
        'desc': 'true',
        'offset': 0,
        'replaceUBBLarge': 'true',
        'type': 'status',
        'entryId': int(stat['id']),
        'entryOwnerId': userId
      }
      url = 'http://comment.renren.com/comment/xoa2?' + urllib.urlencode(queryData)
      commentResponse = self.fetchURL(url).read()
      # commentJson is a list of comments json objects
      commentJson = json.loads(commentResponse)['comments']
      conversation = []
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
      # Retrieve like number for the status
      queryData = {
        'stype': 'status',
        'sourceId': int(stat['id']),
        'owner': userId,
        'gid': 'status_' + str(int(stat['id'])),
        'uid': userId
      }
      url = 'http://like.renren.com/showlikedetail?' + urllib.urlencode(queryData)
      likeResponse = self.fetchURL(url).read()
      likeJson = json.loads(likeResponse)
      # status info
      status.append({
        'userId': userId,
        'userName': stat['name'],
        'statusId': int(stat['id']),
        'statusDate': stat['dtime'],
        'isPrivate': False,
        'like': likeJson['likeCount'],
        'statusContent': stat['content'],
        'comments': conversation
      })
    Logging.Logging.success(userId + u'/Status>>> Fetching page ' + str(page) + ' DONE!')
    return status

  def fetchGossip(self, userId=None, page=1):
    # If id is none, id = the logged id, self.__id
    if userId is None:
      userId = self.__userId
    if userId is None:
      return
    userId = str(userId)
    Logging.Logging.info(u'>>> Fetching target: ' + userId + '/Gossip')
    # Fetch the gossip url with the requested page
    Logging.Logging.info(userId + u'/Gossip>>> Fetching page ' + str(page) + u'...')
    queryData = {
      'userId': userId,
      # 'curpage': -1,
      # 'destpage': 0,
      # 'hostBeginId': None,
      # 'hostEndId': None,
      # 'guestBeginId': None,
      # 'guestEndId': None,
      'page': page - 1,
      'id': userId
    }
    url = 'http://gossip.renren.com/ajaxgossiplist.do'
    gossipResponse = self.fetchURL(url, urllib.urlencode(queryData)).read()
    gossipJson = json.loads(gossipResponse)['array']
    gossips = []
    for gossip in gossipJson:
      gossips.append({
        'gossipId': gossip['id'],
        'authorId': gossip['guestId'],
        'authorName': gossip['guestName'],
        'owner': gossip['owner'],
        'gossipDate': gossip['time'],
        'gossipContent': gossip['filterOriginalBody']
      })
    Logging.Logging.success(userId + u'/Gossip>>> Fetching page ' + str(page) + ' DONE!')
    return gossips
      


  def fetchURL(self, url, data=None, headers=None):
    if headers is None:
      headers = self.headers
    req = urllib2.Request(url, data = data, headers = headers)
    response = urllib2.urlopen(req)
    return response

  def statusOutput(self, statusDict, fname=None):
    if fname is None:
      fname = 'Status' + badFileName
    try:
      Logging.Logging.info(u'Printing status and comments to ' + badFileName)
      fh = open(fname, 'a')
      for stat in statusDict:
        fh.write(('Date: ' + stat['statusDate'] + '\t' + stat['userName'] + '\n').encode('utf8'))
        fh.write((stat['statusContent'] + '\n').encode('utf8'))
        for comment in stat['comments']:
          fh.write(('\tDate: ' + comment['commentDate'] + '\t' + comment['authorName'] +'\n').encode('utf8'))
          fh.write(('\t' + comment['commentContent'] + '\n').encode('utf8'))
      fh.close()
      Logging.Logging.success(u'Printing DONE!')
    except:
      Logging.Logging.error(u'Error')
      return

  def gossipOutput(self, gossipDict, fname=None):
    if fname is None:
      fname = 'Gossip' + badFileName
    try:
      Logging.Logging.info(u'Printing gossips to ' + fname)
      fh = open(fname, 'a')
      for gossip in gossipDict:
        fh.write(('Date: ' + gossip['gossipDate'] + '\t' + gossip['authorName'] + '\n').encode('utf8'))
        fh.write((gossip['gossipContent'] + '\n').encode('utf8'))
      fh.close()
      Logging.Logging.success(u'Printing DONE!')
    except:
      Logging.Logging.error(u'Error')
      return
  

if __name__ == '__main__':
  cookie = raw_input('Enter your cookie: ')
  rr = renren(cookie)
  dd = rr.fetchGossip()
  rr.gossipOutput(dd)



