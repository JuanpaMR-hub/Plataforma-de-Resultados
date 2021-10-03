from configparser import ConfigParser

config = ConfigParser()
config.read('./embed_report/configs/config.ini')


print(type(config.get('power_bi_app','REPORT_ID')))