# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
from configparser import ConfigParser
import msal

class AadService:
    

    def get_access_token():
        '''Generates and returns Access token

        Returns:
            string: Access token
        '''
        config = ConfigParser()
        config.read('./embed_report/configs/config.ini')
        response = None
        try:
            if config.get('power_bi_app','AUTHENTICATION_MODE').lower() == 'masteruser':

                # Create a public client to authorize the app with the AAD app
                clientapp = msal.PublicClientApplication(config.get('power_bi_app','CLIENT_ID'), authority=config.get('power_bi_app','AUTHORITY'))
                accounts = clientapp.get_accounts(username=config.get('power_bi_app','POWER_BI_USER'))

                if accounts:
                    # Retrieve Access token from user cache if available
                    response = clientapp.acquire_token_silent(config.get('power_bi_app','SCOPE'), account=accounts[0])

                if not response:
                    # Make a client call if Access token is not available in cache
                    response = clientapp.acquire_token_by_username_password(config.get('power_bi_app','POWER_BI_USER'), config.get('power_bi_app','POWER_BI_PASS'), scopes=config.get('power_bi_app','SCOPE'))     

            # Service Principal auth is the recommended by Microsoft to achieve App Owns Data Power BI embedding
            elif config.get('power_bi_app','AUTHENTICATION_MODE').lower() == 'serviceprincipal':
                authority = config.get('power_bi_app','AUTHORITY').replace('organizations', config.get('power_bi_app','TENANT_ID'))
                clientapp = msal.ConfidentialClientApplication(config.get('power_bi_app','CLIENT_ID'), client_credential=config.get('power_bi_app','CLIENT_SECRET'), authority=authority)

                # Make a client call if Access token is not available in cache
                response = clientapp.acquire_token_for_client(scopes=config.get('power_bi_app','SCOPE'))

            try:
                return response['access_token']
            except KeyError:
                raise Exception(response['error_description'])

        except Exception as ex:
            raise Exception('Error retrieving Access token\n' + str(ex))