from st2actions.runners.pythonrunner import Action
from st2common import log as logging

import ldap

LOG = logging.getLogger(__name__)



class LDAPServer(object):
    """
    Backend which reads authentication information from a ldap server.

    Authentication steps:
        1. bind to ldap using the bind_dn & bind_pw and fetch user attributes.
        2. rebind using users DN.
        3. if group_dn is provided (optional)
            - serch ldap using group_dn.
        4. all of the above steps are succesful
            - return successful .
    """
    def __init__(self, ldap_server, bind_dn, bind_pw, base_dn, group_dn, scope, use_tls, search_filter):
        """
        :param ldap_server: URL of the LDAP Server.
        :type ldap_server: ``str``
        :param base_dn: Base DN on the LDAP Server.
        :type base_dn: ``str``
        :param bind_dn: The Distinguish Name account to bind to the ldap server.
        :type bind_dn: ``str``
        :param bind_pw: The Distinguish Name account's password.
        :type bind_pw: ``str``
        :param group_dn: Group DN on the LDAP Server which contains the user as member.
        :type group_dn: ``str``
        :param scope: Scope search parameter. Can be base, onelevel or subtree (default: subtree)
        :type scope: ``str``
        :param use_tls: Boolean parameter to set if tls is required.
        :type use_tls: ``bool``
        :param tls_valid_cert: Boolean parameter to set if the server certificate must be valid.
        :type tls_valid_cert: ``bool``
        :param search_filter: Should contain the placeholder %(username)s for the username.
        :type search_filter: ``str``
        """
        self._ldap_server = ldap_server
        self._base_dn = base_dn
        self._group_dn = group_dn
        self._bind_dn = bind_dn
        self._bind_pw = bind_pw

        if "base" in scope:
            self._scope = ldap.SCOPE_BASE
        elif "onelevel" in scope:
            self._scope = ldap.SCOPE_ONELEVEL
        else:
            self._scope = ldap.SCOPE_SUBTREE
        if use_tls != "True" or "ldaps" in ldap_server:
            self._use_tls = False
            self._tls_valid_cert = False
        else:
            self._use_tls = True
        self._search_filter = search_filter


    def authenticate(self, username, password):
        if self._search_filter:
            search_filter = self._search_filter % {'username': username}
        else:
            search_filter = 'uniqueMember=uid=' + username + ',' + self._base_dn
        self._ldap_connect()


    def _ldap_connect(self):
        try:
            ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
            connect = ldap.initialize(self._ldap_server)
            connect.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
            if self._use_tls:
                connect.set_option(ldap.OPT_X_TLS, ldap.OPT_X_TLS_DEMAND)
                connect.start_tls_s()
                LOG.debug('using TLS')
            connect.simple_bind_s("uid=" + username + "," + self._base_dn, password)
            try:
                result = connect.search_s(self._group_dn, self._scope, search_filter)
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
        except ldap.LDAPError as e:
            LOG.debug('LDAP Error: %s' % (str(e)))
            return False

    def get_user(self, username):
        pass



class ReadAttribute(Action):
    """
    Read information for LDAP.
    """
    def run(self):
        raise NotImplementedError



class WriteAttribute(Action):
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



