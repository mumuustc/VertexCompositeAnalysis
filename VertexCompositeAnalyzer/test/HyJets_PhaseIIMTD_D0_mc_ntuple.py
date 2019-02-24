import FWCore.ParameterSet.Config as cms

process = cms.Process("d0ana")

# initialize MessageLogger and output report
process.load("FWCore.MessageLogger.MessageLogger_cfi")
#process.MessageLogger.cerr.threshold = 'INFO'
#process.MessageLogger.categories.append('Demo')
#process.MessageLogger.cerr.INFO = cms.untracked.PSet(
#        limit = cms.untracked.int32(-1)
#        )
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)
process.options   = cms.untracked.PSet( wantSummary = 
cms.untracked.bool(True) )

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) 
)

process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
'/store/user/yousen/Hydjet_5p02TeV_TuneCP5_MTD/hyjets_mc_mtd_Skim_v1/190207_195017/0000/hyjets_10.root'
                ),
                            )
process.load("VertexCompositeAnalysis.VertexCompositeAnalyzer.d0selector_cff")
process.load("VertexCompositeAnalysis.VertexCompositeAnalyzer.d0analyzer_ntp_cff")

process.TFileService = cms.Service("TFileService",
                                       fileName = 
cms.string('hyjets_mc_mtd.root')
                                   )

process.d0ana_mc.isUseMtd = cms.untracked.bool(True);
process.d0ana_mc.doRecoNtuple = cms.untracked.bool(True);
process.d0ana_mc.doGenNtuple = cms.untracked.bool(True);
process.d0ana_mc.doGenMatching = cms.untracked.bool(False);
process.d0ana_mc.VertexCollection = cms.untracked.InputTag("offlinePrimaryVertices4D")
process.d0ana_mc.VertexCompositeCollection = cms.untracked.InputTag("d0selector:D0")
process.d0ana_mc.MVACollection = cms.InputTag("d0selector:MVAValuesNewD0")
process.d0ana_mc.isCentrality = cms.bool(True)

process.d0selectorMC.VertexCollection = cms.untracked.InputTag("offlinePrimaryVertices4D")

process.d0ana_seq = cms.Sequence(process.d0selectorMC * process.d0ana_mc)

process.p = cms.Path(process.d0ana_seq)