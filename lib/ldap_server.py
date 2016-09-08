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
    def __init__(self, ldap_uri, use_tls, bind_dn, bind_pw, base_dn):
        self.ldap_uri = ldap_uri
        self.base_dn = base_dn
        self.bind_dn = bind_dn
        self.bind_pw = bind_pw

        if "base" in scope:
            self._scope = ldap.SCOPE_BASE
        elif "onelevel" in scope:
            self._scope = ldap.SCOPE_ONELEVEL
        else:
            self._scope = ldap.SCOPE_SUBTREE

        if use_tls != "True" or "ldaps" in ldap_server:
            self.use_tls = False
            self.tls_valid_cert = False
        else:
            self.use_tls = True



    def connect(self):
        try:
            ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
            connect = ldap.initialize(self._ldap_server)
            connect.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
            if self.use_tls:
                connect.set_option(ldap.OPT_X_TLS, ldap.OPT_X_TLS_DEMAND)
                connect.start_tls_s()
                LOG.debug('using TLS')
            connect.simple_bind_s(self.bind_dn, self.bind_pw)
            return connect
        except ldap.LDAPError as e:
            LOG.debug('LDAP Error: %s' % (str(e)))


    def disconnect(self, connect):
        connect.unbind()


    def search(self, search_filter, scope, attributes):
        connect = self.connect()
            try:
                result = connect.search_s(, self._scope, search_filter)
                if result is None:
                    LOG.debug('User "%s" doesn\'t exist in group "%s"' % (username, self._group_dn))
                elif result:
                    LOG.debug('Authentication for user "%s" successful' % (username))
                    return True
                return False
            except:
                return False
            finally:
                connect.unbind()

            return False


    def add(self, connect, attributes):
        ldif = modlist.addModlist(attributes)
        connect.add_s(dn,ldif)



    def modify(self, connect, old, new):
        """
        old = {'attribute':'value'}
        new = {'attribute':'value'}
        """
        ldif = modlist.modifyModlist(old,new)
        connect.modify_s(dn,ldif)


    def delete(self, connect, delete_dn):
        try:
            connect.delete_s(delete_dn)
            connect.unbind_s()
        except ldap.LDAPError, e:
            print e



class Search(Action):
    """
    Lookup information from the directory.
    @base_dn The directory branch distinguished name to the search from.
    @scope The type of search to perform object, one_leve, subtree
    @search_filter The criteria to select objects to be returned in the result.
    @attributes The object's attributes to return.
    """
    def run(self, base_dn, scope, search_filter, attributes):
        raise NotImplementedError


class Add(Action):
    """
    Lookup information from the directory.
    @base_dn The directory branch distinguished name to the search from.
    @scope The type of search to perform object, one_leve, subtree
    @search_filter The criteria to select objects to be returned in the result.
    @attributes The object's attributes to return.
    """
    def run(self, base_dn, scope, search_filter, attributes):
        raise NotImplementedError



class Modify(Action):
    """
    Write information to LDAP.
    """
    def run(self):
        raise NotImplementedError



class Delete(Action):
    """
    Delete an entity from the LDAP database.
    """
    def run(self):
        raise NotImplementedError

