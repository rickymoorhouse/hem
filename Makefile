buildContainer:
	cp requirements.txt Docker/
	cd Docker;docker build -t rickymoorhouse/hem:10.6 .
	cd Docker;docker tag rickymoorhouse/hem:10.6 rickymoorhouse/hem:latest
