import json


class tester():
   def __init__(self):
      """
		Deals with user entered emails
		"""
      with open('info.json') as file:
         self.info = json.load(file)
         file.close()
      self.count = 0

   def run(self):
      print(self.info['customize'])
      print(self.info['password']['password'])
      str = self.info['emails'][0]
      print("str is ", str)


if __name__ == '__main__':
   test = tester()
   test.run()

