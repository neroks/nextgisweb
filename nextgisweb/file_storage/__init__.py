# -*- coding: utf-8 -*-
import os
from shutil import copyfileobj

from ..component import Component
from ..core import BackupBase

from .models import Base, FileObj
from . import command  # NOQA

__all__ = ['FileStorageComponent', 'FileObj']


@BackupBase.registry.register
class FileObjBackup(BackupBase):
    identity = 'fileobj'

    def is_binary(self):
        return True

    def backup(self):
        fileobj = FileObj.filter_by(uuid=self.key).one()
        with open(self.comp.filename(fileobj), 'rb') as fd:
            copyfileobj(fd, self.binfd)

    def restore(self):
        fileobj = FileObj.filter_by(uuid=self.key).one()
        fn = self.comp.filename(fileobj, makedirs=True)
        if os.path.isfile(fn):
            pass
        else:
            with open(fn, 'wb') as fd:
                copyfileobj(self.binfd, fd)


@Component.registry.register
class FileStorageComponent(Component):
    identity = 'file_storage'
    metadata = Base.metadata

    def initialize(self):
        self.path = self.settings.get('path') or self.env.core.gtsdir(self)

    def initialize_db(self):
        if 'path' not in self.settings:
            self.env.core.mksdir(self)

    def backup(self):
        for i in super(FileStorageComponent, self).backup():
            yield i

        for fileobj in FileObj.query():
            yield FileObjBackup(self, fileobj.uuid)

    def fileobj(self, component):
        obj = FileObj(component=component)
        return obj

    def filename(self, fileobj, makedirs=False):
        assert fileobj.component, "Component not set!"

        # Разделяем на два уровня директорий по первым символам id
        levels = (fileobj.uuid[0:2], fileobj.uuid[2:4])
        path = os.path.join(self.path, fileobj.component, *levels)

        # Создаем директории если нужно
        if makedirs and not os.path.isdir(path):
            os.makedirs(path)

        return os.path.join(path, str(fileobj.uuid))

    settings_info = (
        dict(key='path', desc=u"Директория для хранения файлов (обязательно)"),
    )
