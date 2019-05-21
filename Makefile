redis-ubuntu:
	sudo docker run --name redis-server --network host --rm redis:latest --port 6381
redis-macos:
	docker run --name=redis-server --publish=6381:6381 --rm --hostname=redis redis:latest --port 6381
cassandra:
	sudo docker run --name main_cass -p 9042:9042 --rm cassandra:3