#!/usr/bin/python3
#
# Ejemplo muy muy muy mínimo de un sistema de archivos virtual:
# AumentandoFS contiene un sólo archivo, que cada vez que lo leemos,
# entrega el número entero consecutivo inmediato superior al de la
# última vez que lo leímos.

from fusepy import FUSE, FuseOSError, Operations, LoggingMixIn
import errno
import logging
import os
import stat
import sys

class AumentandoFS(LoggingMixIn, Operations):
    def __init__(self):
        self.consecutivo = 0

    def getattr(self, path, fh=None):
        if path == '/':
            st = os.lstat(path)
            return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime', 'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))
        elif path == '/data':
            return {'st_atime': 0,
                    'st_ctime': 0,
                    'st_gid': 0,
                    # consultar man inode, stat
                    'st_mode': stat.S_IFREG | stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH,
                    'st_size': len('%d' % self.consecutivo),
                    'st_mtime': 0,
                    'st_nlink': 1,
                    'st_uid': 0}
        else:
            return FuseOSError(errno.ENOENT)

    def read(self,path,size,offset,fh):
        self.consecutivo = self.consecutivo + 1
        return str( self.consecutivo )

    def readdir(self,path,fh):
        return ['.', '..', 'data']


if __name__== '__main__':
    if len(sys.argv) != 2 or (not os.path.isdir(sys.argv[1])):
        print('Error de invocación: ', sys.argv[0], '<punto_mnt>')
        print('<punto_mnt>: ruta de un directorio en el que el usuario actual tenga')
        print('             permisos de lectura, escritura y ejecución, donde se ')
        print('             montará el sistema de archivos..')
        sys.exit(1)

    mountpoint = sys.argv[1]
#    logging.basicConfig(level=logging.DEBUG)
    FUSE(AumentandoFS(), mountpoint, nothreads=True, foreground=True)
