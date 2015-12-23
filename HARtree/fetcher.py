#!/usr/bin/python2
# -*- coding: utf-8 -*-

import sys
import subprocess
import json

from time import gmtime, strftime

class HARfetcher:
	
	supportedEngines = ["phantomjs", "ph", "browsermobproxy+selenium", "bs"]
	supportedBrowsers = ["firefox", "ff", "chrome", "ch"] # only for engines that support this

	@staticmethod
	def fetch(url, config, output_directory, fetchEngine="browsermobproxy+selenium", browser="firefox"):

		if fetchEngine in ("phantomjs", "ph"):

			data = subprocess.check_output( config['fetchEngines']['phantomjs_command'].replace("$url", url), shell=True )

		elif fetchEngine in ("browsermobproxy+selenium", "bs"):

			from browsermobproxy import Server
			from selenium import webdriver

			server = Server(config['fetchEngines']['browsermobproxy_binary'])
			server.start()
			proxy = server.create_proxy()

			if browser in ("firefox", "ff"):
				profile = webdriver.FirefoxProfile()
				profile.set_proxy(proxy.selenium_proxy())
				driver = webdriver.Firefox(firefox_profile=profile)
			else:
				chrome_options = webdriver.ChromeOptions()
				chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
				driver = webdriver.Chrome(chrome_options = chrome_options)

			proxy.new_har(url, options={'captureHeaders': True})
			driver.get(url)

			data = json.dumps(proxy.har, ensure_ascii=False)

			server.stop()
			driver.quit()
		else:
			sys.exit("Unrecognized engine.")

		if (data):
			fileName = output_directory + "/" + url.replace("http://", "").replace("https://", "") + "_" + strftime("%Y-%m-%d_%H:%M:%S", gmtime()) + ".har"
			f = open(fileName, "w")
			f.write(data.encode("utf8"))
			f.close()

			return fileName
		else:
			return None