# dsa-pywnprpc
RPC for Lua over windows named pipes

Goal is to make Lua <-> python RPC over NamedPipe. 
Lua library is reference protocol implementation. 
This python library is just a port of Lua one.
And it has only client part, which connects to pipe created by the server.
Lua library has both client and server.

Link to Lua library: [lua-wnp-rpc]

Note that protocol is not thread-safe. Since Lua is in general single-threaded there 
should not be any problems. But if your setup is multi-threaded, it 
is your responsibility to prevent concurrent access to the pipe.

Library code is in package `dsa.pywnprpc`. 
Example of using the library is in file `example-client.py`.

[lua-wnp-rpc]:https://github.com/dsabdrashitov/lua-wnp-rpc
