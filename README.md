Before getting into this, it would be nice to revisit the [dns terminologies](http://jvns.ca/blog/2022/02/14/some-dns-terminology) and believe me the way I've used it might be different as well :wink:

*Chronicles begin*
## Ch1: Stub Resolver
The first part implements a **UDP DNS stub resolver + forwarder**:

`client -> stub -> 8.8.8.8 -> answer`

- Listens locally for DNS queries (from your OS / browser)
- Forwards the **raw DNS packet** to an upstream resolver (**Google DNS `8.8.8.8:53` by default**)
- Relays the upstream response back to the original client

It is **not** a recursive resolver. It is a **packet forwarder** with minimal parsing for logging. Also it **cannot handle concurrent requests**

## Ch2: Handling Concurrent Requests & Caching
What happens when QPS(*Queries per Second*) explode

## Ch3: Getting over the stubborn - Recursive Resolver
Implementing '8.8.8.8' `client -> stub -> recursive-resovler -> root -> TLD -> authoritative -> answer`