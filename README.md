# LDAP Integration Pack

This pack allows integration with LDAP server implementations allowing queries to read, write, create and delete entries.

## Actions

The following actions are supported along with the arguments:

  * `search`
  * `add`
  * `modify`
  * `delete`

### search

Search for entries that match the provided filter.  The search will be applied based on the scope provided and return the attributes specified.

1. **ldap_profile**: Used to select the profile configured in the LDAP pack's config.yaml file.
2. **base_dn**: Search base in the directory tree to perform the search.
3. **scope**: Limit the scope of the search to `object`, `one-level`, or `subtree`.
4. **search_filter**: LDAP filter to use in the query.
5. **attributes**: The attributes to be returned in the returned result set.

### add
 To be implemented.

### modify
 To be implemented.

### delete
 To be implemented.

## Configuration

The pack must be configured with an LDAP profile.  The profile is used to define the server uri and an account to use to bind to the directory.

### Profile parameters
 1. **url** (_string_): The LDAP server url. `ldap://<hostname>:<port>`
 2. **use_tls** (_boolean_): Enable TLS on servers that support it.  _It's an error to enable TLS when using `ldaps` in the ldap uri._
 3. **bind_dn** (_string_): The distinguished name to bind to the LDAP server.
 4. **bind_pw** (_string_): Password for the distinguished name.

See the file `config.yaml` which has two examples of the syntax.

## Authentication

The following authentication methods are supported

 * Simple Anonymous Bind
 * Simple DN Bind

## Limitations

  * No SASL authentication.

## References

  https://www.ldap.com/ldap-filters

## Thanks to
https://icons8.com for the use of their ![icon](icon.png)
