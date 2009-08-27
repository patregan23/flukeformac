"""
Main Fluke class. Accepts a string or a list of files upon initiation.
"""
__all__ = ['itunes']

import sys,os
import itunes, EasyDialogs

class FLAC(object):
    def __init__(self,files=None):
        self.fileList = []

        if files:
            files = self.checkArgs(files)
            self.fileList = self.processFiles(files)

    def itunesAdd(self):
        """Add processed tracks to iTunes"""
        for f in self.fileList:
            self.setFileTypeToOggs(f)
            if itunes.add(f) == False:
                print "Couldn't add the file(s). Please restart iTunes or reinstall Fluke."
                return False
    
    def files(self,files=None):
        """Get and set list of files to process"""
        if files:
            self.__init__(files)
        return self.fileList

    def processFiles(self, files):
        """
        Recurse through dirs if any are given and filter out non-flacs
        """
        results = []
        for f in files: 
            if os.path.isdir(f):
                flacs = [os.path.join(f,s) for s in os.listdir(f)
                        if os.path.splitext(s)[1] == '.flac']
                
                results.extend(flacs)
            else: 
                results.append(f)

        return results

    def checkArgs(self,args):
        """Check if argument was a list or a string. Always return a list"""
        
        import types

        if type(args) == types.StringType:
            return [args]
        else:
            return list(args)

    def setFileTypeToOggs(self,fn):
        """Set filetype to OggS to allow playback in iTunes"""
        from Carbon import File, Files

        fl, is_dir = File.FSPathMakeRef(fn)
        if is_dir:
            return False
        ci, _fn, fsspc, pfl = fl.FSGetCatalogInfo(Files.kFSCatInfoFinderInfo)

        finfo = fsspc.FSpGetFInfo()
        finfo.Type = 'OggS'

        fsspc.FSpSetFInfo(finfo)
        return True

    def openFileDialog(self):
        """Currently unused and really belongs in the Controller"""
        panel = NSOpenPanel.openPanel()
        panel.setCanCreateDirectories_(True)
        panel.setCanChooseDirectories_(True)
        panel.setCanChooseFiles_(True)
        panel.setAllowsMultipleSelection_(True)
        if panel.runModalForTypes_(('flac',)) == NSOKButton:
            return panel
        return 

    def __str__(self):
        return str(self.fileList)