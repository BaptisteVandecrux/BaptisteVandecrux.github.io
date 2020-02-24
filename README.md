# BaptisteVandecrux.github.io

** GPT

#+BEGIN_SRC sh :results verbatim :exports both
~/local/snap/bin/gpt --diag
#+END_SRC

#+RESULTS:
#+begin_example
SNAP Release version 7.0
SNAP home: /home/kdm/local/snap/bin//..
SNAP debug: null
SNAP log level: null
Java home: /home/kdm/local/snap/jre
Java version: 1.8.0_202
Processors: 8
Max memory: 18.7 GB
Cache size: 1024.0 MB
Tile parallelism: 8
Tile size: 512 x 512 pixels

To configure your gpt memory usage:
Edit snap/bin/gpt.vmoptions

To configure your gpt cache size and parallelism:
Edit .snap/etc/snap.properties or gpt -c ${cachesize-in-GB}G -q ${parallelism} 
#+end_example
