* Use timeout feature instead of dedicated muting role
    * Working in [timeout](https://github.com/TechSupportCentral/TSCBot-py/tree/timeout)
      branch, but not applied because Discord doesn't yet allow certain
      channels to bypass timeouts. One of the important features of our
      current mute implementation is that users can still open and use
      tickets while muted, but that wouldn't work here until Discord
      allows timeout exceptions for certain channels.
