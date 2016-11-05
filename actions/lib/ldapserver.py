from st2common import log as logging

import six
import json
import ldap
import ldap.modlist as modlist


class LDAPServer(object):
    """
    This object provides common functionality to authenticate and interact
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

        if use_tls.lower() != "true" or "ldaps" in ldap_uri:
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
        try:
            self.scope = {
                "base": ldap.SCOPE_BASE,
                "onelevel": ldap.SCOPE_ONELEVEL,
                "subtree": ldap.SCOPE_SUBTREE
            }[scope.lower()]
        except KeyError as e:
            self.logger.debug("'{}' isn't a valid scope, defaulting to 'subtree'.".format(scope))
            self.scope = ldap.SCOPE_SUBTREE

        self.connect()
        # Stackstorm uses unicode for list elements so we cast them to
        # bytecode to be compatiable with ldap module.
        if isinstance(attributes, list):
            stringy_attributes = [str(i) for i in attributes]
        res = self.cxn.search_s(base_dn, self.scope, search_filter, stringy_attributes)
        return json.dumps(res)


    def add(self, dn, attributes):
        """
        Add a new set of attributes to the directory.
        """
        try:
            self.connect()
            ldif = modlist.addModlist(attributes)
            self.cxn.add_s(dn, ldif)
            self.disconnect()
        except Exception as e:
            self.logger.warn("Error adding attributes: {}".format(str(e)))
            self.disconnect()
            return False
        return True


    def modify(self, dn, old, new):
        """
        Modify an existing attribute with another.
        old = {'attribute':'value'}
        new = {'attribute':'value'}
        """
        try:
            self.connect()
            ldif = modlist.modifyModlist(old, new)
            self.cxn.modify_s(dn, ldif)
            self.disconnect()
        except Exception as e:
            self.logger.warn("Error modifying attribute: {}".format(str(e)))
            self.disconnect()
            return False
        return True


    def delete(self, delete_dn):
        """
        Delete a distinguished name from the directory.
        """
        try:
            self.connect()
            self.cxn.delete_s(delete_dn)
            self.disconnect()
        except Exception as e:
            self.logger.warn("Error while deleting DN. {}".format(str(e)))
            self.disconnect()
            return False
        return True
