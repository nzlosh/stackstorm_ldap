from st2actions.runners.pythonrunner import Action
from st2common import log as logging

import ldap
import ldap.modlist as modlist

LOG = logging.getLogger(__name__)



class LDAPServer(object):
    """
    This object provides common functionality to authenticate and interact
    with an LDAP server.
    """
    def __init__(self, ldap_uri, use_tls, bind_dn, bind_pw):
        """
        @ldap_uri -
        @use_tls -
        @bind_dn -
        @bind_pw -
        """
        self.ldap_uri = ldap_uri
        self.bind_dn = bind_dn
        self.bind_pw = bind_pw

        self.cxn = None

        if use_tls != "True" or "ldaps" in ldap_uri:
            self.use_tls = False
            self.tls_valid_cert = False
        else:
            self.use_tls = True



    def connect(self):
        """
        Establish a connection to the LDAP server.
        """
        try:
            ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
            self.cxn = ldap.initialize(self.ldap_uri)
            self.cxn.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
            if self.use_tls:
                self.cxn.set_option(ldap.OPT_X_TLS, ldap.OPT_X_TLS_DEMAND)
                self.cxn.start_tls_s()
                LOG.debug('using TLS')
            self.cxn.simple_bind_s(self.bind_dn, self.bind_pw)
            return True
        except ldap.LDAPError as e:
            LOG.debug('LDAP Error: %s' % (str(e)))
        finally:
            self.cxn.unbind_s()
            return False



    def disconnect(self):
        """
        Disconnect the existing LDAP session.
        """
        self.cxn.unbind()
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
            LOG.debug("'{}' isn't a valid scope, defaulting to 'subtree'.".format(scope))
            self.scope = ldap.SCOPE_SUBTREE

        try:
            res = self.connect()
            if res:
                res = self.cxn.search_s(base_dn, scope, search_filter, attributes)
                self.disconnect()
            return res
        except Exception as e:
            LOG.warn("Error during search. {}".format(str(e)))
            self.disconnect()
            return False



    def add(self, attributes):
        """
        Add a new set of attributes to the directory.
        """
        try:
            if self.connect():
                ldif = modlist.addModlist(attributes)
                self.cxn.add_s(dn, ldif)
                self.disconnect()
            return True
        except Exception as e:
            LOG.warn("Error adding attributes: {}".format(str(e)))
            self.disconnect()
            return False


    def modify(self, old, new):
        """
        Modify an existing attribute with another.
        old = {'attribute':'value'}
        new = {'attribute':'value'}
        """
        try:
            res = self.connect()
            if res:
                ldif = modlist.modifyModlist(old, new)
                self.cxn.modify_s(dn, ldif)
                self.disconnect()
            return res
        except Exception as e:
            LOG.warn("Error modifying attribute: {}".format(str(e)))
            self.disconnect()
            return False



    def delete(self, delete_dn):
        """
        Delete a distinguished name from the directory.
        """
        try:
            res = self.connect()
            if res:
                self.cxn.delete_s(delete_dn)
                self.disconnect()
            return res
        except Exception as e:
            LOG.warn("Error while deleting DN. {}".format(str(e)))
            self.disconnect()
            return False
