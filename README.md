### 执行CPP程序

1. `make Makefile`

   生成类似与 [wasi-sdk](https://github.com/WebAssembly/wasi-sdk) 的工具， 创建基于wasi-libc的sysroot环境，生成用于编译wasm程序的工具链；

   生成工具链放置在`runtime/toolchain`中， sysroot环境放置在`runtime/llvm-sysroot`；

   显然我们需要通过交叉编译的方式，将本地的cpp/c代码编译为wasm程序， 交叉编译的配置文件为`WasiToolchain.cmake`


2. `pip3 install -r requirements.txt` && `pip3 install .`
   安装运行tasks中的invoke任务所需要的基本package，其中`pip3 install .`
   是安装`rfittools`，这里面封装了执行cmake的接口和一些基本的变量


3. `inv install`

   此操作是将`WasiToolchain.cmake`和`Makefile.envs`复制到`runtime/toolchain/tools`中


4. `inv librfit`

   编译librfit，并将编译的结果的链接库和头文件分别安装到
   `runtime/llvm-sysroot/lib/wasm32-wasi`和`runtime/llvm-sysroot/include/rfit`
   目录中

   这里面我们包含了我们自定义的由WAVM负责实现的接口，其中wasi的相关头文件和链接库 已经在第1步就安装好了，这里主要是我们自定义的接口

   librfit编译后的链接库显然也是wasm程序


5. `inv func.compile/func.register/func.invoke`

   编译wasm程序/注册/调用

### 执行Python程序

1. `./bin/install_build_python.sh`

   将在`runtime/python3.8`中安装完整的python工具包


2. `inv libffi`
   用于安装，在python动态链接C库时，所需要的库，
   否则会出现`ModuleNotFoundError: No module named _ctypes`
   的报错信息


2. `inv cpython`

   将cpython编译为wasm，然后将链接库、头文件等复制到`runtime`中：

    - `third-party/cpython/install/wasm/lib/libpython3.8.a`  TO  `runtime/llvm-sysroot/lib/wasm32-wasi/libpython3.8.a`
    - `third-party/cpython/install/wasm/include/python3.8` TO `runtime/llvm-sysroot/include/python3.8`
    - `third-party/cpython/install/wasm/lib` TO `runtime_root/lib`


3. `./bin/crossenv_setup.sh`


4. `. ./cross_venv/bin/activate` && `inv lib-rfit-python.install`


5. `inv runtime`

   `cross_venv/cross/lib/python3.8/site-packages` TO `/home/kingdo/CLionProjects/RFIT/Function/wasm/runtime_root/lib/python3.8/site-packages`