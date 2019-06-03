redis-ubuntu:
	sudo docker run --name redis-server --network host --rm redis:latest --port 6381
redis-macos:
	docker run --name redis-server --publish 6381:6381 --rm --hostname redis redis:latest --port 6381
cassandra:
	sudo docker run --name main_cass -p 9042:9042 --rm cassandra:3
elastic-ubuntu:
	sudo docker run --network host --name elastic --rm -e "http.port=10000" -e "discovery.type=single-node" \
	ądocker.elastic.co/elasticsearch/elasticsearch:6.6.2
elastic-macos:
	docker run --name elastic --publish 10000:10000 --rm --hostname elastic -e "http.port=10000" -e "discovery.type=single-node" \
	docker.elastic.co/elasticsearch/elasticsearch:6.6.2