.PHONY: elastic-ui
elastic-ui:
	docker run -d -it -p 9100:9100 mobz/elasticsearch-head:5-alpine /bin/ash -c "apk add paxctl --no-cache && paxctl -cm /usr/local/bin/node && node_modules/http-server/bin/http-server _site -p 9100"
