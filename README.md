# QR_ERP

QR ERP is a product demo for a cloud based QR scanning system. Small manufacturing facilities need an inventory tracking solution that is lightweight, fast, and accessible without all the expensive bells and whistles that large ERPs typically come with. 

At it's core, QR ERP comes with the following set of features:

	* Backend Azure System with different Azure SQL tables
	* Front-end triggerable stored procs to manipulate Azure SQL tables
	* Auto QR generation to trigger front-end app for incrementing inventory
	* DataFeed into excel to see on-hand inventory

With this setup, small manufacturing factories can print QRcodes and auto-increment inventory with their phone! The Azure SQL solution also makes it easy to maintain and keep track of existing tables to update future functionality. 

Repo: 

	* https://github.com/IamJasonBian/QR_ERP 

Pitch Slide:

	* https://github.com/IamJasonBian/QR_ERP/blob/master/QR-ERP-Manufacturing%20Implementation.pptx


Demo Site (Please wait 60 seconds for it to load as we are using a small VM):

	* qr-app-test.azurewebsites.net