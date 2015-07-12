import sms_server
import config

raw = config.ConfigReader("config.json")
dic = config.Config(raw.get_conf_dict())
S = sms_server.SMSServer(dic)
S.start()

