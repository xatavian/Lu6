Lu6
===

Template engine for C++ code generation

## What is Lu6

Lu6 (pronounce "Lucyx") is an atypical template engine mostly suited for C++ code generation. The observation that motivates the project is that most template engines are suited for Web Development and don't produce well indented code when it comes to C++ code generation.

Lu6 tries to generate coherant and "beautiful" code respecting indentation, as well as adding direct logic inside the templates themselves. It follows a Java-like syntax which is conveniant for class and function declarations.

## Getting started

Lu6 is currently not available on Pypi so you have to directly download the source code from Git. Luckilly, Lu6 does not require any external library.

Here is how you can do a generate a simple *Hello, world!* class:

```python
from lu6 import Lu6Engine

template="""
@class HelloWorldClass {
    @constructor() {
        @print "std::cout << \"Hello, World!";";
    };
};
"""

engine = Lu6Engine()
engine.set_source(Lu6Engine.STRING, template)
engine.set_output(Lu6Engine.OUTPUT_TO_STRING)

result = engine.generate()
print(result)
```

When running this code, the output is:
```c++
class HelloWorldClass {
public:
    HelloWorldClass() {
        std::cout << "Hello, world!";
    }
};
```


Lu6 templates can be loaded from / written to files and can also contain references to external content:
```python
from lu6 import Lu6Engine

engine = Lu6Engine()
engine.set_source(Lu6Engine.FILE, "hello_world.lu6")
engine.set_output(Lu6Engine.OUTPUT_TO_FILE, "hello_world.cpp")

engine.add_in_context("$hello", "Hello, World!");
engine.generate()
```

Considering that *hello_world.lu6* contain the following code:
```
@class HellowWorldClass {
    @constructor() {
        @print "std::cout << \"" + $hello + "\"";
    };
};
```

*hello_world.cpp would contain:
```c++
class HelloWorldClass {
    HelloWorldClass() {
        std::cout << "Hello, World!";
    }
};
```

For more details about what can be achieved in a Lu6 file, see grammar-details.md

## Want to contribute ?

If you want to contribute to the project, feel free to make a pull request for the requested feature. The project is not really ready yet for thorough collaboration but any help is welcome.
