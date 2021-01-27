#!/usr/bin/python3

from datetime import datetime
from fusepy import FUSE, FuseOSError, Operations, LoggingMixIn

import errno
import logging
import os
import stat
import sys
import time
import yaml

class YamlFS(LoggingMixIn, Operations):
    class WrongFileFormat(RuntimeError):
        pass

    def __refresh__(self):
        fh = open(self.basefs, 'r')
        data = yaml.load(fh, Loader=yaml.FullLoader)
        if data.__class__ != dict:
            raise WrongFileFormat('%s no contiene a un "dict" en primer nivel' % basefs)
        self.data = data
        self.direntries = data.keys()

    def __entry_stats__(self, path):
        path = self.__drop_root__(path)

        now = time.mktime( datetime.today().timetuple() )
        entry = {'st_atime': now,
                 'st_ctime': now,
                 'st_gid': 0,
                 # Consultar man inode, stat
                 'st_mode': stat.S_IFREG | stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH,
                 'st_mtime': now,
                 'st_nlink': 1,
                 'st_size': len(self.data[path]),
                 'st_uid': 0}
        return entry

    def __drop_root__(self, path):
        if path[0:1] == '/':
            path = path[1:]
        return path

    def __init__(self, basefs):
        self.basefs = basefs
        self.__refresh__()

    # Operaciones sobre el directorio
    #################################
    def access(self, path, mode):
        path = self.__drop_root__(path)

    def getattr(self, path, fh=None):
        if path == '/':
            # Los atributos del directorio raiz se los pasamos al
            # sistema de archivos real superior
            st = os.lstat(path)
            return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                                                            'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))
        path = self.__drop_root__(path)

        if path not in self.direntries:
            raise FuseOSError(errno.ENOENT)

        return self.__entry_stats__(path)

    def readdir(self, path, fh):
        if path != '/':
            raise FuseOSError(errno.ENOENT)
        yield '.'
        yield '..'
        for item in self.direntries:
            yield item

    def readlink(self, path):
        return path

    def mkdir(self, path):
        raise FuseOSError(errno.EINVAL)

    # Operaciones sobre un archivo
    ##############################

    def read(self, path, length, offset, fh):
        #self.log.msg('Leyendo %s: %s' % (path,flags))
        path = self.__drop_root__(path)

        if path not in self.direntries:
            #self.log.msg('%s no existe.' % path)
            raise FuseOSError(errno.ENOENT)

        # El API indica que nos pueden solicitar leer desde
        # determinado punto y un tamaño dado. Van los recortes
        # necesarios:
        data = self.data[path]
        datalen = len(data)
        # ¿Nos piden un punto de inicio menor al tamaño total? Si no,
        # regresamos una cadena vacía
        if offset < datalen:
            # ¿El punto de inicio mas el tamaño solicitado caen dentro
            # del total del archivo? Si no, recortamos el total a
            # devolver.
            if offset + length > datalen:
                size = datalen - offset
            return data[offset:offset + length]
        else:
            return b''

if __name__ == '__main__':
    if len(sys.argv) != 3 or (not os.path.isfile(sys.argv[1])) or (not os.path.isdir(sys.argv[2])):
        print('Error de invocación: ', sys.argv[0], '<archivo> <punto_mnt>')
        print('<archivo>: nombre de un archivo YAML válido.')
        print('<punto_mnt>: ruta de un directorio en el que el usuario actual tenga')
        print('             permisos de lectura, escritura y ejecución, donde se ')
        print('             montará el sistema de archivos..')
        sys.exit(1)

    basefs = sys.argv[1]
    mountpoint = sys.argv[2]
    logging.basicConfig(level=logging.DEBUG)
    FUSE(YamlFS(basefs), mountpoint, nothreads=True, foreground=True)
