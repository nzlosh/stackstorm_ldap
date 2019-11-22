# ldap integration pack v0.1.0

> Interact with LDAP servers
Carlos <nzlosh@yahoo.com>


## Configuration

The following options are required to be configured for the pack to work correctly.

| Option | Type | Required | Secret | Description |
|---|---|---|---|---|
| `profiles` | array |  |  | A list of available ldap servers |
| `available_profiles` | array | True | False | The list of available profiles to be presented in the WebUI's dropdown list |


## Actions


The pack provides the following actions:

### add
_Add a new entity to the directory tree_

| Parameter | Type | Required | Secret | Description |
|---|---|---|---|---|
| `ldap_profile` | string | True | default | _Used to select the profile configured in the LDAP pack's config.yaml file._ |
| `distinguished_name` | string | True | default | _The distinguished name to add to the directory._ |
| `attributes` | object | True | default | _The attributes to be added to the DN object._ |
### delete
_Delete a DN from the directory tree_

| Parameter | Type | Required | Secret | Description |
|---|---|---|---|---|
| `ldap_profile` | string | True | default | _Used to select the profile configured in the LDAP pack's config.yaml file._ |
| `delete_dn` | string | True | default | _The DN to be deleted._ |
### modify
_Modify an existing entity in the directory tree._

| Parameter | Type | Required | Secret | Description |
|---|---|---|---|---|
| `ldap_profile` | string | True | default | _Used to select the profile configured in the LDAP pack's config.yaml file._ |
| `modify_dn` | string | True | default | _The DN to be modified._ |
| `old` | object | True | default | _The old attribute to be modified for the given 'modify_dn'._ |
| `new` | object | True | default | _The new attribute to be modified for the given 'modify_dn'._ |
### search
_Search for entities in the directory tree._

| Parameter | Type | Required | Secret | Description |
|---|---|---|---|---|
| `ldap_profile` | string | True | default | _Used to select the profile configured in the LDAP pack's config.yaml file._ |
| `base_dn` | string | True | default | _Search base in the directory tree to perform the search._ |
| `scope` | string | False | default | _Limit the scope of the search to 'object', 'one-level', or 'subtree'._ |
| `search_filter` | string | False | default | _LDAP filter to use in the query._ |
| `attributes` | array | False | default | _The attributes to be returned in the returned result set._ |



## Sensors

There are no sensors available for this pack.


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

<sub>Documentation generated using [pack2md](https://github.com/nzlosh/pack2md)</sub>