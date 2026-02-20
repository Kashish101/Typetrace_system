# import json
# import re
# import logging
# from pathlib import Path
#
#
# class DataFilter:
#     def __init__(self, pattern_file):
#         self.patterns = self._load_patterns(pattern_file)
#
#     def _load_patterns(self, pattern_file):
#         try:
#             with open(pattern_file, 'r') as f:
#                 data = json.load(f)
#                 return [re.compile(p['regex']) for p in data['patterns']]
#         except Exception as e:
#             logging.error(f"Error loading patterns: {e}")
#             return []
#
#     def redact(self, text):
#         try:
#             for pattern in self.patterns:
#                 text = pattern.sub(f'[{pattern.pattern} REDACTED]', text)
#             return text
#         except Exception as e:
#             logging.error(f"Redaction error: {e}")
#             return text


#
# import json
# import re
# import logging
#
#
# class DataFilter:
#     def __init__(self, pattern_file):
#         self.patterns = self._load_patterns(pattern_file)
#         self.history = ""  # Keep history of typed characters
#
#     def _load_patterns(self, pattern_file):
#         try:
#             with open(pattern_file, 'r') as f:
#                 data = json.load(f)
#                 return [(p['name'], re.compile(p['regex'])) for p in data['patterns']]
#         except Exception as e:
#             logging.error(f"Error loading patterns: {e}")
#             return []
#
#     def redact(self, char):
#         try:
#             self.history += char  # Add current character to history
#
#             redacted_text = self.history
#             replaced = False
#
#             for name, pattern in self.patterns:
#                 if pattern.search(self.history):
#                     redacted_text = pattern.sub(f'[{name.upper()} REDACTED]', self.history)
#                     replaced = True
#                     break  # One match is enough to redact
#
#             if replaced:
#                 self.history = ""  # Reset history after a match
#                 return redacted_text  # Return full redacted string
#             else:
#                 return char  # No match, return character normally
#         except Exception as e:
#             logging.error(f"Redaction error: {e}")
#             return char


#
#
# import json
# import re
# import logging
#
#
# class DataFilter:
#     def __init__(self, pattern_file):
#         self.patterns = self._load_patterns(pattern_file)
#         self.history = ""
#
#     def _load_patterns(self, pattern_file):
#         try:
#             with open(pattern_file, 'r') as f:
#                 data = json.load(f)
#                 return [(p['name'], re.compile(p['regex'])) for p in data['patterns']]
#         except Exception as e:
#             logging.error(f"Error loading patterns: {e}")
#             return []
#
#     def redact(self, char):
#         try:
#             self.history += char
#
#             # Check for any sensitive pattern
#             for name, pattern in self.patterns:
#                 if pattern.search(self.history):
#                     redacted = pattern.sub(f'[{name.upper()} REDACTED]', self.history)
#                     self.history = ""
#                     return redacted
#
#             # If user ends a sentence or inputs space/newline, flush safe content
#             if char in [' ', '\n', '\t'] and len(self.history) > 100:
#                 output = self.history
#                 self.history = ""
#                 return output
#
#             # If nothing matched and not ready to flush, return empty (wait)
#             return ''
#         except Exception as e:
#             logging.error(f"Redaction error: {e}")
#             return char
#
# import json
# import re
# import logging
#
#
# class DataFilter:
#     def __init__(self, pattern_file):
#         self.patterns = self._load_patterns(pattern_file)
#         self.history = ""
#
#     def _load_patterns(self, pattern_file):
#         try:
#             with open(pattern_file, 'r') as f:
#                 data = json.load(f)
#                 return [(p['name'], re.compile(p['regex'])) for p in data['patterns']]
#         except Exception as e:
#             logging.error(f"Error loading patterns: {e}")
#             return []
#
#     def redact(self, char):
#         try:
#             self.history += char
#
#             # Check for sensitive data
#             for name, pattern in self.patterns:
#                 match = pattern.search(self.history)
#                 if match:
#                     # redact matched part
#                     redacted = pattern.sub(f'[{name.upper()} REDACTED]', self.history)
#                     output = redacted
#                     self.history = ""
#                     return output
#
#             # If user ends word (e.g., space or enter), flush normal word
#             if char in [' ', '\n', '\t']:
#                 output = self.history
#                 self.history = ""
#                 return output
#
#             # Otherwise, wait (don't flush mid-word or mid-pattern)
#             return ''
#         except Exception as e:
#             logging.error(f"Redaction error: {e}")
#             return char
#




import json
import re
import logging
from pathlib import Path


class DataFilter:
    def __init__(self, pattern_file):
        self.patterns = self._load_patterns(pattern_file)

    def _load_patterns(self, pattern_file):
        try:
            with open(pattern_file, 'r') as f:
                data = json.load(f)
                return [re.compile(p['regex']) for p in data['patterns']]
        except Exception as e:
            logging.error(f"Error loading patterns: {e}")
            return []

    def redact(self, text):
        try:
            for pattern in self.patterns:
                text = pattern.sub('[REDACTED]', text)
            return text
        except Exception as e:
            logging.error(f"Redaction error: {e}")
            return text
