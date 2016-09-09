from lib.ldapserver import LDAPServer

        
class Delete(Action):
    """
    Delete an entity from the LDAP database.
    """
    def run(self, ldap_profile, delete_dn):
        cfg = self.config["profiles"][ldap_profile]
        ldap_server = LDAPServer(cfg["url"], cfg["use_tls"], cfg["bind_dn"], cfg["bind_pw"])
        if ldap_server:
            res = ldap.delete(delete_dn)
            return res

        return False


