all: build

build: clean
	mkdir build/
	zip -r build/BoneJuice.zip src/

clean:
	rm -rf build/
	rm -rf src/__pycache__