from lib.ldapserver import LDAPServer


class Modify(Action):
    """
    Modify an object in the directory.
    """
    def run(self, ldap_profile, old, new):
        cfg = self.config["profiles"][ldap_profile]
        ldap_server = LDAPServer(cfg["url"], cfg["use_tls"], cfg["bind_dn"], cfg["bind_pw"])
        if ldap_server:
            res = ldap.modify(old, new)
            return res

        return False
