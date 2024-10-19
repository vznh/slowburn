const num = 42;

function faultyFunction() {
  num = 10; // Attempt to reassign a constant variable
  console.log(num);
}

faultyFunction();
