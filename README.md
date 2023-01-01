# Microservices Example

## Goals

The goal of this python project is to try and implement the skeleton of an application
using a hybrid design between a (modular) monolith and a microservice architecture.
The goal is to learn about the challenges of such a design while experimenting with gRPC, Python sub-processes and
Unix Domain Sockets.  
I understand that a monolith is simple, fast to code but does not scale too well in the very long run while
microservices are complex and hard to maintain/orchestrate but are isolated and scale well.
The idea is to experiment with a design pattern that is not too costly, hard to reason about,
scale at the start of a project and can be expanded without major refactors when the application scales in terms of
codebase, architecture complexity and deployment process.
One of the major advantages of microservices is that deployment can be done at separate times. Using "microservices"
that are still processes on the same machine and are statically linked in the code is in antithesis with the whole idea
but the point is not to achieve a full microservice system now, but rather trying out a compromise
that can be refactored easily later.

The idea is to use Python in tandem with gRPC to create modular microservices that are made concrete by
a Python subprocess. The root Python process will handle all orchestration, network setup and discovery needs for
the sub-processes microservices.
On the side of performance, we will use Unix Domain Sockets.
