from st2common import log as logging

import six
import json
import ldap
import ldap.modlist as modlist


class LDAPClient(object):
    """
    LDAPClient object provides common functionality to authenticate and interact
    with an LDAP server.
    """
    def __init__(self, ldap_uri, use_tls, bind_dn, bind_pw):
        """
        @ldap_uri - ldap server url
        @use_tls - Enable TLS for the connection.
        @bind_dn - Distinguished Name used to bind to server.
        @bind_pw - Password for the Distinguished Name account.
        """
        self.ldap_uri = ldap_uri
        self.bind_dn = bind_dn
        self.bind_pw = bind_pw

        self.cxn = None

        if use_tls != True or "ldaps" in ldap_uri:
            self.use_tls = False
            self.tls_valid_cert = False
        else:
            self.use_tls = True

        self.logger = logging.getLogger(__name__)


    def connect(self):
        """
        Establish a connection to the LDAP server.
        """
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
        self.cxn = ldap.initialize(self.ldap_uri)
        ldap.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
        if self.use_tls:
            lda.set_option(ldap.OPT_X_TLS, ldap.OPT_X_TLS_DEMAND)
            self.cxn.start_tls_s()
            self.logger.debug('using TLS')
        self.cxn.simple_bind_s(self.bind_dn, self.bind_pw)


    def disconnect(self):
        """
        Disconnect the existing LDAP session.
        """
        if self.cxn:
            self.cxn.unbind_s()
        self.cxn = None


    def search(self, base_dn, scope='subtree', search_filter='(objectClass=*)', attributes=None):
        """
        search method queries
        """
        self.scope = {
            "base": ldap.SCOPE_BASE,
            "onelevel": ldap.SCOPE_ONELEVEL,
            "subtree": ldap.SCOPE_SUBTREE
        }.get(scope.lower()) or None

        if self.scope is None:
            self.logger.debug("'{}' isn't a valid scope, defaulting to 'subtree'.".format(scope))
            self.scope = ldap.SCOPE_SUBTREE

        self.connect()
        # Cast Stackstorm unicode list elements to bytecode to be compatiable with ldap module.
        stringy_attributes = None
        if isinstance(attributes, list):
            stringy_attributes = [str(i) for i in attributes]
        res = self.cxn.search_s(base_dn, self.scope, search_filter, stringy_attributes)
        return json.dumps(res)


    def add(self, dn, attributes):
        """
        Add a new set of attributes to the directory.

        Each element in the list modlist should be a tuple of the form
        (mod_op,mod_type,mod_vals)
        mod_op indicates the operation (one of ldap.MOD_ADD, ldap.MOD_DELETE, or ldap.MOD_REPLACE)
        mod_type is a string indicating the attribute type name
        mod_vals is either a string value or a list of string values to add, delete or replace
        respectively. For the delete operation, mod_vals may be None indicating that all attributes
        are to be deleted.
        """
        try:
            self.connect()
            for i, v in enumerate(attributes):
                attributes[i] = self._convert_mod_string_to_ldap(attributes[i])
            ldif = modlist.addModlist(attributes)
            self.cxn.add_s(dn, ldif)
            self.disconnect()
        except Exception as e:
            self.logger.warn("Error adding attributes: {}".format(str(e)))
            self.disconnect()
            return False
        return True


    def _convert_mod_string_to_ldap(self, attribute):
        """
        Convert the text representation of the ldap modify operation to the corresponding
        LDAP module flag value.
        """
        conv = {
            "add": ldap.MOD_ADD,
            "delete": ldap.MOD_DELETE,
            "replace": ldap.MOD_REPLACE
        }.get(attribute[0].lower())

        if not conv:
            self.logger.warn("Invalid attribute operation.")
            raise TypeError

        return (conv, attribute[1], attribute[2])


    def modify(self, dn, old, new):
        """
        Modify an existing attribute with another.
        old = {'attribute':'value'}
        new = {'attribute':'value'}
        """
        ret_val = True
        try:
            self.connect()
            ldif = modlist.modifyModlist(old, new)
            self.cxn.modify_s(dn, ldif)
        except Exception as e:
            self.logger.warn("Error modifying attribute: {}".format(str(e)))
            ret_val = False
        finally:
            self.disconnect()
        return ret_val


    def delete(self, delete_dn):
        """
        Delete a distinguished name from the directory.
        """
        ret_val = True
        try:
            self.connect()
            self.cxn.delete_s(delete_dn)
        except Exception as e:
            self.logger.warn("Error while deleting DN. {}".format(str(e)))
            ret_val = False
        finally:
            self.disconnect()
        return ret_val
