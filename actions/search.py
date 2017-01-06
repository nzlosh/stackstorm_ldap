from st2actions.runners.pythonrunner import Action
from lib.ldapserver import LDAPServer


class Search(Action):
    """
    Lookup information from the directory.
    @ldap_profile The profile to use to connect to the ldap server.
    @base_dn The distinguished name to the search from.
    @scope The type of search to perform; 'object', 'one_level' or 'subtree'
    @search_filter The criteria to select objects to be returned in the result.
    @attributes The list of object attributes to return.
    """
    def run(self, ldap_profile, base_dn, scope, search_filter, attributes):
        self.logger.debug("LDAP_CONFIG: {}".format(self.config))
        for profile in self.config.get("profiles"):
            if profile.get("name") == ldap_profile:
                cfg = profile
                break
        else:
            # No matching profile - FIXME: return an object compatiable with st2.
            return "Configuration doesn't have a profile '{}'".format(ldap_profile)

        ldap_server = LDAPServer(
            cfg.get("url"),
            cfg.get("use_tls"),
            cfg.get("bind_dn"),
            cfg.get("bind_pw")
        )

        self.logger.info("LDAP Search arguments: {}".format([base_dn, search_filter,
                                                                        scope, attributes]))
        return ldap_server.search(base_dn, scope, search_filter, attributes)
