from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import ClientException
from httplib import HTTPException

# We want to put all the CRAB project directories from the tasks we submit here into one common directory.
# That's why we need to set this parameter (here or above in the configuration file, it does not matter, we will not overwrite it).
from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.section_("General")
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = False

config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PbPbSkimAndTree2015_DiMuContBoth_cfg.py'

config.section_('Data')
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/HI/Cert_262548-263757_PromptReco_HICollisions15_JSON_MuonPhys_v2.txt'
config.Data.runRange = '262548-263757'
config.Data.publication = False
config.JobType.allowUndistributedCMSSW = False

config.section_('Site')
config.Data.ignoreLocality = True
config.Site.whitelist = ['T1_US_*','T1_FR_*','T2_US_*','T2_CH_CERN']
config.Site.storageSite = 'T2_CH_CERN'

def submit(config):
    try:
        crabCommand('submit', config = config, dryrun=False)
    except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
    except ClientException as cle:
        print "Failed submitting task: %s" % (cle)

#############################################################################################
## From now on that's what users should modify: this is the a-la-CRAB2 configuration part. ##
#############################################################################################

dataMap = {
            "HISingleMuon": { "PD": "/HIEWQExo/HIRun2015-PromptReco-v1/AOD", "Units": 8, "Memory": 1600, "RunTime": 1180 },
            "HIDoubleMuon0": { "PD": "/HIOniaL1DoubleMu0/HIRun2015-PromptReco-v1/AOD", "Units": 4, "Memory": 1200, "RunTime": 1180 },
            "HIDoubleMuon1": { "PD": "/HIOniaL1DoubleMu0B/HIRun2015-PromptReco-v1/AOD", "Units": 4, "Memory": 1200, "RunTime": 1180 },
            "HIDoubleMuon2": { "PD": "/HIOniaL1DoubleMu0C/HIRun2015-PromptReco-v1/AOD", "Units": 4, "Memory": 1200, "RunTime": 1180 },
            "HIDoubleMuon3": { "PD": "/HIOniaL1DoubleMu0D/HIRun2015-PromptReco-v1/AOD", "Units": 4, "Memory": 1200, "RunTime": 1180 },
            "HIDoubleMuonPeri": { "PD": "/HIOniaPeripheral30100/HIRun2015-PromptReco-v1/AOD", "Units": 8, "Memory": 1400, "RunTime": 1180 },
            "HIForward": { "PD": "/HIForward/HIRun2015-PromptReco-v1/AOD", "Units": 16, "Memory": 1400, "RunTime": 700 }
          }

## Submit the muon PDs
for key, val in dataMap.items():
    config.General.requestName = 'VertexCompositeTree_'+key+'_HIRun2015_DiMuMassMin7_20190420'
    config.Data.inputDataset = val["PD"]
    config.Data.unitsPerJob = val["Units"]
    config.JobType.maxMemoryMB = val["Memory"]
    config.JobType.maxJobRuntimeMin = val["RunTime"]
    config.Data.outputDatasetTag = config.General.requestName
    config.Data.outLFNDirBase = '/store/group/phys_heavyions/%s/RiceHIN/PbPb2015/TREE/%s' % (getUsernameFromSiteDB(), config.General.requestName)
    print("Submitting CRAB job for: "+val["PD"])
    submit(config)
