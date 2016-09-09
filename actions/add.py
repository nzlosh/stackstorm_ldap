from lib.ldapserver import LDAPServer


class Add(Action):
    """
    Add attributes to the directory.
    @base_dn The directory branch distinguished name to the search from.
    @scope The type of search to perform object, one_leve, subtree
    @search_filter The criteria to select objects to be returned in the result.
    @attributes The object's attributes to return.
    """
    def run(self, ldap_profile, attributes):
        cfg = self.config["profiles"][ldap_profile]
        ldap_server = LDAPServer(cfg["url"], cfg["use_tls"], cfg["bind_dn"], cfg["bind_pw"])
        if ldap_server:
            res = ldap.add(base_dn, attributes)
            return res

        return False
