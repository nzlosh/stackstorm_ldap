from st2actions.runners.pythonrunner import Action
from lib.base import BaseLDAPAction


class Search(BaseLDAPAction):
    """
    Lookup information from the directory.
    @ldap_profile The profile to use to connect to the ldap server.
    @base_dn The distinguished name to the search from.
    @scope The type of search to perform; 'object', 'one_level' or 'subtree'
    @search_filter The criteria to select objects to be returned in the result.
    @attributes The list of object attributes to return.
    """
    def run(self, ldap_profile, base_dn, scope, search_filter, attributes):
 
        return ldap_client.search(base_dn, scope, search_filter, attributes)
