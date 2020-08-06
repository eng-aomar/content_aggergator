import re

class DataClean:
    ''' Calss DataClean is responssible for cleaning scrapped data from source url '''
    @classmethod
    def clean_string(cls, scrapped_datum):
        ''' remove white spaces, newlines, $ and other symbols  from scrapped_datum and returned '''
        # cleaned_string.replace(',', '')
        cleaned_string = str(scrapped_datum)
        re.sub('\n', '', cleaned_string)
        re.sub('$', '', cleaned_string)
        re.sub('.', '', cleaned_string)
        re.sub(r"^\s+", "", cleaned_string)
        re.sub(r"\s+$", "", cleaned_string)
        return cleaned_string


# x = '\r\n\tالموقع الرسمي لمنظمة الصحة العالمية\r\n'
# y = DataClean.clean_string(x)
# print('y = ',y)
