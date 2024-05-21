from ycappuccino.core.decorator_app import App

from ycappuccino.api.decorators import Item, ItemReference, Empty, Property, Reference
from ycappuccino.api.models import Model


"""
    model that decribe a account 
"""


@Empty()
def empty():
    _empty = Account()
    _empty.id("test")
    _empty.login("client_pyscript_core")
    _empty.name("client_pyscript_core")
    _empty.role("client_pyscript_core")

    return _empty


@App(name="ycappuccino_permissions")
@Item(
    collection="accounts",
    name="account",
    plural="accounts",
    secure_write=True,
    secure_read=True,
)
@ItemReference(from_name="account", field="login", item="login")
@ItemReference(from_name="account", field="role", item="role")
class Account(Model):
    """describe an account in the application"""

    def __init__(self, a_dict=None):
        super().__init__(a_dict)
        self._login = None
        self._name = None
        self._role = None

    @Property(name="name")
    def name(self, a_value):
        self._name = a_value

    @Reference(name="login")
    def login(self, a_value):
        self._login = a_value

    @Reference(name="role")
    def role(self, a_value):
        self._role = a_value


empty()
