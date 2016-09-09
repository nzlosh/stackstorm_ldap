from lib.ldapserver import LDAPServer


class Search(Action):
    """
    Lookup information from the directory.
    @base_dn The directory branch distinguished name to the search from.
    @scope The type of search to perform object, one_leve, subtree
    @search_filter The criteria to select objects to be returned in the result.
    @attributes The object's attributes to return.
    """
    def run(self, ldap_profile, base_dn, scope, search_filter, attributes):

        cfg = self.config["profiles"][ldap_profile]
        ldap_server = LDAPServer(cfg["url"], cfg["use_tls"], cfg["bind_dn"], cfg["bind_pw"])
        if ldap_server:
            res = ldap.search(base_dn, search_filter, scope, attributes)
            return res

        return False
