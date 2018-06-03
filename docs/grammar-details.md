Understand Lu6's Grammar
========================

*The complete grammar is available in docs/grammar.txt file*.

## Comments

Single-line comment are preceded with symbol `@//` symbol; multi-line comments are contained between two symbols `@/*` and `*/@`.

## Global file structure

The structure of a Lu6 file is similar of C++ files. The root of the document can contain `@include` instructions and type definitions.

```
@include "<iostream>";
@include "<vector>";

@// Type declarations
@/*
    ...
*/@
```

A type declaration is either a class declaration or a function declaration.

## Class declaration

A class is declared with token `@class` followed by the name of the class. Inheritance is possible using the `@extends` instruction. A class declaration must be followed by a semi colon.

**Example:**

```
@class MyClass @extends BaseClass {
    @// ...
};

@/*
Generated code

class MyClass: public BaseClass {
    // ...
};
*/@
```

### Member declaration

Classes can contain attributes and methods which are declared by the `@attribute` and `@method` symbols. For instance,
`@attribute int my_attr;` declare an attribute named `my_attr` of type `int`; `@method void test();` declares a method named `test` with return type `void` and no body.

By default, attributes are declared private and methods are declared public. To change this behavior, add a colon after the `@attribute`/`@method` instruction followed by one or more keywords in `public`, `private`, `protected`, `static`, `const` (separated by commas).

Member declarations must ALWAYS be followed by a semi-colon.

**Example:**

```
@class MyClass {
    @method void test(); @// Public method with no body
    @attribute:public,static int my_attr; @// Public and static attribute
    @attribute CustomType customTypeAttr;
};

@/*
Generated code:

class MyClass {
public:
  void test();
public:
  static int my_attr;
private:
  CustomType customTypeAttr;
};
*/@
```

#### Method declarations

Methods can obviously have a body but they can also have parameters. The parameters have no influence on the body of the method but will be printed during code generation.

**Example:**

```
@class MyClass {
    @method void test(int param1, int param2) {
        @print "int hello = 2;";
        @print "std::cout << hello; ";
    };
};

@/*
Generated code:

class MyClass {
public:
    void test(int param1, int param2) {
        int hello = 2;
        std::cout << hello;
    }
};
*/@
```

See the Statements section for more informations about the possible statements.

To declare a constructor, use the `@constructor` instruction. Constructors don't need a name nor a return type. If the generated class derives from another, the super call is automatically resolved from the base class.

*Note: for now, constructors can only execute super calls with no parameters. Moreover, they can only be declared public.*

**Example:**

```
@class MyClass @extends BaseClass {
    @constructor(CustomType param1) {
        @print "std::cout << param1;";
    };
};

@/*
Generated code:

class MyClass: public BaseClass {
public:
  MyClass (CustomType param1): BaseClass(){
    std::cout << param1;
  }
};
*/@
```

## Function declaration

Lu6 also allows function declaration outside a class. To do so, use the `@function` instruction. Parameters can be declared like for method declarations, and all the statements (see Statements sections) are allowed inside a function.

Like a class declaration, a function declaration must be followed by a semi-colon.

**Example:**

```
@function isHelloWorld(std::string test) {
    @print "return test == \"Hello, world! \"";
};
```

## Statements

Here is a list of statements that can be used in a Lu6 file.
*Note: `...` represents a single instruction or a sequence of instructions gathered in a block (delimited by curly brackets)*

### Using variables

Variables can be declared inside the Lu6 file with identifiers starting with a `$` symbol.

Currently, variables declared inside templates only support number and string types. Variables added as external content can have any type (they can even be objects).

```
@/* ... */@
$var1 = "a = \"Hello, world\"";
@print $var1 + ";";
@/* .... */@

@/*
Generated code:

/* ... */
a = "Hello, world";
/* ... */
```

### If statements

Basic syntax: `@if( <condition> ) ... @else ...`

Else if syntax: `@if( <condition> ) ... @else @if ( <other condition>) ... @else ...`.

If statements are not followed by a semi-colon. Else clauses are obviously optional.

### While loops

Basic syntax: `@while( <condition>) ...`

While loops are not followed by a semi-colon.

### Print instructions

* `@print <expression>;` prints the result of the expression
* `@println <expression>;` prints the result of the expression and adds a new line.
* `@instruction <expression>;` prints the result of the expression, adds a semi-colon and a new line.

*Note: `@println` and `@instruction` are not implemented yet.*

**Example:**

```
@class MyClass {
    @method void tests() {
        $var1 = "std::string a = \"Hello, world!"";
        @instruction $var1;
        @instruction "std::cout << a";
    };
};

@/*
Generated code:

class MyClass {
public:
    void tests() {
        std::string a = "Hello, world!";
        std::cout << a;
    }
};
*/@
```

