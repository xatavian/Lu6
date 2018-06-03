Lu6 Grammar
===========

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