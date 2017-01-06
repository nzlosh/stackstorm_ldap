from st2actions.runners.pythonrunner import Action
from lib.ldapserver import LDAPServer


class Add(Action):
    """
    Add attributes to the directory.
    @base_dn The directory branch distinguished name to the search from.
    @scope The type of search to perform object, one_leve, subtree
    @search_filter The criteria to select objects to be returned in the result.
    @attributes The object's attributes to return.

    Each element in the list modlist should be a tuple of the form
    (mod_op,mod_type,mod_vals)
    mod_op indicates the operation (one of ldap.MOD_ADD, ldap.MOD_DELETE, or ldap.MOD_REPLACE)
    mod_type is a string indicating the attribute type name
    mod_vals is either a string value or a list of string values to add, delete or replace
    respectively. For the delete operation, mod_vals may be None indicating that all attributes
    are to be deleted.
    """
    def run(self, ldap_profile, dn, attributes):
        cfg = self.config["profiles"][ldap_profile]
        ldap_server = LDAPServer(cfg["url"], cfg["use_tls"], cfg["bind_dn"], cfg["bind_pw"])
        if ldap_server:
            res = ldap.add(base_dn, attributes)
            return res

        return False
