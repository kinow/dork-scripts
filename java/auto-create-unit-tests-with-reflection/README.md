This script auto creates unit tests with reflection. In a project I worked, we had
to write unit tests for that had a certain annotation, and some pattern in how the
methods were created.

For that, I simply copied this piece of code into the class and executed the main
method. That would output in stdout the assert's to be copied into the unit test.