import os
import sys

from engines import EtherpadFullEngine, EtherpadSectionEngine
from tempfile import NamedTemporaryFile
from ConfigParser import SafeConfigParser

def runCommand(cmd):
    '''Run given command interactively. Return command exit code.'''
    cmd = cmd.split()
    code = os.spawnvpe(os.P_WAIT, cmd[0], cmd, os.environ)
    if code == 127:
        sys.stderr.write('{0}: command not found\n'.format(cmd[0]))
    return code

def recordConsole(engine, logfile):
    engine.start()
    runCommand('script -f ' + logfile)
    engine.stop()

def parseArgs(args):
    logfile = NamedTemporaryFile(delete=True).name
    print 'Using temp file: ',logfile
    padID = args['<padID>']
    doSection = args['--section']
    marker = args['--marker']

    defaultConfig = {
            'apikey'  : 'no-api-key',
            'baseurl': 'http://localhost:9001/api'
        }
    config = SafeConfigParser(defaultConfig)
    config.add_section('shelter')
    if args['--config']:
        config.read(args['--config'])
    apikey = config.get('shelter', 'apikey')
    baseurl = config.get('shelter', 'baseurl')

    doMain(apikey, padID, marker, baseurl, logfile, doSection)


def doMain(apikey, padID, marker, baseurl, logfile, doSection):
    if doSection:
        engine = EtherpadSectionEngine(apikey, padID, targetFile=logfile, marker=marker, base_url=baseurl)
    else:
        engine = EtherpadFullEngine(apikey, padID, targetFile=logfile, base_url=baseurl)
    recordConsole(engine, logfile)
