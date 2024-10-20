// Intentionally problematic TypeScript program

// Error: Class 'Person' incorrectly implements interface 'IPerson'.
interface IPerson {
  name: string;
  age: number;
  greet(): void;
}

class Person implements IPerson {
  constructor(public name: string) {} // Missing 'age' property

  // Error: Property 'greet' is missing in type 'Person' but required in type 'IPerson'
}

// Error: Cannot find name 'console'. Did you mean 'Console'?
console.log("Hello, TypeScript!");

// Error: Parameter 'x' implicitly has an 'any' type.
function add(x, y: number): number {
  return x + y;
}

// Error: Type 'string' is not assignable to type 'number'.
let result: number = add(5, "10");

// Error: Property 'toUppercase' does not exist on type 'string'. Did you mean 'toUpperCase'?
let uppercaseName = "john".toUppercase();

// Error: Type '{ firstName: string; lastName: string; }' is not assignable to type 'IPerson'.
//   Object literal may only specify known properties, and 'firstName' does not exist in type 'IPerson'.
let person: IPerson = {
  firstName: "John",
  lastName: "Doe",
  age: 30,
};

// Error: Cannot find name 'Promise'. Do you need to change your target library? Try changing the 'lib' compiler option to include 'dom'.
function fetchData(): Promise<string> {
  return new Promise((resolve) => {
    resolve("Data");
  });
}

// Error: Cannot use 'new' with an expression whose type lacks a call or construct signature.
let arr = new Array(5).fill("a");

// Error: Property 'push' does not exist on type 'readonly string[]'.
const readonlyArray: readonly string[] = ["a", "b", "c"];
readonlyArray.push("d");

// Error: Type 'number' is not assignable to type 'string'.
let strArray: string[] = [1, 2, 3];

// Error: Type 'string | number' is not assignable to type 'boolean'.
//   Type 'string' is not assignable to type 'boolean'.
let flag: boolean = Math.random() > 0.5 ? true : "false";

// Error: Cannot find name 'SQLException'. Did you mean 'AggregateError'?
try {
  // Some code that might throw an error
} catch (error: SQLException) {
  // Handle error
}

// Error: Cannot find name 'enum'. Did you mean 'Enum'?
enum Color {
  Red,
  Green,
  Blue,
}

// Error: 'const' declarations must be initialized.
const uninitializedConst: number;

// Error: Type '"hello"' is not assignable to type 'number'.
let num: number = "hello";

export {}; // To make this a module and avoid "cannot redeclare block-scoped variable" errors
