# [START __tests__.py]
import unittest
from utils.utils import (
    parse_error_stack,
    graph_related_files,
    get_repo_details,
    get_related_details,
    resolve_import,
    build_dependency_graph
)
import os

class TestUtils(unittest.TestCase):
    def test_parse_error_stack(self):
        """Test case for the parse_error_stack function.

        This method simulates an error stack trace in a string format,
        which is typically produced by Python during a runtime error.
        It checks that the function correctly extracts the filename
        from the provided error string.
        """
        print("Running test_parse_error_stack()")
        error_string = '''File "/Users/vinh/Documents/calhacks24/test.py", line 2
          print(hello
               ^
      SyntaxError: '(' was never closed
'''
        expected_files = {"test.py"}
        print("Finished test_parse_error_stack()")
        result = set(parse_error_stack(error_string))
        print(f'Expected file: {expected_files}, Actual found: {result}')
        self.assertEqual(result, expected_files)

    def test_graph_related_files(self):
        """Test case for the graph_related_files function.

        This method tests the behavior of the graph_related_files function.
        As its output is currently not defined, this test checks the function's
        behavior for a given sample input and verifies that no output is produced.
        """
        result = graph_related_files("sample error", False)
        print(f'Graph related files output: {result}')
        self.assertIsNone(result)

    def test_get_repo_details(self):
        """Test case for the get_repo_details function.

        This integration test checks whether the get_repo_details function
        can correctly retrieve details of a repository from a sample directory.
        The test ensures that the expected files match the actual output.
        """
        if os.path.isdir('./sample_repo'):
            result = get_repo_details('./sample_repo')
            expected_files = {os.path.abspath('./sample_repo/test1.py'), os.path.abspath('./sample_repo/test2.py')}
            print(f'Expected: {expected_files}, Actual: {set(result)}')
            self.assertEqual(set(result), expected_files)

    def test_get_related_details(self):
        """Test case for the get_related_details function.

        This method creates a temporary file that imports modules and checks
        whether the function accurately identifies the imported modules
        from the specified file. After the test, the temporary file is removed.
        """
        with open('test_file.py', 'w') as f:
            f.write("import os\nfrom utils import something\n")

        expected_imports = {"os", "utils"}
        result = get_related_details('test_file.py')
        print(f'Expected: {expected_imports}, Actual: {result}')
        self.assertEqual(result, expected_imports)
        os.remove('test_file.py')

    def test_resolve_import(self):
        """Test case for the resolve_import function.

        This method sets up a dummy file structure to test the import resolution
        for modules. It checks whether the function returns the correct path for
        the specified module. The cleanup is performed after the test.
        """
        os.mkdir('test_dir')
        with open('test_dir/test_module.py', 'w') as f:
            f.write("")

        result = resolve_import('test_module', 'test_dir/test_module.py')
        print(f'Expected: {os.path.abspath("test_dir/test_module.py")}, Actual: {result}')
        self.assertEqual(result, os.path.abspath('test_dir/test_module.py'))

        os.rmdir('test_dir')  # Clean up

    def test_build_dependency_graph(self):
        """Test case for the build_dependency_graph function.

        This method sets up a mock dependency scenario with two sample files
        and verifies whether the dependency graph is constructed correctly.
        It checks the number of nodes in the graph and ensures that the
        expected relationships between nodes exist.
        """
        with open('A.py', 'w') as f:
            f.write('import B\n')

        with open('B.py', 'w') as f:
            f.write('')

        files = {os.path.abspath('A.py'), os.path.abspath('B.py')}
        graph = build_dependency_graph(files)

        print(f'Number of nodes: {len(graph.nodes)}')
        print(f'Graph connections: {list(graph.successors(os.path.abspath("A.py")))}')
        self.assertEqual(len(graph.nodes), 2)
        self.assertIn(os.path.abspath('B.py'), graph.successors(os.path.abspath('A.py')))

        os.remove('A.py')
        os.remove('B.py')

if __name__ == '__main__':
    unittest.main()
# [END __tests__.py]
