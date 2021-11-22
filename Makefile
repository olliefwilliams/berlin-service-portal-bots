install:
	pip3 install -r requirements.txt

auslanderbehorde:
	python3 ./berlin_service_portal_bot/auslanderbehorde_bot.py

service_portal:
	python3 ./berlin_service_portal_bot/service_portal_bot.py

test:
	nosetests tests