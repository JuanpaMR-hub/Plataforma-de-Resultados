from configparser import ConfigParser

config = ConfigParser()

config.add_section('power_bi_app')

 # Can be set to 'MasterUser' or 'ServicePrincipal'
config.set('power_bi_app','AUTHENTICATION_MODE','ServicePrincipal')

# Workspace Id in which the report is present
config.set('power_bi_app','WORKSPACE_ID','819e773c-b0ef-4c18-a9ac-34861fef270c')

# Report Id for which Embed token needs to be generated
config.set('power_bi_app','REPORT_ID','f0ccaaf3-9cfc-4dcc-acca-d101345c692c')
    
# Id of the Azure tenant in which AAD app and Power BI report is hosted. Required only for ServicePrincipal authentication mode.
config.set('power_bi_app','TENANT_ID','68885347-9938-403c-b30a-d4c014abc45f')

# Client Id (Application Id) of the AAD app
config.set('power_bi_app','CLIENT_ID','f6b1ee2f-5a1a-4204-8942-d861603447f1')

# Client Secret (App Secret) of the AAD app. Required only for ServicePrincipal authentication mode.
config.set('power_bi_app','CLIENT_SECRET','MekwyGh9Eq5O~i4ELN~-9_EE~E6W_ai~5e')

# Scope of AAD app. Use the below configuration to use all the permissions provided in the AAD app through Azure portal.
config.set('power_bi_app','SCOPE','https://analysis.windows.net/powerbi/api/.default')

# URL used for initiating authorization request
config.set('power_bi_app','AUTHORITY','https://login.microsoftonline.com/organizations')

with open(file='./embed_report/configs/config.ini',mode= 'w+') as f:
    config.write(f)
