import smtplib
import mail_credentials

"""
  for Gmail to accept the application, enable the following settings
  https://www.google.com/settings/security/lesssecureapps
  https://accounts.google.com/DisplayUnlockCaptcha
"""

class MailSender():
  def __init__(self, user_name=None, password=None):
    self._username = user_name
    self._password = password

    if (user_name is None or password is None):
      # get the credentials from the config folder
      self._username, self._password = self.retrive_credentials()

  def retrive_credentials(self):
    import mail_credentials
    credentials = mail_credentials.credentials
    username = credentials['username']
    password = credentials['password']

    if username is None or password is None:
      raise Exception('No Credentials fields exist in the file!')

    elif username != "" and password != "":
      return username, password

    else:
      raise Exception('Credentials are empty!')

  """
    toaddrs: can be a list of email address
    msg: should have 'Subject:', otherwise the title will be empty
      msg = "\r\n".join([
        "Subject: hmy subject here",
        "my message boy here"
        ])
  """
  def sendmail(self, toaddrs, msg):
    username = self._username
    password = self._password
    fromaddr = username

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username, password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

def main():
  sender = MailSender()
  msg = "\r\n".join([
    "Subject: here it is",
    "Why, oh why"
    ])

  sender.sendmail('utest0095@gmail.com', msg)

main()