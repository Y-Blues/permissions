from ycappuccino_core.models.decorators  import Item, Property, Empty
from ycappuccino_storage.models.model import Model
from ycappuccino_core.decorator_app import App
"""
    model that describe a permission that should admin domain:action:filter
"""
@Empty()
def empty():
    _empty = Permission()
    _empty.id("client_pyscript_core")
    _empty.name("client_pyscript_core")
    _empty.permission("tout")
    return _empty

@App(name="ycappuccino_permissions")
@Item(collection="permissions", name="permission", plural="permissions", secure_write=True,
      secure_read=True)
class Permission(Model):
    def __init__(self, a_dict=None):
        super().__init__(a_dict)
        self._name = None
        self._permission = None

    @Property(name="name")
    def name(self, a_value):
        self._name = a_value

    @Property(name="permission")
    def permission(self, a_value):
        """ list of right permission """
        self._permission = a_value

empty()