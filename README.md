# Gravithaum - Readme

## Installation

### Dependancies

#### glfw3

To compile glfw3 on linux, you will need to install dependancies as specified
at :
http://www.glfw.org/docs/latest/compile.html#compile_deps_x11

Then, execute the following commands:

                wget https://github.com/glfw/glfw/releases/download/3.1.1/glfw-3.1.1.zip
                tar -xvf glfw-3.1.1.zip
                cd glfw-3.1.1
                mkdir build
                cd build
                cmake -DBUILD_SHARED_LIBS=true ..
                make
                sudo make install

#### glfw3 for python

We suggest to use pip:

                sudo apt-get install python-pip
                sudo pip install glfw
                sudo pip install pyopengl


### Execution

                python gravithaum.py

