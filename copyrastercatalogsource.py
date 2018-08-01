"""
Copy source rasters as referenced in a raster catalog

Dion Liddell, Taupo District Council, March 2011
"""

import os
import sys
import shutil
import glob
import arcpy

class RasterCatalog():
    def __init__(self, raster_catalog_lyr):
        self.raster_catalog_lyr = raster_catalog_lyr

    def copy_to(self, destination_dir):
        paths = self.paths()
        oid = arcpy.Describe(self.raster_catalog_lyr).OIDFieldName
        rows = arcpy.SearchCursor(self.raster_catalog_lyr)
        for row in rows:
            raster_image_name = paths[row.getValue(oid)]
            raster_fileset = os.path.splitext(raster_image_name)[0]
            source_files = glob.glob(raster_fileset + '.*')
            self._copy(source_files, destination_dir)
        del row
        del rows

    def paths(self):
        """
        returns raster source paths for raster catalog as
        a dictionary: {SourceOID:PATH}
        """
        raster_paths = 'in_memory/raster_paths'
        arcpy.ExportRasterCatalogPaths_management(self.raster_catalog_lyr, 'ALL', raster_paths)
        rows = arcpy.SearchCursor(raster_paths)
        paths_dic = {}
        for row in rows:
            paths_dic[row.getValue('SourceOID')] = row.getValue('Path')
            
        del row
        del rows
        arcpy.Delete_management(raster_paths)
        
        return paths_dic

    def _copy(self, source_files, destination):
        for file_name in source_files:
            arcpy.AddMessage('Copying %s to %s' % (file_name, destination))
            shutil.copy(file_name, destination)
        
if __name__ == '__main__':
    g_raster_catalog_lyr = sys.argv[1]
    g_destination_dir = sys.argv[2]
    
    g_raster_catalog = RasterCatalog(g_raster_catalog_lyr)
    g_raster_catalog.copy_to(g_destination_dir)
    
