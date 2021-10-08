all: build

build: clean
	mkdir build/
	cp -rf src BoneJuice
	zip -r build/BoneJuice.zip BoneJuice/
	rm -rf BoneJuice

clean:
	rm -rf build/
	rm -rf src/__pycache__