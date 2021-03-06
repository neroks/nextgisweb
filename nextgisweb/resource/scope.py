# -*- coding: utf-8 -*-
""" Универсальные наборы прав доступа
=====================================

"""

from __future__ import unicode_literals
from .permission import Scope, Permission
from .util import _

__all__ = [
    'ResourceScope',
    'MetadataScope',
    'DataStructureScope',
    'DataScope',
    'ConnectionScope',
    'ServiceScope',
]

P = Permission


class ResourceScope(Scope):
    """ Базовый набор прав ресурса """

    identity = 'resource'
    label = _("Resource")

    read = P(_("Read"))
    """ Чтение: возможность прочитать атрибуты класс, наименование и ключ
    ресурса. Так же от этого права зависит большинство других прав ресурса,
    например изменение, таким образом нельзя изменить ресурс не имея
    возможности его прочитать. """

    create = P(_("Create")).require(read)
    """ Создание: довольно туманное право, сейчас не используется. Идея была
    в том, что при создании нового ресурса проверялось наличие в нем права на
    создание, но сейчас проверяется только право :py:attr:`manage_children`
    для дочернего ресурса. Возможно потом стоит к этому вернуться, без этого
    права невозможно ограничить создание новых ресурсов определенного типа. """

    update = P(_("Update")).require(read)
    """ Изменение: изменение наименования и ключа ресурса, по аналогии с правом
    :py:attr:`read`. На изменение остальных атрибутов это ни как не влияет. """

    delete = P(_("Delete")).require(read)
    """ Удаление: право на удаление этого ресурса. Помимо этого для реального
    удаления ресурса необходимо наличие права :py:attr:`manage_children`
    у родительского ресурса. """

    manage_children = P(_("Manage children")).require(read)
    """ Управление дочерними ресурсами """

    change_permissions = P(_("Change permissions")).require(read)
    """ Управление правами доступа """


class MetadataScope(Scope):
    """ Набор прав метаданных ресурса. Типичный пример метаданных ресурса -
    его описание в свободной форме. Это описание фактически ни на что не
    влияет, его изменение не приводит к изменению структуры данных или
    чего-либо еще. Поскольку у каждого типа ресурсов есть описание, то этот
    набор прав включен для всех ресурсов на уровне класса Resource. """

    identity = 'metadata'
    label = _("Metadata")

    read = P(_("Read"))                   #: Чтение
    write = P(_("Write")).require(read)   #: Запись


class DataStructureScope(Scope):
    """ Набор прав структуры данных ресурса, например стурктура полей
    векторного слоя, ее изменение может приводить к изменению содержимого
    самих данных. """

    identity = 'datastruct'
    label = _("Data structure")

    read = P(_("Read"))                   #: Чтение
    write = P(_("Write")).require(read)   #: Запись


class DataScope(Scope):
    """ Набор прав доступа к данным """

    identity = 'data'
    label = _("Data")

    read = P(_("Read"))                   #: Чтение
    write = P(_("Write")).require(read)   #: Запись


class ConnectionScope(Scope):
    """ Набор прав параметров внешнего соединения. В некоторых случаях
    требуется хранить в ресурсе параметры доступа к внешним ресурсам. Эти
    параметры могут содержать чувствительные данные с точки зрения
    безопасности, например логины и пароли для доступа к удаленной БД. """

    identity = 'connection'
    label = _("Connection")

    read = P(_("Read"))
    write = P(_("Write")).require(read)
    connect = P(_("Connect"))


class ServiceScope(Scope):
    """ Набор прав предоставляемого сервиса, например WMS или WFS. Нужна чтобы
    можно было разделить права на настройку сервиса и на его использование.
    Впрочем если сервис внутри использует другие ресурсы, то права на них
    должны проверяться отдельно. """

    identity = 'service'
    label = _('Service')

    connect = P(_("Connect"))                       #: Подключение
    configure = P(_("Configure")).require(connect)  #: Настройка
