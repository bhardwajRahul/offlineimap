# Copyright (C) 2007 John Goerzen
# <jgoerzen@complete.org>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

import offlineimap.version
import urllib
from threading import *

class MachineParsable(UIBase):
    def __init__(s, config, verbose = 0):
        UIBase.__init__(s, config, verbose)
        s.iswaiting = 0
        s.outputlock = Lock()

    def isusable(s):
        return True

    def _printData(s, command, data, dolock = True):
        s._printDataOut(s, 'msg', command, data, dolock)

    def _printWarn(s, command, data, dolock = True):
        s._printDataOut(s, 'warn', command, data, dolock)

    def _printDataOut(s, datatype, command, data, dolock = True):
        if dolock:
            s.outputlock.acquire()
        try:
            print "%s\n%s\n%s\n%s\n" % \
                    (datatype,
                     urllib.quote(command, ' '), 
                     urllib.quote(currentThread().getName(), ' '),
                     urllib.quote(data, ' '))
            sys.stdout.flush()
        finally:
            if dolock:
                s.outputlock.release()

    def acct(s, accountname):
        s._printData('acct', accountname)

    def connecting(s, hostname, port):
        s._printData('connecting', "%s\n%s" % (hostname, str(port)))

    def syncfolders(s, srcrepos, destrepos):
        s._printData('syncfolders', "%s\n%s" % (s.getnicename(srcrepos), 
                                                s.getnicename(destrepos)))

    def syncingfolder(s, srcrepos, srcfolder, destrepos, destfolder):
        s._printData('syncingfolder', "%s\n%s\n%s\n%s\n" % \
                (s.getnicename(srcrepos), srcfolder.getname(),
                 s.getnicename(destrepos), destfolder.getname()))

    def loadmessagelist(s, repos, folder):
        s._printData('loadmessagelist', "%s\n%s" % (s.getnicename(repos),
                                                    folder.getvisiblename()))

    def syncingmessages(s, sr, sf, dr, df):
        s._printData('syncingmessages', "%s\n%s\n%s\n%s\n" % \
                (s.getnicename(sr), sf.getname(), s.getnicename(dr),
                 df.getname()))

    def copyingmessage(s, uid, src, destlist):
        ds = s.folderlist(destlist)
        s._printData('copyingmessage', "%d\n%s\n%s\n%s"  % \
                (uid, s.getnicename(src), src.getname(), ds)
        
    def folderlist(s, list):
        return ("\f".join(["%s\t%s" % (s.getnicename(x), x.getname()) for x in list]))

    def deletingmessage(s, uid, destlist):
        s.deletingmessages(s, [uid], destlist)

    def uidlist(s, list):
        return ("\f".join([str(u) for u in list]))

    def deletingmessages(s, uidlist, destlist):
        ds = s.folderlist(destlist)
        s._printData('deletingmessages', "%s\n%s" % (s.uidlist(uidlist), ds))

    def addingflags(s, uidlist, flags, destlist):
        ds = s.folderlist(destlist)
        s._printData("addingflags", "%s\n%s\n%s" % (s.uidlist(uidlist),
                                                    "\f".join(flags),
                                                    ds))

    def deletingflags(s, uidlist, flags, destlist):
        ds = s.folderlist(destlist)
        s._printData('deletingflags', "%s\n%s\n%s" % (s.uidlist(uidlist),
                                                      "\f".join(flags),
                                                      ds))

    def threadException(s, thread):
        s._printData('threadException', "%s\n%s" % \
                     (thread.getName(), s.getThreadExceptionString(thread)))
        s.delThreadDebugLog(thread)
        s.terminate(100)

    def mainException(s):
        s._printData('mainException', s.getMainExceptionString())

    def threadExited(s, thread):
        s._printData('threadExited', thread.getName())
        UIBase.threadExited(s, thread)

    def sleeping(s, sleepsecs, remainingsecs):
        s._printData('sleeping', "%d\n%d" % (sleepsecs, remainingsecs))
        if sleepsecs > 0:
            time.sleep(sleepsecs)
        return 0






                    

    def getpass(s, accountname, config, errmsg = None):
        s.outputlock.acquire()
        try:
            if errmsg:
                s._printData('getpasserror', "%s\n%s" % (accountname, errmsg),
                             False)
            s._printData('getpass', accountname, False)
            return (sys.stdin.readline()[:-1])
        finally:
            s.outputlock.release()

