# coding=utf-8

__all__ = [
    'BaseLDAPAction'
]


class MaskContent(object):
    def __init__(self, sensitive_content):
        self.sensitive_content = sensitive_content

    def __repr__(self):
        return "******"

    def use_unmasked(self):
        return self.sensitive_content


class Action(object):
    def __init__(self, config):
        self.config = config


class BaseLDAPAction(Action):
    def __init__(self, config):
        super(BaseLDAPAction, self).__init__(config=config)
        self._client = self._get_client()
       self.logger.debug("LDAP_CONFIG: {}".format(self.config))
        for profile in self.config.get("profiles"):
            if profile.get("name") == ldap_profile:
                cfg = profile
                break
        else:
            # No matching profile - FIXME: return an object compatiable with st2.
            return "Configuration doesn't have a profile '{}'".format(ldap_profile)

        ldap_client = LDAPClient(
            cfg.get("url"),
            cfg.get("use_tls"),
            cfg.get("bind_dn"),
            cfg.get("bind_pw")
        )

        self.logger.info("LDAP Search arguments: {}".format(
                [base_dn, search_filter, scope, attributes]
            )
        )
        
    def _get_client(self):
        config = self.config

        options = {'server': config['url']}

        rsa_cert_file = config['rsa_cert_file']
        rsa_key_content = self._get_file_content(file_path=rsa_cert_file)

        return client
