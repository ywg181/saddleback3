import ast
import logging


class Gsys(object):
    @staticmethod
    def line_to_dict(gsys_line):
        remove_empty_fields = ' '.join([x for x in gsys_line.split(' ')
                                        if x]).replace('" "', '""')

        return ast.literal_eval(
            '{ "' +
            remove_empty_fields.replace('" ', '", "').replace('=', '" : ') +
            ' }')

    @staticmethod
    def get_dict(gsys_response, find_strings, term_char='\n'):
        """Finds the correct lines in gsys response and retries if corrupt.

        Args:
          gsys_response: The gsys response.
          find_strings: A list of strings to find in the gsys response. The
            first line containing all elements is returned as a dictionary.
          term_char: The terminal character that ends each line in gsys_response
        Returns:
          gsys_dict: The first gsys line matching all elements of find_strings
            is returned (as a dictionary). If no matches found None is returned.
        Raises:
          Error handled by OpenTest.
        """
        lines = gsys_response.split(term_char)
        for find_string in find_strings:
            lines = [line for line in lines if find_string in line]

        if not lines:
            return None

        try:
            gsys_dict = Gsys.line_to_dict(lines[0])
        except SyntaxError:
            logging.debug('Invalid gsys response detected.')
            raise

        return gsys_dict
