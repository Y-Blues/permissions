"""
    bootstrap of default data for manage account, role permission if it's manage by the server as a IDP


"""

from ycappuccino.api.core import IActivityLogger
from ycappuccino.api.proxy import YCappuccinoRemote
from ycappuccino.api.storage import IManager, IBootStrap
from ycappuccino.core.decorator_app import Layer

import logging
from pelix.ipopo.decorators import (
    ComponentFactory,
    Requires,
    Validate,
    Invalidate,
    Property,
    Provides,
    Instantiate,
)

from ycappuccino.permissions.models.account import Account
from ycappuccino.permissions.models.login import Login
from ycappuccino.permissions.models.role import Role
from ycappuccino.permissions.models.role_permission import RolePermission
from ycappuccino.permissions.models.role_account import RoleAccount


_logger = logging.getLogger(__name__)


@ComponentFactory("AccountBootStrap-Factory")
@Provides(specifications=[YCappuccinoRemote.__name__, IBootStrap.__name__])
@Requires("_log", IActivityLogger.__name__, spec_filter="'(name=main)'")
@Requires("_manager_account", IManager.__name__, spec_filter="'(item_id=account)'")
@Requires(
    "_manager_role_permission",
    IManager.__name__,
    spec_filter="'(item_id=rolePermission)'",
)
@Requires(
    "_manager_role_account", IManager.__name__, spec_filter="'(item_id=roleAccount)'"
)
@Requires("_manager_login", IManager.__name__, spec_filter="'(item_id=login)'")
@Requires("_manager_role", IManager.__name__, spec_filter="'(item_id=role)'")
@Property("_id", "id", "core")
@Instantiate("AccountBootStrap")
@Layer(name="ycappuccino-permissions")
class AccountBootStrap(IBootStrap):

    def __init__(self):
        super(IBootStrap, self).__init__()
        self._manager_account = None
        self._manager_login = None
        self._manager_role = None
        self._manager_role_permission = None
        self._manager_role_account = None
        self._right_access = None

        self._log = None
        self._id = "core"

    def get_id(self):
        return self._id

    def bootstrap(self):

        w_subject = self.get_token_subject("bootstrap", "system")

        w_admin_login = Login()
        w_admin_login.id("superadmin")
        w_admin_login.login("superadmin")
        w_admin_login.password("client_pyscript_core")

        w_admin_role = Role()
        w_admin_role.id("superadmin")
        w_admin_role.name("superadmin")

        w_admin_account = Account({})
        w_admin_account.id("superadmin")
        w_admin_account.name("superadmin")
        w_admin_account.login("superadmin")
        w_admin_account.role("superadmin")

        w_admin_role_permission = RolePermission({})
        w_admin_role_permission.id("superadmin")
        w_admin_role_permission.role("superadmin")
        w_admin_role_permission.rights(["*:*:*"])

        w_admin_role_account = RoleAccount({})
        w_admin_role_account.id("superadmin")
        w_admin_role_account.role("superadmin")
        w_admin_role_account.account("superadmin")
        w_admin_role_account.organization("system")

        self._manager_role.up_sert_model("superadmin", w_admin_role, w_subject)
        self._manager_account.up_sert_model("superadmin", w_admin_account, w_subject)
        self._manager_role_permission.up_sert_model(
            "superadmin", w_admin_role_permission, w_subject
        )
        self._manager_role_account.up_sert_model(
            "superadmin", w_admin_role_account, w_subject
        )

        if self._manager_login.get_one("login", "superadmin", w_subject) is None:
            self._manager_login.up_sert_model("superadmin", w_admin_login, w_subject)

    @Validate
    def validate(self, context):
        self._log.info("AccountBootStrap validating")
        try:
            self.bootstrap()
        except Exception as e:
            self._log.error("AccountBootStrap Error {}".format(e))
            self._log.exception(e)

        self._log.info("AccountBootStrap validated")

    @Invalidate
    def invalidate(self, context):
        self._log.info("AccountBootStrap invalidating")
        try:
            pass
        except Exception as e:
            self._log.error("AccountBootStrap Error {}".format(e))
            self._log.exception(e)
        self._log.info("AccountBootStrap invalidated")
